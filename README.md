# serprolim4

Sitio web para servicio de limpieza de pozos ciegos y cámaras sépticas. Django + Wagtail CMS con sistema de landing pages multi-país, blog, SEO y WhatsApp.

## Stack

- **Backend**: Django 4+ / Wagtail CMS
- **Frontend**: Tailwind CSS v4 + DaisyUI v5
- **Mapa**: Leaflet.js (cotizador con geolocalización)
- **JS build**: Vite (`home/index-home.js` → `static/js/home.js`)
- **Deploy**: Gunicorn + Nginx + systemd

## Estructura de apps

| App | Función |
|-----|---------|
| `home` | Landing pages por país (LandingPage, LandingService, LandingFAQ) |
| `blog` | Blog con Wagtail (BlogPage, BlogIndexPage) |
| `config` | CountrySettings, GeneralSettings, middleware de país |
| `tracking` | Snippets HTML/JS de analytics (GTM, GA, Meta Pixel, etc.) |
| `chat` | Proxy de WhatsApp hacia webhook n8n (`/chat/api/send/`) |
| `theme` | Configuración de Tailwind CSS v4 |

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows
pip install -r requirements/dev.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

CSS (en otra terminal):
```bash
python manage.py tailwind start
```

JS del mapa (en otra terminal, desde `home/`):
```bash
cd home && npm install && npm run vite
```

## Variables de entorno

Crear `.env` en la raíz del proyecto:

```env
SECRET_KEY=clave-secreta-larga
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
```

## Settings

| Archivo | Uso |
|---------|-----|
| `core/settings.py` | Base compartida |
| `core/dev.py` | Desarrollo (DEBUG=True, browser-reload) |
| `core/prod.py` | Producción (lee `.env`, caché en disco) |

`manage.py` usa `core.dev` por defecto.

## URLs principales

| Ruta | Descripción |
|------|-------------|
| `/` | Landing page (multi-país) |
| `/blog/` | Blog |
| `/admin/` | Django admin |
| `/admin_blog/` | Wagtail CMS |
| `/chat/api/send/` | API proxy WhatsApp |
| `/sitemap.xml` | Sitemap SEO |

## Deploy en VPS

```bash
# 1. Clonar y preparar
git clone <repo> && cd serprolim4
python -m venv .venv && pip install -r requirements/prod.txt
cp .env.example .env   # completar SECRET_KEY y ALLOWED_HOSTS

# 2. Build de assets
python manage.py tailwind build --settings=core.prod
cd home && npm install && npm run vite && cd ..

# 3. Generar configs nginx + systemd
bash deploy.sh

# 4. SSL con certbot
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

## Comandos útiles

```bash
python manage.py tailwind build     # compilar CSS
python manage.py collectstatic      # recolectar estáticos (prod)
python manage.py migrate            # aplicar migraciones
python manage.py shell_plus         # shell con modelos cargados
```
