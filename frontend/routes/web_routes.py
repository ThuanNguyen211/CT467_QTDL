from flask import Blueprint, render_template, redirect, url_for
import requests

web_bp = Blueprint('web', __name__)

# -- Home ---
@web_bp.route('/')
def home():
    return render_template('home.html')

@web_bp.route('/login')
def login():
    return render_template('login.html')


# ----------- BÁC SĨ -------------
@web_bp.route('/doctor/profile')
def doctor_profile():
    return render_template('doctor/profile.html', doctor={})

@web_bp.route('/doctor/medicines')
def doctor_medicines():
    try:
        response = requests.get('http://localhost:5000/medicines')
        response.raise_for_status()
        medicines = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        medicines = []
    return render_template('doctor/medicines.html', medicines=medicines)


# Thêm thuốc (Tín)
@web_bp.route('/doctor/medicines/new', methods=['GET', 'POST'])
def doctor_medicine_new():
    return render_template('doctor/medicine_form.html', medicine=None)




@web_bp.route('/doctor/medicines/<ma_thuoc>/edit', methods=['GET', 'POST'])
def doctor_medicine_edit(ma_thuoc):
    return render_template('doctor/medicine_form.html', medicine_id=ma_thuoc)

@web_bp.route('/doctor/departments')
def doctor_departments():
    return render_template('doctor/departments.html', departments=[])

@web_bp.route('/doctor/appointments')
def doctor_appointments():

    return render_template(
        'doctor/appointments.html',

    )

@web_bp.route('/doctor/examinations/new', methods=['GET', 'POST'])
def doctor_examination_new():
    return render_template('doctor/examination_form.html', examination=None)


# In phiếu khám
@web_bp.route('/doctor/examinations/<int:ma_phieu_kham>/print')
def print_exam(ma_phieu_kham):
    return render_template('doctor/print_exam.html', ma_phieu_kham=ma_phieu_kham)


@web_bp.route('/doctor/prescriptions/new', methods=['GET', 'POST'])
def doctor_prescription_new():
    return render_template('doctor/prescription_form.html', prescription=None, medicines=[])

@web_bp.route('/doctor/examinations/history')
def doctor_examinations_history():
    try:
        response = requests.get('http://localhost:5000/doctors/patients')
        response.raise_for_status()
        medical_exams= response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        medical_exams = []
    return render_template('doctor/examinations.html', examinations= medical_exams)

@web_bp.route('/doctor/statistics')
def doctor_statistics():
    return render_template('doctor/statistics.html', stats={'so_benh_nhan': 0, 'doanh_thu': 0})


@web_bp.route('/doctor/statistics/patients')
def doctor_statistics_patients():
    ma_bac_si = request.args.get('ma_bac_si')
    if not ma_bac_si:
        return {"error": "Thiếu tham số ma_bac_si"}, 400

    try:
        response = requests.get(f'http://localhost:5000/doctors/patients?ma_bac_si={ma_bac_si}')
        response.raise_for_status()
        patients = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        patients = []

    return render_template('doctor/statistics_patients.html', patients=patients)


# ----------- BỆNH NHÂN -------------

@web_bp.route('/patient/profile')
def patient_profile():
    return render_template('patient/profile.html')

@web_bp.route('/patient/appointments')
def patient_appointments():
    return render_template('patient/appointments.html', appointments=[])

@web_bp.route('/patient/appointments/new', methods=['GET', 'POST'])
def patient_appointment_new():
    return render_template('patient/appointment_form.html', doctors=[], available_times=[])

@web_bp.route('/patient/appointments/<ma_lich_hen>/cancel', methods=['POST'])
def patient_appointment_cancel(ma_lich_hen):
    return redirect(url_for('web.patient_appointments'))

@web_bp.route('/patient/examinations/history')
def patient_examinations_history():
    return render_template('patient/examinations.html', examinations=[])
