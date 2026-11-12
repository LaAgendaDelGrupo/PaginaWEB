# WEB 2.0 · Contexto del proyecto

> Última actualización: **12/11/2026**
> Este archivo sirve para seguir el proyecto desde cualquier ordenador. Se actualiza al final de cada sesión de trabajo.
> No se publica en la web (empieza por «_»), pero **el repositorio de GitHub es público**: aquí nunca van contraseñas, tokens, PINs, claves de API ni datos privados.

---

## 1. Qué es esto

Web pública de **Grupo 2.0** (bares de copas, restaurante y discoteca en Madrid): **https://grupodospuntocero.com**

- Código: HTML + CSS + JS sin frameworks. Todo vive en esta carpeta.
- Repositorio: `github.com/LaAgendaDelGrupo/PaginaWEB` (rama `main`, **público**).
- Publicación: GitHub Pages. Cada `git push` a `main` publica en 1–2 minutos.
- Dominio en IONOS. Search Console dado de alta (propiedad de dominio).

## 2. Mapa de la carpeta

| Ruta | Qué es | ¿Se edita a mano? |
|---|---|---|
| `index.html` | Portada (español) | Sí |
| `locales/_generar.py` | **Generador** de casi todas las demás páginas | Sí: aquí se cambian textos, horarios, cartas |
| `locales/<local>/` | Página de cada local (español) | **No** (generada) |
| `locales/index.html` | Todos los locales por zona | **No** (generada) |
| `en/`, `en/venues/<local>/` | Versión en inglés | **No** (generada) |
| `eventos/` | Cenas de empresa y eventos privados | **No** (generada) |
| `404.html`, `sitemap.xml` | Página de error y sitemap | **No** (generados) |
| `green-2-0/`, `contacto/`, `home/`… | Redirecciones de URLs de la web antigua (WordPress), lista `REDIRECCIONES` | **No** (generadas) |
| `traviesa/` | Landing de Navidad de La Traviesa (diseño de su agencia) | Sí |
| `menu/` | Menú del día por QR (herramienta interna). **Oculto desde el 11/11/2026:** no se publica (`exclude` en `_config.yml`); para reactivarlo, quitar `menu` de ahí | Sí |
| `cartas/` | Cartas originales (PDF/imagen) | Sustituir archivo |
| `fotos/<local>/1-4.webp`, `logos/` | Imágenes | Sustituir archivo |
| `robots.txt`, `llms.txt` | Instrucciones para buscadores e IA | Sí |
| `CLAUDE.md`, `_CONTEXTO.md` | Instrucciones y contexto para Claude | Sí |

**Cómo regenerar:** desde esta carpeta, `python3 locales/_generar.py` (la fecha `lastmod` del sitemap se pone sola con la del día). Después, `git add -A && git commit -m "..." && git push`.

## 3. Locales (datos públicos)

| Local | Dirección | Tipo | Horario |
|---|---|---|---|
| Las Tablas 2.0 | C/ General Oraá, 26 | Bar de copas | J–S 20:00–02:00 |
| La Pequeña 2.0 | C/ General Oraá, 27 | Bar de copas (restaurante en pausa desde 03/11) | J–S 20:00–02:00 |
| La Chula 2.0 | C/ Claudio Coello, 116 | Bar de copas | J 20:00–03:00 · V–S 20:00–03:30 |
| La Peluquería 2.0 | C/ Alberto Alcocer, 32 | Bar de copas | J–S 20:00–02:00 |
| La Traviesa 2.0 | C/ López de Hoyos, 7 | Restaurante y bar | L–X 08–17 · J–V 08–01 · S 18–01 · D cerrado |
| Juanita 2.0 | C/ Alberto Alcocer, 33 | Discoteca | **Cerrada temporalmente** (sin página propia) |
| Green 2.0 | P.º de la Castellana, 40 bis | Restaurante, bar y discoteca | L–X 08–22 · J–V 08–06 · S 18–06 |

**Si cambia un horario o una dirección, hay que actualizarlo en cuatro sitios:**
1. `LOCALES` en `_generar.py`, y luego regenerar.
2. En `index.html`: `HORARIOS{}`, `D.<local>.hor`, la etiqueta `lc-tag` de la tarjeta del local y el JSON-LD de la cabecera.
3. `llms.txt`.
4. Si afecta a los textos, también la traducción en `EN` (en `_generar.py`).

Contacto público: WhatsApp 656 48 50 99 · hola@grupodospuntocero.com · Instagram @grupo_2.0 · TikTok @grupo2.0_

Marca: negro, rosa `#EF89B0`, fucsia `#e0477e`, cyan `#66c6e0` · Archivo Black + Montserrat · tono canalla, sarcástico, muy español.

## 4. Lo que está hecho (SEO)

- **Datos estructurados** (JSON-LD):
  - Organización y cada local con su horario.
  - Cartas de La Traviesa y Green como `Menu`, con platos y precios.
  - Migas de pan.
  - `Service` para eventos.
- **Páginas por local** en `/locales/<local>/`, con texto, horario, fotos, preguntas frecuentes, carta en texto (Traviesa y Green) y aviso «abierto ahora».
- **`/locales/`**: los 6 locales por zona (Salamanca, Chamartín, Castellana) y una tabla de direcciones y horarios.
- **`/eventos/`**: cenas de empresa, cumpleaños, despedidas y menús de Navidad de 45–65 € en La Traviesa. Reserva en Komvo.
- **Inglés**: portada en `/en/` y locales en `/en/venues/<local>/`.
  - Enlazadas con `hreflang` y botón ES/EN.
  - Los platos de la carta se quedan en español.
- **`sitemap.xml`** con fotos, `robots.txt` (bloquea `/menu/`), `llms.txt` y página 404 propia.
- **Redirecciones** de 16 URLs de la web antigua (WordPress) que Google seguía mostrando como 404 (p. ej. `/green-2-0/` → `/locales/green/`). Si aparece otra en Search Console > Indexación > «No se ha encontrado (404)», añadirla a `REDIRECCIONES` y regenerar.
- **Diseño**: modo día/noche en todas las páginas (preferencia compartida `g20theme`).
- **Rendimiento**: logos reducidos, animaciones solo en pantalla, sin `blur` ni `mix-blend-mode` en elementos animados.

## 5. Reglas al tocar la web

- **Generadas:** nunca editar a mano las páginas generadas; se cambia `_generar.py` y se regenera.
- **Al cambiar un texto de un local,** cambiar también su traducción inglesa (`EN` en `_generar.py`).
- **Al cambiar la carta impresa,** actualizar también `CARTAS` en `_generar.py`; el texto es lo que lee Google.
- **Logos nuevos:** reducirlos (máx. 1400×640) antes de subirlos.
- **Mayúsculas en GitHub:** distingue mayúsculas y minúsculas. Comprobar el nombre exacto de carpetas y archivos.
- **Píxeles de seguimiento:** si se añade Meta Pixel o GA4, actualizar la política de cookies y privacidad, que ahora dice que no hay cookies de seguimiento.
- **Claves y contraseñas:** nunca en la web ni en este archivo.
- **Probar en local:** servir la carpeta con un servidor estático y abrir `http://localhost:<puerto>`. En el Mac de oficina hay una configuración `pagina-web` en el puerto 8765.

## 6. Pendiente

**Del lado del cliente (hacer en Google o pedir a quien corresponda):**
- [x] Google Business (revisado 10/11): las 7 fichas enlazan a su página de local (Juanita a la portada), Juanita sale «cerrado temporalmente» y La Chula tiene el viernes hasta las 03:30. Green tiene dos fichas: «Green 2.0 Restaurante» y «Green 2.0 Discoteca».
- [ ] Google Business: horarios corregidos en Google el 10/11. Comprobar en unos días que se ven en Maps:
  - La Pequeña: ya se ve J–S 20:00–02:00 ✔
  - La Traviesa: aún salía el antiguo (J–V 8–02, S 19–02). Debe quedar L–X 08–17 · J–V 08–01 · S 18–01 · D cerrado.
  - Green: el bueno es el de su ficha de Google (L–X 08–22 · J–V 08–06 · S 18–06); la web se cambió a ese horario el 10/11. Green tiene dos fichas: Restaurante y Discoteca (J–S 23:30–06).
- [ ] Google Business: el enlace a la carta de La Traviesa y de Green no se ve aún en Maps (puede estar en revisión). Volver a mirar en unos días.
- [x] Search Console: «Validar corrección» de los 404 iniciada el 10/11. Google tarda hasta ~2 semanas; mirar el resultado en Indexación > «No se ha encontrado (404)».
- [x] Search Console (revisado 11/11): sitemap leído el 11/11 con las 17 páginas, sin errores. Indexadas la portada, `/locales/`, `/eventos/`, `/traviesa/`, las 6 páginas de local en español, `/en/` y 5 de las 6 páginas de local en inglés. Pedida la indexación de `/en/venues/green/` (la única que Google no conocía).
- [ ] Search Console: mirar en 2–3 semanas si La Traviesa sube en «la traviesa madrid», «restaurante la traviesa» y «bar la traviesa madrid» (el 11/11 estaba en 8,3 / 10,4 / 15,1).
- [x] Search Console: `/en/venues/green/` ya indexada (comprobado 12/11). Ya están en Google las 17 páginas del sitemap. Los «404» que quedan son archivos del WordPress antiguo (`wp-content/…`); es normal, desaparecerán solos.
- [ ] Códigos postales de Claudio Coello 116 y Alberto Alcocer 32.
- [x] URL del canal de WhatsApp: ya está puesta en la portada (sección Contacto).
- [x] Datos fiscales del aviso legal: ya están en la portada (Aviso legal y Privacidad).
- [x] Prensa: emails enviados a Time Out Madrid, Madrid Secreto y Guía del Ocio (10/11). Si publican algo, añadir «Nos han mencionado en…».

**Agencias:**
- [ ] La Traviesa: cuando su agencia publique `traviesa.grupodospuntocero.com` con SSL, redirigir `/traviesa/` a ese subdominio y quitarlo del sitemap.
- [ ] Green: esperar el ZIP de su agencia y subirlo a `/green/` sin indexar.

**Ideas propuestas, sin hacer:**
- Página de Nochevieja de Green (falta confirmar fiesta y precios en Fourvenues).
- Si el personal habla inglés, decirlo en la versión inglesa.
- Página «Nos han mencionado en…» cuando salga algo en prensa.
- Versión inglesa de `/eventos/`.

## 7. Historial de sesiones

- **03/11/2026:**
  - Auditoría SEO, datos estructurados, robots, sitemap y llms.txt.
  - Páginas por local.
  - Rendimiento.
  - Landing de La Traviesa.
  - Ágora (reservas de La Traviesa) y Fourvenues (entradas de Green).
- **04/11/2026:**
  - Páginas de local con la estética de la portada y modo día/noche.
  - Viernes de La Chula hasta las 03:30.
  - Cartas en texto y página `/eventos/`.
  - Carta definitiva de Green.
  - Emails de prensa.
  - Página `/locales/`, 404 y sitemap con fotos.
  - Versión en inglés.
- **10/11/2026:**
  - Carpeta renombrada de «Pagina Web» a «WEB 2.0».
  - Creados este contexto y `CLAUDE.md`.
  - Emails de prensa enviados; carpeta de borradores eliminada.
  - Revisadas las fichas de Google Business: webs, Juanita y La Chula bien; corregidos horarios de La Pequeña, La Traviesa y Green en Google.
  - Search Console (semana 2–8/11): 200 clics, 3.810 impresiones, posición media 5,9; impresiones diarias de ~200 a ~800. 14 páginas indexadas.
  - Redirecciones de 16 URLs antiguas de WordPress (la de Green tenía 744 impresiones en la semana).
  - Green: lunes a miércoles pasa a 08:00–22:00 en toda la web (portada, datos para Google, páginas ES/EN, /locales/ y llms.txt).
- **11/11/2026:**
  - Revisión de código: 37 páginas sin enlaces rotos; generador y portada revisados.
  - Corregidas las etiquetas de horario de la portada: La Traviesa «L–M» → «L–X» (tarjeta y ficha) y Green «L–M 08–17» → «L–X 08–22».
  - Inglés: la carta de Green decía «20:00 to 00:00»; ahora «20:00 to 06:00», como en español.
  - Portada: tema día/noche aplicado antes de pintar (sin parpadeo) y almacenamiento del navegador protegido, para que la página no se rompa si está bloqueado.
  - Política de cookies: menciona también el sessionStorage de la animación de entrada.
  - Quitado de Juanita el enlace a un evento de Fourvenues ya pasado.
  - `menu/supabase_setup.sql` → `menu/_supabase_setup.sql` (ya no se publica en la web).
  - Sitemap con la fecha del día automática.
  - Revisión fusionada y publicada en `main`.
  - Franja «En directo» de la portada: solo salen los locales abiertos ahora mismo (antes salían también los cerrados con «Abre mañana…»). Si no hay ninguno abierto, sale «Ahora mismo descansamos».
  - Search Console revisado con la usuaria (213 clics en la semana; 14 páginas indexadas y casi todas las nuevas ya dentro). Solicitada la indexación de `/en/venues/green/`.
  - Menú del día (`/menu/`) oculto: ya no se publica, aunque los archivos siguen en la carpeta.
  - Desde hoy se publica directamente: cada cambio comprobado se sube a `main` sin rama ni PR (regla 5 de `CLAUDE.md`).
  - SEO de La Traviesa (datos de Search Console 2–9/11: 49 clics, 946 impresiones; sale 2.º–4.º buscando «la traviesa 2.0», pero 8.º–15.º en «la traviesa madrid», «restaurante la traviesa» o «bar la traviesa madrid»). Reforzada su página ES/EN:
    - título con «Madrid»;
    - descripción con comidas de trabajo, tapas y cenas de empresa;
    - párrafo nuevo sobre la cocina;
    - dos preguntas frecuentes nuevas (qué se come; comida de trabajo / cena de empresa);
    - en los datos para Google, `alternateName` («La Traviesa», «Traviesa 2.0», «La Traviesa Madrid») y `servesCuisine`.
    Campos nuevos opcionales del generador: `alt_nombres` y `cocina`.
  - 12/11: pedida en Search Console la reindexación de `/locales/la-traviesa/` y `/en/venues/la-traviesa/` (las dos ya estaban indexadas; es para que lea el texto nuevo).
