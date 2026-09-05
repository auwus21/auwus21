#!/usr/bin/env python3
"""
Ranking de juegos mas vendidos de epicodes.com.ar segun el contador "ENTREGADAS".

Recorre el sitio, busca en cada pagina el numero que aparece junto a la palabra
"ENTREGADAS", y genera un ranking ordenado de mayor a menor en TXT y CSV.

Uso basico:
    python3 epicodes_ranking.py

Opciones utiles:
    --base URL        sitio a recorrer (default: https://epicodes.com.ar/)
    --out ARCHIVO     salida de texto (default: mas_vendidos.txt)
    --csv ARCHIVO     salida CSV (default: mas_vendidos.csv)
    --max-pages N     limite de paginas a visitar (default: 400)
    --delay SEG       espera entre pedidos, para no golpear el server (default: 0.5)
    --render          renderiza con Playwright (usalo si el sitio es una SPA y
                      el modo normal no encuentra nada)

Solo necesita Python 3.8+. El modo --render necesita:
    pip install playwright && playwright install chromium
"""

import argparse
import csv
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque

UA = "Mozilla/5.0 (compatible; epicodes-ranking/1.0)"

# extensiones que no son paginas HTML
SKIP_EXT = (
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".ico",
    ".css", ".js", ".mjs", ".json", ".xml", ".txt", ".pdf", ".zip",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".webm", ".mp3",
)

# Un numero: o con separador de miles (1.990 / 12.480), o suelto (846).
# Ojo: el espacio ASCII NO cuenta como separador de miles, porque si no
# "Spider-Man 2 846 entregadas" se leeria como 2846.
NUM = r"(\d{1,3}(?:[\.\,  ]\d{3})+|\d+)"
# separadores visuales que pueden quedar entre el numero y la palabra
SEP = r"[\s |/·•:\-–—]*"

# "1.990 ENTREGADAS", "1990 entregadas", "846 entregados"
RE_ENTREGADAS = re.compile(
    NUM + SEP + r"(?:unidades" + SEP + r")?entregad[ao]s?\b",
    re.IGNORECASE,
)
# variante invertida: "ENTREGADAS: 1.990"
RE_ENTREGADAS_INV = re.compile(
    r"entregad[ao]s?" + SEP + NUM,
    re.IGNORECASE,
)
RE_PRECIO = re.compile(r"\$\s?[0-9][0-9\.\,]*")
RE_TAG = re.compile(r"<(script|style|noscript)\b.*?</\1>", re.IGNORECASE | re.DOTALL)
RE_ANY_TAG = re.compile(r"<[^>]+>")
RE_HREF = re.compile(r"""href\s*=\s*["']([^"'#]+)""", re.IGNORECASE)
RE_H1 = re.compile(r"<h1[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
RE_OG_TITLE = re.compile(
    r"""<meta[^>]+property\s*=\s*["']og:title["'][^>]+content\s*=\s*["']([^"']+)""",
    re.IGNORECASE,
)
RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)


def a_numero(bruto):
    """'1.990' -> 1990 ; '12.480' -> 12480 ; '846' -> 846. None si no sirve."""
    limpio = re.sub(r"[\s ]", "", bruto)
    limpio = limpio.rstrip(".,")
    if not limpio:
        return None
    # formato argentino: el punto (o la coma) es separador de miles
    if re.fullmatch(r"\d{1,3}(?:[\.\,]\d{3})+", limpio):
        limpio = re.sub(r"[\.\,]", "", limpio)
    elif re.fullmatch(r"\d+", limpio):
        pass
    else:
        return None
    try:
        return int(limpio)
    except ValueError:
        return None


def a_texto(doc):
    """HTML -> texto plano, con espacios donde habia etiquetas."""
    sin_script = RE_TAG.sub(" ", doc)
    sin_tags = RE_ANY_TAG.sub(" ", sin_script)
    return re.sub(r"[ \t\r\n]+", " ", html.unescape(sin_tags)).strip()


def buscar_entregadas(doc, texto):
    """Devuelve la cantidad entregada, o None."""
    for regex in (RE_ENTREGADAS, RE_ENTREGADAS_INV):
        for m in regex.finditer(texto):
            n = a_numero(m.group(1))
            if n is not None:
                return n
    # ultimo intento: campos JSON embebidos (Next.js, Nuxt, etc.)
    for m in re.finditer(
        r'"(entregadas|entregados|delivered|sold|ventas|sales_count|deliveries)"\s*:\s*"?(\d+)',
        doc,
        re.IGNORECASE,
    ):
        n = a_numero(m.group(2))
        if n is not None:
            return n
    return None


def buscar_titulo(doc, url):
    for regex in (RE_H1, RE_OG_TITLE, RE_TITLE):
        m = regex.search(doc)
        if m:
            t = re.sub(r"\s+", " ", html.unescape(RE_ANY_TAG.sub(" ", m.group(1)))).strip()
            t = re.split(r"\s+[\|–—\-]\s+", t)[0].strip()
            if t:
                return t
    return url.rstrip("/").rsplit("/", 1)[-1] or url


def buscar_precio(texto):
    precios = RE_PRECIO.findall(texto)
    # el ultimo suele ser el precio final (el primero es el tachado)
    return precios[-1].replace(" ", "") if precios else ""


def descargar(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        ctype = r.headers.get("Content-Type", "").lower()
        if ctype and not ("html" in ctype or "octet-stream" in ctype or ctype.startswith("text/")):
            return None
        crudo = r.read(3_000_000)
    charset = "utf-8"
    m = re.search(r"charset=([\w\-]+)", ctype, re.IGNORECASE)
    if m:
        charset = m.group(1)
    doc = crudo.decode(charset, errors="replace")
    # algunos servidores no declaran text/html: confirmamos mirando el contenido
    if "html" not in ctype and "<" not in doc[:2000]:
        return None
    return doc


def hacer_render(urls, delay):
    """Renderiza cada URL con Playwright y devuelve {url: html}."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit(
            "Falta Playwright para --render.\n"
            "  pip install playwright && playwright install chromium"
        )
    salida = {}
    with sync_playwright() as p:
        navegador = p.chromium.launch()
        pagina = navegador.new_page(user_agent=UA)
        for u in urls:
            try:
                pagina.goto(u, wait_until="networkidle", timeout=30000)
                salida[u] = pagina.content()
            except Exception as e:  # noqa: BLE001
                print(f"  ! no se pudo renderizar {u}: {e}", file=sys.stderr)
            time.sleep(delay)
        navegador.close()
    return salida


def es_interna(url, host):
    p = urllib.parse.urlparse(url)
    return p.scheme in ("http", "https") and p.netloc == host


def normalizar(url):
    p = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((p.scheme, p.netloc, p.path or "/", "", p.query, ""))


def recorrer(base, max_pages, delay, render):
    host = urllib.parse.urlparse(base).netloc
    pendientes = deque([normalizar(base)])
    vistas = set()
    docs = {}

    while pendientes and len(vistas) < max_pages:
        url = pendientes.popleft()
        if url in vistas:
            continue
        vistas.add(url)
        try:
            doc = descargar(url)
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            print(f"  ! {url}: {e}", file=sys.stderr)
            continue
        if not doc:
            continue
        docs[url] = doc
        print(f"  . {len(vistas):3d}/{max_pages} {url}", file=sys.stderr)

        for href in RE_HREF.findall(doc):
            destino = normalizar(urllib.parse.urljoin(url, href.strip()))
            if not es_interna(destino, host):
                continue
            if destino.lower().endswith(SKIP_EXT):
                continue
            if destino not in vistas:
                pendientes.append(destino)
        time.sleep(delay)

    if render:
        print(f"\nRenderizando {len(docs)} paginas con Playwright...", file=sys.stderr)
        docs.update(hacer_render(list(docs), delay))

    return docs


def extraer(docs):
    filas = []
    for url, doc in docs.items():
        texto = a_texto(doc)
        cantidad = buscar_entregadas(doc, texto)
        if cantidad is None:
            continue
        filas.append(
            {
                "entregadas": cantidad,
                "juego": buscar_titulo(doc, url),
                "precio": buscar_precio(texto),
                "url": url,
            }
        )
    # deduplica por nombre, quedandose con el numero mas alto
    mejor = {}
    for f in filas:
        clave = f["juego"].strip().lower()
        if clave not in mejor or f["entregadas"] > mejor[clave]["entregadas"]:
            mejor[clave] = f
    return sorted(mejor.values(), key=lambda f: f["entregadas"], reverse=True)


def escribir_txt(filas, ruta, base):
    ancho = max([len(f["juego"]) for f in filas] + [10])
    total = sum(f["entregadas"] for f in filas)
    with open(ruta, "w", encoding="utf-8") as fh:
        fh.write("MAS VENDIDOS - {}\n".format(base))
        fh.write("Generado: {}\n".format(time.strftime("%Y-%m-%d %H:%M")))
        fh.write("{} juegos | {:,} entregas totales\n".format(len(filas), total).replace(",", "."))
        fh.write("=" * (ancho + 34) + "\n")
        fh.write("{:>3}  {:<{w}}  {:>10}  {:>10}\n".format("#", "JUEGO", "ENTREGADAS", "PRECIO", w=ancho))
        fh.write("-" * (ancho + 34) + "\n")
        for i, f in enumerate(filas, 1):
            fh.write(
                "{:>3}  {:<{w}}  {:>10}  {:>10}\n".format(
                    i,
                    f["juego"],
                    "{:,}".format(f["entregadas"]).replace(",", "."),
                    f["precio"] or "-",
                    w=ancho,
                )
            )
    return total


def escribir_csv(filas, ruta):
    with open(ruta, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["puesto", "juego", "entregadas", "precio", "url"])
        w.writeheader()
        for i, f in enumerate(filas, 1):
            w.writerow({"puesto": i, **f})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="https://epicodes.com.ar/")
    ap.add_argument("--out", default="mas_vendidos.txt")
    ap.add_argument("--csv", default="mas_vendidos.csv")
    ap.add_argument("--max-pages", type=int, default=400)
    ap.add_argument("--delay", type=float, default=0.5)
    ap.add_argument("--render", action="store_true")
    args = ap.parse_args()

    print("Recorriendo {} ...".format(args.base), file=sys.stderr)
    docs = recorrer(args.base, args.max_pages, args.delay, args.render)
    filas = extraer(docs)

    if not filas:
        print(
            "\nNo se encontro ningun contador de 'entregadas' en {} paginas.\n"
            "Si el sitio carga el contenido con JavaScript, volve a correrlo con --render".format(len(docs)),
            file=sys.stderr,
        )
        sys.exit(1)

    total = escribir_txt(filas, args.out, args.base)
    escribir_csv(filas, args.csv)
    print("\nListo: {} juegos, {} entregas totales".format(len(filas), total), file=sys.stderr)
    print("  -> {}\n  -> {}".format(args.out, args.csv), file=sys.stderr)


if __name__ == "__main__":
    main()
