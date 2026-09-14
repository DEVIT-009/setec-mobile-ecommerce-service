import os
import importlib
from django.apps import AppConfig

class PersistenceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'infrastructure.persistence'

    def ready(self):
        models_dir = os.path.join(os.path.dirname(__file__), "models")
        for filename in os.listdir(models_dir):
            if filename.endswith(".py") and filename != "__init__.py" and "model" in filename:
                module_name = f"infrastructure.persistence.models.{filename[:-3]}"
                importlib.import_module(module_name)
