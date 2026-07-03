document.addEventListener("DOMContentLoaded", function() {
    const dock = document.querySelector(".magnification-dock");
    if (!dock) return;

    const items = dock.querySelectorAll(".dock-item");
    const baseSize = 36;       // Base item size
    const magnification = 46; // Max magnification size
    const distance = 100;     // Magnification range radius

    // Spring constants (mass = 0.1, stiffness = 90, damping = 15 for smoother interaction)
    const mass = 0.1;
    const stiffness = 90;
    const damping = 15;

    // Track spring state for each item
    const states = Array.from(items).map(item => ({
        element: item,
        size: baseSize,
        targetSize: baseSize,
        velocity: 0,
        x: 0 // Center X coordinate of item
    }));

    let mouseX = Infinity;
    let isHovered = false;
    let isLangOpen = false;
    let langTimeout = null;

    // Listen to mouse events on dock
    dock.addEventListener("mousemove", (e) => {
        isHovered = true;
        mouseX = e.pageX;
    });

    dock.addEventListener("mouseleave", () => {
        isHovered = false;
        mouseX = Infinity;
    });

    // Timing tracking for delta time
    let lastTime = performance.now();

    function animate(now) {
        let dt = (now - lastTime) / 1000; // Convert to seconds
        lastTime = now;

        // Cap dt to avoid spring explosions on tab switch
        if (dt > 0.1) dt = 0.1;
        if (dt <= 0) dt = 0.016; // Fallback to 60fps frame time if 0

        // 1. Recalculate item positions relative to document
        states.forEach(state => {
            const rect = state.element.getBoundingClientRect();
            state.x = rect.left + window.scrollX + rect.width / 2;
        });

        // 2. Solve spring physics for each item with stable sub-stepping
        states.forEach(state => {
            // Freeze sizes if language menu is open to prevent cursor shifting
            if (isLangOpen) {
                state.velocity = 0;
                state.element.style.width = `${state.size}px`;
                state.element.style.height = `${state.size}px`;
                return;
            }

            let target = baseSize;

            if (isHovered && mouseX !== Infinity) {
                const dist = Math.abs(mouseX - state.x);
                if (dist < distance) {
                    const factor = 1 - (dist / distance); // 0 to 1
                    target = baseSize + (magnification - baseSize) * factor;
                }
            }

            state.targetSize = target;

            // Sub-stepping loop (4ms steps) for mathematical stability under any framerate
            let accum = dt;
            const step = 0.004;
            
            while (accum > 0) {
                const substep = Math.min(accum, step);
                
                const displacement = state.size - state.targetSize;
                const springForce = -stiffness * displacement;
                const dampingForce = -damping * state.velocity;
                const acceleration = (springForce + dampingForce) / mass;

                state.velocity += acceleration * substep;
                state.size += state.velocity * substep;
                
                accum -= substep;
            }

            // Clamping boundaries to prevent any possible NaN or size explosion
            if (isNaN(state.size) || state.size < baseSize) {
                state.size = baseSize;
                state.velocity = 0;
            } else if (state.size > magnification * 1.5) {
                state.size = magnification;
                state.velocity = 0;
            }

            // Apply size styles
            state.element.style.width = `${state.size}px`;
            state.element.style.height = `${state.size}px`;
        });

        // Loop animation
        requestAnimationFrame(animate);
    }

    const langSelector = dock.querySelector(".lang-selector");
    const langDropdown = dock.querySelector(".lang-dropdown");
    if (langSelector && langDropdown) {
        const openLang = () => {
            if (langTimeout) {
                clearTimeout(langTimeout);
                langTimeout = null;
            }
            isLangOpen = true;
            langSelector.classList.add("is-open");
            
            // Dynamically adjust dropdown direction based on screen space
            const rect = langSelector.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            if (spaceBelow < 150) {
                langDropdown.classList.add("open-up");
                langDropdown.classList.remove("open-down");
            } else {
                langDropdown.classList.add("open-down");
                langDropdown.classList.remove("open-up");
            }
        };

        const closeLang = () => {
            if (langTimeout) clearTimeout(langTimeout);
            langTimeout = setTimeout(() => {
                isLangOpen = false;
                langSelector.classList.remove("is-open");
            }, 300); // 300ms debounce delay before closing
        };

        // Hover listeners
        langSelector.addEventListener("mouseenter", openLang);
        langSelector.addEventListener("mouseleave", closeLang);

        // Keyboard/focus listeners
        langSelector.addEventListener("focusin", openLang);
        langSelector.addEventListener("focusout", (e) => {
            if (!langSelector.contains(e.relatedTarget)) {
                closeLang();
            }
        });

        // Touch/click listener
        langSelector.addEventListener("click", (e) => {
            if (e.target.closest(".lang-option")) return;
            
            e.preventDefault();
            e.stopPropagation();
            if (isLangOpen) {
                isLangOpen = false;
                langSelector.classList.remove("is-open");
            } else {
                openLang();
            }
        });

        // Click outside to close
        document.addEventListener("click", (e) => {
            if (!langSelector.contains(e.target)) {
                isLangOpen = false;
                langSelector.classList.remove("is-open");
            }
        });

        // Escape key to close
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                isLangOpen = false;
                langSelector.classList.remove("is-open");
            }
        });
    }

    // Start requestAnimationFrame loop
    requestAnimationFrame(animate);
});

// --- External language switch (desktop/web): lives outside the dock,
// to its right. Independent of the dock's spring physics. ---
document.addEventListener("DOMContentLoaded", function() {
    const extSwitch = document.querySelector(".lang-switch-external");
    if (!extSwitch) return;

    const extDropdown = extSwitch.querySelector(".lang-dropdown");
    const extToggle = extSwitch.querySelector(".lang-switch-toggle");
    if (!extDropdown) return;

    let isOpen = false;
    let closeTimeout = null;

    const setExpanded = (value) => {
        if (extToggle) extToggle.setAttribute("aria-expanded", value ? "true" : "false");
    };

    const openExt = () => {
        if (closeTimeout) {
            clearTimeout(closeTimeout);
            closeTimeout = null;
        }
        isOpen = true;
        extSwitch.classList.add("is-open");
        setExpanded(true);

        const rect = extSwitch.getBoundingClientRect();
        const spaceBelow = window.innerHeight - rect.bottom;
        if (spaceBelow < 150) {
            extDropdown.classList.add("open-up");
            extDropdown.classList.remove("open-down");
        } else {
            extDropdown.classList.add("open-down");
            extDropdown.classList.remove("open-up");
        }
    };

    const closeExt = () => {
        if (closeTimeout) clearTimeout(closeTimeout);
        closeTimeout = setTimeout(() => {
            isOpen = false;
            extSwitch.classList.remove("is-open");
            setExpanded(false);
        }, 300);
    };

    extSwitch.addEventListener("mouseenter", openExt);
    extSwitch.addEventListener("mouseleave", closeExt);

    extSwitch.addEventListener("focusin", openExt);
    extSwitch.addEventListener("focusout", (e) => {
        if (!extSwitch.contains(e.relatedTarget)) closeExt();
    });

    extSwitch.addEventListener("click", (e) => {
        if (e.target.closest(".lang-option")) return;
        e.preventDefault();
        e.stopPropagation();
        if (isOpen) {
            isOpen = false;
            extSwitch.classList.remove("is-open");
            setExpanded(false);
        } else {
            openExt();
        }
    });

    document.addEventListener("click", (e) => {
        if (!extSwitch.contains(e.target)) {
            isOpen = false;
            extSwitch.classList.remove("is-open");
            setExpanded(false);
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") {
            isOpen = false;
            extSwitch.classList.remove("is-open");
            setExpanded(false);
        }
    });
});


// --- Scroll Reveal Intersection Observer ---
document.addEventListener("DOMContentLoaded", function() {
    const revealTargets = document.querySelectorAll("img, .philosophy-col, .service-card, .footer-col, .project-stack-card");
    
    const observerOptions = {
        threshold: 0.05,
        rootMargin: "0px 0px -30px 0px"
    };
    
    const revealObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("revealed");
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    revealTargets.forEach(target => {
        target.classList.add("reveal-on-scroll");
        revealObserver.observe(target);
    });
});

// --- Mobile Hamburger Menu Handler ---
document.addEventListener("DOMContentLoaded", function() {
    const isMobile = window.innerWidth <= 768;
    const isTabletTouch = window.innerWidth <= 1024 && window.matchMedia('(pointer: coarse)').matches;
    if (!isMobile && !isTabletTouch) return; // Solo móvil o tablet táctil

    const header = document.querySelector("header");
    if (!header) return;

    // Move dock to body level so position:fixed is relative to viewport
    // (avoids backdrop-filter on header creating a new containing block)
    const dock = document.querySelector(".magnification-dock");
    if (dock) document.body.appendChild(dock);

    // Create overlay
    const overlay = document.createElement("div");
    overlay.className = "mobile-menu-overlay";
    document.body.appendChild(overlay);

    // Create hamburger button
    const hamburger = document.createElement("button");
    hamburger.className = "hamburger-menu";
    hamburger.id = "hamburger-btn";
    hamburger.setAttribute("aria-label", "Abrir menú");
    hamburger.innerHTML = "<span></span><span></span><span></span>";
    
    header.appendChild(hamburger);

    hamburger.addEventListener("click", function(e) {
        e.stopPropagation();
        const isOpen = hamburger.classList.toggle("open");
        header.classList.toggle("nav-active", isOpen);
        overlay.classList.toggle("active", isOpen);
        if (dock) {
            dock.classList.toggle("nav-active", isOpen);
            if (isOpen) {
                document.body.style.overflow = "hidden";
            } else {
                document.body.style.overflow = "";
            }
        }
    });

    // Close menu when clicking on the overlay
    overlay.addEventListener("click", function() {
        hamburger.classList.remove("open");
        header.classList.remove("nav-active");
        overlay.classList.remove("active");
        if (dock) dock.classList.remove("nav-active");
        document.body.style.overflow = "";
    });

    // Close menu when clicking a dock item
    const dockItems = document.querySelectorAll(".magnification-dock .dock-item");
    dockItems.forEach(item => {
        if (item.classList.contains("lang-selector")) return;
        item.addEventListener("click", () => {
            hamburger.classList.remove("open");
            header.classList.remove("nav-active");
            overlay.classList.remove("active");
            if (dock) dock.classList.remove("nav-active");
            document.body.style.overflow = "";
        });
    });
});


