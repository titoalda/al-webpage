document.addEventListener("DOMContentLoaded", function() {
    const dock = document.querySelector(".magnification-dock");
    if (!dock) return;

    const items = dock.querySelectorAll(".dock-item");
    const baseSize = 36;       // Base item size
    const magnification = 46; // Max magnification size
    const distance = 100;     // Magnification range radius

    // Spring constants matching Framer Motion config (mass = 0.1, stiffness = 150, damping = 12)
    const mass = 0.1;
    const stiffness = 150;
    const damping = 12;

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

    // Start requestAnimationFrame loop
    requestAnimationFrame(animate);
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
    if (window.innerWidth > 768) return; // Only execute on mobile screens

    const header = document.querySelector("header");
    if (!header) return;

    // Move dock to body level so position:fixed is relative to viewport
    // (avoids backdrop-filter on header creating a new containing block)
    const dock = document.querySelector(".magnification-dock");
    if (dock) document.body.appendChild(dock);

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
        if (dock) {
            if (isOpen) {
                dock.classList.add("nav-active");
                document.body.style.overflow = "hidden";
            } else {
                dock.classList.remove("nav-active");
                document.body.style.overflow = "";
            }
        }
    });

    // Close menu when clicking outside
    document.addEventListener("click", function(e) {
        if (dock && dock.classList.contains("nav-active") && !dock.contains(e.target) && e.target !== hamburger) {
            hamburger.classList.remove("open");
            header.classList.remove("nav-active");
            dock.classList.remove("nav-active");
            document.body.style.overflow = "";
        }
    });

    // Close menu when clicking a dock item
    const dockItems = document.querySelectorAll(".magnification-dock .dock-item");
    dockItems.forEach(item => {
        item.addEventListener("click", () => {
            hamburger.classList.remove("open");
            header.classList.remove("nav-active");
            if (dock) dock.classList.remove("nav-active");
            document.body.style.overflow = "";
        });
    });
});
