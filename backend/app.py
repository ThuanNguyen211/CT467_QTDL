from flask import Flask
from flask_cors import CORS
from routes.doctor_routes import doctor_bp
from routes.booking_routes import booking_bp
from routes.medical_exam_routes import medical_exam_bp
from routes.user_routes import user_bp
from routes.prescription_routes import prescription_bp
from routes.specialty_routes import specialty_bp
from routes.medicine_routes import medicine_bp
from routes.patient_routes import patient_bp


<<<<<<< HEAD


=======
>>>>>>> origin/main
app = Flask(__name__)
CORS(app)

# Đăng ký Blueprint
app.register_blueprint(doctor_bp)
app.register_blueprint(booking_bp)
app.register_blueprint(medical_exam_bp)
app.register_blueprint(user_bp)
app.register_blueprint(prescription_bp)
app.register_blueprint(specialty_bp)
app.register_blueprint(medicine_bp)
app.register_blueprint(patient_bp)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
