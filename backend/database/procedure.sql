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


DELIMITER $$
DROP PROCEDURE IF EXISTS LichHenCuaToi $$
CREATE PROCEDURE LichHenCuaToi(IN benh_nhan INT)
BEGIN
    SELECT lh.*, bs.ten_bac_si FROM benh_nhan bn
    JOIN lich_hen lh on lh.ma_benh_nhan = bn.ma_benh_nhan
    JOIN bac_si bs on bs.ma_bac_si = lh.ma_bac_si
    WHERE bn.ma_benh_nhan = benh_nhan;
END $$
DELIMITER ;