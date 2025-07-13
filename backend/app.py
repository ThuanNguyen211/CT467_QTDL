from flask import Flask
from flask_cors import CORS
from routes.doctor_routes import doctor_bp
from routes.booking_routes import booking_bp
from routes.medical_exam_routes import medical_exam_bp

app = Flask(__name__)
CORS(app)

# Đăng ký Blueprint
app.register_blueprint(doctor_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(medical_exam_bp)

if __name__ == '__main__':
    app.run(port=5000)