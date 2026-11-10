# WEB 2.0 · Contexto del proyecto

> Última actualización: **10/11/2026**
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
| `traviesa/` | Landing de Navidad de La Traviesa (diseño de su agencia) | Sí |
| `menu/` | Menú del día por QR (herramienta interna, excluida de Google) | Sí |
| `cartas/` | Cartas originales (PDF/imagen) | Sustituir archivo |
| `fotos/<local>/1-4.webp`, `logos/` | Imágenes | Sustituir archivo |
| `robots.txt`, `llms.txt` | Instrucciones para buscadores e IA | Sí |
| `CLAUDE.md`, `_CONTEXTO.md` | Instrucciones y contexto para Claude | Sí |

**Cómo regenerar:** desde esta carpeta, `python3 locales/_generar.py`. Después, `git add -A && git commit -m "..." && git push`.

## 3. Locales (datos públicos)

| Local | Dirección | Tipo | Horario |
|---|---|---|---|
| Las Tablas 2.0 | C/ General Oraá, 26 | Bar de copas | J–S 20:00–02:00 |
| La Pequeña 2.0 | C/ General Oraá, 27 | Bar de copas (restaurante en pausa desde 03/11) | J–S 20:00–02:00 |
| La Chula 2.0 | C/ Claudio Coello, 116 | Bar de copas | J 20:00–03:00 · V–S 20:00–03:30 |
| La Peluquería 2.0 | C/ Alberto Alcocer, 32 | Bar de copas | J–S 20:00–02:00 |
| La Traviesa 2.0 | C/ López de Hoyos, 7 | Restaurante y bar | L–X 08–17 · J–V 08–01 · S 18–01 · D cerrado |
| Juanita 2.0 | C/ Alberto Alcocer, 33 | Discoteca | **Cerrada temporalmente** (sin página propia) |
| Green 2.0 | P.º de la Castellana, 40 bis | Restaurante, bar y discoteca | L–X 08–17 · J–V 08–06 · S 18–06 |

**Si cambia un horario o una dirección, hay que actualizarlo en cuatro sitios:**
1. `LOCALES` en `_generar.py`, y luego regenerar.
2. En `index.html`: `HORARIOS{}`, `D.<local>.hor` y el JSON-LD de la cabecera.
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
- [ ] Google Business: en la ficha de cada local, poner como web su página (`grupodospuntocero.com/locales/<local>/`), revisar horario y categoría y marcar Juanita como «cerrado temporalmente».
- [ ] Google Business: enlazar la carta de La Traviesa y de Green (`/locales/<local>/#carta`) y poner el viernes de La Chula hasta las 03:30.
- [ ] Search Console: reenviar `sitemap.xml` y pedir indexación de `/locales/`, `/en/`, las páginas de cada local y `/eventos/`.
- [ ] Códigos postales de Claudio Coello 116 y Alberto Alcocer 32.
- [ ] URL del canal de WhatsApp (marcador `CANAL_WA_URL` en la portada).
- [ ] Datos fiscales para el aviso legal (razón social, CIF, domicilio).
- [ ] Reseñas reales de Google para el carrusel de la portada (ahora son de ejemplo).
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
