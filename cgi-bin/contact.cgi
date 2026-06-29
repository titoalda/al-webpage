#!/bin/sh
# Cogemos el POST (cat), lo codificamos en Base64 en una sola linea, y lo guardamos
echo "[NUEVO_CONTACTO] $(cat | base64 -w 0)" >> /usr/local/apache2/logs/contact.log

# Redirigimos al usuario a la web principal con un parametro de exito
echo "Content-type: text/html"
echo "Location: /?contacto=exito"
echo ""
