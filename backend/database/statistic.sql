USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS ThongKeBenhNhanBacSi $$
CREATE PROCEDURE ThongKeBenhNhanBacSi(IN ma_bac_si VARCHAR(10), IN thang INT, IN nam INT)
BEGIN
    SELECT COUNT(DISTINCT lh.ma_benh_nhan) AS so_benh_nhan
    FROM bac_si bs
    JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    WHERE bs.ma_bac_si = ma_bac_si
      AND MONTH(pk.ngay_kham) = thang
      AND YEAR(pk.ngay_kham) = nam;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS ThongKeBenhNhanChuyenKhoa $$
CREATE PROCEDURE ThongKeBenhNhanChuyenKhoa(IN ma_chuyen_khoa VARCHAR(10))
BEGIN
    SELECT COUNT(DISTINCT lh.ma_benh_nhan) AS so_benh_nhan
    FROM bac_si bs
    JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    WHERE bs.ma_chuyen_khoa = ma_chuyen_khoa;
END $$
DELIMITER ;