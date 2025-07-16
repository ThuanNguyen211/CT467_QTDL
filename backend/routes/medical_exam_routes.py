from flask import Blueprint, request, jsonify
from db import get_connection
from datetime import datetime, timedelta

medical_exam_bp = Blueprint('medical_exam', __name__)

@medical_exam_bp.route('/medical_exams', methods=['GET'])
def get_medical_exams():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM phieu_kham")
    rows = cursor.fetchall()
    conn.close()

    # Chuyển đổi datetime và timedelta thành chuỗi
    for row in rows:
        for key, value in row.items():
            if isinstance(value, (datetime, timedelta)):
                row[key] = str(value)

    return jsonify(rows)

@medical_exam_bp.route('/medical_exams', methods=['POST'])
def add_medical_exam():
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO phieu_kham (ma_lich_hen, trieu_chung, chan_doan, ngay_kham)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(sql, (
        data['ma_lich_hen'],
        data['trieu_chung'],
        data['chan_doan'],
        data['ngay_kham']
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Thêm phiếu khám thành công'}), 200

@medical_exam_bp.route('/medical_exams/<ma_phieu_kham>', methods=['PUT'])
def update_medical_exam(ma_phieu_kham):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE phieu_kham
        SET trieu_chung = %s,
            chan_doan = %s,
            ngay_kham = %s
        WHERE ma_phieu_kham = %s
    """
    cursor.execute(sql, (
        data['trieu_chung'],
        data['chan_doan'],
        data['ngay_kham'],
        ma_phieu_kham
    ))

    conn.commit()
    conn.close()

    return jsonify({'message': 'Cập nhật phiếu khám thành công'}), 200

@medical_exam_bp.route('/medical_exams/<ma_phieu_kham>', methods=['DELETE'])
def delete_medical_exam(ma_phieu_kham):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM phieu_kham WHERE ma_phieu_kham = %s", (ma_phieu_kham,))
    if cursor.fetchone() is None:
        conn.close()
        return jsonify({'error': 'Không tìm thấy phiếu khám'}), 404

    cursor.execute("DELETE FROM phieu_kham WHERE ma_phieu_kham = %s", (ma_phieu_kham,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Xóa phiếu khám thành công'}), 200
