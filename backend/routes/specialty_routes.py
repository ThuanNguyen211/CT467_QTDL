from flask import Blueprint, request, jsonify
from db import get_connection

specialty_bp = Blueprint('specialty', __name__)

@specialty_bp.route('/specialty', methods=['GET'])
def get_specialty():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chuyen_khoa")
        result = cursor.fetchall()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
            return jsonify({'error': str(e)}), 500


@specialty_bp.route('/specialty/<string:ma_chuyen_khoa>', methods=['GET'])
def get_specialty_id(ma_chuyen_khoa):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM chuyen_khoa WHERE ma_chuyen_khoa = %s"
        cursor.execute(sql, (ma_chuyen_khoa,))
        result = cursor.fetchall()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
            return jsonify({'error': str(e)}), 500

@specialty_bp.route('/specialty', methods=['POST'])
def add_specialty():
    try:
        data = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO chuyen_khoa (ten_chuyen_khoa, mo_ta) VALUES (%s, %s)"
        cursor.execute(sql, (
            data['ten_chuyen_khoa'],
            data['mo_ta']
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Thêm chuyên khoa thành công'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@specialty_bp.route('/specialty/<string:ma_chuyen_khoa>', methods=['PUT'])
def update_specialty(ma_chuyen_khoa):
    try:
        data = request.get_json()
        conn = get_connection()
        cursor = conn.cursor()
        sql = "UPDATE chuyen_khoa SET ten_chuyen_khoa = %s, mo_ta = %s WHERE ma_chuyen_khoa = %s"
        cursor.execute(sql, (
            data['ten_chuyen_khoa'],
            data['mo_ta'],
            ma_chuyen_khoa
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cập nhật chuyên khoa thành công'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@specialty_bp.route('/specialty/<string:ma_chuyen_khoa>', methods=['DELETE'])
def delete_specialty(ma_chuyen_khoa):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chuyen_khoa WHERE ma_chuyen_khoa = %s", (ma_chuyen_khoa,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Xóa chuyên khoa thành công'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@specialty_bp.route('/specialty/patients', methods=['GET'])
def get_specialty_patient_count():
    try:
        ma_chuyen_khoa = request.args.get('ma_chuyen_khoa')
        
        if not ma_chuyen_khoa:
            return jsonify({'error': 'Thiếu tham số ma_chuyen_khoa'}), 400
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('ThongKeBenhNhanChuyenKhoa', (ma_chuyen_khoa,))
        
        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
            
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi thống kê bệnh nhân theo chuyên khoa:", e)
        return jsonify({'error': str(e)}), 500