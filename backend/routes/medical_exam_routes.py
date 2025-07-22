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

@medical_exam_bp.route('/medical_exams/<int:ma_phieu_kham>', methods=['GET'])
def get_medical_exam_by_id(ma_phieu_kham):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    sql = """
        SELECT pk.ma_phieu_kham, pk.ngay_kham, pk.trieu_chung, pk.chan_doan,
               bn.ten_benh_nhan
        FROM phieu_kham pk
        JOIN lich_hen lh ON pk.ma_lich_hen = lh.ma_lich_hen
        JOIN benh_nhan bn ON lh.ma_benh_nhan = bn.ma_benh_nhan
        WHERE pk.ma_phieu_kham = %s
    """
    cursor.execute(sql, (ma_phieu_kham,))
    exam = cursor.fetchone()

    conn.close()

    if not exam:
        return jsonify({'error': 'Không tìm thấy phiếu khám'}), 404

    return jsonify(exam), 200


@medical_exam_bp.route('/medical_exams', methods=['POST'])
def create_medical_exam():
    try:
        data = request.json
        ma_lich_hen = data.get('ma_lich_hen')
        trieu_chung = data.get('trieu_chung')
        chan_doan = data.get('chan_doan')
        ngay_kham = data.get('ngay_kham')
        don_thuoc = data.get('don_thuoc', [])

        conn = get_connection()
        cursor = conn.cursor()

        # 1. Tạo phiếu khám
        sql_insert_exam = """
            INSERT INTO phieu_kham (ma_lich_hen, trieu_chung, chan_doan, ngay_kham)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql_insert_exam, (ma_lich_hen, trieu_chung, chan_doan, ngay_kham))
        ma_phieu_kham = cursor.lastrowid

        # 2. Ghi đơn thuốc (nếu có)
        for item in don_thuoc:
            sql_don_thuoc = """
                INSERT INTO don_thuoc (ma_phieu_kham, ma_thuoc, lieu_dung, cach_dung)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_don_thuoc, (
                ma_phieu_kham,
                item.get('ma_thuoc'),
                item.get('lieu_dung'),
                item.get('cach_dung')
            ))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Tạo phiếu khám thành công'}), 201

    except Exception as e:
        return jsonify({'error': f'Lỗi khi tạo phiếu khám: {str(e)}'}), 500

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
