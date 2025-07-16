USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS LichHenBacSiTheoNgay $$
CREATE PROCEDURE LichHenBacSiTheoNgay(IN bac_si INT, IN ngay date)
BEGIN
    SELECT lh.* FROM bac_si bs
    JOIN lich_hen lh on lh.ma_bac_si = bs.ma_bac_si
    WHERE bs.ma_bac_si = bac_si AND lh.ngay_hen = ngay;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS LichHenBacSiTheoTrangThai $$
CREATE PROCEDURE LichHenBacSiTheoTrangThai(IN bac_si INT, IN trang_thai VARCHAR(20))
BEGIN
    SELECT lh.* FROM bac_si bs
    JOIN lich_hen lh on lh.ma_bac_si = bs.ma_bac_si
    WHERE bs.ma_bac_si = bac_si AND lh.trang_thai = trang_thai;
END $$
DELIMITER ;
