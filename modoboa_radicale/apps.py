"""AppConfig for radicale."""

from django.apps import AppConfig


class RadicaleConfig(AppConfig):
    """App configuration."""

    name = "modoboa_radicale"
    verbose_name = "Modoboa Radicale frontend"

    def ready(self):
        from . import handlers
