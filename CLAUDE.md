# WEB 2.0 · Instrucciones para Claude

Web pública de Grupo 2.0 (grupodospuntocero.com). Habla siempre en español con el usuario.

1. **Al empezar:** lee `_CONTEXTO.md` antes de nada. Ahí están el estado del proyecto, las reglas y lo pendiente. Recuerda al usuario las tareas pendientes que le tocan.
2. **Al terminar o cuando el usuario se despida:** actualiza `_CONTEXTO.md`:
   - fecha de última actualización;
   - lo hecho en la sesión, en «Historial de sesiones»;
   - pendientes nuevos o cerrados;
   - reglas nuevas.

   Después súbelo con `git add -A && git commit && git push`, para que esté al día en el otro ordenador.
3. **El repositorio es público:** nunca escribas en `_CONTEXTO.md`, en este archivo ni en la web contraseñas, tokens, PINs, claves de API, datos personales ni fallos de seguridad.
4. **Páginas generadas:** casi todas salen de `locales/_generar.py`. No edites a mano los HTML de `locales/`, `en/`, `eventos/`, `404.html` ni `sitemap.xml`. Cambia el generador y ejecuta `python3 locales/_generar.py`.
