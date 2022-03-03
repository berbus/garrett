from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    FRONTEND_ENDPOINT = 'http://localhost:3000'
