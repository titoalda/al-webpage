#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build i18n: genera en/index.html y gl/index.html desde index.html (ES).

La home en español es la ÚNICA fuente de verdad (layout, CSS, JS).
Este script le aplica, por idioma:
  1. Ajuste de rutas (static/, selector de idioma, canonical, og:url...)
  2. Una tabla de traducciones de cadenas exactas (visible + meta + JS)

Uso:  python3 tools/build_i18n.py          (desde la raíz del repo)

Si cambias el diseño o el texto en index.html, vuelve a ejecutarlo y las
otras dos lenguas se regeneran a la vez. Si añades texto nuevo en ES,
añade su traducción a las tablas EN/GL de abajo (el script avisa de
cualquier cadena de la tabla que ya no encuentre en la fuente).
"""
import os, sys, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")

# --------------------------------------------------------------------------
# Cableado por idioma (rutas, selector de idioma, URLs canónicas)
# --------------------------------------------------------------------------

def wire(s, lang):
    # assets un nivel arriba
    s = s.replace('href="static/', 'href="../static/')
    s = s.replace('src="static/', 'src="../static/')
    # URLs canónicas / sociales propias del idioma
    s = s.replace('<link rel="canonical" href="https://aldaraalvarez.es/">',
                  f'<link rel="canonical" href="https://aldaraalvarez.es/{lang}/">')
    s = s.replace('<meta property="og:url" content="https://aldaraalvarez.es/">',
                  f'<meta property="og:url" content="https://aldaraalvarez.es/{lang}/">')
    s = s.replace('<meta name="twitter:url" content="https://aldaraalvarez.es/">',
                  f'<meta name="twitter:url" content="https://aldaraalvarez.es/{lang}/">')
    s = s.replace('"url": "https://aldaraalvarez.es/",',
                  f'"url": "https://aldaraalvarez.es/{lang}/",')
    s = s.replace('<html lang="es">', f'<html lang="{lang}">')

    # selector de idioma del dock (nav): ES(./ activo), EN(en/), GAL(gl/)
    s = s.replace('<a href="./" class="lang-option active">ES</a>',
                  '<a href="../" class="lang-option">ES</a>')
    if lang == "en":
        # 1ª aparición (nav) pasa a activa; 2ª (switch externo) pasa a ES
        s = s.replace('<a href="en/" class="lang-option">EN</a>',
                      '<a href="./" class="lang-option active">EN</a>', 1)
        s = s.replace('<a href="en/" class="lang-option">EN</a>',
                      '<a href="../" class="lang-option">ES</a>', 1)
        s = s.replace('<a href="gl/" class="lang-option">GAL</a>',
                      '<a href="../gl/" class="lang-option">GAL</a>')
        s = s.replace('aria-expanded="false">ES</button>', 'aria-expanded="false">EN</button>')
    else:  # gl
        s = s.replace('<a href="en/" class="lang-option">EN</a>',
                      '<a href="../en/" class="lang-option">EN</a>', 1)
        s = s.replace('<a href="en/" class="lang-option">EN</a>',
                      '<a href="../" class="lang-option">ES</a>', 1)
        s = s.replace('<a href="gl/" class="lang-option">GAL</a>',
                      '<a href="./" class="lang-option active">GAL</a>', 1)
        s = s.replace('<a href="gl/" class="lang-option">GAL</a>',
                      '<a href="../en/" class="lang-option">EN</a>', 1)
        s = s.replace('aria-expanded="false">ES</button>', 'aria-expanded="false">GAL</button>')
    return s

# --------------------------------------------------------------------------
# Tablas de traducción: (cadena exacta en ES) -> (traducción)
# --------------------------------------------------------------------------

EN = [
    # head
    ("<title>Aldara Álvarez | Diseñadora</title>",
     "<title>Aldara Álvarez | Graphic, Editorial and Brand Designer</title>"),
    ('content="Portafolio de diseño de Aldara Álvarez, diseñadora gráfica. Especializada en diseño editorial e identidad de marca, con proyectos de dirección de arte y maquetación."',
     'content="Design portfolio of Aldara Álvarez, graphic designer in Galicia. Specialized in editorial design, brand identity and art direction."'),
    ('content="Aldara Álvarez | Diseñadora Gráfica, Editorial y de Marca"',
     'content="Aldara Álvarez | Graphic, Editorial and Brand Designer"'),
    ('content="Explora el portafolio de diseño de Aldara Álvarez. Soluciones visuales en diseño editorial, identidad de marca y dirección de arte."',
     'content="Explore the design portfolio of Aldara Álvarez. Visual solutions in editorial design, brand identity and art direction."'),
    ('"jobTitle": "Diseñadora Gráfica"', '"jobTitle": "Graphic Designer"'),
    ('"description": "Diseñadora gráfica especializada en identidad de marca, diseño editorial y dirección de arte."',
     '"description": "Graphic designer specialized in brand identity, editorial design and art direction."'),
    ('"knowsAbout": ["Diseño Editorial", "Identidad de Marca", "Diseño de Packaging", "Modelado 3D", "Diseño UX/UI"]',
     '"knowsAbout": ["Editorial Design", "Brand Identity", "Packaging Design", "3D Modeling", "UX/UI Design"]'),
    # header / dock
    ('data-label="Proyectos"', 'data-label="Projects"'),
    ('class="dock-tooltip">Proyectos</span>', 'class="dock-tooltip">Projects</span>'),
    ('data-label="Sobre Mí"', 'data-label="About Me"'),
    ('class="dock-tooltip">Sobre Mí</span>', 'class="dock-tooltip">About Me</span>'),
    ('data-label="Contacto"', 'data-label="Contact"'),
    ('class="dock-tooltip">Contacto</span>', 'class="dock-tooltip">Contact</span>'),
    ('data-label="Idioma"', 'data-label="Language"'),
    ('class="dock-tooltip">Idioma</span>', 'class="dock-tooltip">Language</span>'),
    # hero (marcado + typewriter JS: "designer" tiene 8 letras, no 10)
    ('<span id="hero-subtitle" class="hero-subtitle"><strong>diseñadora</strong><span class="hero-pipe"> | </span>especialista en identidad de marca y diseño editorial</span>',
     '<span id="hero-subtitle" class="hero-subtitle"><strong>designer</strong><span class="hero-pipe"> | </span>specialist in brand identity and editorial design</span>'),
    ('const text = "diseñadora | especialista en identidad de marca y diseño editorial";',
     'const text = "designer | specialist in brand identity and editorial design";'),
    ("subtitleEl.innerHTML = '<strong>diseñadora</strong><span class=\"hero-pipe\"> | </span>especialista en identidad de marca y diseño editorial';",
     "subtitleEl.innerHTML = '<strong>designer</strong><span class=\"hero-pipe\"> | </span>specialist in brand identity and editorial design';"),
    ("if (i < 10) {", "if (i < 8) {"),
    ('subtitleEl.innerHTML = `<strong>diseñadora</strong><span class="hero-pipe"> | </span>${text.substring(13, i + 1)}`;',
     'subtitleEl.innerHTML = `<strong>designer</strong><span class="hero-pipe"> | </span>${text.substring(11, i + 1)}`;'),
    # carrusel Porta
    ('MI<span class="hint-inline-anchor" id="hint-inline-anchor"></span> ÚLTIMO <span id="hint-right-anchor">PROYECTO</span>',
     'MY<span class="hint-inline-anchor" id="hint-inline-anchor"></span> LATEST <span id="hint-right-anchor">PROJECT</span>'),
    ("Un vistazo a&nbsp;mi última aventura creativa: la&nbsp;creación de&nbsp;la&nbsp;marca y&nbsp;el diseño integral de&nbsp;un <em>mook</em>.",
     "A glimpse of my latest creative adventure: the creation of a brand and the full design of a <em>mook</em>."),
    ("<span>Ver proyecto</span>", "<span>View project</span>"),
    ("Desliza para explorar", "Drag to explore"),
    ('alt="Porta, página interior ', 'alt="Porta, inner page '),
    # secciones de proyectos
    ('<h2 class="section-title">OTROS PROYECTOS</h2>', '<h2 class="section-title">OTHER PROJECTS</h2>'),
    ('<h2 class="section-title">PROYECTOS</h2>', '<h2 class="section-title">PROJECTS</h2>'),
    ("Aquí te dejo una selección de&nbsp;proyectos que&nbsp;espero que&nbsp;te transmitan mi dedicación y&nbsp;pasión por&nbsp;el diseño.",
     "Here is a selection of projects that I hope will convey my dedication and passion for design."),
    ("<span>Ver más proyectos</span>", "<span>View more projects</span>"),
    ('alt="Proyecto ', 'alt="Project '),
    ("DISEÑO DE CUBIERTA E ILUSTRACIÓN", "COVER DESIGN AND ILLUSTRATION"),
    ("DISEÑO EDITORIAL", "EDITORIAL DESIGN"),
    ("DISEÑO DE SEÑALÉTICA", "SIGNAGE DESIGN"),
    ("DISEÑO DE IDENTIDAD CORPORATIVA Y <em>PACKAGING</em>", "CORPORATE IDENTITY AND <em>PACKAGING</em> DESIGN"),
    ("DISEÑO DE MODELO 3D", "3D MODEL DESIGN"),
    ("DISEÑO DE <em>LETTERING</em>", "<em>LETTERING</em> DESIGN"),
    ("DISEÑO DE CUBIERTA", "COVER DESIGN"),
    ('aria-label="Anterior"', 'aria-label="Previous"'),
    ('aria-label="Siguiente"', 'aria-label="Next"'),
    # especialidades
    ("<h2>Especialidades</h2>", "<h2>Specialties</h2>"),
    ("<h3>Diseño Editorial</h3>", "<h3>Editorial Design</h3>"),
    ("<p>Maquetación de&nbsp;publicaciones, dirección tipográfica y&nbsp;diseño de&nbsp;libros, revistas y&nbsp;catálogos con&nbsp;criterio y&nbsp;detalle.</p>",
     "<p>Layout of publications, typographic direction and design of books, magazines and catalogs with criteria and detail.</p>"),
    ("<h3>Identidad de&nbsp;Marca</h3>", "<h3>Brand Identity</h3>"),
    ("<p>Creación de&nbsp;identidades visuales coherentes y&nbsp;duraderas: logotipo, paleta, tipografía y&nbsp;sistema de&nbsp;marca completo.</p>",
     "<p>Creation of coherent and durable visual identities: logo, palette, typography and complete brand system.</p>"),
    ("<h3>Diseño UX·UI</h3>", "<h3>UX·UI Design</h3>"),
    ("<p>Interfaces digitales centradas en&nbsp;el usuario: wireframes, prototipos y&nbsp;diseño visual de&nbsp;productos web y&nbsp;app.</p>",
     "<p>User-centered digital interfaces: wireframes, prototypes and visual design of web and app products.</p>"),
    ("Explorar proyectos", "Explore projects"),
    # contacto
    ("<h2>Contacto</h2>", "<h2>Contact</h2>"),
    ("¿Tienes algún proyecto en&nbsp;mente o&nbsp;quieres preguntarme algo?",
     "Do you have a project in mind or want to ask me something?"),
    ("Hablemos de&nbsp;forma segura.", "Let's talk securely."),
    ("ENVIANDO MENSAJE", "SENDING MESSAGE"),
    ("Estableciendo conexión segura...", "Establishing secure connection..."),
    ("¡Gracias!", "Thank you!"),
    ("Te contactaré en&nbsp;breve.", "I will contact you shortly."),
    (">Dejar vacío<", ">Leave empty<"),
    ('<label for="name">Nombre</label>', '<label for="name">Name</label>'),
    ('placeholder="¿Cómo te llamas?"', 'placeholder="What is your name?"'),
    ('placeholder="¿A qué correo te respondo?"', 'placeholder="Which email address should I reply to?"'),
    ('<label for="message">Mensaje</label>', '<label for="message">Message</label>'),
    ('placeholder="Cuéntame qué tienes en mente, qué necesitas diseñar y nos ponemos a ello..."',
     'placeholder="Tell me what you have in mind, what you need to design, and let\'s get to work..."'),
    ("<span>ENVIAR MENSAJE</span>", "<span>SEND MESSAGE</span>"),
    # footer
    ("<strong>Aldara Álvarez</strong> — Diseñadora Gráfica.<br>Graduada en Diseño por&nbsp;la&nbsp;UCM y Máster en Diseño Gráfico Digital por&nbsp;la&nbsp;UNIR. Especializada en soluciones visuales conceptuales, diseño editorial e identidad corporativa.",
     "<strong>Aldara Álvarez</strong> — Graphic Designer.<br>Graduate in Design from UCM with a Master's in Digital Graphic Design from UNIR. Specialized in conceptual visual solutions, editorial design and corporate identity."),
    ("<h3>Secciones</h3>", "<h3>Sections</h3>"),
    ('<a href="projects">Proyectos</a>', '<a href="projects">Projects</a>'),
    ('<a href="about">Sobre Mí</a>', '<a href="about">About Me</a>'),
    ('<a href="contact">Contacto</a>', '<a href="contact">Contact</a>'),
    ("<h3>Proyectos Destacados</h3>", "<h3>Featured Projects</h3>"),
    ("<h3>Contacto</h3>", "<h3>Contact</h3>"),
    ("Todos los derechos reservados.", "All rights reserved."),
    ('class="footer-legal-link">Aviso Legal</a>', 'class="footer-legal-link">Legal Notice</a>'),
]

GL = [
    # head
    ("<title>Aldara Álvarez | Diseñadora</title>",
     "<title>Aldara Álvarez | Deseñadora Gráfica, Editorial e de Marca</title>"),
    ('content="Portafolio de diseño de Aldara Álvarez, diseñadora gráfica. Especializada en diseño editorial e identidad de marca, con proyectos de dirección de arte y maquetación."',
     'content="Portafolio de deseño de Aldara Álvarez, deseñadora gráfica en Galicia. Especializada en deseño editorial, identidade de marca e dirección de arte."'),
    ('content="Aldara Álvarez | Diseñadora Gráfica, Editorial y de Marca"',
     'content="Aldara Álvarez | Deseñadora Gráfica, Editorial e de Marca"'),
    ('content="Explora el portafolio de diseño de Aldara Álvarez. Soluciones visuales en diseño editorial, identidad de marca y dirección de arte."',
     'content="Explora o portafolio de deseño de Aldara Álvarez. Solucións visuais en deseño editorial, identidade de marca e dirección de arte."'),
    ('"jobTitle": "Diseñadora Gráfica"', '"jobTitle": "Deseñadora Gráfica"'),
    ('"description": "Diseñadora gráfica especializada en identidad de marca, diseño editorial y dirección de arte."',
     '"description": "Deseñadora gráfica especializada en identidade de marca, deseño editorial e dirección de arte."'),
    ('"knowsAbout": ["Diseño Editorial", "Identidad de Marca", "Diseño de Packaging", "Modelado 3D", "Diseño UX/UI"]',
     '"knowsAbout": ["Deseño Editorial", "Identidade de Marca", "Deseño de Packaging", "Modelado 3D", "Deseño UX/UI"]'),
    # header / dock
    ('data-label="Proyectos"', 'data-label="Proxectos"'),
    ('class="dock-tooltip">Proyectos</span>', 'class="dock-tooltip">Proxectos</span>'),
    ('data-label="Sobre Mí"', 'data-label="Sobre Min"'),
    ('class="dock-tooltip">Sobre Mí</span>', 'class="dock-tooltip">Sobre Min</span>'),
    # hero ("deseñadora" tiene 10 letras: mismos índices que ES en el JS)
    ('<span id="hero-subtitle" class="hero-subtitle"><strong>diseñadora</strong><span class="hero-pipe"> | </span>especialista en identidad de marca y diseño editorial</span>',
     '<span id="hero-subtitle" class="hero-subtitle"><strong>deseñadora</strong><span class="hero-pipe"> | </span>especialista en identidade de marca e deseño editorial</span>'),
    ('const text = "diseñadora | especialista en identidad de marca y diseño editorial";',
     'const text = "deseñadora | especialista en identidade de marca e deseño editorial";'),
    ("subtitleEl.innerHTML = '<strong>diseñadora</strong><span class=\"hero-pipe\"> | </span>especialista en identidad de marca y diseño editorial';",
     "subtitleEl.innerHTML = '<strong>deseñadora</strong><span class=\"hero-pipe\"> | </span>especialista en identidade de marca e deseño editorial';"),
    ('subtitleEl.innerHTML = `<strong>diseñadora</strong><span class="hero-pipe"> | </span>${text.substring(13, i + 1)}`;',
     'subtitleEl.innerHTML = `<strong>deseñadora</strong><span class="hero-pipe"> | </span>${text.substring(13, i + 1)}`;'),
    # carrusel Porta
    ('MI<span class="hint-inline-anchor" id="hint-inline-anchor"></span> ÚLTIMO <span id="hint-right-anchor">PROYECTO</span>',
     'O<span class="hint-inline-anchor" id="hint-inline-anchor"></span> MEU ÚLTIMO <span id="hint-right-anchor">PROXECTO</span>'),
    ("Un vistazo a&nbsp;mi última aventura creativa: la&nbsp;creación de&nbsp;la&nbsp;marca y&nbsp;el diseño integral de&nbsp;un <em>mook</em>.",
     "Unha ollada á&nbsp;miña última aventura creativa: a&nbsp;creación da&nbsp;marca e&nbsp;o deseño integral dun <em>mook</em>."),
    ("<span>Ver proyecto</span>", "<span>Ver proxecto</span>"),
    ('alt="Porta, página interior ', 'alt="Porta, páxina interior '),
    # secciones de proyectos
    ('<h2 class="section-title">OTROS PROYECTOS</h2>', '<h2 class="section-title">OUTROS PROXECTOS</h2>'),
    ('<h2 class="section-title">PROYECTOS</h2>', '<h2 class="section-title">PROXECTOS</h2>'),
    ("Aquí te dejo una selección de&nbsp;proyectos que&nbsp;espero que&nbsp;te transmitan mi dedicación y&nbsp;pasión por&nbsp;el diseño.",
     "Aquí che deixo unha selección de&nbsp;proxectos que&nbsp;espero que&nbsp;che transmitan a&nbsp;miña dedicación e&nbsp;paixón polo&nbsp;deseño."),
    ("<span>Ver más proyectos</span>", "<span>Ver máis proxectos</span>"),
    ('alt="Proyecto ', 'alt="Proxecto '),
    ("DISEÑO DE CUBIERTA E ILUSTRACIÓN", "DESEÑO DE CUBERTA E ILUSTRACIÓN"),
    ("DISEÑO EDITORIAL", "DESEÑO EDITORIAL"),
    ("DISEÑO DE SEÑALÉTICA", "DESEÑO DE SINALÉTICA"),
    ("DISEÑO DE IDENTIDAD CORPORATIVA Y <em>PACKAGING</em>", "DESEÑO DE IDENTIDADE CORPORATIVA E <em>PACKAGING</em>"),
    ("DISEÑO DE MODELO 3D", "DESEÑO DE MODELO 3D"),
    ("DISEÑO DE <em>LETTERING</em>", "DESEÑO DE <em>LETTERING</em>"),
    ("DISEÑO DE CUBIERTA", "DESEÑO DE CUBERTA"),
    ('aria-label="Siguiente"', 'aria-label="Seguinte"'),
    # especialidades
    ("<h3>Diseño Editorial</h3>", "<h3>Deseño Editorial</h3>"),
    ("<p>Maquetación de&nbsp;publicaciones, dirección tipográfica y&nbsp;diseño de&nbsp;libros, revistas y&nbsp;catálogos con&nbsp;criterio y&nbsp;detalle.</p>",
     "<p>Maquetación de&nbsp;publicacións, dirección tipográfica e&nbsp;deseño de&nbsp;libros, revistas e&nbsp;catálogos con&nbsp;criterio e&nbsp;detalle.</p>"),
    ("<h3>Identidad de&nbsp;Marca</h3>", "<h3>Identidade de&nbsp;Marca</h3>"),
    ("<p>Creación de&nbsp;identidades visuales coherentes y&nbsp;duraderas: logotipo, paleta, tipografía y&nbsp;sistema de&nbsp;marca completo.</p>",
     "<p>Creación de&nbsp;identidades visuais coherentes e&nbsp;duradeiras: logotipo, paleta, tipografía e&nbsp;sistema de&nbsp;marca completo.</p>"),
    ("<h3>Diseño UX·UI</h3>", "<h3>Deseño UX·UI</h3>"),
    ("<p>Interfaces digitales centradas en&nbsp;el usuario: wireframes, prototipos y&nbsp;diseño visual de&nbsp;productos web y&nbsp;app.</p>",
     "<p>Interfaces dixitais centradas no&nbsp;usuario: wireframes, prototipos e&nbsp;deseño visual de&nbsp;produtos web e&nbsp;app.</p>"),
    ("Explorar proyectos", "Explorar proxectos"),
    # contacto
    ("¿Tienes algún proyecto en&nbsp;mente o&nbsp;quieres preguntarme algo?",
     "Tes algún proxecto en&nbsp;mente ou&nbsp;queres preguntarme algo?"),
    ("Hablemos de&nbsp;forma segura.", "Falemos de&nbsp;forma segura."),
    ("ENVIANDO MENSAJE", "ENVIANDO MENSAXE"),
    ("Estableciendo conexión segura...", "Establecendo conexión segura..."),
    ("¡Gracias!", "Grazas!"),
    ("Te contactaré en&nbsp;breve.", "Contactarei contigo en&nbsp;breve."),
    (">Dejar vacío<", ">Deixar baleiro<"),
    ('<label for="name">Nombre</label>', '<label for="name">Nome</label>'),
    ('placeholder="¿Cómo te llamas?"', 'placeholder="Cómo te chamas?"'),
    ('placeholder="¿A qué correo te respondo?"', 'placeholder="A qué correo che respondo?"'),
    ('<label for="message">Mensaje</label>', '<label for="message">Mensaxe</label>'),
    ('placeholder="Cuéntame qué tienes en mente, qué necesitas diseñar y nos ponemos a ello..."',
     'placeholder="Cóntame qué tes en mente, qué necesitas deseñar e poñémonos a iso..."'),
    ("<span>ENVIAR MENSAJE</span>", "<span>ENVIAR MENSAXE</span>"),
    # footer
    ("<strong>Aldara Álvarez</strong> — Diseñadora Gráfica.<br>Graduada en Diseño por&nbsp;la&nbsp;UCM y Máster en Diseño Gráfico Digital por&nbsp;la&nbsp;UNIR. Especializada en soluciones visuales conceptuales, diseño editorial e identidad corporativa.",
     "<strong>Aldara Álvarez</strong> — Deseñadora Gráfica.<br>Graduada en Deseño pola UCM e Máster en Deseño Gráfico Dixital pola UNIR. Especializada en solucións visuais conceptuais, deseño editorial e identidade corporativa."),
    ("<h3>Secciones</h3>", "<h3>Seccións</h3>"),
    ('<a href="projects">Proyectos</a>', '<a href="projects">Proxectos</a>'),
    ('<a href="about">Sobre Mí</a>', '<a href="about">Sobre Min</a>'),
    ("<h3>Proyectos Destacados</h3>", "<h3>Proxectos Destacados</h3>"),
    ("Todos los derechos reservados.", "Todos os dereitos reservados."),
]

# --------------------------------------------------------------------------

def build(lang, table):
    s = open(SRC, encoding="utf-8").read()
    s = wire(s, lang)
    missing = 0
    for a, b in table:
        if a not in s:
            print(f"  [AVISO {lang}] cadena no encontrada en la fuente: {a[:70]}...")
            missing += 1
        s = s.replace(a, b)
    out = os.path.join(ROOT, lang, "index.html")
    open(out, "w", encoding="utf-8").write(s)
    print(f"  {out} ({len(s)} bytes){' — ' + str(missing) + ' avisos' if missing else ''}")

if __name__ == "__main__":
    print("Generando desde index.html (ES):")
    build("en", EN)
    build("gl", GL)
