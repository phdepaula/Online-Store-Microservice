import resources.documentation
import resources.products

from app import flask_settings, database


if __name__ == "__main__":
    database.setup_database_environment()
    flask_settings.run_aplication()
