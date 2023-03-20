from django.apps import AppConfig


class UtilsConfig(AppConfig):
    name = "nederlandse_spoorwegen.utils"

    def ready(self):
        from . import checks  # noqa
