document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("contact-form");
    const statusDiv = document.getElementById("form-status");

    // CONFIGURATION: Set your Web3Forms Access Key here to receive emails directly.
    // Get a free key instantly at: https://web3forms.com
    const WEB3FORMS_ACCESS_KEY = "9730a2ad-8c3b-43d9-b68c-ad611768d778"; 

    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault();

            // 1. Honeypot protection (spam mitigation)
            const honeypot = document.getElementById("honeypot").value;
            if (honeypot) {
                console.warn("Spambot detected!");
                form.style.display = "none";
                const loadingOverlay = document.getElementById("loading-overlay");
                if (loadingOverlay) loadingOverlay.style.display = "flex";
                
                setTimeout(() => {
                    if (loadingOverlay) loadingOverlay.style.display = "none";
                    const successOverlay = document.getElementById("success-overlay");
                    const successTitle = document.getElementById("success-title-text");
                    if (successTitle) successTitle.innerText = "¡Gracias!";
                    if (successOverlay) successOverlay.style.display = "flex";
                }, 3000);
                form.reset();
                return;
            }

            // 2. Fetch inputs
            const nameVal = document.getElementById("name").value.trim();
            const emailVal = document.getElementById("email").value.trim();
            const messageVal = document.getElementById("message").value.trim();

            // 3. Email validation regex (Threat sanitization)
            const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
            if (!emailRegex.test(emailVal)) {
                statusDiv.innerText = "Por favor, introduce un email válido.";
                statusDiv.style.color = "#ff4d4d";
                statusDiv.style.display = "block";
                return;
            }

            // 4. HTML sanitization (Escape HTML to prevent XSS)
            function sanitizeHTML(str) {
                const map = {
                    '&': '&amp;',
                    '<': '&lt;',
                    '>': '&gt;',
                    '"': '&quot;',
                    "'": '&#x27;',
                    "/": '&#x2F;'
                };
                const reg = /[&<>"'/]/ig;
                return str.replace(reg, (match) => map[match]);
            }

            const cleanName = sanitizeHTML(nameVal);
            const cleanEmail = sanitizeHTML(emailVal);
            const cleanMessage = sanitizeHTML(messageVal);

            // 5. Hide form, headings, and desc to display the loading animation state centered
            form.style.display = "none";
            
            // Hide intro descriptions (handles both contact.html and index.html)
            const desc = document.querySelector(".contact-page-desc") || document.querySelector(".contact-section .intro") || document.querySelector(".intro");
            if (desc) desc.style.display = "none";
            
            // Hide section heading on index.html to allow clean centering
            const heading = document.querySelector(".contact-section h2");
            if (heading) heading.style.display = "none";

            const loadingOverlay = document.getElementById("loading-overlay");
            if (loadingOverlay) loadingOverlay.style.display = "flex";

            // 6. Submit form in the background using Web3Forms API (no email client popup needed)
            if (WEB3FORMS_ACCESS_KEY && WEB3FORMS_ACCESS_KEY !== "YOUR_ACCESS_KEY_HERE") {
                fetch("https://api.web3forms.com/submit", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Accept": "application/json"
                    },
                    body: JSON.stringify({
                        access_key: WEB3FORMS_ACCESS_KEY,
                        name: cleanName,
                        email: cleanEmail,
                        subject: "Nuevo contacto de: " + cleanName,
                        message: cleanMessage
                    })
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Form submission success:", data);
                })
                .catch(error => {
                    console.error("Form submission error:", error);
                });
            } else {
                console.log("Form submitted locally (Access Key not configured yet):", {
                    name: cleanName,
                    email: cleanEmail,
                    message: cleanMessage
                });
            }

            // 7. Run loading state for 3 seconds, then transition to success page
            setTimeout(() => {
                if (loadingOverlay) loadingOverlay.style.display = "none";
                
                const successOverlay = document.getElementById("success-overlay");
                const successTitle = document.getElementById("success-title-text");
                
                if (successTitle) {
                    successTitle.innerText = `¡Gracias, ${cleanName}!`;
                }
                
                if (successOverlay) {
                    successOverlay.style.display = "flex";
                }
            }, 3000);

            form.reset();
        });
    }
});
