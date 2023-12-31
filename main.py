import resources.documentation
import resources.products
import resources.sales
from app import database, flask_settings, log

if __name__ == "__main__":
    log.start_log()

    log.add_message("Starting the database environment")
    database.setup_database_environment()

    log.add_message("Starting Flask Settings")
    log.add_message("")
    flask_settings.run_aplication()
