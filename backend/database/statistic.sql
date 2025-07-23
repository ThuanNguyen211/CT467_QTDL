USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS ThongKeBenhNhanBacSi $$
CREATE PROCEDURE ThongKeBenhNhanBacSi(
    IN ma_bac_si VARCHAR(10),
    IN ngay INT,
    IN thang INT,
    IN nam INT,
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT 
        bn.ma_benh_nhan,
        bn.ten_benh_nhan,
        DATE(pk.ngay_kham) AS ngay_kham,
        COUNT(DISTINCT pk.ma_phieu_kham) AS so_lan_kham
    FROM bac_si bs
    JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    JOIN benh_nhan bn ON lh.ma_benh_nhan = bn.ma_benh_nhan
    WHERE (ma_bac_si = 'ALL' OR bs.ma_bac_si = ma_bac_si)
      AND (ngay = 0 OR DAY(pk.ngay_kham) = ngay)
      AND (thang = 0 OR MONTH(pk.ngay_kham) = thang)
      AND (nam = 0 OR YEAR(pk.ngay_kham) = nam)
      AND (start_date IS NULL OR pk.ngay_kham >= start_date)
      AND (end_date IS NULL OR pk.ngay_kham <= end_date)
    GROUP BY bn.ma_benh_nhan, bn.ten_benh_nhan, DATE(pk.ngay_kham);
END $$
DELIMITER ;

select * from phieu_kham;
select * from lich_hen;

CALL ThongKeBenhNhanBacSi(1, 18, 7, 2025, NULL, NULL);
CALL ThongKeBenhNhanBacSi(1, 0, 0, 0, '2025-07-01', '2025-07-31');
-- DELIMITER $$
-- DROP PROCEDURE IF EXISTS ThongKeBenhNhanBacSi $$
-- CREATE PROCEDURE ThongKeBenhNhanBacSi(IN ma_bac_si VARCHAR(10), IN thang INT, IN nam INT)
-- BEGIN
--     SELECT DISTINCT pk.ma_phieu_kham, bn.ten_benh_nhan, pk.ngay_kham, pk.trieu_chung, pk.chan_doan, bn.tien_su_benh
--     FROM bac_si bs
--     JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
--     JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
--     JOIN benh_nhan bn ON lh.ma_benh_nhan = bn.ma_benh_nhan
--     WHERE bs.ma_bac_si = ma_bac_si
--       AND MONTH(pk.ngay_kham) = thang
--       AND YEAR(pk.ngay_kham) = nam;
-- END $$
-- DELIMITER ;

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


SHOW GRANTS FOR CURRENT_USER();

SHOW PROCEDURE STATUS WHERE Db = 'phong_kham';