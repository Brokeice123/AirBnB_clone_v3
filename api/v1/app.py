#!/usr/bin/python3
"""
Flask Application
"""

from flask import Flask, jsonify, make_response
import os
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

#Register blueprint
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

# Enable CORS
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


#Teardown app context
@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the storage session after each request
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    404 Error message definition
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
