from flask import Blueprint, request, jsonify
from db import get_connection

medicine_bp = Blueprint('medicine', __name__)

@medicine_bp.route('/medicines', methods=['GET'])
def get_medicines():
    """Lấy danh sách tất cả thuốc"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM thuoc ORDER BY ten_thuoc")
        data = cursor.fetchall()
        conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Lỗi khi lấy danh sách thuốc: {str(e)}'}), 500

@medicine_bp.route('/medicines/<ma_thuoc>', methods=['GET'])
def get_medicine(ma_thuoc):
    """Lấy thông tin một thuốc theo mã"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM thuoc WHERE ma_thuoc = %s", (ma_thuoc,))
        data = cursor.fetchone()
        conn.close()
        
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Không tìm thấy thuốc'}), 404
    except Exception as e:
        return jsonify({'error': f'Lỗi khi lấy thông tin thuốc: {str(e)}'}), 500

@medicine_bp.route('/medicines', methods=['POST'])
def add_medicine():
    """Thêm thuốc mới"""
    try:
        data = request.json

        conn = get_connection()
        cursor = conn.cursor()
        
        # Thêm thuốc
        sql = """
            INSERT INTO thuoc (ten_thuoc, don_vi, gia)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (
            data['ten_thuoc'],
            data['don_vi'],
            data['gia']
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Thêm thuốc thành công'}), 201
    except Exception as e:
        return jsonify({'error': f'Lỗi khi thêm thuốc: {str(e)}'}), 500



@medicine_bp.route('/medicines/<ma_thuoc>', methods=['PUT'])
def update_medicine(ma_thuoc):
    """Cập nhật thông tin thuốc"""
    try:
        data = request.json
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra thuốc có tồn tại không
        cursor.execute("SELECT ma_thuoc FROM thuoc WHERE ma_thuoc = %s", (ma_thuoc,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Không tìm thấy thuốc'}), 404
        
        # Cập nhật thông tin
        update_fields = []
        params = []
        
        if 'ten_thuoc' in data:
            update_fields.append("ten_thuoc = %s")
            params.append(data['ten_thuoc'])
        
        if 'don_vi' in data:
            update_fields.append("don_vi = %s")
            params.append(data['don_vi'])
        
        if 'gia' in data:
            update_fields.append("gia = %s")
            params.append(data['gia'])
        
        if update_fields:
            params.append(ma_thuoc)
            sql = f"UPDATE thuoc SET {', '.join(update_fields)} WHERE ma_thuoc = %s"
            cursor.execute(sql, params)
            conn.commit()
        
        conn.close()
        
        return jsonify({'message': 'Cập nhật thuốc thành công'})
    except Exception as e:
        return jsonify({'error': f'Lỗi khi cập nhật thuốc: {str(e)}'}), 500




@medicine_bp.route('/medicines/<ma_thuoc>', methods=['DELETE'])
def delete_medicine(ma_thuoc):
    """Xóa thuốc"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Kiểm tra thuốc có tồn tại không
        cursor.execute("SELECT ma_thuoc FROM thuoc WHERE ma_thuoc = %s", (ma_thuoc,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({'error': 'Không tìm thấy thuốc'}), 404
        
        # Kiểm tra xem thuốc có được sử dụng trong đơn thuốc nào không
        cursor.execute("SELECT COUNT(*) FROM don_thuoc WHERE ma_thuoc = %s", (ma_thuoc,))
        if cursor.fetchone()[0] > 0:
            conn.close()
            return jsonify({'error': 'Không thể xóa thuốc vì đã được sử dụng trong đơn thuốc'}), 400
        
        # Xóa thuốc
        cursor.execute("DELETE FROM thuoc WHERE ma_thuoc = %s", (ma_thuoc,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Xóa thuốc thành công'})
    except Exception as e:
        return jsonify({'error': f'Lỗi khi xóa thuốc: {str(e)}'}), 500

@medicine_bp.route('/medicines/search', methods=['GET'])
def search_medicines():
    """Tìm kiếm thuốc theo tên"""
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'Tham số tìm kiếm không được để trống'}), 400
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = """
            SELECT * FROM thuoc 
            WHERE ten_thuoc LIKE %s
            ORDER BY ten_thuoc
        """
        search_term = f'%{query}%'
        cursor.execute(sql, (search_term,))
        data = cursor.fetchall()
        conn.close()
        
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f'Lỗi khi tìm kiếm thuốc: {str(e)}'}), 500
    
# Thống kê thuốc đã sử dụng
@medicine_bp.route('/stats/medication/usage', methods=['GET'])
def get_medication_usage():
    try:
        filter_type = request.args.get('filter_type')
        filter_day = request.args.get('filter_day')
        filter_month = request.args.get('filter_month', type=int)
        filter_year = request.args.get('filter_year', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        if not filter_type or filter_type not in ['day', 'month', 'year', 'range']:
            return jsonify({'error': 'Thiếu hoặc sai tham số filter_type'}), 400
        
        if filter_type == 'day' and not filter_day:
            return jsonify({'error': 'Thiếu tham số filter_day'}), 400
        if filter_type == 'month' and (not filter_month or not filter_year):
            return jsonify({'error': 'Thiếu tham số filter_month hoặc filter_year'}), 400
        if filter_type == 'year' and not filter_year:
            return jsonify({'error': 'Thiếu tham số filter_year'}), 400
        if filter_type == 'range' and (not start_date or not end_date):
            return jsonify({'error': 'Thiếu tham số start_date hoặc end_date'}), 400
        
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.callproc('ThongKeThuocSuDung', (
            filter_type,
            filter_day if filter_day else None,
            filter_month if filter_month else 0,
            filter_year if filter_year else 0,
            start_date if start_date else None,
            end_date if end_date else None
        ))
        
        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
        
        conn.close()
        return jsonify(data)
    except Exception as e:
        print("Lỗi thống kê thuốc sử dụng:", e)
        return jsonify({'error': str(e)}), 500