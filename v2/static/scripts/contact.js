document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("contact-form");
    const statusDiv = document.getElementById("form-status");

    if (form) {
        form.addEventListener("submit", function(event) {
            event.preventDefault();

            // 1. Honeypot protection (spam mitigation)
            const honeypot = document.getElementById("honeypot").value;
            if (honeypot) {
                console.warn("Spambot detected!");
                statusDiv.innerText = "¡Mensaje enviado con éxito!";
                statusDiv.style.color = "green";
                statusDiv.style.display = "block";
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

            // 5. Display success state
            statusDiv.innerText = `¡Gracias, ${cleanName}! Tu mensaje ha sido procesado de forma segura.`;
            statusDiv.style.color = "green";
            statusDiv.style.display = "block";
            
            // Construct a mailto link dynamically and open it safely after 1.2s
            setTimeout(() => {
                const subject = encodeURIComponent("Contacto desde Portfolio — " + cleanName);
                const body = encodeURIComponent(`Nombre: ${cleanName}\nEmail: ${cleanEmail}\n\nMensaje:\n${cleanMessage}`);
                window.location.href = `mailto:aldaraalvarezglez@gmail.com?subject=${subject}&body=${body}`;
            }, 1200);

            form.reset();
        });
    }
});
