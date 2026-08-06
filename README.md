# Portfolio personal - Jaime Betancur Espinosa

Sitio estático preparado para **GitHub Pages** con HTML, CSS y JavaScript.

## Estructura

- `index.html`: contenido principal del portfolio
- `styles.css`: estilos modernos y responsivos
- `script.js`: menú móvil + animaciones de aparición
- `cv.pdf`: archivo del CV para descarga

## Publicación en GitHub Pages

1. Ve a **Settings → Pages** en el repositorio.
2. En **Build and deployment**, selecciona:
   - **Source:** Deploy from a branch
   - **Branch:** `main` / `/ (root)`
3. Guarda y espera el despliegue.

## Personalización rápida

- Cambia colores en `:root` dentro de `styles.css`.
- Edita secciones de experiencia/proyectos en `index.html`.
- Reemplaza `cv.pdf` por tu CV real manteniendo el mismo nombre.

## Generar PDF del perfil con Python

Este repositorio incluye un script que convierte el perfil publicado en GitHub Pages en un PDF estilo hoja de vida y siempre actualiza `cv.pdf`.

URL fuente usada por el script:

- `https://jaimebe4.github.io/jaimebetancur.github.io/`

1. Instala dependencias:
   - `pip install -r requirements.txt`
2. Instala Chromium para Playwright (una sola vez):
   - `python -m playwright install chromium`
3. Genera el PDF:
   - `python generar_pdf_perfil.py`

### Opcion rapida en Windows (.bat)

Tambien puedes ejecutar directamente:

- `generar_pdf_perfil.bat`

El .bat usa el script Python y muestra mensajes de error si falta Python o dependencias.

El resultado se guarda en `cv.pdf` en la raiz del proyecto.

> Trigger deploy: 2026-07-29
