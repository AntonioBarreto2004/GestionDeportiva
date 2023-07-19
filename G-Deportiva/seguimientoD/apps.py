from django.apps import AppConfig


class SeguimientodConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'seguimientoD'

    def ready(self):
        import seguimientoD.models  # Importa las señales en el método ready
