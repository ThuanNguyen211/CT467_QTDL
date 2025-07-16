from flask import Blueprint, request, jsonify
from db import get_connection

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT email, ma_bac_si, ma_benh_nhan, role, created_at FROM nguoi_dung")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy thông tin người dùng:", e)
        return jsonify({'error': str(e)}), 500


@user_bp.route('/users/login', methods=['POST'])
def login_user():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('mat_khau')
        if not email or not password:
            return jsonify({'error': 'Vui lòng nhập email và mật khẩu'}), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT email, ma_bac_si, ma_benh_nhan, role, created_at FROM nguoi_dung WHERE email = %s AND mat_khau = %s"
        cursor.execute(sql, (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return jsonify({'message': 'Đăng nhập thành công', 'user': user}), 200
        else:
            return jsonify({'error': 'Sai thông tin đăng nhập'}), 401
    except Exception as e:
        print("Lỗi đăng nhập:", e)
        return jsonify({'error': str(e)}), 500


@user_bp.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO nguoi_dung (email, ma_bac_si, ma_benh_nhan, mat_khau, role)
            VALUES (%s, %s, %s, %s, %s)
            """
        cursor.execute(sql, (
            data['email'],
            data.get('ma_bac_si'),
            data.get('ma_benh_nhan'),
            data['mat_khau'],
            data['role']
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Thêm người dùng thành công'}), 201
    except Exception as e:
        print("Lỗi thêm người dùng:", e)
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<string:email>', methods=['PUT'])
def update_user(email):
    try:
        data = request.json
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE nguoi_dung
            SET ma_bac_si = %s,
                ma_benh_nhan = %s,
                mat_khau = %s,
                role = %s
            WHERE email = %s
        """
        cursor.execute(sql, (
            data.get('ma_bac_si'),
            data.get('ma_benh_nhan'),
            data['mat_khau'],
            data['role'],
            email
        ))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Cập nhật người dùng thành công'}), 200
    except Exception as e:
        print("Lỗi cập nhật người dùng:", e)
        return jsonify({'error': str(e)}), 500

@user_bp.route('/users/<string:email>', methods=['DELETE'])
def delete_user(email):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM nguoi_dung WHERE email = %s"
        cursor.execute(sql, (email,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Xóa người dùng thành công'}), 200
    except Exception as e:
        print("Lỗi xóa người dùng:", e)
        return jsonify({'error': str(e)}), 500