from django.apps import AppConfig


class TestifyConfig(AppConfig):
    name = 'testify'

    def ready(self):
        import testify.signals # noqa