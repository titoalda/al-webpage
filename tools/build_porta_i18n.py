#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Genera en/projects/porta.html y gl/projects/porta.html desde projects/porta.html (ES).
# Uso: python3 tools/build_porta_i18n.py   (desde la raiz del repo)
# Genera en/projects/porta.html y gl/projects/porta.html desde projects/porta.html
import re

SRC = "projects/porta.html"
base = open(SRC, encoding="utf-8").read()

def build(lang, out_path, T):
    s = base
    # 1) rutas de assets: un nivel más de profundidad
    s = s.replace('"../static/', '"../../static/')
    # 2) selector de idioma
    s = s.replace('<a href="porta" class="lang-option active">ES</a>',
                  '<a href="../../projects/porta" class="lang-option">ES</a>')
    s = s.replace('<a href="../en/projects/porta" class="lang-option">EN</a>',
                  '<a href="porta" class="lang-option active">EN</a>' if lang == "en"
                  else '<a href="../../en/projects/porta" class="lang-option">EN</a>')
    s = s.replace('<a href="../gl/projects/porta" class="lang-option">GAL</a>',
                  '<a href="porta" class="lang-option active">GAL</a>' if lang == "gl"
                  else '<a href="../../gl/projects/porta" class="lang-option">GAL</a>')
    # 3) head: lang, canonical, hreflang, URLs og/twitter, breadcrumbs
    s = s.replace('<html lang="es">', f'<html lang="{lang}">')
    s = s.replace('<link rel="canonical" href="https://aldaraalvarez.es/projects/porta">',
                  f'<link rel="canonical" href="https://aldaraalvarez.es/{lang}/projects/porta">')
    s = s.replace(
        '<link rel="alternate" hreflang="es" href="https://aldaraalvarez.es/projects/porta" />\n'
        '        <link rel="alternate" hreflang="x-default" href="https://aldaraalvarez.es/projects/porta" />',
        '<link rel="alternate" hreflang="es" href="https://aldaraalvarez.es/projects/porta" />\n'
        '        <link rel="alternate" hreflang="en" href="https://aldaraalvarez.es/en/projects/porta" />\n'
        '        <link rel="alternate" hreflang="gl" href="https://aldaraalvarez.es/gl/projects/porta" />\n'
        '        <link rel="alternate" hreflang="x-default" href="https://aldaraalvarez.es/projects/porta" />')
    s = s.replace('content="https://aldaraalvarez.es/projects/porta"',
                  f'content="https://aldaraalvarez.es/{lang}/projects/porta"')
    s = s.replace('"url": "https://aldaraalvarez.es/projects/porta"',
                  f'"url": "https://aldaraalvarez.es/{lang}/projects/porta"')
    s = s.replace('"item": "https://aldaraalvarez.es/"', f'"item": "https://aldaraalvarez.es/{lang}/"')
    s = s.replace('"item": "https://aldaraalvarez.es/projects"', f'"item": "https://aldaraalvarez.es/{lang}/projects"')
    s = s.replace('"item": "https://aldaraalvarez.es/projects/porta"',
                  f'"item": "https://aldaraalvarez.es/{lang}/projects/porta"')
    # 4) textos
    for a, b in T:
        if a not in s:
            print(f"[{lang}] NO ENCONTRADO: {a[:70]}...")
        s = s.replace(a, b)
    open(out_path, "w", encoding="utf-8").write(s)
    print(f"{out_path} escrito ({len(s)} bytes)")

DESC_ES = "Proyecto de identidad visual y diseño editorial de Porta, cuadernos de identidad baionesa: naming, logotipo, sistema gráfico, maquetación, fotografía, ilustración y papelería, realizado por Aldara Álvarez."
DESC_EN = "Porta visual identity and editorial design project — a mook about Baiona's heritage: naming, logo, graphic system, editorial layout, photography, illustration and stationery, by Aldara Álvarez."
DESC_GL = "Proxecto de identidade visual e deseño editorial de Porta, cadernos de identidade baionesa: naming, logotipo, sistema gráfico, maquetación, fotografía, ilustración e papelería, realizado por Aldara Álvarez."

EN = [
    ("<title>Porta | Identidad Visual y Diseño Editorial - Aldara Álvarez</title>",
     "<title>Porta | Visual Identity and Editorial Design - Aldara Álvarez</title>"),
    ('content="Porta | Identidad Visual y Diseño Editorial - Aldara Álvarez"',
     'content="Porta | Visual Identity and Editorial Design - Aldara Álvarez"'),
    (f'content="{DESC_ES}"', f'content="{DESC_EN}"'),
    (f'"description": "{DESC_ES}"', f'"description": "{DESC_EN}"'),
    ('"name": "Inicio"', '"name": "Home"'),
    ('"name": "Proyectos"', '"name": "Projects"'),
    # header / nav
    ('data-label="Proyectos"', 'data-label="Projects"'),
    ('class="dock-tooltip">Proyectos</span>', 'class="dock-tooltip">Projects</span>'),
    ('data-label="Sobre Mí"', 'data-label="About Me"'),
    ('class="dock-tooltip">Sobre Mí</span>', 'class="dock-tooltip">About Me</span>'),
    ('data-label="Idioma"', 'data-label="Language"'),
    ('class="dock-tooltip">Idioma</span>', 'class="dock-tooltip">Language</span>'),
    ('data-label="Contacto"', 'data-label="Contact"'),
    ('class="dock-tooltip">Contacto</span>', 'class="dock-tooltip">Contact</span>'),
    ('<span class="back-arrow">←</span> Volver a inicio</a>', '<span class="back-arrow">←</span> Back to home</a>'),
    # intro
    ('alt="Porta — ilustración de portada"', 'alt="Porta — cover illustration"'),
    ('proyecto de&nbsp;diseño de&nbsp;identidad visual y&nbsp;editorial</p>',
     'visual identity and editorial design project</p>'),
    ("<p>Un&nbsp;<em>mook</em> editorial que&nbsp;traduce el&nbsp;patrimonio de&nbsp;Baiona (Galicia) en&nbsp;una experiencia de&nbsp;lectura pausada.</p>",
     "<p>An editorial <em>mook</em> that translates the heritage of Baiona (Galicia) into an unhurried reading experience.</p>"),
    ("<h2>El&nbsp;proyecto</h2>", "<h2>The project</h2>"),
    ("<p>PORTA es&nbsp;un&nbsp;proyecto integral de&nbsp;autor que&nbsp;abarca la&nbsp;conceptualización, edición y&nbsp;producción de&nbsp;principio a&nbsp;fin de&nbsp;un&nbsp;<em>mook</em> —un&nbsp;formato híbrido entre revista y&nbsp;libro— dedicado al&nbsp;patrimonio de&nbsp;Baiona. Ante la&nbsp;saturación de&nbsp;la&nbsp;comunicación turística masiva, la&nbsp;propuesta apuesta por&nbsp;el&nbsp;<em>slow journalism</em>, materializándose en&nbsp;una pieza editorial de&nbsp;coleccionista con&nbsp;un&nbsp;alto valor cultural y&nbsp;estético pensado para&nbsp;perdurar en&nbsp;el&nbsp;tiempo.</p>",
     "<p>PORTA is a comprehensive authorial project covering the conceptualisation, editing and production, from start to finish, of a <em>mook</em> —a hybrid format between magazine and book— devoted to the heritage of Baiona. In response to the saturation of mass tourism communication, the proposal embraces <em>slow journalism</em>, materialising as a collector's editorial piece with high cultural and aesthetic value, designed to stand the test of time.</p>"),
    ("<h2>El&nbsp;reto</h2>", "<h2>The challenge</h2>"),
    ("<p>El&nbsp;desafío radicó en&nbsp;asumir la&nbsp;autoría y&nbsp;dirección de&nbsp;arte 360º de&nbsp;una publicación compleja desde cero. El&nbsp;proyecto exigía ir&nbsp;mucho más allá de&nbsp;la&nbsp;maquetación clásica: implicaba romper con&nbsp;los códigos visuales genéricos del&nbsp;turismo convencional para&nbsp;construir un&nbsp;universo propio, encargándose simultáneamente de&nbsp;la&nbsp;estrategia de&nbsp;<em>branding</em>, la&nbsp;redacción del&nbsp;contenido escrito, la&nbsp;producción visual (fotografía e&nbsp;ilustración) y&nbsp;el&nbsp;diseño editorial de&nbsp;la&nbsp;obra.</p>",
     "<p>The challenge lay in taking on the authorship and 360º art direction of a complex publication from scratch. The project demanded going far beyond classic layout work: it meant breaking away from the generic visual codes of conventional tourism to build a universe of its own, simultaneously handling the <em>branding</em> strategy, the copywriting, the visual production (photography and illustration) and the editorial design of the piece.</p>"),
    ("<h2>La&nbsp;solución</h2>", "<h2>The solution</h2>"),
    ("<p>Para&nbsp;resolver este proyecto global, el&nbsp;flujo de&nbsp;trabajo se&nbsp;estructuró en&nbsp;cuatro fases estratégicas:</p>",
     "<p>To resolve this global project, the workflow was structured into four strategic phases:</p>"),
    ("<p><strong>Estrategia e&nbsp;Identidad de&nbsp;Marca:</strong> Creación del&nbsp;<em>branding</em> desde cero bajo el&nbsp;nombre de&nbsp;PORTA (puerta en&nbsp;gallego), evocando el&nbsp;concepto de&nbsp;puerto de&nbsp;arribada y&nbsp;fortaleza local. Se&nbsp;diseñó el&nbsp;imagotipo (arco de&nbsp;medio punto y&nbsp;vela latina), una paleta cromática basada en&nbsp;el&nbsp;paisaje atlántico y&nbsp;se&nbsp;desarrolló su&nbsp;Manual de&nbsp;Identidad de&nbsp;Marca normativo.</p>",
     "<p><strong>Strategy and Brand Identity:</strong> Creation of the <em>branding</em> from scratch under the name PORTA (door in Galician), evoking the concept of a port of arrival and the local fortress. The imagotype was designed (a round arch and a lateen sail), together with a colour palette based on the Atlantic landscape, and its normative Brand Identity Manual was developed.</p>"),
    ("<p><strong>Dirección de&nbsp;Arte y&nbsp;Contenido:</strong> Redacción íntegra de&nbsp;los textos de&nbsp;la&nbsp;publicación y&nbsp;dirección creativa del&nbsp;universo visual. Esto abarcó la&nbsp;realización de&nbsp;la&nbsp;serie fotográfica editorial en&nbsp;localización y&nbsp;la&nbsp;creación de&nbsp;ilustraciones digitales a&nbsp;medida para&nbsp;enriquecer la&nbsp;narrativa.</p>",
     "<p><strong>Art Direction and Content:</strong> Full copywriting of the publication's texts and creative direction of the visual universe. This included producing the editorial photography series on location and creating bespoke digital illustrations to enrich the narrative.</p>"),
    ("<p><strong>Diseño y&nbsp;Estilo Editorial:</strong> Diseño global de&nbsp;la&nbsp;publicación de&nbsp;96&nbsp;páginas estructurada bajo una retícula modular estricta. Para&nbsp;asegurar la&nbsp;cohesión visual del&nbsp;formato, se&nbsp;desarrolló un&nbsp;Manual de&nbsp;Estilo Editorial exhaustivo que&nbsp;unifica las jerarquías tipográficas y&nbsp;los ritmos de&nbsp;lectura.</p>",
     "<p><strong>Editorial Design and Style:</strong> Global design of the 96-page publication, structured on a strict modular grid. To ensure the visual cohesion of the format, an exhaustive Editorial Style Manual was developed, unifying typographic hierarchies and reading rhythms.</p>"),
    ("<p><strong>Producción Técnica:</strong> Planteamiento y&nbsp;preparación de&nbsp;artes finales para&nbsp;su&nbsp;producción física como objeto premium: impresión <em>offset</em> en&nbsp;papel natural certificado FSC, encuadernación vista cosida a&nbsp;hilo, acabados con&nbsp;estampación en&nbsp;seco (golpe seco) del&nbsp;logotipo en&nbsp;portada y&nbsp;un&nbsp;estuche contenedor rígido.</p>",
     "<p><strong>Technical Production:</strong> Planning and preparation of final artwork for its physical production as a premium object: <em>offset</em> printing on FSC-certified natural paper, exposed thread-sewn binding, blind embossing of the logo on the cover and a rigid slipcase.</p>"),
    ("<h2>Ficha técnica</h2>", "<h2>Technical details</h2>"),
    ("<p><strong>Rol y&nbsp;Disciplinas:</strong> Dirección de&nbsp;arte integral, Redacción y&nbsp;Edición de&nbsp;contenido, Diseño editorial, Identidad de&nbsp;marca, Fotografía, Ilustración y&nbsp;Packaging.</p>",
     "<p><strong>Role and Disciplines:</strong> Integral art direction, Content writing and editing, Editorial design, Brand identity, Photography, Illustration and Packaging.</p>"),
    ("<p><strong>Entregables principales:</strong> <em>Mook</em> impreso (17 × 24&nbsp;cm, 96&nbsp;págs.), Manual de&nbsp;Identidad de&nbsp;Marca, Manual de&nbsp;Estilo Editorial y&nbsp;Estuche contenedor.</p>",
     "<p><strong>Main deliverables:</strong> Printed <em>mook</em> (17 × 24&nbsp;cm, 96 pp.), Brand Identity Manual, Editorial Style Manual and Slipcase.</p>"),
    ("<p><strong>Software utilizado:</strong></p>", "<p><strong>Software used:</strong></p>"),
    ("<p><strong>Adobe InDesign:</strong> Maquetación integral de&nbsp;la&nbsp;publicación, sistemas de&nbsp;retículas, estilos y&nbsp;preparación de&nbsp;artes finales para&nbsp;imprenta.</p>",
     "<p><strong>Adobe InDesign:</strong> Full layout of the publication, grid systems, styles and preparation of print-ready artwork.</p>"),
    ("<p><strong>Adobe Illustrator:</strong> Diseño, vectorización y&nbsp;normativización de&nbsp;la&nbsp;identidad de&nbsp;marca, grafismos y&nbsp;cartografía.</p>",
     "<p><strong>Adobe Illustrator:</strong> Design, vectorisation and standardisation of the brand identity, graphic elements and cartography.</p>"),
    ("<p><strong>Adobe Photoshop:</strong> Tratamiento y&nbsp;revelado de&nbsp;la&nbsp;fotografía editorial, retoque digital y&nbsp;creación de&nbsp;mockups de&nbsp;presentación.</p>",
     "<p><strong>Adobe Photoshop:</strong> Processing and development of the editorial photography, digital retouching and creation of presentation mockups.</p>"),
    ("<p><strong>Procreate:</strong> Creación, abocetado e&nbsp;ilustración digital de&nbsp;los recursos gráficos de&nbsp;la&nbsp;obra.</p>",
     "<p><strong>Procreate:</strong> Creation, sketching and digital illustration of the graphic resources of the piece.</p>"),
    # flipbook
    ('Hojea el&nbsp;<em>mook</em></h2>', 'Flip through the&nbsp;<em>mook</em></h2>'),
    ("<span>Ver manual de&nbsp;identidad corporativa</span>", "<span>View the brand identity manual</span>"),
    ("<span>Ver manual de&nbsp;estilo editorial</span>", "<span>View the editorial style manual</span>"),
    ('aria-label="Página anterior"', 'aria-label="Previous page"'),
    ('aria-label="Página siguiente"', 'aria-label="Next page"'),
    ("Compra tu&nbsp;ejemplar aquí</p>", "Buy your copy here</p>"),
    ('class="button-circle">Ir a&nbsp;la&nbsp;tienda</a>', 'class="button-circle">Go to the store</a>'),
    # gallery
    ("Porta — identidad visual y&nbsp;editorial</p>", "Porta — visual and editorial identity</p>"),
    ("Galería del&nbsp;proyecto</h2>", "Project gallery</h2>"),
    ('alt="Logotipo de Porta"', 'alt="Porta logo"'),
    ('alt="Cubierta y slipcase de Porta"', 'alt="Porta cover and slipcase"'),
    ('alt="Monograma de Porta"', 'alt="Porta monogram"'),
    ('alt="Iconografía de Porta: barco, ola y arco"', 'alt="Porta iconography: boat, wave and arch"'),
    ('alt="Maquetación editorial de Porta"', 'alt="Porta editorial layout"'),
    ('alt="Monasterio de Baiona"', 'alt="Baiona monastery"'),
    ('alt="Ilustración a acuarela de Porta"', 'alt="Porta watercolour illustration"'),
    ('alt="Faro de Cabo Silleiro"', 'alt="Cape Silleiro lighthouse"'),
    ('alt="Monumento a la Virgen de la Roca"', 'alt="Virgen de la Roca monument"'),
    ('alt="Flora del entorno de Baiona"', 'alt="Flora around Baiona"'),
    ('alt="Petroglifos del Val Miñor"', 'alt="Val Miñor petroglyphs"'),
    ('alt="Patrimonio marítimo de Baiona"', 'alt="Maritime heritage of Baiona"'),
    ('alt="Papelería corporativa de Porta"', 'alt="Porta corporate stationery"'),
    ('alt="Merchandising de Porta"', 'alt="Porta merchandising"'),
    ('alt="Mockup editorial de Porta"', 'alt="Porta editorial mockup"'),
    ('alt="Colección editorial de Porta"', 'alt="Porta editorial collection"'),
    ('alt="Slipcase de Porta"', 'alt="Porta slipcase"'),
    # cta + footer
    ('class="button-circle center">VER MÁS PROYECTOS</a>', 'class="button-circle center">VIEW MORE PROJECTS</a>'),
    ("¿TIENES ALGÚN PROYECTO EN&nbsp;MENTE?</p>", "DO YOU HAVE A PROJECT IN MIND?</p>"),
    ("¡HABLEMOS!</p>", "LET'S TALK!</p>"),
    ("<span>ENVIAR MENSAJE</span>", "<span>SEND MESSAGE</span>"),
    ("Siempre es un placer conectar con&nbsp;nuevos proyectos y&nbsp;personas.</p>",
     "It is always a pleasure to connect with new projects and people.</p>"),
    ("<strong>Aldara Álvarez</strong> — Diseñadora Gráfica.<br>Graduada en Diseño por&nbsp;la&nbsp;UCM y Máster en Diseño Gráfico Digital por&nbsp;la&nbsp;UNIR. Especializada en soluciones visuales conceptuales, diseño editorial e identidad corporativa.",
     "<strong>Aldara Álvarez</strong> — Graphic Designer.<br>Graduate in Design from UCM with a Master's in Digital Graphic Design from UNIR. Specialized in conceptual visual solutions, editorial design and corporate identity."),
    ("<h3>Secciones</h3>", "<h3>Sections</h3>"),
    ('<a href="../projects">Proyectos</a>', '<a href="../projects">Projects</a>'),
    ('<a href="../about">Sobre Mí</a>', '<a href="../about">About Me</a>'),
    ('<a href="../contact">Contacto</a>', '<a href="../contact">Contact</a>'),
    ("<h3>Proyectos Destacados</h3>", "<h3>Featured Projects</h3>"),
    ("<h3>Contacto</h3>", "<h3>Contact</h3>"),
    ("Todos los derechos reservados.", "All rights reserved."),
    ('class="footer-legal-link">Aviso Legal</a>', 'class="footer-legal-link">Legal Notice</a>'),
    ('alt="Página ', 'alt="Page '),
    (' del mook PORTA"', ' of the PORTA mook"'),
]

GL = [
    ("<title>Porta | Identidad Visual y Diseño Editorial - Aldara Álvarez</title>",
     "<title>Porta | Identidade Visual e Deseño Editorial - Aldara Álvarez</title>"),
    ('content="Porta | Identidad Visual y Diseño Editorial - Aldara Álvarez"',
     'content="Porta | Identidade Visual e Deseño Editorial - Aldara Álvarez"'),
    (f'content="{DESC_ES}"', f'content="{DESC_GL}"'),
    (f'"description": "{DESC_ES}"', f'"description": "{DESC_GL}"'),
    ('"name": "Proyectos"', '"name": "Proxectos"'),
    # header / nav
    ('data-label="Proyectos"', 'data-label="Proxectos"'),
    ('class="dock-tooltip">Proyectos</span>', 'class="dock-tooltip">Proxectos</span>'),
    ('data-label="Sobre Mí"', 'data-label="Sobre Min"'),
    ('class="dock-tooltip">Sobre Mí</span>', 'class="dock-tooltip">Sobre Min</span>'),
    ('<span class="back-arrow">←</span> Volver a inicio</a>', '<span class="back-arrow">←</span> Volver ao inicio</a>'),
    # intro
    ('alt="Porta — ilustración de portada"', 'alt="Porta — ilustración de portada"'),
    ('proyecto de&nbsp;diseño de&nbsp;identidad visual y&nbsp;editorial</p>',
     'proxecto de&nbsp;deseño de&nbsp;identidade visual e&nbsp;editorial</p>'),
    ("<p>Un&nbsp;<em>mook</em> editorial que&nbsp;traduce el&nbsp;patrimonio de&nbsp;Baiona (Galicia) en&nbsp;una experiencia de&nbsp;lectura pausada.</p>",
     "<p>Un&nbsp;<em>mook</em> editorial que&nbsp;traduce o&nbsp;patrimonio de&nbsp;Baiona (Galicia) nunha experiencia de&nbsp;lectura pausada.</p>"),
    ("<h2>El&nbsp;proyecto</h2>", "<h2>O&nbsp;proxecto</h2>"),
    ("<p>PORTA es&nbsp;un&nbsp;proyecto integral de&nbsp;autor que&nbsp;abarca la&nbsp;conceptualización, edición y&nbsp;producción de&nbsp;principio a&nbsp;fin de&nbsp;un&nbsp;<em>mook</em> —un&nbsp;formato híbrido entre revista y&nbsp;libro— dedicado al&nbsp;patrimonio de&nbsp;Baiona. Ante la&nbsp;saturación de&nbsp;la&nbsp;comunicación turística masiva, la&nbsp;propuesta apuesta por&nbsp;el&nbsp;<em>slow journalism</em>, materializándose en&nbsp;una pieza editorial de&nbsp;coleccionista con&nbsp;un&nbsp;alto valor cultural y&nbsp;estético pensado para&nbsp;perdurar en&nbsp;el&nbsp;tiempo.</p>",
     "<p>PORTA é&nbsp;un&nbsp;proxecto integral de&nbsp;autor que&nbsp;abarca a&nbsp;conceptualización, edición e&nbsp;produción de&nbsp;principio a&nbsp;fin dun&nbsp;<em>mook</em> —un&nbsp;formato híbrido entre revista e&nbsp;libro— dedicado ao&nbsp;patrimonio de&nbsp;Baiona. Ante a&nbsp;saturación da&nbsp;comunicación turística masiva, a&nbsp;proposta aposta polo&nbsp;<em>slow journalism</em>, materializándose nunha peza editorial de&nbsp;coleccionista cun&nbsp;alto valor cultural e&nbsp;estético pensado para&nbsp;perdurar no&nbsp;tempo.</p>"),
    ("<h2>El&nbsp;reto</h2>", "<h2>O&nbsp;reto</h2>"),
    ("<p>El&nbsp;desafío radicó en&nbsp;asumir la&nbsp;autoría y&nbsp;dirección de&nbsp;arte 360º de&nbsp;una publicación compleja desde cero. El&nbsp;proyecto exigía ir&nbsp;mucho más allá de&nbsp;la&nbsp;maquetación clásica: implicaba romper con&nbsp;los códigos visuales genéricos del&nbsp;turismo convencional para&nbsp;construir un&nbsp;universo propio, encargándose simultáneamente de&nbsp;la&nbsp;estrategia de&nbsp;<em>branding</em>, la&nbsp;redacción del&nbsp;contenido escrito, la&nbsp;producción visual (fotografía e&nbsp;ilustración) y&nbsp;el&nbsp;diseño editorial de&nbsp;la&nbsp;obra.</p>",
     "<p>O&nbsp;desafío radicou en&nbsp;asumir a&nbsp;autoría e&nbsp;dirección de&nbsp;arte 360º dunha publicación complexa desde cero. O&nbsp;proxecto esixía ir&nbsp;moito máis alá da&nbsp;maquetación clásica: implicaba romper cos&nbsp;códigos visuais xenéricos do&nbsp;turismo convencional para&nbsp;construír un&nbsp;universo propio, encargándose simultaneamente da&nbsp;estratexia de&nbsp;<em>branding</em>, da&nbsp;redacción do&nbsp;contido escrito, da&nbsp;produción visual (fotografía e&nbsp;ilustración) e&nbsp;do&nbsp;deseño editorial da&nbsp;obra.</p>"),
    ("<h2>La&nbsp;solución</h2>", "<h2>A&nbsp;solución</h2>"),
    ("<p>Para&nbsp;resolver este proyecto global, el&nbsp;flujo de&nbsp;trabajo se&nbsp;estructuró en&nbsp;cuatro fases estratégicas:</p>",
     "<p>Para&nbsp;resolver este proxecto global, o&nbsp;fluxo de&nbsp;traballo estruturouse en&nbsp;catro fases estratéxicas:</p>"),
    ("<p><strong>Estrategia e&nbsp;Identidad de&nbsp;Marca:</strong> Creación del&nbsp;<em>branding</em> desde cero bajo el&nbsp;nombre de&nbsp;PORTA (puerta en&nbsp;gallego), evocando el&nbsp;concepto de&nbsp;puerto de&nbsp;arribada y&nbsp;fortaleza local. Se&nbsp;diseñó el&nbsp;imagotipo (arco de&nbsp;medio punto y&nbsp;vela latina), una paleta cromática basada en&nbsp;el&nbsp;paisaje atlántico y&nbsp;se&nbsp;desarrolló su&nbsp;Manual de&nbsp;Identidad de&nbsp;Marca normativo.</p>",
     "<p><strong>Estratexia e&nbsp;Identidade de&nbsp;Marca:</strong> Creación do&nbsp;<em>branding</em> desde cero baixo o&nbsp;nome de&nbsp;PORTA, evocando o&nbsp;concepto de&nbsp;porto de&nbsp;arribada e&nbsp;fortaleza local. Deseñouse o&nbsp;imagotipo (arco de&nbsp;medio punto e&nbsp;vela latina), unha paleta cromática baseada na&nbsp;paisaxe atlántica e&nbsp;desenvolveuse o&nbsp;seu Manual de&nbsp;Identidade de&nbsp;Marca normativo.</p>"),
    ("<p><strong>Dirección de&nbsp;Arte y&nbsp;Contenido:</strong> Redacción íntegra de&nbsp;los textos de&nbsp;la&nbsp;publicación y&nbsp;dirección creativa del&nbsp;universo visual. Esto abarcó la&nbsp;realización de&nbsp;la&nbsp;serie fotográfica editorial en&nbsp;localización y&nbsp;la&nbsp;creación de&nbsp;ilustraciones digitales a&nbsp;medida para&nbsp;enriquecer la&nbsp;narrativa.</p>",
     "<p><strong>Dirección de&nbsp;Arte e&nbsp;Contido:</strong> Redacción íntegra dos&nbsp;textos da&nbsp;publicación e&nbsp;dirección creativa do&nbsp;universo visual. Isto abarcou a&nbsp;realización da&nbsp;serie fotográfica editorial en&nbsp;localización e&nbsp;a&nbsp;creación de&nbsp;ilustracións dixitais á&nbsp;medida para&nbsp;enriquecer a&nbsp;narrativa.</p>"),
    ("<p><strong>Diseño y&nbsp;Estilo Editorial:</strong> Diseño global de&nbsp;la&nbsp;publicación de&nbsp;96&nbsp;páginas estructurada bajo una retícula modular estricta. Para&nbsp;asegurar la&nbsp;cohesión visual del&nbsp;formato, se&nbsp;desarrolló un&nbsp;Manual de&nbsp;Estilo Editorial exhaustivo que&nbsp;unifica las jerarquías tipográficas y&nbsp;los ritmos de&nbsp;lectura.</p>",
     "<p><strong>Deseño e&nbsp;Estilo Editorial:</strong> Deseño global da&nbsp;publicación de&nbsp;96&nbsp;páxinas estruturada baixo unha retícula modular estrita. Para&nbsp;asegurar a&nbsp;cohesión visual do&nbsp;formato, desenvolveuse un&nbsp;Manual de&nbsp;Estilo Editorial exhaustivo que&nbsp;unifica as&nbsp;xerarquías tipográficas e&nbsp;os ritmos de&nbsp;lectura.</p>"),
    ("<p><strong>Producción Técnica:</strong> Planteamiento y&nbsp;preparación de&nbsp;artes finales para&nbsp;su&nbsp;producción física como objeto premium: impresión <em>offset</em> en&nbsp;papel natural certificado FSC, encuadernación vista cosida a&nbsp;hilo, acabados con&nbsp;estampación en&nbsp;seco (golpe seco) del&nbsp;logotipo en&nbsp;portada y&nbsp;un&nbsp;estuche contenedor rígido.</p>",
     "<p><strong>Produción Técnica:</strong> Formulación e&nbsp;preparación de&nbsp;artes finais para&nbsp;a&nbsp;súa produción física como obxecto premium: impresión <em>offset</em> en&nbsp;papel natural certificado FSC, encadernación vista cosida a&nbsp;fío, acabados con&nbsp;estampación en&nbsp;seco (golpe seco) do&nbsp;logotipo na&nbsp;portada e&nbsp;un&nbsp;estoxo contedor ríxido.</p>"),
    ("<h2>Ficha técnica</h2>", "<h2>Ficha técnica</h2>"),
    ("<p><strong>Rol y&nbsp;Disciplinas:</strong> Dirección de&nbsp;arte integral, Redacción y&nbsp;Edición de&nbsp;contenido, Diseño editorial, Identidad de&nbsp;marca, Fotografía, Ilustración y&nbsp;Packaging.</p>",
     "<p><strong>Rol e&nbsp;Disciplinas:</strong> Dirección de&nbsp;arte integral, Redacción e&nbsp;Edición de&nbsp;contido, Deseño editorial, Identidade de&nbsp;marca, Fotografía, Ilustración e&nbsp;Packaging.</p>"),
    ("<p><strong>Entregables principales:</strong> <em>Mook</em> impreso (17 × 24&nbsp;cm, 96&nbsp;págs.), Manual de&nbsp;Identidad de&nbsp;Marca, Manual de&nbsp;Estilo Editorial y&nbsp;Estuche contenedor.</p>",
     "<p><strong>Entregables principais:</strong> <em>Mook</em> impreso (17 × 24&nbsp;cm, 96&nbsp;páxs.), Manual de&nbsp;Identidade de&nbsp;Marca, Manual de&nbsp;Estilo Editorial e&nbsp;Estoxo contedor.</p>"),
    ("<p><strong>Software utilizado:</strong></p>", "<p><strong>Software empregado:</strong></p>"),
    ("<p><strong>Adobe InDesign:</strong> Maquetación integral de&nbsp;la&nbsp;publicación, sistemas de&nbsp;retículas, estilos y&nbsp;preparación de&nbsp;artes finales para&nbsp;imprenta.</p>",
     "<p><strong>Adobe InDesign:</strong> Maquetación integral da&nbsp;publicación, sistemas de&nbsp;retículas, estilos e&nbsp;preparación de&nbsp;artes finais para&nbsp;imprenta.</p>"),
    ("<p><strong>Adobe Illustrator:</strong> Diseño, vectorización y&nbsp;normativización de&nbsp;la&nbsp;identidad de&nbsp;marca, grafismos y&nbsp;cartografía.</p>",
     "<p><strong>Adobe Illustrator:</strong> Deseño, vectorización e&nbsp;normativización da&nbsp;identidade de&nbsp;marca, grafismos e&nbsp;cartografía.</p>"),
    ("<p><strong>Adobe Photoshop:</strong> Tratamiento y&nbsp;revelado de&nbsp;la&nbsp;fotografía editorial, retoque digital y&nbsp;creación de&nbsp;mockups de&nbsp;presentación.</p>",
     "<p><strong>Adobe Photoshop:</strong> Tratamento e&nbsp;revelado da&nbsp;fotografía editorial, retoque dixital e&nbsp;creación de&nbsp;mockups de&nbsp;presentación.</p>"),
    ("<p><strong>Procreate:</strong> Creación, abocetado e&nbsp;ilustración digital de&nbsp;los recursos gráficos de&nbsp;la&nbsp;obra.</p>",
     "<p><strong>Procreate:</strong> Creación, bosquexo e&nbsp;ilustración dixital dos&nbsp;recursos gráficos da&nbsp;obra.</p>"),
    # flipbook
    ('Hojea el&nbsp;<em>mook</em></h2>', 'Folla o&nbsp;<em>mook</em></h2>'),
    ("<span>Ver manual de&nbsp;identidad corporativa</span>", "<span>Ver manual de&nbsp;identidade corporativa</span>"),
    ("<span>Ver manual de&nbsp;estilo editorial</span>", "<span>Ver manual de&nbsp;estilo editorial</span>"),
    ('aria-label="Página anterior"', 'aria-label="Páxina anterior"'),
    ('aria-label="Página siguiente"', 'aria-label="Páxina seguinte"'),
    ("Compra tu&nbsp;ejemplar aquí</p>", "Merca o&nbsp;teu exemplar aquí</p>"),
    ('class="button-circle">Ir a&nbsp;la&nbsp;tienda</a>', 'class="button-circle">Ir á&nbsp;tenda</a>'),
    # gallery
    ("Porta — identidad visual y&nbsp;editorial</p>", "Porta — identidade visual e&nbsp;editorial</p>"),
    ("Galería del&nbsp;proyecto</h2>", "Galería do&nbsp;proxecto</h2>"),
    ('alt="Cubierta y slipcase de Porta"', 'alt="Cuberta e slipcase de Porta"'),
    ('alt="Iconografía de Porta: barco, ola y arco"', 'alt="Iconografía de Porta: barco, onda e arco"'),
    ('alt="Maquetación editorial de Porta"', 'alt="Maquetación editorial de Porta"'),
    ('alt="Monasterio de Baiona"', 'alt="Mosteiro de Baiona"'),
    ('alt="Ilustración a acuarela de Porta"', 'alt="Ilustración á acuarela de Porta"'),
    ('alt="Monumento a la Virgen de la Roca"', 'alt="Monumento á Virxe da Rocha"'),
    ('alt="Flora del entorno de Baiona"', 'alt="Flora da contorna de Baiona"'),
    ('alt="Petroglifos del Val Miñor"', 'alt="Petróglifos do Val Miñor"'),
    ('alt="Patrimonio marítimo de Baiona"', 'alt="Patrimonio marítimo de Baiona"'),
    ('alt="Papelería corporativa de Porta"', 'alt="Papelería corporativa de Porta"'),
    ('alt="Colección editorial de Porta"', 'alt="Colección editorial de Porta"'),
    # cta + footer
    ('class="button-circle center">VER MÁS PROYECTOS</a>', 'class="button-circle center">VER MÁIS PROXECTOS</a>'),
    ("¿TIENES ALGÚN PROYECTO EN&nbsp;MENTE?</p>", "TES ALGÚN PROXECTO EN&nbsp;MENTE?</p>"),
    ("¡HABLEMOS!</p>", "FALEMOS!</p>"),
    ("<span>ENVIAR MENSAJE</span>", "<span>ENVIAR MENSAXE</span>"),
    ("Siempre es un placer conectar con&nbsp;nuevos proyectos y&nbsp;personas.</p>",
     "Sempre é un pracer conectar con&nbsp;novos proxectos e&nbsp;persoas.</p>"),
    ("<strong>Aldara Álvarez</strong> — Diseñadora Gráfica.<br>Graduada en Diseño por&nbsp;la&nbsp;UCM y Máster en Diseño Gráfico Digital por&nbsp;la&nbsp;UNIR. Especializada en soluciones visuales conceptuales, diseño editorial e identidad corporativa.",
     "<strong>Aldara Álvarez</strong> — Deseñadora Gráfica.<br>Graduada en Deseño pola UCM e Máster en Deseño Gráfico Dixital pola UNIR. Especializada en solucións visuais conceptuais, deseño editorial e identidade corporativa."),
    ("<h3>Secciones</h3>", "<h3>Seccións</h3>"),
    ('<a href="../projects">Proyectos</a>', '<a href="../projects">Proxectos</a>'),
    ('<a href="../about">Sobre Mí</a>', '<a href="../about">Sobre Min</a>'),
    ("<h3>Proyectos Destacados</h3>", "<h3>Proxectos Destacados</h3>"),
    ("Todos los derechos reservados.", "Todos os dereitos reservados."),
    ('alt="Página ', 'alt="Páxina '),
]

build("en", "en/projects/porta.html", EN)
build("gl", "gl/projects/porta.html", GL)
