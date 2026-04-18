from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        from . import sqlite_config  # noqa: F401
        from . import signals  # noqa: F401
