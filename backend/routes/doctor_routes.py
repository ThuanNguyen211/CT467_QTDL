from flask import Blueprint, request, jsonify
from db import get_connection

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/doctors', methods=['GET'])
def get_doctors():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM bac_si bs JOIN chuyen_khoa ck ON ck.ma_chuyen_khoa = bs.ma_chuyen_khoa")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy thông tin bác sĩ:", e)
        return jsonify({'error': str(e)}), 500

@doctor_bp.route('/doctors/<string:ma_bac_si>', methods=['GET'])
def get_doctor(ma_bac_si):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """
            SELECT b.*, ck.ten_chuyen_khoa 
            FROM bac_si b 
            JOIN chuyen_khoa ck ON b.ma_chuyen_khoa = ck.ma_chuyen_khoa 
            WHERE b.ma_bac_si = %s
        """
        cursor.execute(sql, (ma_bac_si,))
        result = cursor.fetchone()
        conn.close()
        return jsonify(result), 200
    except Exception as e:
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
    

@doctor_bp.route('/doctors/patients', methods=['GET'])
def get_doctor_patients():
    response = {'patients': [], 'total_patients': 0, 'total_visits': 0}
    try:
        ma_bac_si = request.args.get('ma_bac_si')
        ngay = request.args.get('ngay', type=int, default=0)
        thang = request.args.get('thang', type=int, default=0)
        nam = request.args.get('nam', type=int, default=0)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not ma_bac_si:
            response['error'] = 'Thiếu tham số ma_bac_si'
            return jsonify(response), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('ThongKeBenhNhanBacSi', (ma_bac_si, ngay, thang, nam, start_date, end_date))

        data = []
        for result in cursor.stored_results():
            data = result.fetchall()

        response['patients'] = data or []
        response['total_patients'] = len(set(item['ma_benh_nhan'] for item in data)) if data else 0
        response['total_visits'] = sum(item['so_lan_kham'] for item in data) if data else 0

        conn.close()
        return jsonify(response), 200

    except Exception as e:
        print("Lỗi thống kê bác sĩ:", e)
        response['error'] = f'Lỗi server: {str(e)}'
        if 'conn' in locals():
            conn.close()
        return jsonify(response), 500
    

@doctor_bp.route('/doctors/examinations', methods=['GET'])
def get_doctor_patient_count():
    try:
        ma_bac_si = request.args.get('ma_bac_si')
        # thang = request.args.get('thang', type=int)
        # nam = request.args.get('nam', type=int)
        
        if not ma_bac_si:
            return jsonify({'error': 'Thiếu tham số ma_bac_si'}), 400
        # if not ma_bac_si or thang is None or nam is None:
        #     return jsonify({'error': 'Thiếu tham số ma_bac_si, thang hoặc nam'}), 400
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('LichSuKhamBacSi', (ma_bac_si, ))
        # cursor.callproc('LichSuKhamBacSi', (ma_bac_si, thang, nam))
        
        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
            
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi thống kê bệnh nhân của bác sĩ:", e)
        return jsonify({'error': str(e)}), 500