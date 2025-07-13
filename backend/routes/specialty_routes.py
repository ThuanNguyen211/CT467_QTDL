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
        sql = "INSERT INTO chuyen_khoa (ma_chuyen_khoa, ten_chuyen_khoa, mo_ta) VALUES (%s, %s, %s)"
        cursor.execute(sql, (
            data['ma_chuyen_khoa'],
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