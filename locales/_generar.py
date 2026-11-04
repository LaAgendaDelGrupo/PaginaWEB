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
    horario=[(['Th'], '20:00', '03:00'), (['Fr', 'Sa'], '20:00', '03:30')],
    title='La Chula 2.0 · Bar de copas en Claudio Coello, Madrid',
    desc='La Chula 2.0: bar de copas con neón en Claudio Coello, 116 (barrio de Salamanca). Jueves hasta las 3:00; viernes y sábados hasta las 3:30. Reservas por WhatsApp.',
    tagline='Noches de neón, chupito de tregua y besos con lengua.',
    intro=[
      'La Chula 2.0 es el bar de copas con más neón de la familia, en la calle Claudio Coello, 116, en el barrio de Salamanca. Luz rosa, música alta y ese chupito de tregua que siempre aparece cuando hace falta.',
      'Es de los que más tarde cierran: los jueves hasta las tres de la madrugada y los viernes y sábados hasta las tres y media. Perfecto para alargar la noche sin tener que cambiar de barrio.',
    ],
    planes=['Noches largas: hasta las 3:30 los viernes y sábados', 'Cumpleaños con foto de neón asegurada', 'Plan de amigas, de pareja o de grupo grande'],
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

# Cartas en texto (SEO: Google y los buscadores con IA leen los platos y precios).
# Transcritas de cartas/traviesa.pdf y cartas/green.webp (04/11/2026; Green: versión definitiva «Green Social Club 2.0»). Al cambiar la carta impresa,
# actualizar también esto y volver a generar. Platos: (nombre, descripción, precio, [nº alérgenos]).
ALERGENOS_TRAVIESA = ['Gluten', 'Crustáceos', 'Huevo', 'Pescado', 'Cacahuetes', 'Soja', 'Lácteos', 'Frutos de cáscara',
                      'Apio', 'Mostaza', 'Sésamo', 'Sulfitos', 'Altramuces', 'Moluscos']
ALERGENOS_GREEN = ['Gluten', 'Huevo', 'Crustáceos', 'Pescado', 'Cacahuetes', 'Soja', 'Lácteos', 'Apio',
                   'Frutos de cáscara', 'Sésamo', 'Moluscos', 'Mostaza', 'Altramuces', 'Sulfitos']
CARTAS = {
  'traviesa': dict(
    alergenos=ALERGENOS_TRAVIESA,
    intro='Cocina de producto para picar, compartir o sentarse en serio: gildas y montaditos por unidad, tapeo, huerta, principales y postres caseros, con una carta de vinos de Rioja, Ribera, Rueda, Valdeorras y Rías Baixas.',
    secciones=[
      ('Por unidad', [
        ('Gilda clásica', '', '3,50', [1, 4]),
        ('Anchoa 00', 'Sobre pan tostado con mantequilla ahumada', '6,50', [1, 4, 7]),
        ('Sardina ahumada', 'Sobre pan tostado con gelatina de tomate y AOVE', '6,50', [1, 4]),
        ('Huevo relleno de bonito', '', '3,50', [3, 4]),
        ('Pimiento de piquillo relleno de bacalao desmigado', '', '4,50', [1, 4]),
        ('Zamburiña a la plancha', 'Con sofrito de alga wakame y ron', '4,50', [2, 14]),
      ]),
      ('Tapeo', [
        ('Torreznitos con escamas de sal', '', '11,50', []),
        ('Ensaladilla rusa con bonito y piparras', '', '8,00', [3, 4]),
        ('Croquetas cremosas de jamón', '5 unidades', '9,00', [1, 3, 7]),
        ('Cecina de León', 'Con almendras tostadas y AOVE', '13,50', [8]),
        ('Pepito de solomillo de vaca', 'Con pimientos caramelizados', '13,50', [1]),
        ('Bocata de chipirones fritos', 'Con mayonesa cítrica', '9,50', [1, 3, 14]),
        ('Tacos de bacalao en tempura', 'Con mayonesa cítrica', '15,50', [1, 3, 4]),
        ('Potito travieso', '', '10,00', [3, 7]),
        ('Mejillones a la crema', '', '13,50', [7, 14]),
        ('Coquinas a la plancha', '', '22,50', [14]),
      ]),
      ('Huerta', [
        ('Puerro asado con salsa romescu', '', '12,50', [8]),
        ('Tomate azul', 'Preparado con emulsión de tomate, AOVE y sal', '11,50', []),
        ('Piparras fritas', '', '10,50', []),
        ('Burrata', 'Sobre pimientos caramelizados y polvo de pistacho', '16,50', [7, 8]),
        ('Alcachofas confitadas con huevo de codorniz', '', '12,50', [3]),
      ]),
      ('Principales', [
        ('Fideuá negra con chipirones', '', '23,00', [1, 2, 3, 4, 14]),
        ('Kokotxas al pil pil', 'Con huevos fritos y patatas chips', '23,50', [3, 4]),
        ('Arroz meloso con rabo de toro', '', '17,50', [7]),
        ('Fino escalope', 'Con huevo poché y queso manchego rallado', '22,50', [1, 3, 7]),
        ('Tataki de pluma ibérica', 'Con mermelada de piquillos', '23,50', [6]),
      ]),
      ('Guarniciones', [
        ('Patatas fritas', '', '3,50', []),
        ('Pimientos caramelizados', '', '3,50', []),
      ]),
      ('Postres', [
        ('Lemon curd', '', '6,50', [1, 3, 7]),
        ('Brownie con helado de canela', '', '6,50', [1, 3, 7]),
        ('Natillas con polvo Biscoff', '', '6,50', [1, 3, 7]),
        ('Arroz con leche', '', '6,50', [7]),
        ('Crema de mascarpone con pistacho', '', '6,50', [7, 8]),
      ]),
      ('Vinos tintos', [
        ('Viña Vigenza Crianza', 'D.O. Rioja · Marqués de Reinosa · Tempranillo', '22', []),
        ('Ramón Bilbao Crianza', 'D.O. Rioja · Bodegas Ramón Bilbao · Tempranillo', '25', []),
        ('Azpilicueta Reserva', 'D.O. Rioja · Azpilicueta · Tempranillo, Graciano y Mazuelo', '29', []),
        ('Vilano Roble', 'Ribera del Duero · Bodegas Vilano · Tinta del País', '22', []),
        ('Cantovera 9 Meses', 'Ribera del Duero · Cantovera · Tempranillo', '25', []),
        ('Cepa 21', 'Ribera del Duero · Bodegas Cepa 21 · Tempranillo', '39', []),
        ('La Rinconada', 'Barcolobo · Tempranillo', '24', []),
        ('Victoria', 'Barcolobo · Cabernet Sauvignon, Syrah y Tempranillo', '29', []),
        ('Habla del Silencio', 'Bodegas Habla · Syrah, Cabernet Sauvignon y Tempranillo', '29', []),
      ]),
      ('Vinos blancos', [
        ('José Pariente Verdejo', 'Rueda · José Pariente · Verdejo', '26', []),
        ('O Luar do Sil', 'Valdeorras · Pago de los Capellanes · Godello', '31', []),
        ('Godeval', 'Valdeorras · Bodegas Godeval · Godello', '29', []),
        ('Lagar de Deuses', 'Monterrei · Méndez-Rojo · Godello', '27', []),
        ('Carta Marina', 'Rías Baixas · Vía Atlántica · Albariño', '24', []),
        ('Mar de Frades', 'Rías Baixas · Mar de Frades · Albariño', '35', []),
        ('Paco & Lola', 'Rías Baixas · Paco & Lola · Albariño', '29', []),
        ('Flor Innata', 'Castilla y León · Valdecuevas · Verdejo y Sauvignon Blanc', '21', []),
        ('Valdecuevas Sauvignon Blanc', 'Castilla y León · Valdecuevas · Sauvignon Blanc', '26', []),
      ]),
    ]),
  'green': dict(
    alergenos=ALERGENOS_GREEN,
    intro='La carta de Green Social Club 2.0 para picar entre copa y copa, disponible jueves, viernes y sábado de 20:00 a 06:00: brioches, bravas, croquetas, tequeños, torreznos y más.',
    secciones=[
      ('Para picar', [
        ('Cono de patatas paja', '', '2,50', []),
        ('Slice de pizza', 'BBQ, york y queso o pepperoni', '3,00', [1, 2, 6, 7]),
        ('Brioche Green', 'Rabas con mahonesa cítrica, pulled pork BBQ, pollo con queso de cabra o carrillera de ternera', '6,50', [1, 2, 3, 6, 7, 8, 14]),
        ('Bravas Green', '', '9,00', []),
        ('Croquetas de jamón', '', '10,00', [1, 2, 7]),
        ('Tequeños', '', '12,00', [1, 2, 7]),
        ('Torreznos', '', '12,00', []),
        ('Fingers de pollo', '', '14,00', [1, 2, 6, 7]),
        ('Trufada de patata', '', '14,00', [2, 7, 14]),
      ]),
    ]),
}


def esc(s):
    return html.escape(s, quote=True)


def u(path):
    """URL absoluta con espacios/acentos codificados."""
    return BASE + quote(path)


# Estética de cada local, igual que en la portada (index.html): número y etiqueta del capítulo,
# etiquetas de horario/dirección, color en RGB y color de texto legible en noche/día.
ESTILO = {
    'tablas':   dict(num='01', label='BAR DE COPAS', tag_hor='Jue–Sáb · 20:00–02:00', tag_dir='C/ General Oraá, 26',
                     rgb='229,29,30', txt_n='#ff5a5b', txt_d='#c2181a'),
    'pequeña':  dict(num='02', label='BAR DE COPAS', tag_hor='Jue–Sáb · 20:00–02:00', tag_dir='C/ General Oraá, 27',
                     rgb='58,75,168', txt_n='#8d9cf0', txt_d='#2f388b'),
    'chula':    dict(num='03', label='COPAS Y NEÓN', tag_hor='J 20–03 · V–S 20–03:30', tag_dir='C/ Claudio Coello, 116',
                     rgb='231,47,138', txt_n='#ff6fb0', txt_d='#c0186c'),
    'peluca':   dict(num='04', label='BAR DE COPAS', tag_hor='Jue–Sáb · 20:00–02:00', tag_dir='C/ Alberto Alcocer, 32',
                     rgb='29,183,217', txt_n='#4fd2ef', txt_d='#0b7590'),
    'traviesa': dict(num='05', label='RESTAURANTE', tag_hor='L–X 08–17 · J–V 08–01 · S 18–01', tag_dir='C/ López de Hoyos, 7',
                     rgb='138,127,192', txt_n='#b3a9ea', txt_d='#5b4f8a'),
    'green':    dict(num='07', label='RESTAURANTE · BAR · DISCOTECA', tag_hor='L–X 08–17 · J–V 08–06 · S 18–06', tag_dir='P.º de la Castellana, 40 bis',
                     rgb='74,222,128', txt_n='#4ade80', txt_d='#15803d'),
}

# animación del logo de cada local (las mismas que en la portada)
ANIM_LOGO = {
    'tablas': "animation:tablasPunch 2.8s cubic-bezier(.36,.07,.19,.97) infinite}@keyframes tablasPunch{0%,90%,100%{transform:translate(0,0) rotate(0)}92%{transform:translate(-3px,1px) rotate(-1deg)}94%{transform:translate(3px,-1px) rotate(1.2deg)}96%{transform:translate(-2px,0) rotate(-.8deg)}98%{transform:translate(2px,1px) rotate(.5deg)}",
    'pequeña': "animation:peqFloat 5s ease-in-out infinite}@keyframes peqFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}",
    'chula': "animation:chulaNeon 3.2s ease-in-out infinite}@keyframes chulaNeon{0%,100%{filter:drop-shadow(0 0 5px rgba(231,47,138,.45)) brightness(1)}8%{filter:none}10%{filter:drop-shadow(0 0 10px rgba(231,47,138,.7)) brightness(1.07)}12%{filter:drop-shadow(0 0 3px rgba(231,47,138,.3)) brightness(.9)}14%{filter:drop-shadow(0 0 12px rgba(231,47,138,.8)) brightness(1.1)}50%{filter:drop-shadow(0 0 7px rgba(231,47,138,.55)) brightness(1.03)}",
    'peluca': "animation:pelWobble 4s ease-in-out infinite}@keyframes pelWobble{0%,100%{transform:rotate(0)}20%{transform:rotate(1.8deg)}40%{transform:rotate(-1.5deg)}60%{transform:rotate(1deg)}80%{transform:rotate(-1deg)}",
    'traviesa': "animation:travBreathe 6s ease-in-out infinite}@keyframes travBreathe{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}",
    'green': "animation:greenSway 7s ease-in-out infinite;transform-origin:50% 85%}@keyframes greenSway{0%,100%{transform:rotate(0) translateY(0)}25%{transform:rotate(2deg) translateY(-3px)}75%{transform:rotate(-1.6deg) translateY(2px)}",
}


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
    menu = menu_schema(l)
    if menu:
        nodo['hasMenu'] = menu
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
         'Claro. Organizamos cumpleaños, cenas de empresa, despedidas y celebraciones. Cuéntanos la fecha y cuántos sois por WhatsApp o en <a href="mailto:hola@grupodospuntocero.com">hola@grupodospuntocero.com</a>, o mira cómo funcionan los <a href="/eventos/">eventos en Grupo 2.0</a>.'),
    ] + l['extra_faq']
    return '\n'.join(f'<details class="fq rev"><summary>{esc(q)}<span class="fq-i" aria-hidden="true"></span></summary><p>{a}</p></details>' for q, a in preguntas)


def precio_num(p):
    return p.replace(',', '.')


def carta_html(l):
    c = CARTAS.get(l['key'])
    if not c:
        return ''
    al = c['alergenos']
    secs = []
    for titulo, platos in c['secciones']:
        items = []
        for nombre, desc, precio, ns in platos:
            alg = f'<span class="mn-al">{esc(", ".join(al[n - 1] for n in ns))}</span>' if ns else ''
            d = f'<span class="mn-d">{esc(desc)}</span>' if desc else ''
            items.append(f'<li><div class="mn-row"><span class="mn-n">{esc(nombre)}</span><span class="mn-dots" aria-hidden="true"></span><span class="mn-p">{esc(precio)} €</span></div>{d}{alg}</li>')
        secs.append(f'<div class="mn-sec rev"><h3>{esc(titulo)}</h3><ul>{"".join(items)}</ul></div>')
    pdf = l.get('carta', '')
    descarga = f'<a class="btn btn-ghost" href="{quote(pdf)}" target="_blank" rel="noopener">{ICO["carta"]} Carta original{" (PDF)" if pdf.endswith(".pdf") else ""}</a>' if pdf else ''
    return f'''
<section class="sec" id="carta" aria-labelledby="h-carta">
  <div class="ci rev"><div><div class="ci-eyebrow">La carta</div><h2 id="h-carta">Qué se come en {esc(l['nombre'])}</h2></div></div>
  <p class="mn-intro rev">{esc(c['intro'])}</p>
  <div class="mn-grid">
{chr(10).join(secs)}
  </div>
  <div class="mn-foot rev"><p>Precios con IVA incluido según la carta vigente; pueden cambiar. Debajo de cada plato, sus alérgenos: si tienes alguna alergia o intolerancia, avísanos al pedir.</p>{descarga}</div>
</section>
'''


def menu_schema(l):
    c = CARTAS.get(l['key'])
    if not c:
        return BASE + l['carta'] if l.get('carta') else None
    return {
        '@type': 'Menu', 'name': f'Carta de {l["nombre"]}', 'inLanguage': 'es',
        'url': f'{BASE}/locales/{l["slug"]}/#carta',
        'hasMenuSection': [{
            '@type': 'MenuSection', 'name': t,
            'hasMenuItem': [dict({'@type': 'MenuItem', 'name': n,
                                  'offers': {'@type': 'Offer', 'price': precio_num(p), 'priceCurrency': 'EUR'}},
                                 **({'description': d} if d else {}))
                            for n, d, p, _ in platos]} for t, platos in c['secciones']],
    }


WA_PATH = 'M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12 0C5.373 0 0 5.373 0 12c0 2.125.558 4.124 1.527 5.854L0 24l6.335-1.508A11.956 11.956 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.848 0-3.584-.479-5.096-1.32l-.364-.217-3.763.896.944-3.669-.235-.378A9.956 9.956 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z'
ICO = {
  'wa': f'<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg>',
  'pin': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
  'ig': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".5" fill="currentColor"/></svg>',
  'carta': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
  'cal': '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
  'arrow': '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M5 12h14M12 5l7 7-7 7"/></svg>',
  'tt': '<svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19.6 6.7a4.8 4.8 0 0 1-3.8-4.2V2h-3.4v13.7a2.9 2.9 0 1 1-2-2.7V9.5a6.3 6.3 0 1 0 5.4 6.2V8.8a8.2 8.2 0 0 0 4.8 1.5V6.9a4.8 4.8 0 0 1-1-.2z"/></svg>',
}

# Mismos tokens, tipografías y piezas que index.html (nav, botones, capítulos, ticker, pie, tema día/noche)
CSS = """
:root{
  --bg:#0a0908;--surface:#11100e;--txt:#f0ebe4;--txt2:rgba(240,235,228,.68);--txt3:rgba(240,235,228,.52);
  --bdr:rgba(255,255,255,.07);--bdr2:rgba(255,255,255,.12);--fucsia:#e72f8a;
  --ease:cubic-bezier(.22,1,.36,1);--easeSnap:cubic-bezier(.34,1.56,.64,1);
  --nav-scrolled:rgba(10,9,8,.78);--nav-bdr:rgba(255,255,255,.05);--tag-bg:rgba(255,255,255,.06);--tag-txt:rgba(240,235,228,.72);
  --card:#161412;--outline:rgba(240,235,228,.07);--photo-shadow:rgba(0,0,0,.5);--soc-bg:rgba(255,255,255,.05);--ft-bg:#080706;
  --arrow-bdr:rgba(255,255,255,.22);--glow:.14
}
[data-theme="day"]{
  --bg:#f5f0e8;--surface:#ece5da;--txt:#1a1510;--txt2:rgba(26,21,16,.72);--txt3:rgba(26,21,16,.62);
  --bdr:rgba(0,0,0,.08);--bdr2:rgba(0,0,0,.13);--nav-scrolled:rgba(245,240,232,.82);--nav-bdr:rgba(0,0,0,.06);
  --tag-bg:rgba(0,0,0,.06);--tag-txt:rgba(26,21,16,.75);--card:#fbf7f0;--outline:rgba(26,21,16,.08);--photo-shadow:rgba(0,0,0,.2);
  --soc-bg:rgba(0,0,0,.06);--ft-bg:#ebe4d8;--arrow-bdr:rgba(0,0,0,.24);--glow:.1
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;scrollbar-gutter:stable}
/* color de texto del local: se resuelve en body, donde están --lct-n / --lct-d */
body{--lct:var(--lct-n)}
[data-theme="day"] body{--lct:var(--lct-d)}
body{background:var(--bg);color:var(--txt);font-family:'Montserrat',sans-serif;font-size:16px;line-height:1.65;overflow-x:hidden;-webkit-font-smoothing:antialiased;transition:background .5s,color .5s}
a{color:inherit;text-decoration:none}
img{max-width:100%}
::selection{background:var(--fucsia);color:#fff}
:focus{outline:none}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--lc);outline-offset:3px;border-radius:6px}
.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.skip-link{position:fixed;top:-60px;left:12px;z-index:9999;background:var(--fucsia);color:#fff;padding:11px 18px;border-radius:8px;font-weight:700;font-size:13px;transition:top .25s var(--ease)}
.skip-link:focus{top:12px}

/* cursor copa (solo con ratón) */
#cur{position:fixed;left:0;top:0;pointer-events:none;z-index:9000;width:7px;height:7px;border-radius:50%;background:var(--fucsia);transform:translate(-50%,-50%)}
#cur:not(.on){opacity:0}
html.copa-cursor #cur{width:34px;height:34px;border-radius:0;background:none}
html.copa-cursor #cur img{width:100%;height:100%;object-fit:contain;display:block;filter:drop-shadow(0 2px 6px rgba(0,0,0,.3))}
@media(hover:hover){html.copa-cursor,html.copa-cursor *{cursor:none!important}}
@media(hover:none){#cur{display:none}}

/* nav */
#nav{position:fixed;top:0;left:0;right:0;z-index:500;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:22px 48px;transition:padding .4s var(--ease),background .4s,border-color .4s;border-bottom:1px solid transparent}
#nav.scrolled{background:var(--nav-scrolled);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);padding:13px 48px;border-bottom-color:var(--nav-bdr)}
.nav-pill{font-family:'Archivo Black',sans-serif;font-size:13px;letter-spacing:.16em;border:2px solid var(--txt);border-radius:100px;padding:7px 18px;display:inline-block;transition:background .3s,color .3s}
.nav-pill:hover{background:var(--txt);color:var(--bg)}
.nav-links{display:flex;gap:34px;list-style:none}
.nav-links a{font-size:11px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;opacity:.6;transition:opacity .2s;position:relative}
.nav-links a::after{content:'';position:absolute;left:0;bottom:-5px;width:0;height:1.5px;background:var(--lc);transition:width .3s var(--ease)}
.nav-links a:hover{opacity:1}.nav-links a:hover::after{width:100%}
.nav-res{font-size:11px;font-weight:800;letter-spacing:.1em;text-transform:uppercase;background:var(--txt);color:var(--bg);border-radius:100px;padding:11px 24px;transition:transform .3s var(--easeSnap),box-shadow .3s;white-space:nowrap}
.nav-res:hover{transform:scale(1.06);box-shadow:0 6px 24px rgba(var(--lcr),.4)}
#burger{display:none;flex-direction:column;justify-content:center;gap:5px;width:44px;height:44px;background:none;border:none;cursor:pointer;z-index:521}
#burger span{display:block;width:24px;height:2px;border-radius:2px;background:var(--txt);margin:0 auto;transition:transform .35s var(--ease),opacity .25s}
#burger.on span:nth-child(1){transform:translateY(7px) rotate(45deg)}
#burger.on span:nth-child(2){opacity:0}
#burger.on span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
#mobnav{position:fixed;inset:0;z-index:510;background:var(--bg);opacity:0;pointer-events:none;transform:translateY(-12px);transition:opacity .35s var(--ease),transform .35s var(--ease);display:flex;align-items:center;padding:90px clamp(28px,8vw,56px) 40px;overflow-y:auto}
#mobnav.on{opacity:1;pointer-events:all;transform:none}
body.mn-open #nav{z-index:530;background:transparent;border-bottom-color:transparent;backdrop-filter:none;-webkit-backdrop-filter:none}
.mn-inner{display:flex;flex-direction:column;gap:2px;width:100%}
.mn-t{font-size:11px;font-weight:700;letter-spacing:.28em;text-transform:uppercase;color:var(--txt3);margin-bottom:10px}
.mn-link{display:flex;align-items:baseline;gap:14px;font-family:'Archivo Black',sans-serif;font-size:clamp(24px,7.4vw,38px);text-transform:uppercase;padding:6px 0;line-height:1.15}
.mn-link .mn-i{font-family:'Anton',sans-serif;font-size:13px;letter-spacing:.2em;color:var(--oc);opacity:.9}
.mn-link.on{color:var(--lct)}
.mn-res{margin-top:24px;background:#25D366;color:#fff;text-align:center;font-weight:800;font-size:14px;letter-spacing:.05em;text-transform:uppercase;padding:18px;border-radius:100px;display:flex;align-items:center;justify-content:center;gap:9px}
@media(max-width:900px){.nav-links{display:none}}
@media(max-width:760px){#burger{display:flex}.nav-res{display:none}#nav,#nav.scrolled{padding:12px 18px}}

/* botón tema (igual que la portada) */
#theme-btn{position:fixed;bottom:96px;right:24px;z-index:700;width:46px;height:46px;border-radius:50%;border:1px solid var(--bdr2);background:var(--surface);cursor:pointer;display:flex;align-items:center;justify-content:center;transition:transform .3s var(--easeSnap),background .5s,border-color .5s;box-shadow:0 4px 18px rgba(0,0,0,.25)}
#theme-btn:hover{transform:scale(1.12) rotate(15deg)}
#theme-btn::before{content:'☾';font-size:19px;color:var(--txt)}
[data-theme="day"] #theme-btn::before{content:'☀'}
#waf{position:fixed;bottom:24px;right:24px;z-index:700;width:56px;height:56px;border-radius:50%;background:#25D366;color:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 24px rgba(37,211,102,.45);transition:transform .3s var(--easeSnap)}
#waf:hover{transform:scale(1.12)}
@media(max-width:760px){
  #theme-btn{top:12px;bottom:auto;right:66px;width:44px;height:44px;background:transparent;border-color:transparent;box-shadow:none;z-index:520}
  #waf{width:52px;height:52px;right:16px;bottom:calc(16px + env(safe-area-inset-bottom))}
}

/* hero = capítulo del local a pantalla completa */
.hero{position:relative;min-height:100svh;display:flex;flex-direction:column;justify-content:center;overflow:hidden;padding:110px 0 56px}
.hero::before{content:'';position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 18% 45%,rgba(var(--lcr),var(--glow)),transparent 62%),radial-gradient(ellipse 60% 60% at 90% 80%,rgba(var(--lcr),calc(var(--glow)*.6)),transparent 60%);pointer-events:none}
.marq{position:absolute;top:50%;left:0;width:100%;transform:translateY(-50%);overflow:hidden;pointer-events:none;opacity:.55}
.marq-in{display:flex;width:max-content;animation:tickMove 40s linear infinite;font-family:'Anton',sans-serif;font-size:clamp(110px,22vw,300px);line-height:1;text-transform:uppercase;color:transparent;-webkit-text-stroke:1px var(--outline);white-space:nowrap}
.marq-in span{padding-right:6vw}
@keyframes tickMove{to{transform:translateX(-50%)}}
.hero-in{position:relative;z-index:2;display:grid;grid-template-columns:1.05fr .95fr;align-items:center;gap:48px;padding:0 clamp(20px,5vw,72px);max-width:1440px;margin:0 auto;width:100%}
.crumbs{font-size:12px;color:var(--txt3);margin-bottom:22px;letter-spacing:.04em}
.crumbs a{border-bottom:1px solid var(--bdr2);transition:color .2s}
.crumbs a:hover{color:var(--txt)}
.lc-num{font-family:'Anton',sans-serif;font-size:13px;letter-spacing:.3em;color:var(--lct);display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:14px}
.lc-open{display:inline-flex;align-items:center;gap:7px;font-family:'Montserrat',sans-serif;font-size:11px;font-weight:800;letter-spacing:.14em;padding:5px 11px;border-radius:100px;text-transform:uppercase;background:var(--tag-bg);color:var(--txt3);border:1px solid var(--bdr2)}
.lc-open .od{width:6px;height:6px;border-radius:50%;background:currentColor}
.lc-open.si{background:rgba(74,222,128,.12);color:#16a34a;border-color:rgba(74,222,128,.35)}
[data-theme="night"] .lc-open.si,:root:not([data-theme="day"]) .lc-open.si{color:#4ade80}
.lc-open.si .od{animation:odPulse 1.6s ease-in-out infinite}
@keyframes odPulse{0%,100%{box-shadow:0 0 0 0 rgba(74,222,128,.5)}50%{box-shadow:0 0 0 5px rgba(74,222,128,0)}}
/* logos oscuros (La Traviesa, La Pequeña, Green): contorno de luz en modo noche para que se lean */
:root:not([data-theme="day"]) .lc-logo.oscuro img{filter:drop-shadow(0 0 1px rgba(255,255,255,.55)) drop-shadow(0 0 16px rgba(var(--lcr),.55))}
.lc-logo img{display:block;height:clamp(120px,19vw,260px);width:auto;max-width:100%;object-fit:contain;object-position:left center;transform-origin:center}
h1{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:clamp(26px,3.6vw,46px);line-height:1;text-transform:uppercase;margin-top:22px;max-width:16ch}
h1 em{font-style:normal;color:var(--lct)}
.tagline{font-size:clamp(15px,1.5vw,17px);font-style:italic;color:var(--txt2);line-height:1.6;margin-top:16px;max-width:460px}
.tags{display:flex;gap:8px;margin-top:18px;flex-wrap:wrap}
.tag{font-size:11px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:7px 12px;border-radius:5px;background:var(--tag-bg);color:var(--tag-txt);border:1px solid rgba(var(--lcr),.3)}
.ctas{display:flex;gap:12px;flex-wrap:wrap;margin-top:28px}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:48px;font-weight:800;font-size:12px;letter-spacing:.06em;text-transform:uppercase;padding:14px 26px;border-radius:100px;border:1.5px solid transparent;transition:transform .3s var(--easeSnap),box-shadow .3s,border-color .3s,background .3s;cursor:pointer}
.btn:hover{transform:translateY(-2px)}
.btn-pri{background:rgb(var(--lcr));color:var(--on-lc)}
.btn-pri:hover{box-shadow:0 8px 30px rgba(var(--lcr),.45)}
.btn-wa{background:#25D366;color:#fff}
.btn-wa:hover{box-shadow:0 8px 30px rgba(37,211,102,.45)}
.btn-wa.ghost{background:transparent;border-color:#25D366;color:#1fa855}
:root:not([data-theme="day"]) .btn-wa.ghost{color:#25D366}
.btn-ghost{background:transparent;color:var(--txt);border-color:var(--bdr2);font-weight:700}
.btn-ghost:hover{border-color:var(--txt)}
.hero-photos{display:grid;grid-template-columns:1fr 1fr;gap:14px;perspective:900px}
.lph{position:relative;border-radius:16px;overflow:hidden;box-shadow:0 18px 44px var(--photo-shadow);aspect-ratio:4/3;transform:rotate(var(--tilt,0deg));transition:transform .5s var(--ease)}
.lph:nth-child(1){--tilt:-1.4deg}
.lph:nth-child(2){--tilt:1.2deg;margin-top:26px}
.lph:nth-child(3){--tilt:.8deg;grid-column:1/3;aspect-ratio:21/9;margin-top:-8px}
.lph img{width:100%;height:100%;object-fit:cover;display:block;transform:scale(1.12);animation:kenburns 14s ease-in-out infinite alternate}
.lph:nth-child(2) img{animation-delay:-5s}.lph:nth-child(3) img{animation-delay:-9s}
@keyframes kenburns{0%{transform:scale(1.12) translate(0,0)}100%{transform:scale(1.22) translate(-2.5%,2%)}}
.lph::after{content:'';position:absolute;inset:0;background:linear-gradient(160deg,rgba(var(--lcr),.13),transparent 45%,rgba(0,0,0,.12));pointer-events:none}
.hero.off .marq-in,.hero.off .lph img,.hero.off .lc-logo img{animation-play-state:paused}

/* ticker en el color del local */
.ticker{overflow:hidden;padding:15px 0;background:rgb(var(--lcr))}
.ticker-track{display:flex;width:max-content;animation:tickMove 30s linear infinite}
.ticker:hover .ticker-track{animation-play-state:paused}
.tick{font-family:'Archivo Black',sans-serif;font-size:15px;letter-spacing:.1em;text-transform:uppercase;white-space:nowrap;display:flex;align-items:center;color:var(--on-lc)}
.tick-dot{width:6px;height:6px;border-radius:50%;background:currentColor;opacity:.5;margin:0 26px;flex-shrink:0}

/* capítulos */
.sec{max-width:1440px;margin:0 auto;padding:clamp(64px,9vw,110px) clamp(20px,5vw,72px)}
.sec+.sec{padding-top:0}
.ci{display:flex;align-items:flex-end;justify-content:space-between;gap:30px;margin-bottom:clamp(30px,5vw,50px)}
.ci-eyebrow{font-size:11px;font-weight:700;letter-spacing:.28em;text-transform:uppercase;color:var(--lct);margin-bottom:16px;display:flex;align-items:center;gap:12px}
.ci-eyebrow::before{content:'';width:30px;height:1px;background:currentColor}
h2{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:clamp(30px,5.4vw,68px);line-height:.96;text-transform:uppercase}
.ci-count{font-family:'Anton',sans-serif;font-size:clamp(70px,12vw,170px);line-height:.8;color:transparent;-webkit-text-stroke:1.5px var(--outline);user-select:none}
.grid2{display:grid;grid-template-columns:1.25fr .75fr;gap:clamp(28px,5vw,64px);align-items:start}
.txt p{color:var(--txt2);margin-bottom:16px;max-width:62ch;font-size:clamp(15px,1.3vw,17px)}
.txt p a,.fq p a{color:var(--lct);border-bottom:1px solid currentColor}
.planes{list-style:none;margin-top:14px;border-top:1px solid var(--bdr)}
.planes li{display:flex;gap:16px;align-items:baseline;padding:15px 0;border-bottom:1px solid var(--bdr);font-weight:600}
.planes li::before{content:counter(p,decimal-leading-zero);counter-increment:p;font-family:'Anton',sans-serif;font-size:13px;letter-spacing:.2em;color:var(--lct);flex-shrink:0}
.planes{counter-reset:p}
.planes a{color:var(--lct);border-bottom:1px solid currentColor}
.card{background:var(--card);border:1px solid var(--bdr2);border-radius:22px;padding:26px;position:relative;overflow:hidden;box-shadow:0 18px 44px rgba(0,0,0,.12)}
.card::before{content:'';position:absolute;left:0;top:0;right:0;height:3px;background:rgb(var(--lcr));box-shadow:0 0 18px rgb(var(--lcr))}
.card-l{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--txt3);margin-bottom:12px}
table{width:100%;border-collapse:collapse;font-size:15px;font-variant-numeric:tabular-nums}
td{padding:9px 0;border-bottom:1px solid var(--bdr)}td:last-child{text-align:right;font-weight:700}
tr.hoy td{color:var(--lct)}
tr.hoy td:first-child::after{content:' · hoy';font-weight:600;font-size:12px}
.mic{margin-top:18px;padding-top:16px;border-top:1px solid var(--bdr)}
.mic b{display:block;font-size:15px}.mic span{font-size:13px;color:var(--txt2)}
.card .btn{width:100%;margin-top:18px}
.gal{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.gal figure{border-radius:16px;overflow:hidden;box-shadow:0 14px 34px var(--photo-shadow);transform:rotate(var(--t,0deg));transition:transform .5s var(--ease)}
.gal figure:nth-child(odd){--t:-.8deg}.gal figure:nth-child(even){--t:.8deg;margin-top:22px}
.gal figure:hover{transform:rotate(0) scale(1.03)}
.gal img{width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;display:block}
.fq{border-bottom:1px solid var(--bdr)}
.fq:first-of-type{border-top:1px solid var(--bdr)}
.fq summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;gap:20px;padding:22px 0;font-family:'Archivo Black',sans-serif;font-size:clamp(16px,1.8vw,21px);line-height:1.2;text-transform:uppercase;min-height:44px}
.fq summary::-webkit-details-marker{display:none}
.fq-i{width:44px;height:44px;border-radius:50%;border:1.5px solid var(--arrow-bdr);flex-shrink:0;position:relative;transition:transform .4s var(--ease),background .3s,border-color .3s}
.fq-i::before,.fq-i::after{content:'';position:absolute;left:50%;top:50%;width:14px;height:2px;background:currentColor;transform:translate(-50%,-50%)}
.fq-i::after{transform:translate(-50%,-50%) rotate(90deg);transition:transform .3s var(--ease)}
.fq[open] .fq-i{transform:rotate(45deg);background:rgb(var(--lcr));border-color:rgb(var(--lcr));color:var(--on-lc)}
.fq p{color:var(--txt2);padding:0 64px 24px 0;max-width:75ch}
.otros{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.oc{position:relative;display:flex;flex-direction:column;gap:6px;padding:24px 22px 22px;border:1px solid var(--bdr2);border-radius:18px;background:var(--card);overflow:hidden;transition:transform .35s var(--ease),border-color .3s,box-shadow .3s}
.oc::before{content:'';position:absolute;left:0;top:0;right:0;height:3px;background:var(--oc)}
.oc:hover{transform:translateY(-4px);border-color:var(--oc);box-shadow:0 14px 34px rgba(0,0,0,.15)}
.oc-n{font-family:'Anton',sans-serif;font-size:12px;letter-spacing:.24em;color:var(--txt3)}
.oc b{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:20px;text-transform:uppercase;line-height:1.1}
.oc span{font-size:13px;color:var(--txt2)}
.oc i{position:absolute;right:18px;bottom:18px;width:38px;height:38px;border-radius:50%;border:1.5px solid var(--arrow-bdr);display:flex;align-items:center;justify-content:center;font-style:normal;transition:all .35s var(--ease)}
.oc:hover i{background:var(--oc);border-color:var(--oc);color:#fff;transform:rotate(-45deg)}

/* carta en texto */
.mn-intro{color:var(--txt2);max-width:70ch;margin:-12px 0 34px;font-size:clamp(15px,1.3vw,17px)}
.mn-grid{columns:2 420px;column-gap:clamp(28px,5vw,72px)}
.mn-sec{break-inside:avoid;margin-bottom:38px}
.mn-sec h3{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:clamp(18px,2vw,22px);text-transform:uppercase;letter-spacing:.02em;color:var(--lct);padding-bottom:10px;margin-bottom:6px;border-bottom:1.5px solid rgba(var(--lcr),.45)}
.mn-sec ul{list-style:none}
.mn-sec li{padding:11px 0;border-bottom:1px solid var(--bdr)}
.mn-row{display:flex;align-items:baseline;gap:10px}
.mn-n{font-weight:700;font-size:15px}
.mn-dots{flex:1;border-bottom:1.5px dotted var(--bdr2);transform:translateY(-4px);min-width:16px}
.mn-p{font-weight:800;font-size:15px;font-variant-numeric:tabular-nums;white-space:nowrap}
.mn-d{display:block;font-size:13.5px;color:var(--txt2);margin-top:2px;max-width:52ch}
.mn-al{display:block;font-size:12px;color:var(--txt3);margin-top:3px}
.mn-al::before{content:'Alérgenos: '}
.mn-foot{display:flex;align-items:center;justify-content:space-between;gap:18px;flex-wrap:wrap;border-top:1px solid var(--bdr);padding-top:22px;margin-top:6px}
.mn-foot p{font-size:13px;color:var(--txt3);max-width:70ch}
/* pie (igual que la portada) */
footer{background:var(--ft-bg);border-top:1px solid var(--bdr);padding:44px clamp(20px,5vw,72px) 28px}
.ft-top{display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;padding-bottom:28px;border-bottom:1px solid var(--bdr);margin-bottom:20px}
.ft-logo{font-family:'Archivo Black',sans-serif;font-size:14px;letter-spacing:.14em;text-transform:uppercase;opacity:.5}
.ft-locs{display:flex;gap:6px 18px;flex-wrap:wrap}
.ft-locs a{font-size:12px;letter-spacing:.1em;text-transform:uppercase;opacity:.6;padding:10px 0;transition:opacity .2s}
.ft-locs a:hover,.ft-locs a[aria-current]{opacity:1}
.ft-bot{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.ft-copy{font-size:12px;opacity:.6}
.lg-links{display:flex;gap:16px;margin-top:6px}
.lg-links a{font-size:12px;opacity:.6;padding:10px 0}
.lg-links a:hover{opacity:1}
.ft-soc{display:flex;gap:10px}
.ft-soc a{width:44px;height:44px;border-radius:8px;background:var(--soc-bg);display:flex;align-items:center;justify-content:center;opacity:.65;transition:opacity .2s,transform .2s}
.ft-soc a:hover{opacity:1;transform:translateY(-3px)}

/* aparición */
.rev{opacity:0;transform:translateY(28px);transition:opacity .8s var(--ease),transform .8s var(--ease)}
.rev.vis{opacity:1;transform:none}
.hero .rev{transition-duration:.6s}
.hero .rev:nth-child(2){transition-delay:.08s}.hero .rev:nth-child(3){transition-delay:.16s}

@media(max-width:1000px){.hero-in,.grid2{grid-template-columns:1fr}.hero-photos{max-width:620px}.gal{grid-template-columns:1fr 1fr}.ci-count{display:none}}
@media(max-width:760px){
  .hero{padding:92px 0 44px;min-height:auto}
  .lc-logo img{height:auto;max-height:110px}
  .ctas .btn{flex:1 1 auto}
  .fq p{padding-right:0}
  footer{padding-bottom:96px}
}
@media(prefers-reduced-motion:reduce){
  html{scroll-behavior:auto}
  *,*::before,*::after{animation:none!important;transition:none!important}
  .rev{opacity:1;transform:none}
}
"""


def pagina(l):
    s = l['slug']
    e = ESTILO[l['key']]
    url = f'{BASE}/locales/{s}/'
    foto1 = quote(f'/fotos/{l["fotos"]}/1.webp')
    wa_txt = quote(f'Hola! Quiero reservar en {l["nombre"]}')
    wa = f'https://wa.me/{WA}?text={wa_txt}'
    # texto sobre el color del local: negro en los colores claros (Green, Peluquería), blanco en el resto
    on_lc = '#0a0908' if l['key'] in ('green', 'peluca') else '#fff'
    ctas = []
    if l.get('reservar'):
        ctas.append(f'<a class="btn btn-pri" href="{esc(l["reservar"])}" target="_blank" rel="noopener">{ICO["cal"]} Reservar mesa</a>')
        ctas.append(f'<a class="btn btn-wa ghost" href="{wa}" target="_blank" rel="noopener">{ICO["wa"]} WhatsApp</a>')
    elif l.get('entradas'):
        ctas.append(f'<a class="btn btn-pri" href="{esc(l["entradas"])}" target="_blank" rel="noopener">{ICO["cal"]} Entradas y eventos</a>')
        ctas.append(f'<a class="btn btn-wa ghost" href="{wa}" target="_blank" rel="noopener">{ICO["wa"]} Reservar mesa</a>')
    else:
        ctas.append(f'<a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ICO["wa"]} Reservar por WhatsApp</a>')
    if l.get('carta'):
        if l['key'] in CARTAS:
            ctas.append(f'<a class="btn btn-ghost" href="#carta">{ICO["carta"]} Ver carta</a>')
        else:
            ctas.append(f'<a class="btn btn-ghost" href="{quote(l["carta"])}" target="_blank" rel="noopener">{ICO["carta"]} Ver carta</a>')
    ctas.append(f'<a class="btn btn-ghost" href="https://maps.google.com/?q={l["maps"]}" target="_blank" rel="noopener">{ICO["pin"]} Cómo llegar</a>')
    filas = '\n'.join(f'<tr data-d="{i}"><td>{d}</td><td>{h}</td></tr>' for i, (d, h) in enumerate(horario_filas(l)))
    fotos_hero = '\n'.join(
        f'<div class="lph"><img src="{quote("/fotos/" + l["fotos"] + f"/{i}.webp")}" alt="Ambiente de {esc(l["nombre"])}" width="1600" height="1066"{" fetchpriority=" + chr(34) + "high" + chr(34) if i == 1 else ""} decoding="async"></div>'
        for i in (1, 2, 3))
    gal = '\n'.join(
        f'<figure class="rev"><img src="{quote("/fotos/" + l["fotos"] + f"/{i}.webp")}" alt="Ambiente de {esc(l["nombre"])} ({i} de 4)" width="1600" height="1066" loading="lazy" decoding="async"></figure>'
        for i in (4, 1, 2, 3))
    cerca = [POR_SLUG[x] for x in l['otros_cerca']]
    resto = cerca + [o for o in LOCALES if o['slug'] != s and o not in cerca]
    otros = '\n'.join(
        f'<a class="oc rev" href="/locales/{o["slug"]}/" style="--oc:rgb({ESTILO[o["key"]]["rgb"]})"><span class="oc-n">{ESTILO[o["key"]]["num"]} / 07</span><b>{esc(o["nombre"])}</b><span>{esc(o["tipo_txt"])} · {esc(ESTILO[o["key"]]["tag_dir"])}</span><i>{ICO["arrow"]}</i></a>'
        for o in resto)
    mob = '\n'.join(
        f'<a class="mn-link{" on" if o["slug"] == s else ""}" href="/locales/{o["slug"]}/" style="--oc:rgb({ESTILO[o["key"]]["rgb"]})"{" aria-current=" + chr(34) + "page" + chr(34) if o["slug"] == s else ""}><span class="mn-i">{ESTILO[o["key"]]["num"]}</span>{esc(o["nombre"])}</a>'
        for o in LOCALES)
    pie = ''.join(f'<a href="/locales/{o["slug"]}/"{" aria-current=" + chr(34) + "page" + chr(34) if o["slug"] == s else ""}>{esc(o["nombre"])}</a>' for o in LOCALES)
    calle_corta = l['calle'].replace('Calle de ', '').replace('Calle del ', '')
    ticks = [l['nombre'], e['tag_dir'], e['tag_hor'], l['tipo_txt'], l['zona'], '@' + l['ig']]
    tick_html = ''.join(f'<span class="tick">{esc(t)}<span class="tick-dot"></span></span>' for t in ticks * 2)
    marq = ''.join(f'<span>{esc(l["nombre"])}</span>' for _ in range(3))
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
<meta name="theme-color" content="#0a0908" id="theme-color-meta">
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
<script>
/* tema antes de pintar (sin parpadeo): el mismo que la portada (localStorage g20theme o día/noche por hora) */
(function(){{var t;try{{t=localStorage.getItem('g20theme')}}catch(e){{}}if(!t){{var h=new Date().getHours();t=(h>=7&&h<20)?'day':'night'}}document.documentElement.setAttribute('data-theme',t)}})();
</script>
<link rel="preload" as="image" href="{foto1}" fetchpriority="high">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo+Black&family=Montserrat:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema(l)}
</script>
<style>{CSS}.lc-logo img{{{ANIM_LOGO[l['key']]}}}</style>
</head>
<body style="--lc:rgb({e['rgb']});--lcr:{e['rgb']};--lct-n:{e['txt_n']};--lct-d:{e['txt_d']};--on-lc:{on_lc}">
<a class="skip-link" href="#main">Saltar al contenido</a>
<div id="cur" aria-hidden="true"></div>
<button id="theme-btn" aria-label="Cambiar tema día/noche" title="Cambiar tema"></button>

<nav id="nav" aria-label="Principal">
  <a class="nav-pill" href="/">GRUPO_2.0</a>
  <ul class="nav-links">
    <li><a href="/#locales">Locales</a></li>
    <li><a href="/eventos/">Eventos</a></li>
    <li><a href="/#socios">Socios</a></li>
    <li><a href="/#contacto">Contacto</a></li>
  </ul>
  <a class="nav-res" href="{esc(l.get('reservar') or wa)}" target="_blank" rel="noopener">Reservar ↗</a>
  <button id="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobnav"><span></span><span></span><span></span></button>
</nav>
<div id="mobnav" aria-hidden="true">
  <div class="mn-inner">
    <p class="mn-t">Los locales de la familia</p>
{mob}
    <a class="mn-res" href="{wa}" target="_blank" rel="noopener">{ICO['wa']} Reservar en {esc(l['nombre'])}</a>
  </div>
</div>

<main id="main">
<header class="hero" id="hero">
  <div class="marq" aria-hidden="true"><div class="marq-in">{marq}</div></div>
  <div class="hero-in">
    <div>
      <nav class="crumbs rev" aria-label="Ruta"><a href="/">Grupo 2.0</a> / <a href="/#locales">Locales</a> / {esc(l['nombre'])}</nav>
      <div class="rev">
        <span class="lc-num">{e['num']} / 07 — {esc(e['label'])}<span class="lc-open" id="estado" hidden><span class="od"></span><span class="ot"></span></span></span>
        <div class="lc-logo{" oscuro" if l["key"] in ("traviesa", "pequeña", "green") else ""}"><img src="{quote('/logos/' + l['logo'])}" alt="Logo de {esc(l['nombre'])}" width="1400" height="400"></div>
        <h1><span class="sr-only">{esc(l['nombre'])}: </span>{esc(l['tipo_txt'])} en <em>{esc(calle_corta.split(',')[0])}</em></h1>
        <p class="tagline">“{esc(l['tagline'])}”</p>
        <div class="tags"><span class="tag">{esc(e['tag_hor'])}</span><span class="tag">{esc(e['tag_dir'])}</span><span class="tag">{esc(l['zona'])}</span></div>
        <div class="ctas">
          {chr(10).join('          ' + c for c in ctas).strip()}
        </div>
      </div>
    </div>
    <div class="hero-photos rev" aria-hidden="true">
{fotos_hero}
    </div>
  </div>
</header>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{tick_html}</div></div>

<section class="sec" aria-labelledby="h-asi">
  <div class="ci rev"><div><div class="ci-eyebrow">El local</div><h2 id="h-asi">Así es {esc(l['nombre'])}</h2></div><div class="ci-count" aria-hidden="true">{e['num']}</div></div>
  <div class="grid2">
    <div class="txt rev">
      {''.join(f'<p>{p}</p>' for p in l['intro'])}
      <ul class="planes">{''.join(f'<li>{p}</li>' for p in l['planes'])}</ul>
    </div>
    <aside class="card rev" aria-labelledby="h-hor">
      <p class="card-l" id="h-hor">Horario</p>
      <table><tbody>
{filas}
      </tbody></table>
      <div class="mic"><b>{esc(l['calle'])}</b><span>Madrid · {esc(l['zona'])}</span></div>
      <div class="mic"><b>656 48 50 99</b><span>WhatsApp y reservas</span></div>
      <a class="btn btn-wa" href="{wa}" target="_blank" rel="noopener">{ICO['wa']} Escríbenos</a>
    </aside>
  </div>
</section>

{carta_html(l)}
<section class="sec" aria-labelledby="h-fotos">
  <div class="ci rev"><div><div class="ci-eyebrow">Fotos</div><h2 id="h-fotos">Para que vayas abriendo boca</h2></div></div>
  <div class="gal">
{gal}
  </div>
</section>

<section class="sec" aria-labelledby="h-faq">
  <div class="ci rev"><div><div class="ci-eyebrow">Dudas</div><h2 id="h-faq">Preguntas rápidas</h2></div></div>
  {faq(l)}
</section>

<section class="sec" aria-labelledby="h-otros">
  <div class="ci rev"><div><div class="ci-eyebrow">La familia 2.0</div><h2 id="h-otros">Más planes</h2></div></div>
  <div class="otros">
{otros}
  </div>
</section>
</main>

<footer>
  <div class="ft-top">
    <div class="ft-logo">GRUPO_2.0</div>
    <nav class="ft-locs" aria-label="Locales">{pie}<a href="/eventos/">Eventos</a></nav>
  </div>
  <div class="ft-bot">
    <div><p class="ft-copy">© 2026 Grupo 2.0 · Madrid · 656 485 099 · <a href="mailto:hola@grupodospuntocero.com">hola@grupodospuntocero.com</a></p>
    <div class="lg-links"><a href="/#aviso">Aviso legal</a><a href="/#privacidad">Privacidad</a><a href="/#cookies">Cookies</a></div></div>
    <div class="ft-soc">
      <a href="https://www.instagram.com/{l['ig']}" target="_blank" rel="noopener" aria-label="Instagram de {esc(l['nombre'])}">{ICO['ig']}</a>
      <a href="https://www.tiktok.com/@grupo2.0_" target="_blank" rel="noopener" aria-label="TikTok Grupo 2.0">{ICO['tt']}</a>
      <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp Grupo 2.0">{ICO['wa']}</a>
    </div>
  </div>
</footer>

<a href="{wa}" id="waf" target="_blank" rel="noopener" aria-label="Reservar por WhatsApp"><svg width="25" height="25" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg></a>

<script>
(function(){{
  var root=document.documentElement,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,hover=matchMedia('(hover: hover)').matches;
  /* tema día/noche (misma clave que la portada) */
  var btn=document.getElementById('theme-btn'),meta=document.getElementById('theme-color-meta');
  function setT(t){{root.setAttribute('data-theme',t);btn.setAttribute('aria-label',t==='day'?'Cambiar a modo noche':'Cambiar a modo día');if(meta)meta.content=t==='day'?'#f5f0e8':'#0a0908'}}
  setT(root.getAttribute('data-theme'));
  btn.addEventListener('click',function(){{var n=root.getAttribute('data-theme')==='day'?'night':'day';setT(n);try{{localStorage.setItem('g20theme',n)}}catch(e){{}}}});
  /* nav al hacer scroll */
  var nav=document.getElementById('nav'),tk=false;
  function onS(){{nav.classList.toggle('scrolled',scrollY>40);tk=false}}
  addEventListener('scroll',function(){{if(!tk){{tk=true;requestAnimationFrame(onS)}}}},{{passive:true}});onS();
  /* menú móvil */
  var b=document.getElementById('burger'),mn=document.getElementById('mobnav');
  function tog(o){{b.classList.toggle('on',o);mn.classList.toggle('on',o);b.setAttribute('aria-expanded',o);mn.setAttribute('aria-hidden',!o);b.setAttribute('aria-label',o?'Cerrar menú':'Abrir menú');document.body.style.overflow=o?'hidden':'';document.body.classList.toggle('mn-open',o)}}
  b.addEventListener('click',function(){{tog(!mn.classList.contains('on'))}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape'&&mn.classList.contains('on'))tog(false)}});
  /* abierto ahora + día de hoy */
  var H={js_h};
  function t(s){{var p=s.split(':');return +p[0]+p[1]/60}}
  var n=new Date(),d=n.getDay(),h=n.getHours()+n.getMinutes()/60,prev=(d+6)%7,on=false;
  H.forEach(function(r){{var a=t(r[1]),c=t(r[2]);if(c<=a)c+=24;
    if(r[0].indexOf(d)>-1&&h>=a&&h<Math.min(c,24))on=true;
    if(r[0].indexOf(prev)>-1&&c>24&&h<c-24)on=true;}});
  var es=document.getElementById('estado');es.hidden=false;es.classList.add(on?'si':'no');es.querySelector('.ot').textContent=on?'Abierto ahora':'Cerrado ahora';
  var fila=document.querySelector('tr[data-d="'+((d+6)%7)+'"]');if(fila)fila.className='hoy';
  /* apariciones */
  var io=new IntersectionObserver(function(en){{en.forEach(function(x){{if(x.isIntersecting){{x.target.classList.add('vis');io.unobserve(x.target)}}}})}},{{threshold:.12,rootMargin:'0px 0px -40px 0px'}});
  document.querySelectorAll('.rev').forEach(function(el){{io.observe(el)}});
  /* el hero aparece nada más cargar, sin esperar al observer */
  setTimeout(function(){{document.querySelectorAll('.hero .rev').forEach(function(el){{el.classList.add('vis');io.unobserve(el)}})}},30);
  /* animaciones del hero solo mientras se ve */
  var hero=document.getElementById('hero');
  new IntersectionObserver(function(en){{hero.classList.toggle('off',!en[0].isIntersecting)}}).observe(hero);
  if(reduce||!hover)return;
  /* cursor copa (como en la portada): transform y en reposo cuando no se mueve */
  var c=document.getElementById('cur'),mx=-99,my=-99,lx=0,tilt=0,run=false;
  var img=new Image();img.onload=function(){{root.classList.add('copa-cursor');img.alt='';c.appendChild(img)}};img.src='/logos/copa.webp';
  function loop(){{tilt+=((mx-lx)*.9-tilt)*.14;lx=mx;var r=Math.max(-22,Math.min(22,tilt));
    c.style.transform='translate3d('+mx+'px,'+my+'px,0) translate(-50%,-50%) rotate('+r+'deg)';
    if(Math.abs(tilt)>.05)requestAnimationFrame(loop);else run=false}}
  document.addEventListener('mousemove',function(e){{mx=e.clientX;my=e.clientY;c.classList.add('on');if(!run){{run=true;requestAnimationFrame(loop)}}}},{{passive:true}});
  /* inclinación 3D suave de las fotos del hero */
  document.querySelectorAll('.lph').forEach(function(el){{
    el.addEventListener('mousemove',function(e){{var r=el.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;
      el.style.transform='rotate(var(--tilt,0deg)) rotateY('+(x*9)+'deg) rotateX('+(-y*9)+'deg) scale(1.025)'}});
    el.addEventListener('mouseleave',function(){{el.style.transform=''}});
  }});
}})();
</script>
</body>
</html>
'''


# JS común de las páginas sin horario (tema, nav, menú móvil, apariciones, cursor copa)
JS_COMUN = """
(function(){
  var root=document.documentElement,reduce=matchMedia('(prefers-reduced-motion: reduce)').matches,hover=matchMedia('(hover: hover)').matches;
  var btn=document.getElementById('theme-btn'),meta=document.getElementById('theme-color-meta');
  function setT(t){root.setAttribute('data-theme',t);btn.setAttribute('aria-label',t==='day'?'Cambiar a modo noche':'Cambiar a modo día');if(meta)meta.content=t==='day'?'#f5f0e8':'#0a0908'}
  setT(root.getAttribute('data-theme'));
  btn.addEventListener('click',function(){var n=root.getAttribute('data-theme')==='day'?'night':'day';setT(n);try{localStorage.setItem('g20theme',n)}catch(e){}});
  var nav=document.getElementById('nav'),tk=false;
  function onS(){nav.classList.toggle('scrolled',scrollY>40);tk=false}
  addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(onS)}},{passive:true});onS();
  var b=document.getElementById('burger'),mn=document.getElementById('mobnav');
  function tog(o){b.classList.toggle('on',o);mn.classList.toggle('on',o);b.setAttribute('aria-expanded',o);mn.setAttribute('aria-hidden',!o);b.setAttribute('aria-label',o?'Cerrar menú':'Abrir menú');document.body.style.overflow=o?'hidden':'';document.body.classList.toggle('mn-open',o)}
  b.addEventListener('click',function(){tog(!mn.classList.contains('on'))});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&mn.classList.contains('on'))tog(false)});
  var io=new IntersectionObserver(function(en){en.forEach(function(x){if(x.isIntersecting){x.target.classList.add('vis');io.unobserve(x.target)}})},{threshold:.12,rootMargin:'0px 0px -40px 0px'});
  document.querySelectorAll('.rev').forEach(function(el){io.observe(el)});
  setTimeout(function(){document.querySelectorAll('.hero .rev').forEach(function(el){el.classList.add('vis');io.unobserve(el)})},30);
  var hero=document.getElementById('hero');
  new IntersectionObserver(function(en){hero.classList.toggle('off',!en[0].isIntersecting)}).observe(hero);
  if(reduce||!hover)return;
  var c=document.getElementById('cur'),mx=-99,my=-99,lx=0,tilt=0,run=false;
  var img=new Image();img.onload=function(){root.classList.add('copa-cursor');img.alt='';c.appendChild(img)};img.src='/logos/copa.webp';
  function loop(){tilt+=((mx-lx)*.9-tilt)*.14;lx=mx;var r=Math.max(-22,Math.min(22,tilt));
    c.style.transform='translate3d('+mx+'px,'+my+'px,0) translate(-50%,-50%) rotate('+r+'deg)';
    if(Math.abs(tilt)>.05)requestAnimationFrame(loop);else run=false}
  document.addEventListener('mousemove',function(e){mx=e.clientX;my=e.clientY;c.classList.add('on');if(!run){run=true;requestAnimationFrame(loop)}},{passive:true});
})();
"""

# ─────────────────────────── Página de eventos: /eventos/ ───────────────────────────
KOMVO = 'https://grupodospuntocero.komvoapp.com/restaurantes'

EVENTOS_TIPOS = [
    ('Cenas y comidas de empresa', 'La cena de Navidad que sí apetece, la comida del equipo o el brindis de fin de trimestre. Mesa, menú cerrado y sobremesa sin mirar el reloj.', '231,47,138'),
    ('Cumpleaños', 'Cumples años, no neuronas. Tú pones las velas y la lista de invitados; nosotros, el sitio, las copas y la música.', '229,29,30'),
    ('Despedidas', 'De soltera, de soltero o del compañero que se va. Cena, copas y baile en la misma noche, sin tener que cruzar Madrid.', '29,183,217'),
    ('Afterwork y fiestas de equipo', 'El afterwork que mañana será leyenda en el grupo del curro. Te traes al jefe y te lo devolvemos bailando.', '74,222,128'),
]
# qué plan encaja en cada local (enlaza a su página)
EVENTOS_LOCALES = [
    ('la-traviesa', 'Comidas y cenas sentados', 'Restaurante en López de Hoyos con menús de grupo y de Navidad con bebida incluida.'),
    ('green', 'Cena + fiesta hasta las 6:00', 'Restaurante, bar y discoteca en la Castellana: empezar cenando y acabar bailando.'),
    ('la-chula', 'Cumpleaños con neón', 'Bar de copas en Claudio Coello abierto hasta las 3:30 los viernes y sábados.'),
    ('las-tablas', 'Copas en grupo', 'Bar de copas en General Oraá, justo enfrente de La Pequeña 2.0.'),
    ('la-pequena', 'Celebraciones de barrio', 'Bar de copas en General Oraá con trato de casa.'),
    ('la-peluqueria', 'Afterwork en la zona norte', 'Bar de copas en Alberto Alcocer (Chamartín).'),
]
EVENTOS_FAQ = [
    ('¿Cómo reservo un evento en Grupo 2.0?', f'Puedes reservarlo online con el botón «Reservar evento online», escribirnos por WhatsApp al 656 48 50 99 o mandar un email a <a href="mailto:hola@grupodospuntocero.com">hola@grupodospuntocero.com</a> con la fecha, el número de personas y el tipo de plan.'),
    ('¿Tenéis menús cerrados para cenas de empresa?', 'Sí. En La Traviesa 2.0 hay menús de Navidad para grupos de 45 € a 65 € por persona con bebida incluida, y un formato cóctel para grupos grandes. Los tienes en <a href="/traviesa/">grupodospuntocero.com/traviesa</a>. Para otras fechas preparamos la propuesta a medida.'),
    ('¿Con cuánta antelación tengo que reservar?', 'Cuanto antes, mejor, sobre todo en diciembre y para viernes y sábados, que es cuando más se llenan los locales. Escríbenos aunque aún no tengas el número exacto de personas.'),
    ('¿Se puede cenar y seguir la fiesta en el mismo sitio?', 'Sí: en Green 2.0 (Paseo de la Castellana, 40 bis) puedes cenar y quedarte en la discoteca hasta las 6:00 de jueves a sábado.'),
    ('¿Se puede reservar un local entero?', 'Depende del local, la fecha y el tamaño del grupo. Cuéntanos tu plan y te decimos qué opciones hay.'),
]


def pagina_eventos():
    url = f'{BASE}/eventos/'
    title = 'Cenas de empresa y eventos privados en Madrid · Grupo 2.0'
    desc = 'Organiza tu cena de empresa, cumpleaños o despedida en Madrid en los locales de Grupo 2.0. Menús de Navidad desde 45 € con bebida. Reserva online o por WhatsApp.'
    wa = f'https://wa.me/{WA}?text=' + quote('Hola! Quiero organizar un evento con Grupo 2.0')
    wa_emp = f'https://wa.me/{WA}?text=' + quote('Hola! Quiero organizar una cena de empresa con Grupo 2.0')
    foto1 = quote('/fotos/la traviesa/1.webp')
    ld = json.dumps({'@context': 'https://schema.org', '@graph': [
        {'@type': 'Service', '@id': f'{url}#servicio', 'name': 'Cenas de empresa y eventos privados en Madrid',
         'serviceType': 'Organización de cenas de empresa, cumpleaños, despedidas y eventos privados',
         'description': desc, 'url': url, 'areaServed': {'@type': 'City', 'name': 'Madrid'},
         'provider': {'@id': f'{BASE}/#org'},
         'offers': {'@type': 'AggregateOffer', 'priceCurrency': 'EUR', 'lowPrice': '45', 'highPrice': '65',
                    'description': 'Menús de Navidad para grupos en La Traviesa 2.0, bebida incluida'},
         'potentialAction': {'@type': 'ReserveAction', 'target': KOMVO}},
        {'@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Grupo 2.0', 'item': BASE + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Eventos', 'item': url}]},
    ]}, ensure_ascii=False, indent=1)
    tipos = '\n'.join(
        f'<div class="oc ev rev" style="--oc:rgb({rgb})"><span class="oc-n">0{i + 1}</span><h3>{esc(t)}</h3><span>{esc(p)}</span></div>'
        for i, (t, p, rgb) in enumerate(EVENTOS_TIPOS))
    locs = '\n'.join(
        f'<a class="oc rev" href="/locales/{s}/" style="--oc:rgb({ESTILO[POR_SLUG[s]["key"]]["rgb"]})"><span class="oc-n">{esc(POR_SLUG[s]["nombre"])}</span><b>{esc(plan)}</b><span>{esc(txt)}</span><i>{ICO["arrow"]}</i></a>'
        for s, plan, txt in EVENTOS_LOCALES)
    faqs = '\n'.join(f'<details class="fq rev"><summary>{esc(q)}<span class="fq-i" aria-hidden="true"></span></summary><p>{a}</p></details>' for q, a in EVENTOS_FAQ)
    pie = ''.join(f'<a href="/locales/{o["slug"]}/">{esc(o["nombre"])}</a>' for o in LOCALES)
    mob = '\n'.join(
        f'<a class="mn-link" href="/locales/{o["slug"]}/" style="--oc:rgb({ESTILO[o["key"]]["rgb"]})"><span class="mn-i">{ESTILO[o["key"]]["num"]}</span>{esc(o["nombre"])}</a>'
        for o in LOCALES)
    ticks = ['Cenas de empresa', 'Cumpleaños', 'Despedidas', 'Afterwork', 'Navidad 2026', 'Menús desde 45 €']
    tick_html = ''.join(f'<span class="tick">{esc(t)}<span class="tick-dot"></span></span>' for t in ticks * 2)
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<!-- Página generada por locales/_generar.py — no editar a mano -->
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0a0908" id="theme-color-meta">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Grupo 2.0">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}{foto1}">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="1066">
<meta property="og:image:alt" content="Cena de grupo en La Traviesa 2.0">
<meta name="twitter:card" content="summary_large_image">
<script>
(function(){{var t;try{{t=localStorage.getItem('g20theme')}}catch(e){{}}if(!t){{var h=new Date().getHours();t=(h>=7&&h<20)?'day':'night'}}document.documentElement.setAttribute('data-theme',t)}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Archivo+Black&family=Montserrat:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
<script type="application/ld+json">
{ld}
</script>
<style>{CSS}
.ev-hero{{text-align:left}}
.ev-hero h1{{font-size:clamp(34px,6.4vw,92px);max-width:14ch;margin-top:10px;line-height:.92}}
.ev-hero .tagline{{max-width:560px}}
.ev h3{{font-family:'Archivo Black',sans-serif;font-weight:400;font-size:20px;text-transform:uppercase;line-height:1.1}}
.ev{{padding-bottom:26px}}
.nav-band{{display:grid;grid-template-columns:1.1fr .9fr;gap:clamp(24px,5vw,64px);align-items:center}}
.nav-band .lph{{aspect-ratio:4/3}}
.precios{{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:22px}}
.precio{{border:1px solid var(--bdr2);border-radius:16px;padding:16px 18px;background:var(--card)}}
.precio b{{display:block;font-family:'Archivo Black',sans-serif;font-weight:400;font-size:26px;color:var(--lct)}}
.precio span{{font-size:13px;color:var(--txt2)}}
.pasos{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;counter-reset:s}}
.paso{{border-top:2px solid rgb(var(--lcr));padding-top:18px}}
.paso::before{{counter-increment:s;content:'0' counter(s);font-family:'Anton',sans-serif;font-size:40px;line-height:1;color:transparent;-webkit-text-stroke:1.5px var(--lct);display:block;margin-bottom:10px}}
.paso b{{display:block;font-size:17px;margin-bottom:6px}}
.paso span{{color:var(--txt2);font-size:15px}}
.mail{{margin-top:18px;font-size:14px;color:var(--txt2)}}.mail a{{color:var(--lct);border-bottom:1px solid currentColor}}
@media(max-width:1000px){{.nav-band,.pasos{{grid-template-columns:1fr}}}}
</style>
</head>
<body style="--lc:rgb(231,47,138);--lcr:231,47,138;--lct-n:#ff6fb0;--lct-d:#c0186c;--on-lc:#fff">
<a class="skip-link" href="#main">Saltar al contenido</a>
<div id="cur" aria-hidden="true"></div>
<button id="theme-btn" aria-label="Cambiar tema día/noche" title="Cambiar tema"></button>

<nav id="nav" aria-label="Principal">
  <a class="nav-pill" href="/">GRUPO_2.0</a>
  <ul class="nav-links">
    <li><a href="/#locales">Locales</a></li>
    <li><a href="/eventos/" aria-current="page">Eventos</a></li>
    <li><a href="/#socios">Socios</a></li>
    <li><a href="/#contacto">Contacto</a></li>
  </ul>
  <a class="nav-res" href="{KOMVO}" target="_blank" rel="noopener">Reservar evento ↗</a>
  <button id="burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobnav"><span></span><span></span><span></span></button>
</nav>
<div id="mobnav" aria-hidden="true">
  <div class="mn-inner">
    <p class="mn-t">Los locales de la familia</p>
{mob}
    <a class="mn-res" href="{wa}" target="_blank" rel="noopener">{ICO['wa']} Cuéntanos tu evento</a>
  </div>
</div>

<main id="main">
<header class="hero" id="hero">
  <div class="marq" aria-hidden="true"><div class="marq-in"><span>Eventos 2.0</span><span>Eventos 2.0</span><span>Eventos 2.0</span></div></div>
  <div class="hero-in">
    <div class="ev-hero">
      <nav class="crumbs rev" aria-label="Ruta"><a href="/">Grupo 2.0</a> / Eventos</nav>
      <div class="rev">
        <span class="lc-num">EVENTOS PRIVADOS · MADRID</span>
        <h1>Cenas de empresa y eventos en <em>Madrid</em></h1>
        <p class="tagline">Cenas de empresa, cumpleaños, despedidas y afterworks en seis locales de Grupo 2.0 en Salamanca, Chamartín y la Castellana. Tú traes a la gente; nosotros, el sitio, la comida, las copas y la música.</p>
        <div class="tags"><span class="tag">Menús de Navidad desde 45 €</span><span class="tag">Bebida incluida</span><span class="tag">Reserva online</span></div>
        <div class="ctas">
          <a class="btn btn-pri" href="{KOMVO}" target="_blank" rel="noopener">{ICO['cal']} Reservar evento online</a>
          <a class="btn btn-wa ghost" href="{wa_emp}" target="_blank" rel="noopener">{ICO['wa']} Cuéntanos tu plan</a>
        </div>
        <p class="mail">¿Prefieres email? <a href="mailto:hola@grupodospuntocero.com?subject=Evento%20con%20Grupo%202.0">hola@grupodospuntocero.com</a></p>
      </div>
    </div>
    <div class="hero-photos rev" aria-hidden="true">
      <div class="lph"><img src="{foto1}" alt="" width="1600" height="1066" fetchpriority="high" decoding="async"></div>
      <div class="lph"><img src="{quote('/fotos/green/2.webp')}" alt="" width="1600" height="1066" decoding="async"></div>
      <div class="lph"><img src="{quote('/fotos/la chula/3.webp')}" alt="" width="1600" height="1066" decoding="async"></div>
    </div>
  </div>
</header>

<div class="ticker" aria-hidden="true"><div class="ticker-track">{tick_html}</div></div>

<section class="sec" aria-labelledby="h-tipos">
  <div class="ci rev"><div><div class="ci-eyebrow">Qué celebramos</div><h2 id="h-tipos">Cualquier excusa vale</h2></div><div class="ci-count" aria-hidden="true">2.0</div></div>
  <div class="otros">
{tipos}
  </div>
</section>

<section class="sec" aria-labelledby="h-navidad">
  <div class="nav-band">
    <div class="rev">
      <div class="ci-eyebrow">Navidad 2026</div>
      <h2 id="h-navidad">Cenas de Navidad de empresa en La Traviesa</h2>
      <p class="mn-intro" style="margin:18px 0 0">Comidas y cenas de Navidad para empresas, amigos y familia en La Traviesa 2.0 (López de Hoyos, 7): platos para compartir, principal a elegir, postres caseros y bebida incluida durante toda la comida.</p>
      <div class="precios">
        <div class="precio"><b>45 €</b><span>Menú Travieso</span></div>
        <div class="precio"><b>55 €</b><span>Menú Muy Travieso</span></div>
        <div class="precio"><b>65 €</b><span>Menú La Glotona</span></div>
        <div class="precio"><b>45 €</b><span>Menú Cóctel, para grupos grandes</span></div>
      </div>
      <div class="ctas"><a class="btn btn-pri" href="/traviesa/">{ICO['carta']} Ver los menús de Navidad</a></div>
    </div>
    <div class="lph rev"><img src="{quote('/fotos/la traviesa/2.webp')}" alt="Comedor de La Traviesa 2.0" width="1600" height="1066" loading="lazy" decoding="async"></div>
  </div>
</section>

<section class="sec" aria-labelledby="h-donde">
  <div class="ci rev"><div><div class="ci-eyebrow">Dónde</div><h2 id="h-donde">Elige el sitio según el plan</h2></div></div>
  <div class="otros">
{locs}
  </div>
</section>

<section class="sec" aria-labelledby="h-pasos">
  <div class="ci rev"><div><div class="ci-eyebrow">Cómo funciona</div><h2 id="h-pasos">Tres pasos y a celebrar</h2></div></div>
  <div class="pasos">
    <div class="paso rev"><b>Cuéntanos el plan</b><span>Fecha, cuántos sois y qué queréis celebrar. Online, por WhatsApp o por email.</span></div>
    <div class="paso rev"><b>Te proponemos sitio y menú</b><span>Te decimos qué local encaja mejor y cerramos menú, bebida y horario.</span></div>
    <div class="paso rev"><b>Tú solo vienes</b><span>Nosotros nos encargamos del resto. Lo de mañana en la oficina ya es cosa tuya.</span></div>
  </div>
  <div class="ctas rev" style="margin-top:34px">
    <a class="btn btn-pri" href="{KOMVO}" target="_blank" rel="noopener">{ICO['cal']} Reservar evento online</a>
    <a class="btn btn-wa ghost" href="{wa}" target="_blank" rel="noopener">{ICO['wa']} WhatsApp</a>
  </div>
</section>

<section class="sec" aria-labelledby="h-faq">
  <div class="ci rev"><div><div class="ci-eyebrow">Dudas</div><h2 id="h-faq">Preguntas rápidas</h2></div></div>
  {faqs}
</section>
</main>

<footer>
  <div class="ft-top">
    <div class="ft-logo">GRUPO_2.0</div>
    <nav class="ft-locs" aria-label="Locales">{pie}<a href="/eventos/" aria-current="page">Eventos</a></nav>
  </div>
  <div class="ft-bot">
    <div><p class="ft-copy">© 2026 Grupo 2.0 · Madrid · 656 485 099 · <a href="mailto:hola@grupodospuntocero.com">hola@grupodospuntocero.com</a></p>
    <div class="lg-links"><a href="/#aviso">Aviso legal</a><a href="/#privacidad">Privacidad</a><a href="/#cookies">Cookies</a></div></div>
    <div class="ft-soc">
      <a href="https://www.instagram.com/grupo_2.0" target="_blank" rel="noopener" aria-label="Instagram Grupo 2.0">{ICO['ig']}</a>
      <a href="https://www.tiktok.com/@grupo2.0_" target="_blank" rel="noopener" aria-label="TikTok Grupo 2.0">{ICO['tt']}</a>
      <a href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp Grupo 2.0">{ICO['wa']}</a>
    </div>
  </div>
</footer>

<a href="{wa}" id="waf" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp"><svg width="25" height="25" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="{WA_PATH}"/></svg></a>
<script>{JS_COMUN}</script>
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
    os.makedirs(os.path.join(raiz, '..', 'eventos'), exist_ok=True)
    with open(os.path.join(raiz, '..', 'eventos', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(pagina_eventos())
    print('ok eventos')
