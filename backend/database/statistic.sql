USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS ThongKeBenhNhanBacSi $$
CREATE PROCEDURE ThongKeBenhNhanBacSi(IN ma_bac_si VARCHAR(10), IN thang INT, IN nam INT)
BEGIN
    SELECT DISTINCT pk.ma_phieu_kham, bn.ten_benh_nhan, pk.ngay_kham, pk.trieu_chung, pk.chan_doan, bn.tien_su_benh
    FROM bac_si bs
    JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    JOIN benh_nhan bn ON lh.ma_benh_nhan = bn.ma_benh_nhan
    WHERE bs.ma_bac_si = ma_bac_si
      AND MONTH(pk.ngay_kham) = thang
      AND YEAR(pk.ngay_kham) = nam;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS ThongKeBenhNhanChuyenKhoa $$
CREATE PROCEDURE ThongKeBenhNhanChuyenKhoa(IN ma_chuyen_khoa INT)
BEGIN
    SELECT COUNT(DISTINCT lh.ma_benh_nhan) AS so_benh_nhan
    FROM bac_si bs
    JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    WHERE bs.ma_chuyen_khoa = ma_chuyen_khoa;
END $$
DELIMITER ;