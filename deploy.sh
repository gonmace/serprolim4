#!/bin/bash
# -*- ENCODING: UTF-8 -*-

read -p "Nombre de la App: " app
read -p "Dominio: " dominio
read -p "Usuario del sistema (ej: ubuntu, deploy): " appuser

cat > ${app}.com <<EOF
# /etc/nginx/sites-available/$app

server {
    server_name $dominio www.${dominio};

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        autoindex off;
        alias $PWD/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
        gzip_static on;
    }

    location /media/ {
        autoindex off;
        alias $PWD/media/;
        expires 7d;
        add_header Cache-Control "public";
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/${app}.sock;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 60s;
    }

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml image/svg+xml;
    gzip_min_length 1024;
}
EOF

cat > ${app}.socket <<EOF
# /etc/systemd/system/$app.socket

[Unit]
Description=gunicorn socket for $app

[Socket]
ListenStream=/run/$app.sock

[Install]
WantedBy=sockets.target
EOF

cat > ${app}.service <<EOF
# /etc/systemd/system/$app.service

[Unit]
Description=gunicorn daemon for $app
Requires=$app.socket
After=network.target

[Service]
User=$appuser
Group=www-data
WorkingDirectory=$PWD
EnvironmentFile=$PWD/.env
ExecStart=$PWD/.venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/$app.sock \
    core.wsgi:application

Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

sudo cp ${app}.socket /etc/systemd/system/${app}.socket
sudo cp ${app}.service /etc/systemd/system/${app}.service
sudo systemctl daemon-reload
sudo systemctl enable ${app}.socket
sudo systemctl start ${app}.socket

sudo cp ${app}.com /etc/nginx/sites-available/${app}.com
sudo ln -sf /etc/nginx/sites-available/${app}.com /etc/nginx/sites-enabled/${app}.com
sudo nginx -t && sudo systemctl reload nginx

echo ""
echo "✓ Desplegado: $app"
echo "  Servicio:  sudo systemctl status $app"
echo "  Logs:      sudo journalctl -u $app -f"
echo "  Nginx:     sudo systemctl reload nginx"
echo ""
echo "  Recuerda correr certbot para SSL:"
echo "  sudo certbot --nginx -d $dominio -d www.$dominio"
