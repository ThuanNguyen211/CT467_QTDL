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

# @medicine_bp.route('/medicines/price-range', methods=['GET'])
# def get_medicines_by_price_range():
#     """Lấy danh sách thuốc theo khoảng giá"""
#     try:
#         min_price = request.args.get('min_price')
#         max_price = request.args.get('max_price')
        
#         if not min_price and not max_price:
#             return jsonify({'error': 'Cần cung cấp ít nhất một trong hai tham số min_price hoặc max_price'}), 400
        
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
        
#         if min_price and max_price:
#             sql = "SELECT * FROM thuoc WHERE gia >= %s AND gia <= %s ORDER BY gia"
#             cursor.execute(sql, (float(min_price), float(max_price)))
#         elif min_price:
#             sql = "SELECT * FROM thuoc WHERE gia >= %s ORDER BY gia"
#             cursor.execute(sql, (float(min_price),))
#         else:
#             sql = "SELECT * FROM thuoc WHERE gia <= %s ORDER BY gia"
#             cursor.execute(sql, (float(max_price),))
        
#         data = cursor.fetchall()
#         conn.close()
        
#         return jsonify(data)
#     except ValueError:
#         return jsonify({'error': 'Giá trị giá không hợp lệ'}), 400
#     except Exception as e:
#         return jsonify({'error': f'Lỗi khi lấy thuốc theo khoảng giá: {str(e)}'}), 500

# @medicine_bp.route('/medicines/unit/<don_vi>', methods=['GET'])
# def get_medicines_by_unit(don_vi):
#     """Lấy danh sách thuốc theo đơn vị"""
#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
        
#         sql = "SELECT * FROM thuoc WHERE don_vi = %s ORDER BY ten_thuoc"
#         cursor.execute(sql, (don_vi,))
#         data = cursor.fetchall()
#         conn.close()
        
#         return jsonify(data)
#     except Exception as e:
#         return jsonify({'error': f'Lỗi khi lấy thuốc theo đơn vị: {str(e)}'}), 500

# @medicine_bp.route('/medicines/statistics', methods=['GET'])
# def get_medicine_statistics():
#     """Lấy thống kê về thuốc"""
#     try:
#         conn = get_connection()
#         cursor = conn.cursor(dictionary=True)
        
#         # Tổng số thuốc
#         cursor.execute("SELECT COUNT(*) as total_medicines FROM thuoc")
#         total_medicines = cursor.fetchone()['total_medicines']
        
#         # Thuốc có giá cao nhất
#         cursor.execute("SELECT * FROM thuoc WHERE gia = (SELECT MAX(gia) FROM thuoc) LIMIT 1")
#         most_expensive = cursor.fetchone()
        
#         # Thuốc có giá thấp nhất
#         cursor.execute("SELECT * FROM thuoc WHERE gia = (SELECT MIN(gia) FROM thuoc) LIMIT 1")
#         cheapest = cursor.fetchone()
        
#         # Giá trung bình
#         cursor.execute("SELECT AVG(gia) as avg_price FROM thuoc")
#         avg_price = cursor.fetchone()['avg_price']
        
#         # Thống kê theo đơn vị
#         cursor.execute("SELECT don_vi, COUNT(*) as count FROM thuoc GROUP BY don_vi")
#         unit_stats = cursor.fetchall()
        
#         conn.close()
        
#         statistics = {
#             'total_medicines': total_medicines,
#             'most_expensive': most_expensive,
#             'cheapest': cheapest,
#             'average_price': float(avg_price) if avg_price else 0,
#             'unit_statistics': unit_stats
#         }
        
#         return jsonify(statistics)
#     except Exception as e:
#         return jsonify({'error': f'Lỗi khi lấy thống kê thuốc: {str(e)}'}), 500 