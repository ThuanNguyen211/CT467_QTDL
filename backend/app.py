from flask import Flask
from flask_cors import CORS
from routes.doctor_routes import doctor_bp
from routes.user_routes import user_bp
from routes.prescription_routes import prescription_bp

app = Flask(__name__)
CORS(app)

# Đăng ký Blueprint
app.register_blueprint(doctor_bp)
app.register_blueprint(user_bp)
app.register_blueprint(prescription_bp)

if __name__ == '__main__':
    app.run(port=5000)