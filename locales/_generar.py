#!/usr/bin/env python3
"""Genera las páginas SEO de cada local: locales/<slug>/index.html

Uso (desde la carpeta "Pagina Web"):  python3 locales/_generar.py
Al cambiar un horario, dirección o enlace: editarlo en LOCALES (abajo), volver a
generar y actualizar también index.html (D{}, HORARIOS{} y el JSON-LD) y llms.txt.
GitHub Pages no publica este archivo (empieza por "_").
"""
import json, os, html
from urllib.parse import quote

BASE = 'https://grupodospuntocero.com'
WA = '34656485099'
TEL = '+34656485099'
DIAS = {'Mo': ('Monday', 'Lunes'), 'Tu': ('Tuesday', 'Martes'), 'We': ('Wednesday', 'Miércoles'),
        'Th': ('Thursday', 'Jueves'), 'Fr': ('Friday', 'Viernes'), 'Sa': ('Saturday', 'Sábado'),
        'Su': ('Sunday', 'Domingo')}
ORDEN = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

# horario: lista de (días, abre, cierra). Cierre menor que apertura = de madrugada del día siguiente.
LOCALES = [
  dict(
    slug='las-tablas', key='tablas', ancla='sec-tablas', nombre='Las Tablas 2.0', color='#e51d1e',
    tipo=['BarOrPub'], tipo_txt='Bar de copas', zona='Barrio de Salamanca',
    calle='Calle del General Oraá, 26', cp='28006', maps='C+General+Ora%C3%A1+26+Madrid',
    ig='lastablas2.0', fotos='tablas', logo='Las Tablas-06-trans.webp',
    horario=[(['Th', 'Fr', 'Sa'], '20:00', '02:00')],
    title='Las Tablas 2.0 · Bar de copas en General Oraá, Madrid',
    desc='Bar de copas en la calle General Oraá, 26 (barrio de Salamanca, Madrid). Abierto de jueves a sábado de 20:00 a 02:00. Reservas y cumpleaños por WhatsApp.',
    tagline='Detrás de la cortina no nos ve la vecina. Y nos importa tres copas.',
    intro=[
      'Las Tablas 2.0 es nuestro bar de copas en la calle General Oraá, en pleno barrio de Salamanca. Un sitio para empezar la noche con una copa bien puesta, quedarte más de lo previsto y salir con la sensación de que el jueves también cuenta como fin de semana.',
      'Ambiente de bar de toda la vida con el punto canalla de la familia 2.0: buena música, gente con ganas y una cortina que guarda lo que pasa dentro. Abrimos de jueves a sábado desde las ocho de la tarde hasta las dos de la madrugada.',
    ],
    planes=['Copas de jueves a sábado sin tener que cruzar Madrid', 'Cumpleaños y quedadas de grupo: escríbenos y te guardamos sitio', 'Primera parada antes de seguir la noche en La Pequeña 2.0, justo enfrente'],
    extra_faq=[('¿Está cerca de La Pequeña 2.0?', 'Sí. La Pequeña 2.0 está en General Oraá, 27, justo enfrente, así que el cambio de bar es cuestión de cruzar la calle.')],
    otros_cerca=['la-pequena'],
  ),
  dict(
    slug='la-pequena', key='pequeña', ancla='sec-peque%C3%B1a', nombre='La Pequeña 2.0', color='#3a4ba8',
    tipo=['BarOrPub'], tipo_txt='Bar de copas', zona='Barrio de Salamanca',
    calle='Calle del General Oraá, 27', cp='28006', maps='C+General+Ora%C3%A1+27+Madrid',
    ig='lapequena2.0', fotos='pequeña', logo='La pequeña_Mesa de trabajo 1-trans.webp',
    horario=[(['Th', 'Fr', 'Sa'], '20:00', '02:00')],
    title='La Pequeña 2.0 · Bar de copas de barrio en General Oraá',
    desc='La Pequeña 2.0: bar de copas de barrio en General Oraá, 27 (Salamanca, Madrid). De jueves a sábado de 20:00 a 02:00. Reserva tu mesa o tu cumple por WhatsApp.',
    tagline='Tan de barrio que hasta el camarero sabe lo que vas a pedir.',
    intro=[
      'La Pequeña 2.0 es el bar de copas más de barrio de la familia: en la calle General Oraá, 27, en el barrio de Salamanca. De esos sitios donde a la segunda visita ya te saludan por tu nombre y a la tercera no hace falta que pidas.',
      'Pequeña de tamaño y grande de planes: copas, música y buen rollo de jueves a sábado, de ocho de la tarde a dos de la madrugada. Ideal para quedar con los de siempre o para traer a los que todavía no conocen el barrio.',
    ],
    planes=['La copa de después del trabajo, sin postureo', 'Celebraciones pequeñas con trato de casa', 'Doble plan con Las Tablas 2.0, que está justo enfrente'],
    extra_faq=[('¿La Pequeña 2.0 sirve comidas?', 'Ahora mismo funciona como bar de copas. Si quieres comer o cenar, en la familia tienes La Traviesa 2.0 (López de Hoyos, 7) y Green 2.0 (Castellana, 40 bis).')],
    otros_cerca=['las-tablas'],
  ),
  dict(
    slug='la-chula', key='chula', ancla='sec-chula', nombre='La Chula 2.0', color='#e72f8a',
    tipo=['BarOrPub'], tipo_txt='Bar de copas', zona='Barrio de Salamanca',
    calle='Calle de Claudio Coello, 116', cp=None, maps='C+Claudio+Coello+116+Madrid',
    ig='lachula2.0', fotos='la chula', logo='La Chula_Mesa de trabajo 1-trans.webp',
    horario=[(['Th', 'Fr'], '20:00', '03:00'), (['Sa'], '20:00', '03:30')],
    title='La Chula 2.0 · Bar de copas en Claudio Coello, Madrid',
    desc='La Chula 2.0: bar de copas con neón en Claudio Coello, 116 (barrio de Salamanca). Jueves y viernes hasta las 3:00 y sábados hasta las 3:30. Reservas por WhatsApp.',
    tagline='Noches de neón, chupito de tregua y besos con lengua.',
    intro=[
      'La Chula 2.0 es el bar de copas con más neón de la familia, en la calle Claudio Coello, 116, en el barrio de Salamanca. Luz rosa, música alta y ese chupito de tregua que siempre aparece cuando hace falta.',
      'Es de los que más tarde cierran: jueves y viernes hasta las tres de la madrugada y los sábados hasta las tres y media. Perfecto para alargar la noche sin tener que cambiar de barrio.',
    ],
    planes=['Noches largas: hasta las 3:30 los sábados', 'Cumpleaños con foto de neón asegurada', 'Plan de amigas, de pareja o de grupo grande'],
    extra_faq=[],
    otros_cerca=[],
  ),
  dict(
    slug='la-peluqueria', key='peluca', ancla='sec-peluca', nombre='La Peluquería 2.0', color='#1db7d9',
    tipo=['BarOrPub'], tipo_txt='Bar de copas', zona='Chamartín',
    calle='Calle de Alberto Alcocer, 32', cp=None, maps='C+Alberto+Alcocer+32+Madrid',
    ig='lapeluqueria_2.0', fotos='la peluqueria', logo='La Peluquería-04-trans.webp',
    horario=[(['Th', 'Fr', 'Sa'], '20:00', '02:00')],
    title='La Peluquería 2.0 · Bar de copas en Alberto Alcocer',
    desc='La Peluquería 2.0: bar de copas en Alberto Alcocer, 32 (Chamartín, Madrid). Abierto de jueves a sábado de 20:00 a 02:00. Reservas y cumpleaños por WhatsApp.',
    tagline='¿Nos volamos la peluca? Mientras nos quede pelo, aquí seguimos.',
    intro=[
      'La Peluquería 2.0 es nuestro bar de copas en la calle Alberto Alcocer, 32, en Chamartín. Un sitio para volarse la peluca sin bajar al centro: copas, música y gente con ganas de que el fin de semana empiece el jueves.',
      'Abrimos de jueves a sábado de ocho de la tarde a dos de la madrugada. Si vives o trabajas por la zona norte de la Castellana, es tu sitio para la copa de después.',
    ],
    planes=['La copa de la zona norte, sin bajar al centro', 'Afterwork de jueves y viernes', 'Cumpleaños y celebraciones de grupo'],
    extra_faq=[],
    otros_cerca=[],
  ),
  dict(
    slug='la-traviesa', key='traviesa', ancla='sec-traviesa', nombre='La Traviesa 2.0', color='#8a7fc0',
    tipo=['Restaurant', 'BarOrPub'], tipo_txt='Restaurante y bar', zona='Barrio de Salamanca',
    calle='Calle de López de Hoyos, 7', cp='28006', maps='C+Lopez+de+Hoyos+7+Madrid',
    ig='latraviesa_2.0', fotos='la traviesa', logo='La traviesa_Mesa de trabajo 1-trans.webp',
    horario=[(['Mo', 'Tu', 'We'], '08:00', '17:00'), (['Th', 'Fr'], '08:00', '01:00'), (['Sa'], '18:00', '01:00')],
    carta='/cartas/traviesa.pdf',
    reservar='https://bookings.agorapos.com/reservas/widget/2169/calendar/82fc0510ac7baef2f81df0cb3bd03bcc59e3d54e',
    title='La Traviesa 2.0 · Restaurante y bar en López de Hoyos',
    desc='La Traviesa 2.0: restaurante y bar en López de Hoyos, 7 (Madrid). Desayunos, comidas, cenas y copas. Carta, reservas online y menús de Navidad para grupos.',
    tagline='La glotona de la familia. Come, bebe, y repite.',
    intro=[
      'La Traviesa 2.0 es la glotona de la familia: restaurante y bar en la calle López de Hoyos, 7, a un paso de la Castellana. Abrimos temprano para desayunos, seguimos con comidas y, de jueves a sábado, alargamos con cenas y copas.',
      'De lunes a miércoles estamos de 8:00 a 17:00; jueves y viernes de 8:00 a 1:00; y los sábados de 18:00 a 1:00. Los domingos descansamos. Consulta la carta de comida y vinos y reserva mesa online en un minuto.',
    ],
    planes=['Desayunos y comidas entre semana', 'Cenas y copas de jueves a sábado', 'Comidas y cenas de empresa: mira nuestros <a href="/traviesa/">menús de Navidad</a>'],
    extra_faq=[('¿Tenéis menús para grupos y empresas?', 'Sí. Para Navidad tenemos menús de grupo con bebida incluida; los tienes en <a href="/traviesa/">grupodospuntocero.com/traviesa</a>. Para otras fechas, escríbenos por WhatsApp.'),
               ('¿Abrís los domingos?', 'No, los domingos La Traviesa 2.0 está cerrada.')],
    otros_cerca=['green'],
  ),
  dict(
    slug='green', key='green', ancla='sec-green', nombre='Green 2.0', color='#4ade80',
    tipo=['Restaurant', 'BarOrPub', 'NightClub'], tipo_txt='Restaurante, bar y discoteca', zona='Paseo de la Castellana',
    calle='Paseo de la Castellana, 40 bis', cp='28046', maps='Paseo+de+la+Castellana+40+bis+Madrid',
    ig='green.madrid_2.0', fotos='green', logo='Green 2.0-trans.webp',
    horario=[(['Mo', 'Tu', 'We'], '08:00', '17:00'), (['Th', 'Fr'], '08:00', '06:00'), (['Sa'], '18:00', '06:00')],
    carta='/cartas/green.webp',
    entradas='https://www.fourvenues.com/iframe/green/events',
    title='Green 2.0 · Restaurante, bar y discoteca en la Castellana',
    desc='Green 2.0: restaurante, bar de copas y discoteca en Paseo de la Castellana, 40 bis (Madrid). Abierto hasta las 6:00 de jueves a sábado. Carta, entradas y reservas.',
    tagline='Tres en uno: restaurante, bar y discoteca. Como la navaja suiza, pero con más alcohol.',
    intro=[
      'Green 2.0 es el tres en uno de la familia: restaurante, bar de copas y discoteca en el Paseo de la Castellana, 40 bis. Puedes entrar a desayunar, quedarte a comer, volver a cenar y acabar bailando sin cambiar de dirección.',
      'De lunes a miércoles abrimos de 8:00 a 17:00. Jueves y viernes, de 8:00 a 6:00 de la madrugada; y los sábados, de 18:00 a 6:00. Consulta la carta, saca tus entradas para los eventos y reserva por WhatsApp.',
    ],
    planes=['Comer o cenar y seguir la fiesta en el mismo sitio', 'Discoteca hasta las 6:00 de jueves a sábado', 'Eventos, fiestas y cenas de empresa en la Castellana'],
    extra_faq=[('¿Cómo compro entradas para las fiestas de Green 2.0?', 'Las entradas y listas de los eventos están en Fourvenues: usa el botón «Entradas y eventos» de esta página.')],
    otros_cerca=['la-traviesa'],
  ),
]
POR_SLUG = {l['slug']: l for l in LOCALES}


def esc(s):
    return html.escape(s, quote=True)


def u(path):
    """URL absoluta con espacios/acentos codificados."""
    return BASE + quote(path)


def horario_filas(l):
    filas = []
    for d in ORDEN:
        tramo = next(((a, c) for ds, a, c in l['horario'] if d in ds), None)
        filas.append((DIAS[d][1], f'{tramo[0]} – {tramo[1]}' if tramo else 'Cerrado'))
    return filas


def horario_corto(l):
    partes = []
    for ds, a, c in l['horario']:
        nombres = [DIAS[d][1] for d in ds]
        dias = nombres[0] if len(nombres) == 1 else (f'{nombres[0]} a {nombres[-1]}' if len(nombres) > 2 else ' y '.join(nombres))
        partes.append(f'{dias.lower()} de {a} a {c}')
    return '; '.join(partes)


def schema(l):
    url = f'{BASE}/locales/{l["slug"]}/'
    addr = {'@type': 'PostalAddress', 'streetAddress': l['calle'], 'addressLocality': 'Madrid',
            'addressRegion': 'Comunidad de Madrid', 'addressCountry': 'ES'}
    if l['cp']:
        addr['postalCode'] = l['cp']
    nodo = {
        '@type': l['tipo'] if len(l['tipo']) > 1 else l['tipo'][0],
        # mismo @id que el JSON-LD de la portada (index.html) para que Google los una
        '@id': f'{BASE}/#{l["slug"].replace("las-", "").replace("la-", "")}',
        'name': l['nombre'], 'description': l['desc'], 'url': url,
        'image': [u(f'/fotos/{l["fotos"]}/{i}.webp') for i in (1, 2, 3, 4)],
        'logo': u(f'/logos/{l["logo"]}'),
        'telephone': TEL, 'priceRange': '€€', 'address': addr,
        'hasMap': f'https://maps.google.com/?q={l["maps"]}',
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': [DIAS[d][0] for d in ds], 'opens': a, 'closes': c}
            for ds, a, c in l['horario']],
        'sameAs': [f'https://www.instagram.com/{l["ig"]}'],
        'parentOrganization': {'@id': f'{BASE}/#org'},
    }
    if l.get('carta'):
        nodo['hasMenu'] = BASE + l['carta']
    if l.get('reservar'):
        nodo['acceptsReservations'] = l['reservar']
    elif 'Restaurant' in l['tipo']:
        nodo['acceptsReservations'] = True
    migas = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Grupo 2.0', 'item': BASE + '/'},
        {'@type': 'ListItem', 'position': 2, 'name': l['nombre'], 'item': url}]}
    return json.dumps({'@context': 'https://schema.org', '@graph': [nodo, migas]}, ensure_ascii=False, indent=1)


def faq(l):
    preguntas = [
        (f'¿Qué horario tiene {l["nombre"]}?', f'{l["nombre"]} abre {horario_corto(l)}. El resto de días está cerrado.'),
        (f'¿Dónde está {l["nombre"]}?', f'En {l["calle"]}, Madrid ({l["zona"]}).'),
        (f'¿Se puede reservar en {l["nombre"]}?',
         'Sí: reserva mesa online con el botón «Reservar mesa» o escríbenos por WhatsApp al 656 48 50 99.' if l.get('reservar')
         else 'Sí, escríbenos por WhatsApp al 656 48 50 99 y te guardamos sitio. Para grupos grandes, avísanos con unos días de antelación.'),
        (f'¿Puedo celebrar un cumpleaños o un evento privado en {l["nombre"]}?',
         'Claro. Organizamos cumpleaños, cenas de empresa, despedidas y celebraciones. Cuéntanos la fecha y cuántos sois por WhatsApp o en hola@grupodospuntocero.com.'),
    ] + l['extra_faq']
    return '\n'.join(f'<details><summary>{esc(q)}</summary><p>{a}</p></details>' for q, a in preguntas)


ICO = {
  'wa': '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.37 0 0 5.37 0 12c0 2.13.56 4.12 1.53 5.85L0 24l6.34-1.51A11.96 11.96 0 0 0 12 24c6.63 0 12-5.37 12-12S18.63 0 12 0zm0 22c-1.85 0-3.58-.48-5.1-1.32l-.36-.22-3.77.9.95-3.67-.24-.38A9.96 9.96 0 0 1 2 12C2 6.48 6.48 2 12 2s10 4.48 10 10-4.48 10-10 10zm5.47-7.62c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.3 1.26.49 1.7.63.71.22 1.36.2 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.08-.13-.27-.2-.57-.35z"/></svg>',
  'pin': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
  'ig': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".5" fill="currentColor"/></svg>',
  'carta': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
  'cal': '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
}

CSS = """
:root{--bg:#0a0908;--surface:#141210;--txt:#f0ebe4;--txt2:rgba(240,235,228,.7);--bdr:rgba(255,255,255,.1)}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--txt);font-family:'Montserrat',system-ui,sans-serif;font-size:16px;line-height:1.65;-webkit-font-smoothing:antialiased}
a{color:inherit}
:focus-visible{outline:3px solid var(--lc);outline-offset:3px;border-radius:6px}
.wrap{max-width:1080px;margin:0 auto;padding:0 clamp(16px,4vw,32px)}
header{position:sticky;top:0;z-index:10;background:rgba(10,9,8,.82);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--bdr)}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:60px}
.brand{font-family:'Archivo Black',sans-serif;font-size:15px;letter-spacing:.04em;text-decoration:none;display:flex;align-items:center;gap:8px}
.brand span{opacity:.55;font-family:'Montserrat',sans-serif;font-weight:600;font-size:12px}
.hwa{display:inline-flex;align-items:center;gap:7px;background:#25d366;color:#04140a;font-weight:700;font-size:13px;text-decoration:none;padding:10px 16px;border-radius:100px;min-height:44px}
.hero{position:relative;min-height:min(78svh,640px);display:flex;align-items:flex-end;overflow:hidden}
.hero img.bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,9,8,.25) 0%,rgba(10,9,8,.55) 45%,var(--bg) 100%)}
.hero .wrap{position:relative;z-index:1;padding-bottom:clamp(28px,6vw,56px);width:100%}
.crumbs{font-size:12px;color:var(--txt2);margin-bottom:18px}
.crumbs a{text-decoration:none;border-bottom:1px solid var(--bdr)}
.logo{height:clamp(54px,9vw,84px);width:auto;margin-bottom:14px;filter:drop-shadow(0 4px 18px rgba(0,0,0,.6))}
.eyebrow{display:inline-block;text-shadow:0 1px 10px rgba(0,0,0,.9),0 0 2px rgba(0,0,0,.8);font-size:12px;font-weight:800;letter-spacing:.14em;text-transform:uppercase;color:var(--lc);margin-bottom:8px}
h1{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:clamp(34px,7vw,68px);line-height:1.02;letter-spacing:-.01em}
.sub{font-size:clamp(15px,2.2vw,18px);color:var(--txt2);margin-top:10px;max-width:640px}
.tagline{font-style:italic;margin-top:16px;font-size:clamp(15px,2vw,17px);border-left:3px solid var(--lc);padding-left:12px;max-width:620px}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}
.btn{display:inline-flex;align-items:center;gap:8px;min-height:46px;padding:12px 20px;border-radius:12px;font-weight:700;font-size:14px;text-decoration:none;border:1px solid var(--bdr);background:rgba(255,255,255,.04);transition:border-color .2s,background .2s}
.btn:hover{border-color:var(--lc)}
.btn.pri{background:var(--lc);border-color:var(--lc);color:#0a0908}
.btn.wa{background:#25d366;border-color:#25d366;color:#04140a}
.estado{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:700;margin-top:18px;color:var(--txt2)}
.estado i{width:9px;height:9px;border-radius:50%;background:#777;display:inline-block}
.estado.on{color:#4ade80}.estado.on i{background:#4ade80;box-shadow:0 0 10px #4ade80}
main section{padding:clamp(40px,7vw,72px) 0;border-top:1px solid var(--bdr)}
h2{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:clamp(24px,4vw,34px);line-height:1.1;margin-bottom:18px}
.grid2{display:grid;grid-template-columns:1.3fr 1fr;gap:clamp(24px,5vw,56px)}
.txt p{color:var(--txt2);margin-bottom:14px;max-width:62ch}
.planes{list-style:none;margin-top:8px}
.planes li{padding:10px 0 10px 28px;position:relative;border-bottom:1px solid var(--bdr)}
.planes li::before{content:'';position:absolute;left:4px;top:19px;width:10px;height:10px;border-radius:50%;background:var(--lc)}
.card{background:var(--surface);border:1px solid var(--bdr);border-radius:18px;padding:22px}
.card h3{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--txt2);margin-bottom:10px}
table{width:100%;border-collapse:collapse;font-size:15px}
td{padding:7px 0;border-bottom:1px solid var(--bdr)}td:last-child{text-align:right;font-weight:700}
tr.hoy td{color:var(--lc)}
.dir{margin-top:20px;font-weight:700}.dir small{display:block;font-weight:400;color:var(--txt2)}
.fotos{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.fotos img{width:100%;height:auto;aspect-ratio:3/2;object-fit:cover;border-radius:14px;display:block}
details{border-bottom:1px solid var(--bdr);padding:16px 0}
summary{cursor:pointer;font-weight:700;font-size:16px;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:'+';color:var(--lc);font-size:22px;line-height:1}
details[open] summary::after{content:'–'}
details p{color:var(--txt2);margin-top:10px;max-width:70ch}
.otros{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px}
.otros a{display:block;text-decoration:none;padding:16px 18px;border:1px solid var(--bdr);border-radius:14px;transition:border-color .2s}
.otros a:hover{border-color:var(--oc)}
.otros b{display:block;font-family:'Archivo Black',sans-serif;font-weight:400;font-size:17px}
.otros span{font-size:13px;color:var(--txt2)}
footer{border-top:1px solid var(--bdr);padding:32px 0 48px;font-size:13px;color:var(--txt2)}
footer .wrap{display:flex;flex-wrap:wrap;gap:12px 24px;justify-content:space-between}
footer nav{display:flex;flex-wrap:wrap;gap:8px 18px}
footer a{text-decoration:none}footer a:hover{color:var(--txt)}
@media (max-width:760px){.grid2{grid-template-columns:1fr}.fotos{grid-template-columns:1fr 1fr}.brand span{display:none}}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""


def pagina(l):
    s = l['slug']
    url = f'{BASE}/locales/{s}/'
    foto1 = quote(f'/fotos/{l["fotos"]}/1.webp')
    wa_txt = quote(f'Hola! Quiero reservar en {l["nombre"]}')
    ctas = []
    if l.get('reservar'):
        ctas.append(f'<a class="btn pri" href="{esc(l["reservar"])}" target="_blank" rel="noopener">{ICO["cal"]} Reservar mesa</a>')
    if l.get('entradas'):
        ctas.append(f'<a class="btn pri" href="{esc(l["entradas"])}" target="_blank" rel="noopener">{ICO["cal"]} Entradas y eventos</a>')
    ctas.append(f'<a class="btn wa" href="https://wa.me/{WA}?text={wa_txt}" target="_blank" rel="noopener">{ICO["wa"]} Reservar por WhatsApp</a>')
    if l.get('carta'):
        ctas.append(f'<a class="btn" href="{quote(l["carta"])}" target="_blank" rel="noopener">{ICO["carta"]} Ver carta</a>')
    ctas.append(f'<a class="btn" href="https://maps.google.com/?q={l["maps"]}" target="_blank" rel="noopener">{ICO["pin"]} Cómo llegar</a>')
    ctas.append(f'<a class="btn" href="https://www.instagram.com/{l["ig"]}" target="_blank" rel="noopener">{ICO["ig"]} @{esc(l["ig"])}</a>')
    filas = '\n'.join(f'<tr data-d="{i}"><td>{d}</td><td>{h}</td></tr>' for i, (d, h) in enumerate(horario_filas(l)))
    fotos = '\n'.join(
        f'<img src="{quote("/fotos/" + l["fotos"] + f"/{i}.webp")}" alt="Ambiente de {esc(l["nombre"])} ({i} de 4)" width="1600" height="1066" loading="lazy" decoding="async">'
        for i in (1, 2, 3, 4))
    cerca = [POR_SLUG[x] for x in l['otros_cerca']]
    resto = cerca + [o for o in LOCALES if o['slug'] != s and o not in cerca]
    otros = '\n'.join(
        f'<a href="/locales/{o["slug"]}/" style="--oc:{o["color"]}"><b>{esc(o["nombre"])}</b><span>{esc(o["tipo_txt"])} · {esc(o["calle"].replace("Calle de ", "").replace("Calle del ", ""))}</span></a>'
        for o in resto)
    pie = '\n'.join(f'<a href="/locales/{o["slug"]}/">{esc(o["nombre"])}</a>' for o in LOCALES)
    # horario para el badge "abierto ahora" (getDay: 0=domingo)
    js_h = json.dumps([[[(ORDEN.index(d) + 1) % 7 for d in ds], a, c] for ds, a, c in l['horario']])
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<!-- Página generada por locales/_generar.py — no editar a mano -->
<title>{esc(l['title'])}</title>
<meta name="description" content="{esc(l['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a0908">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Grupo 2.0">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(l['title'])}">
<meta property="og:description" content="{esc(l['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{foto1}">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1066">
<meta property="og:image:alt" content="{esc(l['nombre'])}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" as="image" href="{foto1}" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Montserrat:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema(l)}
</script>
<style>{CSS}</style>
</head>
<body style="--lc:{l['color']}">
<header><div class="wrap">
  <a class="brand" href="/">GRUPO_2.0 <span>· {len(LOCALES)} locales en Madrid</span></a>
  <a class="hwa" href="https://wa.me/{WA}?text={wa_txt}" target="_blank" rel="noopener">{ICO['wa']} Reservar</a>
</div></header>

<main>
<div class="hero">
  <img class="bg" src="{foto1}" alt="" width="1600" height="1066" fetchpriority="high">
  <div class="wrap">
    <nav class="crumbs" aria-label="Ruta"><a href="/">Grupo 2.0</a> / {esc(l['nombre'])}</nav>
    <img class="logo" src="{quote('/logos/' + l['logo'])}" alt="Logo de {esc(l['nombre'])}">
    <div class="eyebrow">{esc(l['tipo_txt'])} · {esc(l['zona'])}</div>
    <h1>{esc(l['nombre'])}</h1>
    <p class="sub">{esc(l['tipo_txt'])} en {esc(l['calle'])}, Madrid.</p>
    <p class="tagline">“{esc(l['tagline'])}”</p>
    <div class="estado" id="estado"><i></i><span>Horario: {esc(horario_corto(l))}</span></div>
    <div class="ctas">
      {chr(10).join('      ' + c for c in ctas).strip()}
    </div>
  </div>
</div>

<section><div class="wrap grid2">
  <div class="txt">
    <h2>Así es {esc(l['nombre'])}</h2>
    {''.join(f'<p>{p}</p>' for p in l['intro'])}
    <ul class="planes">{''.join(f'<li>{p}</li>' for p in l['planes'])}</ul>
  </div>
  <aside class="card" aria-labelledby="h-hor">
    <h3 id="h-hor">Horario</h3>
    <table><tbody>
{filas}
    </tbody></table>
    <p class="dir">{esc(l['calle'])}<small>Madrid · {esc(l['zona'])}</small></p>
    <p class="dir">656 48 50 99<small>WhatsApp y reservas</small></p>
  </aside>
</div></section>

<section><div class="wrap">
  <h2>Fotos</h2>
  <div class="fotos">
{fotos}
  </div>
</div></section>

<section><div class="wrap">
  <h2>Preguntas rápidas</h2>
  {faq(l)}
</div></section>

<section><div class="wrap">
  <h2>Más planes de la familia 2.0</h2>
  <div class="otros">
{otros}
  </div>
</div></section>
</main>

<footer><div class="wrap">
  <div>© 2026 Grupo 2.0 · Madrid · <a href="https://wa.me/{WA}">656 48 50 99</a> · <a href="mailto:hola@grupodospuntocero.com">hola@grupodospuntocero.com</a></div>
  <nav aria-label="Locales">{pie}</nav>
  <nav aria-label="Legal"><a href="/#aviso">Aviso legal</a><a href="/#privacidad">Privacidad</a><a href="/#cookies">Cookies</a></nav>
</div></footer>

<script>
/* abierto ahora + día de hoy resaltado */
(function(){{
  var H={js_h};
  function t(s){{var p=s.split(':');return +p[0]+p[1]/60}}
  var n=new Date(),d=n.getDay(),h=n.getHours()+n.getMinutes()/60,prev=(d+6)%7,on=false;
  H.forEach(function(r){{var a=t(r[1]),c=t(r[2]);if(c<=a)c+=24;
    if(r[0].indexOf(d)>-1&&h>=a&&h<Math.min(c,24))on=true;
    if(r[0].indexOf(prev)>-1&&c>24&&h<c-24)on=true;}});
  var e=document.getElementById('estado');
  if(on){{e.className='estado on';e.lastChild.textContent='Abierto ahora'}}
  var fila=document.querySelector('tr[data-d="'+((d+6)%7)+'"]');if(fila)fila.className='hoy';
}})();
</script>
</body>
</html>
'''


if __name__ == '__main__':
    raiz = os.path.dirname(os.path.abspath(__file__))
    for l in LOCALES:
        os.makedirs(os.path.join(raiz, l['slug']), exist_ok=True)
        with open(os.path.join(raiz, l['slug'], 'index.html'), 'w', encoding='utf-8') as f:
            f.write(pagina(l))
        print('ok', l['slug'])
