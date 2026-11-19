#!/usr/bin/env python3
"""Revisión diaria de grupodospuntocero.com (no se publica: empieza por _).

Comprueba que todas las páginas del sitemap cargan, que cada imagen, carta y
enlace interno que usan responde, que las redirecciones antiguas siguen ahí,
el certificado HTTPS y el tiempo de respuesta.

Uso:  python3 _revision_diaria.py
Sale con código 0 si todo va bien y 1 si hay algún fallo. Imprime un resumen
en español listo para mandar.
"""
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DOMINIO = 'grupodospuntocero.com'
BASE = f'https://{DOMINIO}'
UA = 'Mozilla/5.0 (compatible; revision-diaria-web/1.0)'
LENTO = 4.0  # segundos

# Redirecciones de las URL antiguas de WordPress (deben seguir respondiendo)
ANTIGUAS = ['/green-2-0/', '/la-traviesa-2-0/', '/la-chula-2-0/', '/juanita-2-0/',
            '/quienes-somos/', '/contacto/', '/hazte-socio/']
# Textos que tienen que aparecer (si falta, la página carga pero está rota)
TEXTOS = {
    '/': 'Grupo 2.0',
    '/locales/green/': 'Green',
    '/locales/la-traviesa/': 'Traviesa',
    '/en/': 'Grupo 2.0',
}
EXTRA = ['/robots.txt', '/sitemap.xml', '/llms.txt', '/og.jpg', '/favicon.png']

fallos, avisos = [], []


def pedir(url, metodo='GET'):
    req = urllib.request.Request(url, method=metodo, headers={'User-Agent': UA})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            cuerpo = r.read() if metodo == 'GET' else b''
            return r.status, cuerpo, time.time() - t, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, b'', time.time() - t, url
    except Exception as e:  # DNS, timeout, SSL...
        return None, str(e).encode(), time.time() - t, url


def nombre(url):
    return urllib.parse.unquote(url.replace(BASE, '') or '/')


def main():
    # 1. Certificado HTTPS
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((DOMINIO, 443), timeout=15) as s:
            with ctx.wrap_socket(s, server_hostname=DOMINIO) as ss:
                fin = ssl.cert_time_to_seconds(ss.getpeercert()['notAfter'])
        dias = int((fin - time.time()) / 86400)
        if dias < 7:
            fallos.append(f'El certificado HTTPS caduca en {dias} días')
        elif dias < 20:
            avisos.append(f'El certificado HTTPS caduca en {dias} días (GitHub suele renovarlo solo)')
    except Exception as e:
        fallos.append(f'No se pudo comprobar el certificado HTTPS: {e}')
        dias = None

    # 2. Páginas del sitemap
    st, cuerpo, _, _ = pedir(BASE + '/sitemap.xml')
    paginas = re.findall(r'<loc>([^<]+)</loc>', cuerpo.decode('utf-8', 'ignore')) if st == 200 else []
    if not paginas:
        fallos.append(f'No se pudo leer el sitemap (respuesta {st})')
        paginas = [BASE + '/']

    recursos, tiempos = set(), []
    for url in paginas:
        st, cuerpo, seg, _ = pedir(url)
        tiempos.append(seg)
        if st != 200:
            fallos.append(f'Página caída: {nombre(url)} (respuesta {st or "sin respuesta"})')
            continue
        html = cuerpo.decode('utf-8', 'ignore')
        if seg > LENTO:
            avisos.append(f'{nombre(url)} tardó {seg:.1f} s en cargar')
        if '</html>' not in html.lower():
            fallos.append(f'{nombre(url)} se carga cortada (falta el final del HTML)')
        txt = TEXTOS.get(nombre(url))
        if txt and txt not in html:
            fallos.append(f'{nombre(url)} carga pero no aparece "{txt}"')
        for ref in re.findall(r'(?:src|href)="([^"#]+)"', html):
            if '${' in ref or ref.startswith(('mailto:', 'tel:', 'data:', 'javascript:')):
                continue
            absol = urllib.parse.urljoin(url, ref)
            if urllib.parse.urlparse(absol).netloc == DOMINIO:
                recursos.add(urllib.parse.quote(absol, safe=':/?&=%~+'))

    # 3. Imágenes, cartas, enlaces internos y archivos clave
    for r in EXTRA:
        recursos.add(BASE + r)
    for url in sorted(recursos - set(paginas)):
        st, _, _, _ = pedir(url, 'HEAD')
        if st == 405:
            st, _, _, _ = pedir(url)
        if st != 200:
            fallos.append(f'No carga: {nombre(url)} (respuesta {st or "sin respuesta"})')

    # 4. Redirecciones de URL antiguas
    for ruta in ANTIGUAS:
        st, cuerpo, _, _ = pedir(BASE + ruta)
        if st != 200 or b'refresh' not in cuerpo.lower():
            fallos.append(f'La redirección antigua {ruta} ya no funciona (respuesta {st})')

    # 5. www y http
    for url in (f'https://www.{DOMINIO}/', f'http://{DOMINIO}/'):
        st, _, _, final = pedir(url)
        if st != 200 or not final.startswith(BASE):
            avisos.append(f'{url} no lleva bien a la web (respuesta {st}, acaba en {final})')

    # Resumen
    hoy = datetime.now().strftime('%d/%m/%Y %H:%M')
    media = sum(tiempos) / len(tiempos) if tiempos else 0
    lineas = []
    if fallos:
        lineas.append(f'⚠️ WEB GRUPO 2.0: HAY {len(fallos)} PROBLEMA(S) · {hoy}')
        lineas += [f'- {f}' for f in fallos]
    else:
        lineas.append(f'✅ Web Grupo 2.0: todo funciona · {hoy}')
    if avisos:
        lineas.append('Avisos (no urgente):')
        lineas += [f'- {a}' for a in avisos]
    lineas.append(f'Revisadas {len(paginas)} páginas, {len(recursos - set(paginas))} imágenes/archivos/enlaces '
                  f'y {len(ANTIGUAS)} redirecciones. Carga media {media:.1f} s.'
                  + (f' Certificado HTTPS válido {dias} días más.' if dias is not None else ''))
    print('\n'.join(lineas))
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
