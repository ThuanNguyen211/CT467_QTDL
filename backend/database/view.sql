USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS DanhSachKhungGioTrong $$
CREATE PROCEDURE DanhSachKhungGioTrong(IN ma_bac_si INT, IN ngay DATE)
BEGIN
    SET @start_hour = 8;
    SET @end_hour = 17;
    
    CREATE TEMPORARY TABLE possible_hours (
        gio TIME
    );
    
    WHILE @start_hour <= @end_hour DO
        INSERT INTO possible_hours (gio) 
        VALUES (MAKETIME(@start_hour, 0, 0));
        SET @start_hour = @start_hour + 1;
    END WHILE;
    
    SELECT TIME_FORMAT(ph.gio, '%H:%i:%s') AS gio
    FROM possible_hours ph
    WHERE ph.gio NOT IN (
        SELECT gio_hen 
        FROM lich_hen 
        WHERE ma_bac_si = ma_bac_si 
        AND ngay_hen = ngay 
        AND trang_thai IN ('Đã đặt', 'Đã khám')
    )
    ORDER BY ph.gio;
    
    DROP TEMPORARY TABLE possible_hours;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS LichSuKhamBenhNhan $$
CREATE PROCEDURE LichSuKhamBenhNhan(IN ma_benh_nhan VARCHAR(10))
BEGIN
    SELECT pk.ma_phieu_kham, bs.ten_bac_si, pk.ngay_kham, pk.trieu_chung, pk.chan_doan, bn.tien_su_benh
    FROM benh_nhan bn
    JOIN lich_hen lh ON lh.ma_benh_nhan = bn.ma_benh_nhan
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    JOIN bac_si bs ON lh.ma_bac_si = bs.ma_bac_si
    WHERE bn.ma_benh_nhan = ma_benh_nhan;
END $$
DELIMITER ;

CALL LichSuKhamBenhNhan(1);

DELIMITER $$
DROP PROCEDURE IF EXISTS LichSuKhamBacSi $$
CREATE PROCEDURE LichSuKhamBacSi(IN ma_bac_si VARCHAR(10))
BEGIN
    SELECT DISTINCT pk.ma_phieu_kham, bn.ten_benh_nhan, pk.ngay_kham, pk.trieu_chung, pk.chan_doan, bn.tien_su_benh
    FROM bac_si bs
    JOIN lich_hen lh ON lh.ma_bac_si = bs.ma_bac_si
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    JOIN benh_nhan bn ON lh.ma_benh_nhan = bn.ma_benh_nhan
    WHERE bs.ma_bac_si = ma_bac_si;
END $$
DELIMITER ;

