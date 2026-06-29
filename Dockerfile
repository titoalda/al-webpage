FROM httpd:alpine

# Habilitar modulos CGI
RUN sed -i 's/.*LoadModule cgi_module/LoadModule cgi_module/g' /usr/local/apache2/conf/httpd.conf && \
    sed -i 's/.*LoadModule cgid_module/LoadModule cgid_module/g' /usr/local/apache2/conf/httpd.conf

# Copiar el script CGI y darle permisos
COPY ./cgi-bin/ /usr/local/apache2/cgi-bin/
RUN chmod +x /usr/local/apache2/cgi-bin/*

# Configurar seguridad y handlers CGI
RUN echo '<Directory "/usr/local/apache2/cgi-bin">' >> /usr/local/apache2/conf/httpd.conf && \
    echo '    AllowOverride None' >> /usr/local/apache2/conf/httpd.conf && \
    echo '    Options +ExecCGI' >> /usr/local/apache2/conf/httpd.conf && \
    echo '    AddHandler cgi-script .cgi' >> /usr/local/apache2/conf/httpd.conf && \
    echo '    Require all granted' >> /usr/local/apache2/conf/httpd.conf && \
    echo '</Directory>' >> /usr/local/apache2/conf/httpd.conf && \
    echo 'LimitRequestBody 5120' >> /usr/local/apache2/conf/httpd.conf && \
    echo 'ErrorDocument 404 /404.html' >> /usr/local/apache2/conf/httpd.conf

# Crear archivo de log para contactos y darle permisos
RUN touch /usr/local/apache2/logs/contact.log && chmod 666 /usr/local/apache2/logs/contact.log

COPY . /usr/local/apache2/htdocs/
RUN rm -rf /usr/local/apache2/htdocs/.git \
    /usr/local/apache2/htdocs/Dockerfile \
    /usr/local/apache2/htdocs/deploy.sh \
    /usr/local/apache2/htdocs/scraper_contacto.py \
    /usr/local/apache2/htdocs/cgi-bin \
    /usr/local/apache2/htdocs/URL.txt
EXPOSE 80
