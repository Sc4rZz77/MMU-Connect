"""
WSGI config for MMUConnect project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

from django.core.asgi import get_asgi_application
import os
from whitenoise import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MMUConnect.settings')
application = ASGIStaticFilesHandler(get_asgi_application())