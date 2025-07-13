from flask import Flask
from flask_cors import CORS
from routes.doctor_routes import doctor_bp
from routes.specialty_routes import specialty_bp

app = Flask(__name__)
CORS(app)

# Đăng ký Blueprint
app.register_blueprint(doctor_bp)
app.register_blueprint(specialty_bp)

if __name__ == '__main__':
    app.run(port=5000)