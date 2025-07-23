from flask import Blueprint, request, jsonify
from db import get_connection

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients', methods=['GET'])
def get_patients():
    """Lấy danh sách tất cả bệnh nhân"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM benh_nhan ORDER BY ten_benh_nhan")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Lỗi khi lấy danh sách bệnh nhân: {str(e)}'}), 500

@patient_bp.route('/patients/<ma_benh_nhan>', methods=['GET'])
def get_patient(ma_benh_nhan):
    """Lấy thông tin một bệnh nhân theo mã"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM benh_nhan WHERE ma_benh_nhan = %s", (ma_benh_nhan,))
        data = cursor.fetchone()
        conn.close()
        
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Không tìm thấy bệnh nhân'}), 404
    except Exception as e:
        return jsonify({'error': f'Lỗi khi lấy thông tin bệnh nhân: {str(e)}'}), 500

@patient_bp.route('/patients', methods=['POST'])
def add_patient():
    """Thêm bệnh nhân mới"""
    try:
        data = request.json
        
        conn = get_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO benh_nhan (ten_benh_nhan, ngay_sinh, so_dien_thoai, dia_chi, tien_su_benh)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            data['ten_benh_nhan'],
            data.get('ngay_sinh'),
            data.get('so_dien_thoai'),
            data.get('dia_chi'),
            data.get('tien_su_benh')
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Thêm bệnh nhân thành công'}), 201
    except Exception as e:
        return jsonify({'error': f'Lỗi khi thêm bệnh nhân: {str(e)}'}), 500

@patient_bp.route('/patients/<ma_benh_nhan>', methods=['PUT'])
def update_patient(ma_benh_nhan):
    """Cập nhật thông tin bệnh nhân"""
    try:
        data = request.json
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra bệnh nhân có tồn tại không
        cursor.execute("SELECT ma_benh_nhan FROM benh_nhan WHERE ma_benh_nhan = %s", (ma_benh_nhan,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Không tìm thấy bệnh nhân'}), 404
        
        # Cập nhật thông tin
        sql = """
            UPDATE benh_nhan 
            SET ten_benh_nhan = %s, ngay_sinh = %s, so_dien_thoai = %s, dia_chi = %s, tien_su_benh = %s
            WHERE ma_benh_nhan = %s
        """
        cursor.execute(sql, (
            data.get('ten_benh_nhan'),
            data.get('ngay_sinh'),
            data.get('so_dien_thoai'),
            data.get('dia_chi'),
            data.get('tien_su_benh'),
            ma_benh_nhan
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Cập nhật bệnh nhân thành công'})
    except Exception as e:
        return jsonify({'error': f'Lỗi khi cập nhật bệnh nhân: {str(e)}'}), 500

@patient_bp.route('/patients/<ma_benh_nhan>', methods=['DELETE'])
def delete_patient(ma_benh_nhan):
    """Xóa bệnh nhân"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra bệnh nhân có tồn tại không
        cursor.execute("SELECT ma_benh_nhan FROM benh_nhan WHERE ma_benh_nhan = %s", (ma_benh_nhan,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Không tìm thấy bệnh nhân'}), 404
        
        # Kiểm tra xem bệnh nhân có lịch hẹn nào không
        cursor.execute("SELECT COUNT(*) FROM lich_hen WHERE ma_benh_nhan = %s", (ma_benh_nhan,))
        appointment_count = cursor.fetchone()[0]
        
        if appointment_count > 0:
            conn.close()
            return jsonify({'error': 'Không thể xóa bệnh nhân vì đã có lịch hẹn'}), 400
        
        # Xóa bệnh nhân
        cursor.execute("DELETE FROM benh_nhan WHERE ma_benh_nhan = %s", (ma_benh_nhan,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Xóa bệnh nhân thành công'})
    except Exception as e:
        return jsonify({'error': f'Lỗi khi xóa bệnh nhân: {str(e)}'}), 500

@patient_bp.route('/patients/search', methods=['GET'])
def search_patients():
    """Tìm kiếm bệnh nhân theo tên hoặc số điện thoại"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Tham số tìm kiếm không được để trống'}), 400
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT * FROM benh_nhan 
            WHERE ten_benh_nhan LIKE %s OR so_dien_thoai LIKE %s
            ORDER BY ten_benh_nhan
        """
        search_term = f'%{query}%'
        cursor.execute(sql, (search_term, search_term))
        data = cursor.fetchall()
        conn.close()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Lỗi khi tìm kiếm bệnh nhân: {str(e)}'}), 500
    
@patient_bp.route('/patients/history', methods=['GET'])
def get_patient_history():
    try:
        ma_benh_nhan = request.args.get('ma_benh_nhan')
        ngay = request.args.get('ngay')
        
        if not ma_benh_nhan or not ngay:
            return jsonify({'error': 'Thiếu tham số ma_benh_nhan hoặc ngay'}), 400
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('LichSuKhamBenhNhan', (ma_benh_nhan, ngay))
        
        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
            
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy lịch sử khám bệnh:", e)
        return jsonify({'error': str(e)}), 500

@patient_bp.route('/stats/patient/usage', methods=['GET'])
def get_patient_usage():
    response = {'patients': [], 'total_patients': 0, 'total_visits': 0}
    try:
        filter_type = request.args.get('filter_type')
        filter_day = request.args.get('filter_day')
        filter_month = request.args.get('filter_month', type=int)
        filter_year = request.args.get('filter_year', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not filter_type or filter_type not in ['day', 'month', 'year', 'range']:
            response['error'] = 'Thiếu hoặc sai tham số filter_type, phải là day, month, year, hoặc range'
            return jsonify(response), 400

        if filter_type == 'day' and not filter_day:
            response['error'] = 'Thiếu tham số filter_day cho filter_type=day'
            return jsonify(response), 400
        if filter_type == 'month' and (not filter_month or not filter_year):
            response['error'] = 'Thiếu tham số filter_month hoặc filter_year cho filter_type=month'
            return jsonify(response), 400
        if filter_type == 'year' and not filter_year:
            response['error'] = 'Thiếu tham số filter_year cho filter_type=year'
            return jsonify(response), 400
        if filter_type == 'range' and (not start_date or not end_date):
            response['error'] = 'Thiếu tham số start_date hoặc end_date cho filter_type=range'
            return jsonify(response), 400

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if filter_type == 'day':
            try:
                year, month, day = map(int, filter_day.split('-'))
                cursor.callproc('ThongKeBenhNhanBacSi', ('ALL', day, month, year, None, None))
            except (ValueError, IndexError):
                response['error'] = 'Định dạng filter_day không hợp lệ, yêu cầu YYYY-MM-DD'
                conn.close()
                return jsonify(response), 400
        elif filter_type == 'month':
            cursor.callproc('ThongKeBenhNhanBacSi', ('ALL', 0, filter_month, filter_year, None, None))
        elif filter_type == 'year':
            cursor.callproc('ThongKeBenhNhanBacSi', ('ALL', 0, 0, filter_year, None, None))
        elif filter_type == 'range':
            cursor.callproc('ThongKeBenhNhanBacSi', ('ALL', 0, 0, 0, start_date, end_date))

        data = []
        for result in cursor.stored_results():
            data = result.fetchall()

        response['patients'] = data or []
        response['total_patients'] = len(set(item['ma_benh_nhan'] for item in data)) if data else 0
        response['total_visits'] = sum(item['so_lan_kham'] for item in data) if data else 0

        conn.close()
        return jsonify(response), 200

    except Exception as e:
        print("Lỗi thống kê bệnh nhân:", e)
        response['error'] = f'Lỗi server: {str(e)}'
        if 'conn' in locals():
            conn.close()
        return jsonify(response), 500