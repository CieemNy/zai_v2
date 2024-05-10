from django.apps import AppConfig


class FilmyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'filmy'

    def ready(self):
        # signals are imported, so that they are defined and can be used
        import filmy.signals
