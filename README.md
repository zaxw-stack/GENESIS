# GENESIS

Django project repository for sik0 tech - Innovative technology solutions.

## Features

- Contact form with admin management
- M-Pesa payment integration (STK Push)
- User authentication (login/register)
- Responsive Bootstrap 5 templates

## Installation

1. Clone the repository
2. Create virtual environment: python -m venv venv
3. Install dependencies: pip install -r requirements.txt
4. Copy .env.example to .env and configure your M-Pesa credentials
5. Run migrations: python manage.py migrate
6. Create superuser: python manage.py createsuperuser
7. Run server: python manage.py runserver

## Environment Variables

Configure the following in your .env file:

- MPESA_CONSUMER_KEY - Safaricom API consumer key
- MPESA_CONSUMER_SECRET - Safaricom API consumer secret
- MPESA_SHORTCODE - Paybill/Till number (sandbox: 174379)
- MPESA_PASSKEY - Lipa Na MPesa passkey
- MPESA_CALLBACK_URL - Your callback endpoint
- SECRET_KEY - Django secret key for production
- DEBUG - Set to False in production

## Default Pages

- / - Home page with contact form
- /blog/ - Blog listing
- /payment/ - M-Pesa payment form
- /show/ - Contact messages admin page
- /login/ - User login
- /register/ - User registration

## Admin

Access admin at /admin/ to manage contact messages.
