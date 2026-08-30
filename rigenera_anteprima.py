#!/usr/bin/env python3
"""Rigenera anteprima.html incorporando i JSON dentro l'HTML.

Serve solo per guardare il sito con un doppio click: i browser bloccano
fetch() sui file locali, quindi index.html da solo non funziona su file://.
Online (GitHub Pages) va usato index.html, non anteprima.html.

Uso:  python rigenera_anteprima.py
"""
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).parent
FILES = ['lega', 'squadre', 'classifica', 'calendario',
         'coppa', 'albo', 'premi', 'regolamento', 'sponsor']


def main():
    html = (BASE / 'index.html').read_text(encoding='utf-8')

    dati = {}
    for nome in FILES:
        p = BASE / 'data' / f'{nome}.json'
        if not p.exists():
            sys.exit(f"manca {p}")
        try:
            dati[nome] = json.loads(p.read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            sys.exit(f"{p.name} non e' JSON valido: {e}")

    inizio = html.index('async function load(name){')
    fine = html.index('}', html.index('return r.json();')) + 1

    # </ va spezzato o chiuderebbe il tag <script> in anticipo
    blob = json.dumps(dati, ensure_ascii=False).replace('</', '<\\/')
    inline = f'const DATI = {blob};\nasync function load(name){{ return DATI[name]; }}'

    out = html[:inizio] + inline + html[fine:]
    out = out.replace('<title>Lega Fantagufi — Fantacalcio</title>',
                      '<title>Lega Fantagufi — ANTEPRIMA</title>')

    (BASE / 'anteprima.html').write_text(out, encoding='utf-8')
    print(f"anteprima.html rigenerata ({len(out) // 1024} KB, {len(FILES)} file incorporati)")


if __name__ == '__main__':
    main()
