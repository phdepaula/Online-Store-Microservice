from flask_openapi3 import Info

from resources.settings import Settings

INFORMATION = Info(title="Online Store", version="1.0.0")
SECRET_KEY = "Advanced Backend Development"
PORT = 5000

flask_settings = Settings(
    information=INFORMATION,
    secret_key=SECRET_KEY,
    port=PORT
)
flask_settings.generate_app()

app = flask_settings.app
