from pathlib import Path


SOURCE_URL = "https://jaimebe4.github.io/jaimebetancur.github.io/"


def expandir_contenido(page):
        """Expande secciones colapsadas para incluir toda la experiencia en el PDF."""
        botones = page.query_selector_all(".timeline-item.long-exp .exp-toggle")
        for boton in botones:
                expanded = boton.get_attribute("aria-expanded")
                if expanded != "true":
                        boton.click()

        summaries = page.query_selector_all("details:not([open]) > summary")
        for summary in summaries:
                summary.click()


def reordenar_secciones_para_cv(page):
        """Ubica Habilidades entre Sobre mi y Experiencia solo para la version PDF."""
        page.evaluate(
                """
                () => {
                    const sobreMi = document.querySelector('#sobre-mi');
                    const habilidades = document.querySelector('#habilidades');
                    const experiencia = document.querySelector('#experiencia');

                    if (!sobreMi || !habilidades || !experiencia) {
                        return;
                    }

                    const parent = sobreMi.parentElement;
                    if (!parent) {
                        return;
                    }

                    // Evita reinsertar si ya esta en la posicion deseada.
                    if (sobreMi.nextElementSibling === habilidades) {
                        return;
                    }

                    parent.insertBefore(habilidades, experiencia);
                }
                """
        )


def filtrar_experiencia_enfoque_desarrollo(page):
        """Elimina contenido de infraestructura para enfocar la experiencia en desarrollo."""
        page.evaluate(
                """
                () => {
                    const palabrasInfra = [
                        'infraestructura',
                        'servidor',
                        'servidores',
                        'active directory',
                        'controlador de dominio',
                        'dominio',
                        'dhcp',
                        'iis',
                        'ftp',
                        'proxy',
                        'isa server',
                        'hosting',
                        'cpanel',
                        'copias de seguridad',
                        'backup',
                        'backups',
                        'red lan',
                        'wi-fi',
                        'wifi',
                        'licenciamiento',
                        'inventario de equipos',
                        'impresoras',
                        'hardware',
                        'conectividad',
                        'equipos de computo',
                        'equipos de c\u00f3mputo',
                        'soporte de infraestructura',
                        'adquisicion',
                        'adquisici\u00f3n',
                        'proveedores',
                        'correo',
                        'redireccionamientos',
                        'listas blancas',
                        'listas negras'
                    ];

                    const normalizar = (texto) =>
                        (texto || '')
                            .toLowerCase()
                            .normalize('NFD')
                            .replace(/[\u0300-\u036f]/g, '');

                    const esInfra = (texto) => {
                        const t = normalizar(texto);
                        return palabrasInfra.some((palabra) => t.includes(normalizar(palabra)));
                    };

                    const seccionExperiencia = document.querySelector('#experiencia');
                    if (!seccionExperiencia) {
                        return;
                    }

                    // Filtra bullets de experiencias largas.
                    seccionExperiencia.querySelectorAll('li').forEach((li) => {
                        if (esInfra(li.textContent)) {
                            li.remove();
                        }
                    });

                    // Filtra parrafos de experiencia con foco en infraestructura.
                    seccionExperiencia.querySelectorAll('.timeline-card > p').forEach((p) => {
                        const texto = normalizar(p.textContent);
                        if (!texto || texto === 'funciones:') {
                            return;
                        }
                        if (esInfra(texto)) {
                            p.remove();
                        }
                    });

                    // Limpieza visual: elimina listas vacias y sus contenedores directos.
                    seccionExperiencia.querySelectorAll('.timeline-card ul').forEach((ul) => {
                        if (ul.querySelectorAll('li').length === 0) {
                            const contenedor = ul.closest('.exp-preview') || ul.parentElement;
                            if (contenedor && contenedor !== ul && contenedor.children.length === 1) {
                                contenedor.remove();
                            } else {
                                ul.remove();
                            }
                        }
                    });
                }
                """
        )


def omitir_tags_sobre_mi(page):
        """Omite en el PDF la linea de tags del bloque Sobre mi."""
        page.evaluate(
                """
                () => {
                    const sobreMi = document.querySelector('#sobre-mi');
                    if (!sobreMi) {
                        return;
                    }

                    const frasesObjetivo = [
                        'oracle ai',
                        'inteligencia artificial',
                        'bases de datos',
                        'desarrollo full stack'
                    ];

                    const normalizar = (texto) =>
                        (texto || '')
                            .toLowerCase()
                            .normalize('NFD')
                            .replace(/[\u0300-\u036f]/g, '');

                    sobreMi.querySelectorAll('.card p').forEach((p) => {
                        const texto = normalizar(p.textContent);
                        const contieneTodas = frasesObjetivo.every((f) => texto.includes(normalizar(f)));
                        if (contieneTodas) {
                            p.remove();
                        }
                    });
                }
                """
        )


def aplicar_estilo_hoja_de_vida(page):
        """Aplica estilo de impresion tipo CV para un PDF legible y presentable."""
        page.add_style_tag(
                content="""
                @page {
                    size: A4;
                    margin: 11mm 10mm 12mm 10mm;
                }

                * {
                    animation: none !important;
                    transition: none !important;
                    box-shadow: none !important;
                }

                html,
                body {
                    background: #ffffff !important;
                    color: #111827 !important;
                    font-family: "Segoe UI", Arial, sans-serif !important;
                    font-size: 10.5pt !important;
                    line-height: 1.35 !important;
                    -webkit-print-color-adjust: exact;
                    print-color-adjust: exact;
                }

                .site-header,
                .hero-actions,
                .exp-toggle,
                .site-footer {
                    display: none !important;
                }

                .container,
                .hero,
                .section {
                    width: 100% !important;
                    max-width: 100% !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                .hero {
                    margin-bottom: 12px !important;
                    border-bottom: 1.6px solid #1f4ea3 !important;
                    padding-bottom: 8px !important;
                }

                .hero-top {
                    display: grid !important;
                    grid-template-columns: 100px 1fr !important;
                    gap: 10px !important;
                    align-items: center !important;
                }

                .hero-photo-wrap {
                    background: transparent !important;
                    padding: 0 !important;
                }

                .hero-photo {
                    width: 96px !important;
                    height: 96px !important;
                    border: 2px solid #1e3a8a !important;
                    outline: 1px solid #9fb5e3 !important;
                    outline-offset: 2px !important;
                }

                h1 {
                    font-size: 22pt !important;
                    line-height: 1.1 !important;
                    margin: 0 0 4px !important;
                    color: #0f172a !important;
                }

                h2 {
                    font-size: 13pt !important;
                    color: #1e3a8a !important;
                    border-bottom: 1px solid #dbe4f5 !important;
                    margin: 12px 0 6px !important;
                    padding-bottom: 2px !important;
                    break-after: avoid-page;
                }

                h3 {
                    font-size: 11pt !important;
                    margin: 0 0 3px !important;
                    color: #0f172a !important;
                }

                .lead,
                .eyebrow,
                .role,
                p,
                li,
                a,
                span,
                strong {
                    color: #111827 !important;
                }

                .lead {
                    font-size: 10pt !important;
                }

                /* Justificado principal del contenido narrativo del CV */
                #sobre-mi p,
                #experiencia p,
                #experiencia li,
                #proyectos p,
                #proyectos li {
                    text-align: justify !important;
                    text-justify: inter-word !important;
                    hyphens: auto !important;
                }

                /* Mantener encabezados cortos legibles y no justificados */
                #experiencia .role,
                #proyectos h3,
                #sobre-mi h2,
                #experiencia h2,
                #proyectos h2 {
                    text-align: left !important;
                }

                .section {
                    break-inside: avoid;
                    page-break-inside: avoid;
                    margin-top: 8px !important;
                }

                .card,
                .timeline-card,
                .skills-group.card {
                    border: 1px solid #dbe4f5 !important;
                    border-radius: 8px !important;
                    background: #ffffff !important;
                    padding: 8px !important;
                    margin-bottom: 6px !important;
                    break-inside: avoid;
                    page-break-inside: avoid;
                }

                .timeline {
                    padding-left: 0 !important;
                    margin-top: 0 !important;
                }

                .timeline::before,
                .timeline-dot {
                    display: none !important;
                }

                .timeline-item {
                    margin-bottom: 8px !important;
                }

                .timeline-year {
                    position: static !important;
                    display: inline-block !important;
                    width: auto !important;
                    margin: 0 0 3px !important;
                    padding: 2px 6px !important;
                    border-radius: 999px !important;
                    border: 1px solid #c5d4f0 !important;
                    background: #f3f7ff !important;
                    font-size: 9pt !important;
                    color: #1f4ea3 !important;
                    text-align: left !important;
                    left: auto !important;
                    top: auto !important;
                }

                #habilidades .skills-columns {
                    display: grid !important;
                    grid-template-columns: 1fr 1fr !important;
                    gap: 6px !important;
                    align-items: start !important;
                }

                #habilidades .skills-group.card {
                    margin-bottom: 4px !important;
                    padding: 6px !important;
                }

                #habilidades .skills-group.card h3 {
                    margin: 0 0 4px !important;
                    border: none !important;
                    color: #1f4ea3 !important;
                    font-size: 10pt !important;
                    line-height: 1.2 !important;
                }

                #habilidades .skills-grid {
                    display: grid !important;
                    grid-template-columns: 1fr !important;
                    gap: 3px !important;
                }

                #habilidades .skill-chip,
                #habilidades .skills-icon-gap .skill-chip {
                    display: grid !important;
                    grid-template-columns: 16px 1fr !important;
                    align-items: center !important;
                    border: 1px solid #d7e3fa !important;
                    background: #f8fbff !important;
                    min-height: 22px !important;
                    padding: 2px 5px !important;
                    gap: 5px !important;
                    border-radius: 5px !important;
                }

                #habilidades .skills-icon-gap .skill-chip i {
                    width: 14px !important;
                    min-width: 14px !important;
                    height: 14px !important;
                    font-size: 8.6pt !important;
                    background: transparent !important;
                }

                #habilidades .skills-icon-gap .skill-chip span {
                    font-size: 8.9pt !important;
                    line-height: 1.15 !important;
                    font-weight: 600 !important;
                }

                #habilidades {
                    break-before: avoid-page;
                    page-break-before: avoid;
                }

                @media print {
                    #habilidades .skills-columns {
                        grid-template-columns: 1fr 1fr !important;
                    }
                }

                ul {
                    margin: 4px 0 0 16px !important;
                    padding: 0 !important;
                }

                li {
                    margin: 0 0 2px !important;
                }

                #contacto a {
                    text-decoration: none !important;
                }

                .reveal {
                    opacity: 1 !important;
                    transform: none !important;
                }
                """
        )


def main() -> int:
        try:
                from playwright.sync_api import sync_playwright
        except ImportError:
                print("No se encontro Playwright.")
                print("Instala dependencias con: pip install -r requirements.txt")
                print("Luego instala Chromium con: python -m playwright install chromium")
                return 1

        raiz = Path(__file__).resolve().parent
        archivo_pdf = raiz / "cv.pdf"

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page(viewport={"width": 1366, "height": 2400})

                page.goto(SOURCE_URL, wait_until="networkidle", timeout=120000)
                page.wait_for_timeout(1200)

                expandir_contenido(page)
                reordenar_secciones_para_cv(page)
                filtrar_experiencia_enfoque_desarrollo(page)
                omitir_tags_sobre_mi(page)
                aplicar_estilo_hoja_de_vida(page)

                page.emulate_media(media="print")
                page.pdf(
                    path=str(archivo_pdf),
                    format="A4",
                    print_background=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    prefer_css_page_size=True,
                )

                browser.close()
        except Exception as exc:
            print("Error al generar el PDF desde la URL publica.")
            print(f"Detalle: {exc}")
            print("Verifica conexion a internet y que la URL sea accesible.")
            return 1

        print(f"PDF estilo hoja de vida generado desde URL: {SOURCE_URL}")
        print(f"Archivo generado: {archivo_pdf}")
        return 0


if __name__ == "__main__":
        raise SystemExit(main())
