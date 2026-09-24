<div align="center">

<img src="static/assets/logo.svg" alt="Parsa Abasnezhad logo" width="96">

# Parsa Abasnezhad

### Personal portfolio built with Django

<p>
  <img src="https://img.shields.io/badge/Python-282c33?style=flat-square&logo=python&logoColor=c778dd" alt="Python">
  <img src="https://img.shields.io/badge/Django-282c33?style=flat-square&logo=django&logoColor=c778dd" alt="Django">
  <img src="https://img.shields.io/badge/SQLite-282c33?style=flat-square&logo=sqlite&logoColor=c778dd" alt="SQLite">
  <img src="https://img.shields.io/badge/Security--focused-c778dd?style=flat-square&logo=shield&logoColor=ffffff" alt="Security focused">
</p>

<p>
  <em>Build. Ship. Improve.</em>
</p>

</div>

> A dark, developer-focused portfolio for presenting profile information,
> skills, projects, and contact options.

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#project-structure">Structure</a> ·
  <a href="#ui--ux-figma">UI/UX</a> ·
  <a href="#local-installation">Installation</a> ·
  <a href="#website-routes">Routes</a> ·
  <a href="#production-deployment">Deployment</a>
</p>

## `01` / Features

- Portfolio homepage with profile information, hero statistics, skills, and a
  "Now Building" section
- Project detail pages with slugs, tags, features, and image galleries
- Full content management through the Django Admin panel
- Contact and meeting-request forms with validation, CSRF protection, and rate
  limiting
- Database storage for contact messages and meeting requests
- Custom 404 and 500 error pages
- `robots.txt` and `sitemap.xml` for SEO
- Security headers, CSP, secure production cookies, and request-size limits
- Sensitive configuration loaded from a local `.env` file

## `02` / Technology Stack

- Python
- Django 6.1.1
- SQLite by default
- Pillow for image uploads and processing
- HTML, CSS, and JavaScript
- Figma for UI/UX design (see [UI / UX (Figma)](#ui--ux-figma))

## `03` / Architecture

The project follows a classic Django MVT (Model–View–Template) layout with a
security layer around every request.

```text
Browser
  │
  ▼
Django URL router  (parsaabasnezhad/urls.py → main/urls.py)
  │
  ▼
Middleware         (security headers, admin rate limiting, CSP)
  │
  ▼
Views              (main/views.py)
  │
  ├── Models / ORM (main/models.py)  →  SQLite / database
  ├── Forms        (main/forms.py)   →  validation + CSRF
  └── Templates    (templates/)      →  HTML responses
        │
        ▼
      Static files (static/css, static/js, static/assets, fonts)
```

### Layers

| Layer | Responsibility |
|---|---|
| **Project config** (`parsaabasnezhad/`) | Settings, root URLs, WSGI/ASGI entrypoints, `.env` loading |
| **Application** (`main/`) | Domain models, views, forms, admin, middleware, SEO helpers |
| **Presentation** (`templates/`) | Server-rendered HTML; `base_site.html` wraps all public pages |
| **Assets** (`static/`) | CSS, JavaScript, fonts, icons, and illustrations |
| **Uploads** (`media/`) | User-uploaded images managed via Admin (not committed to Git) |
| **Design** (Figma account) | Source of truth for UI and UX; implemented in templates/CSS |

### Request flow

1. The reverse proxy or development server receives an HTTP request.
2. Django matches the path in `parsaabasnezhad/urls.py` (admin, sitemap) or
   includes `main.urls` for public routes.
3. Middleware adds security headers and applies rate limits where configured.
4. A view loads data from models, validates forms when needed, and renders a
   template (or returns JSON for form endpoints).
5. Context processors inject shared data (for example, profile details) into
   templates.
6. The browser receives HTML plus static CSS/JS that implement the Figma design.

### Design → code

UI and UX are designed in **Figma**. The frontend implementation mirrors that
design using:

- `templates/base_site.html` as the shared layout (navbar, footer, meta tags)
- Page templates under `templates/portfolio/`
- Styles under `static/css/` (`base.css`, `home.css`, `project.css`, `visit.css`, …)
- Client behavior in `static/js/script.js`

## `04` / Project Structure

```text
.
├── main/                              # Portfolio Django app
│   ├── models.py                      # Profile, projects, skills, messages, …
│   ├── views.py                       # Page views and form handlers
│   ├── views_constants.py             # Shared view helpers / constants
│   ├── urls.py                        # Public website routes
│   ├── forms.py                       # Contact and visit-request forms
│   ├── admin.py                       # Django Admin configuration
│   ├── middleware.py                  # Extra security headers & admin limits
│   ├── security.py                    # Rate limiting and request-size helpers
│   ├── context_processors.py          # Template-wide context
│   ├── sitemaps.py                    # SEO sitemaps
│   ├── tests.py                       # Automated tests
│   └── migrations/                    # Database migrations
├── parsaabasnezhad/                   # Project package
│   ├── settings.py                    # Django settings and .env loading
│   ├── urls.py                        # Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   ├── base_site.html                 # Base HTML layout
│   ├── 404.html / 500.html            # Custom error pages
│   ├── partials/                      # Navbar, footer
│   ├── portfolio/                     # Home, project detail, visit pages
│   └── admin/                         # Admin branding overrides
├── static/
│   ├── css/                           # Stylesheets
│   ├── js/                            # Client-side scripts
│   ├── fonts/                         # Self-hosted Fira Code
│   └── assets/                        # Logos, icons, illustrations
├── media/                             # Uploaded files (gitignored)
├── manage.py
├── start_server.py                    # Dev helper: runserver + open browser
├── requirements.txt
├── .env.example
└── README.md
```

## `05` / UI / UX (Figma)

**All UI and UX design work lives in the Figma account.**

Figma is the design source of truth for layout, typography, color, spacing, and
interaction patterns. This repository contains the Django implementation of
that design (templates, CSS, and assets). When visual changes are required,
update the Figma files first, then mirror them in `templates/` and `static/`.

## `06` / Local Installation

The following commands use Windows PowerShell:

```powershell
git clone <repository-url>
cd ParsaAbasnezhad

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

Replace `DJANGO_SECRET_KEY` in `.env` with a long, random, private value.
Never commit `.env` or publish it to GitHub.

Apply migrations and create an administrator:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

Start the development server:

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in a browser. The `start_server.py` helper can
also start the server and open the browser automatically:

```powershell
python start_server.py
```

## `07` / Environment Configuration

Settings are loaded from `.env` and system environment variables.

| Variable | Purpose |
|---|---|
| `DJANGO_DEBUG` | Development mode; must be `False` in production |
| `DJANGO_SECRET_KEY` | Django cryptographic secret key |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames, separated by commas |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Trusted CSRF origins, separated by commas |
| `DJANGO_ADMIN_URL` | Admin panel path; defaults to `admin/` |
| `DJANGO_TRUST_X_FORWARDED_FOR` | Trust reverse-proxy forwarding headers |
| `GOOGLE_SITE_VERIFICATION` | Optional Google Search Console token |
| `DJANGO_EMAIL_*` | Optional SMTP configuration |

Example production configuration:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=use-a-long-random-production-secret
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com
DJANGO_ADMIN_URL=secure-admin/
DJANGO_TRUST_X_FORWARDED_FOR=True
```

## `08` / Website Routes

| Route | Description |
|---|---|
| `/` | Portfolio homepage |
| `/projects/<slug>/` | Project detail page |
| `/contact/` | Submit a contact message |
| `/visit/` | Meeting-request page |
| `/visit-request/` | Submit a meeting request |
| `/robots.txt` | Crawler rules |
| `/sitemap.xml` | Website sitemap |
| `/<DJANGO_ADMIN_URL>` | Django Admin panel |

The Admin path is not hardcoded in the URL configuration. It is loaded from
the `DJANGO_ADMIN_URL` environment variable.

## `09` / Content Management

After creating a superuser, use the Admin panel to manage:

- `Profile`: name, role, introduction, images, and availability status
- `Hero stats`: statistics displayed in the hero section
- `Now building`: the current project or activity
- `Projects`: projects, publication status, links, tags, features, and gallery
- `Skill categories / Skill items`: skill groups and proficiency levels
- `Contact links`: social and contact links
- `Quotes`: active portfolio quotes
- `Contact messages`: messages submitted by visitors
- `Visit requests`: meeting requests submitted by visitors

For a complete homepage, create at least one `Profile` and add the required
projects, skills, and contact links through the Admin panel.

## `10` / Testing and Validation

Check the Django configuration:

```powershell
python manage.py check
```

Run the test suite:

```powershell
python manage.py test
```

## `11` / Production Deployment

Before deploying:

1. Set `DJANGO_DEBUG=False`.
2. Keep a strong `DJANGO_SECRET_KEY` outside the repository.
3. Configure `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS` precisely.
4. Use a production database and schedule regular backups. SQLite is not
   recommended for high-traffic deployments.
5. Apply migrations:
   ```powershell
   python manage.py migrate
   ```
6. Collect static files:
   ```powershell
   python manage.py collectstatic --noinput
   ```
7. Store `media/` files in persistent storage and back them up.
8. Run the application with an ASGI/WSGI server and a reverse proxy such as
   Nginx or a managed cloud service. `runserver` is for development only.
9. Enable HTTPS, database backups, and restricted access to the Admin panel.

## `12` / Security

- `.env`, the database, and uploaded media are excluded from Git.
- Never place real secrets in `settings.py` or any other source file.
- Never use a development secret in production.
- Hiding the Admin path is not a substitute for strong passwords, HTTPS, and
  access control.
- Rotate any secret immediately if it is exposed.
