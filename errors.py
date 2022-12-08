#imports

from flask import Blueprint, render_template
from app import app

errors_blueprint = Blueprint("errors", __name__, template_folder="templates")

# error handling

@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html"), 400


@app.errorhandler(403)
def page_forbidden(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template("errors/503.html"), 503
