#!/usr/bin/python3
"""
Flask Application
"""

from flask import Flask, jsonify, make_response
import os

# Import storage from models
from models import storage

# Import views from api.v1.views
from api.v1.views import app_views

# Import CORS from falsk_cors
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)

#Register blueprint
app.register_blueprint(app_views)

# Enable CORS
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


#Teardown app context
@app.teardown_appcontext
def teardown_db(exception):
    """
    Closes the storage
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    404 Error
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
