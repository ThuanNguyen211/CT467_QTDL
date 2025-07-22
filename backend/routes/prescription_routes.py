from flask import Blueprint, request, jsonify
from db import get_connection

prescription_bp = Blueprint('prescription', __name__)

@prescription_bp.route('/prescriptions', methods=['GET'])
def get_prescriptions():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM don_thuoc")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy thông tin đơn thuốc:", e)
        return jsonify({'error': str(e)}), 500

@prescription_bp.route('/prescriptions', methods=['POST'])
def add_prescription():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO don_thuoc (ma_phieu_kham, ma_thuoc, so_luong, lieu_dung, cach_dung)
            VALUES (%s, %s, %s, %s, %s)
            """
        cursor.execute(sql, (
            data['ma_phieu_kham'],
            data['ma_thuoc'],
            data['so_luong'],
            data['lieu_dung'],
            data['cach_dung']
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Thêm đơn thuốc thành công'}), 201
    except Exception as e:
        print("Lỗi thêm đơn thuốc:", e)
        return jsonify({'error': str(e)}), 500

@prescription_bp.route('/prescriptions/<string:ma_don_thuoc>', methods=['PUT'])
def update_prescription(ma_don_thuoc):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE don_thuoc
            SET ma_thuoc = %s,
                so_luong = %s,
                lieu_dung = %s,
                cach_dung = %s
            WHERE ma_don_thuoc = %s
        """
        cursor.execute(sql, (
            data['ma_thuoc'],
            data['so_luong'],
            data['lieu_dung'],
            data['cach_dung'],
            ma_don_thuoc
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cập nhật đơn thuốc thành công'}), 200
    except Exception as e:
        print("Lỗi cập nhật đơn thuốc:", e)
        return jsonify({'error': str(e)}), 500

@prescription_bp.route('/prescriptions/<string:ma_don_thuoc>', methods=['DELETE'])
def delete_prescription(ma_don_thuoc):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM don_thuoc WHERE ma_don_thuoc = %s"
        cursor.execute(sql, (ma_don_thuoc,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Xóa đơn thuốc thành công'}), 200
    except Exception as e:
        print("Lỗi xóa đơn thuốc:", e)
        return jsonify({'error': str(e)}), 500




@prescription_bp.route('/prescriptions/<int:ma_phieu_kham>')
def get_prescriptions_by_exam(ma_phieu_kham):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT dt.lieu_dung, dt.cach_dung, t.ten_thuoc
            FROM don_thuoc dt
            JOIN thuoc t ON dt.ma_thuoc = t.ma_thuoc
            WHERE dt.ma_phieu_kham = %s
        """, (ma_phieu_kham,))
        result = cursor.fetchall()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
        print("Lỗi lấy đơn thuốc:", e)
        return jsonify({'error': str(e)}), 500
