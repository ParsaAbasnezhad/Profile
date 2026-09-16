# Parsa Abasnezhad - Portfolio

A personal portfolio website built with Django for presenting profile
information, skills, projects, and contact options.

## Features

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

## Technology Stack

- Python
- Django 6.1.1
- SQLite by default
- Pillow for image uploads and processing
- HTML, CSS, and JavaScript

## Project Structure

```text
.
├── main/                         # Main Django application
│   ├── models.py                 # Profile, project, skill, and message models
│   ├── views.py                  # Website views and form handlers
│   ├── urls.py                   # Public website routes
│   ├── admin.py                  # Django Admin configuration
│   ├── middleware.py             # Security headers and rate limiting
│   └── migrations/               # Database migrations
├── parsaabasnezhad/
│   ├── settings.py               # Django settings and .env loading
│   ├── urls.py                   # Project-level URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── templates/                    # HTML templates
├── static/                       # CSS, JavaScript, and public assets
├── media/                        # Uploaded files, excluded from Git
├── manage.py
├── requirements.txt
└── .env.example
```

## Local Installation

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

## Environment Configuration

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

## Website Routes

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

## Content Management

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

## Testing and Validation

Check the Django configuration:

```powershell
python manage.py check
```

Run the test suite:

```powershell
python manage.py test
```

## Production Deployment

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

## Security

- `.env`, the database, and uploaded media are excluded from Git.
- Never place real secrets in `settings.py` or any other source file.
- Never use a development secret in production.
- Hiding the Admin path is not a substitute for strong passwords, HTTPS, and
  access control.
- Rotate any secret immediately if it is exposed.
