from flask import redirect
from flask_openapi3 import Tag

from app import app

tag_documentation = Tag(
    name="Documentation",
    description="Documentation selection: Swagger, Redoc or RapiDoc.",
)


@app.get("/", tags=[tag_documentation])
def documentation_route():
    """
    Redirects to the /openapi route,\
    a screen that allows choosing the documentation style.
    """
    return redirect("/openapi")
