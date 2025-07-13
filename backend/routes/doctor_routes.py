from flask import Blueprint, request, jsonify
from db import get_connection

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctors', methods=['GET'])
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bac_si")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

@doctor_bp.route('/doctors', methods=['POST'])
def add_doctor():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO bac_si (ma_bac_si, ten_bac_si, ma_chuyen_khoa, so_dien_thoai, kinh_nghiem)
        VALUES (%s, %s, %s, %s, %s)
        """
    cursor.execute(sql, (
        data['ma_bac_si'],
        data['ten_bac_si'],
        data['ma_chuyen_khoa'],
        data['so_dien_thoai'],
        data['kinh_nghiem']
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Thêm bác sĩ thành công'}), 201

# @doctor_bp.route('/doctors', methods=['POST'])
# def add_doctor():
#     try:
#         data = request.json
#         conn = get_connection()
#         cursor = conn.cursor()

#         sql = """
#         INSERT INTO bac_si (ma_bac_si, ten_bac_si, ma_chuyen_khoa, so_dien_thoai, kinh_nghiem)
#         VALUES (%s, %s, %s, %s, %s)
#         """
#         cursor.execute(sql, (
#             data['ma_bac_si'],
#             data['ten_bac_si'],
#             data['ma_chuyen_khoa'],
#             data['so_dien_thoai'],
#             data['kinh_nghiem']
#         ))

#         conn.commit()
#         conn.close()
#         return jsonify({'message': 'Thêm bác sĩ thành công'}), 201

#     except Exception as e:
#         print("Lỗi:", e)
#         return jsonify({'error': str(e)}), 500
