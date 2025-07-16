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
CREATE PROCEDURE LichSuKhamBenhNhan(IN ma_benh_nhan INT, IN ngay DATE)
BEGIN
    SELECT pk.*, lh.ngay_hen, lh.gio_hen, lh.trang_thai, bs.ten_bac_si
    FROM benh_nhan bn
    JOIN lich_hen lh ON lh.ma_benh_nhan = bn.ma_benh_nhan
    JOIN phieu_kham pk ON pk.ma_lich_hen = lh.ma_lich_hen
    JOIN bac_si bs ON lh.ma_bac_si = bs.ma_bac_si
    WHERE bn.ma_benh_nhan = ma_benh_nhan
      AND pk.ngay_kham = ngay;
END $$
DELIMITER ;