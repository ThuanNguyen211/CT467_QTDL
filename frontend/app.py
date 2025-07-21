from flask import Flask
from flask_cors import CORS
from routes.web_routes import web_bp


app = Flask(__name__)
CORS(app)

# Đăng ký Blueprint
app.register_blueprint(web_bp)

if __name__ == '__main__':
    app.run(port=5001, debug=True)
