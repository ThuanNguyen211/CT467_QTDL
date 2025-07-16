from flask import Blueprint, request, jsonify
from db import get_connection

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctors', methods=['GET'])
def get_doctors():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bac_si")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy thông tin bác sĩ:", e)
        return jsonify({'error': str(e)}), 500

@doctor_bp.route('/doctors/<string:ma_bac_si>', methods=['GET'])
def get_doctors_id(ma_bac_si):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM bac_si  WHERE ma_bac_si = %s"
        cursor.execute(sql, (ma_bac_si,))
        data = cursor.fetchone()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy thông tin bác sĩ:", e)
        return jsonify({'error': str(e)}), 500

@doctor_bp.route('/doctors', methods=['POST'])
def add_doctor():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO bac_si (ten_bac_si, ma_chuyen_khoa, so_dien_thoai, kinh_nghiem)
            VALUES (%s, %s, %s, %s)
            """
        cursor.execute(sql, (
            data['ten_bac_si'],
            data['ma_chuyen_khoa'],
            data['so_dien_thoai'],
            data['kinh_nghiem']
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Thêm bác sĩ thành công'}), 201
    except Exception as e:
        print("Lỗi thêm bác sĩ:", e)
        return jsonify({'error': str(e)}), 500

@doctor_bp.route('/doctors/<string:ma_bac_si>', methods=['PUT'])
def update_doctor(ma_bac_si):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE bac_si
            SET ten_bac_si = %s,
                ma_chuyen_khoa = %s,
                so_dien_thoai = %s,
                kinh_nghiem = %s
            WHERE ma_bac_si = %s
        """
        cursor.execute(sql, (
            data['ten_bac_si'],
            data['ma_chuyen_khoa'],
            data['so_dien_thoai'],
            data['kinh_nghiem'],
            ma_bac_si
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cập nhật bác sĩ thành công'}), 200
    except Exception as e:
        print("Lỗi cập nhật bác sĩ:", e)
        return jsonify({'error': str(e)}), 500


@doctor_bp.route('/doctors/<string:ma_bac_si>', methods=['DELETE'])
def delete_doctor(ma_bac_si):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM bac_si WHERE ma_bac_si = %s"
        cursor.execute(sql, (ma_bac_si,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Xóa bác sĩ thành công'}), 200
    except Exception as e:
        print("Lỗi xóa bác sĩ:", e)
        return jsonify({'error': str(e)}), 500