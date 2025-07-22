from flask import Blueprint, request, jsonify
from db import get_connection
from datetime import datetime, timedelta, date

booking_bp = Blueprint('booking', __name__)

@booking_bp.route('/bookings', methods=['GET'])
def get_bookings():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lich_hen")
    rows = cursor.fetchall()
    conn.close()

    # Xử lý chuyển đổi datetime và timedelta thành string
    for row in rows:
        for key, value in row.items():
            if isinstance(value, (datetime, timedelta)):
                row[key] = str(value)

    return jsonify(rows)

@booking_bp.route('/bookings', methods=['POST'])
def add_booking():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO lich_hen (ma_benh_nhan, ma_bac_si, ngay_hen, gio_hen, trang_thai)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['ma_benh_nhan'],
        data['ma_bac_si'],
        data['ngay_hen'],
        data['gio_hen'],
        data['trang_thai']
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Đặt lịch hẹn thành công'}), 200


@booking_bp.route('/bookings/<ma_lich_hen>', methods=['PUT'])
def update_booking(ma_lich_hen):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE lich_hen
        SET ma_bac_si = %s,
            ngay_hen = %s,
            gio_hen = %s,
            trang_thai = %s
        WHERE ma_lich_hen = %s
    """
    cursor.execute(sql, (
        data['ma_bac_si'],
        data['ngay_hen'],
        data['gio_hen'],
        data['trang_thai'],
        ma_lich_hen
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Cập nhật lịch hẹn thành công'}), 200

@booking_bp.route('/bookings/<ma_lich_hen>', methods=['DELETE'])
def delete_booking(ma_lich_hen):
    conn = get_connection()
    cursor = conn.cursor()

    # Kiểm tra lịch hẹn có tồn tại không
    cursor.execute("SELECT 1 FROM lich_hen WHERE ma_lich_hen = %s", (ma_lich_hen,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': 'Không tìm thấy lịch hẹn'}), 404

    # Xóa lịch hẹn
    cursor.execute("DELETE FROM lich_hen WHERE ma_lich_hen = %s", (ma_lich_hen,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Xóa lịch hẹn thành công'}), 200


@booking_bp.route('/booking/available-slots', methods=['GET'])
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
    
@booking_bp.route('/booking/my_booking', methods=['GET'])
def get_my_booking():
    try:
        ma_benh_nhan = request.args.get('ma_benh_nhan')
        
        if not ma_benh_nhan:
            return jsonify({'error': 'Thiếu tham số ma_benh_nhan'}), 400
            
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('LichHenCuaToi', (ma_benh_nhan,))
        
        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
            
        conn.close()

        for row in data:
            for key, value in row.items():
                if isinstance(value, (timedelta, datetime)):
                    row[key] = str(value)
                    
        return jsonify(data)
    except Exception as e:
        print("Lỗi lấy lich hen:", e)
        return jsonify({'error': str(e)}), 500



#Lay lich hen theo bac si
@booking_bp.route('/doctor/get/appointments', methods=['GET'])
def get_bookings_by_doctor_id():
    ma_bs = request.args.get('ma_bac_si')
    ngay = request.args.get('date')
    status = request.args.get('status')  # Có thể là None

    if not ma_bs:
        return jsonify({'error': 'Thiếu ma_bac_si'}), 400

    # Nếu không có ngày thì mặc định là hôm nay
    if not ngay:
        ngay = date.today().strftime('%Y-%m-%d')

    try:
        ngay_date = datetime.strptime(ngay, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Định dạng ngày không hợp lệ'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Gọi stored procedure
    cursor.callproc('LichHenBacSiTheoNgay', [ma_bs, ngay_date])
    # Lấy kết quả
    rows = []
    for result in cursor.stored_results():
        rows = result.fetchall()

    conn.close()

    # Lọc theo trạng thái nếu có
    if status:
        rows = [row for row in rows if row['trang_thai'] == status]

    # Chuyển datetime về string nếu cần
    for row in rows:
        for k, v in row.items():
            if isinstance(v, (datetime, timedelta)):
                row[k] = str(v)
    print(rows)
    return jsonify(rows)

