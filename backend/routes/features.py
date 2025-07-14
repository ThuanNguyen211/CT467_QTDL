from flask import Blueprint, request, jsonify
from db import get_connection   
from datetime import datetime

# Blueprint cho lịch hẹn
appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/appointments/available-slots', methods=['GET'])
def get_available_slots():
    try:
        ma_bac_si = request.args.get('ma_bac_si')
        ngay = request.args.get('ngay')
        
        if not ma_bac_si or not ngay:
            return jsonify({'error': 'Thiếu tham số ma_bac_si hoặc ngay'}), 400
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('DanhSachKhungGioTrong', (ma_bac_si, ngay))
        
        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
            
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy danh sách khung giờ trống:", e)
        return jsonify({'error': str(e)}), 500
