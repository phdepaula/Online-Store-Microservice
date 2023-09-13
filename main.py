import resources.documentation
import resources.products
import resources.sales

from app import flask_settings, database, log


if __name__ == "__main__":
    database.setup_database_environment()
    flask_settings.run_aplication()
    log.start_log()
