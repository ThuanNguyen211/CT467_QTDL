USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS TraCuuBacSi $$
CREATE PROCEDURE TraCuuBacSi(IN chuyen_khoa VARCHAR(10), IN nam_kinh_nghiem INT)
BEGIN
    SELECT * FROM bac_si 
    WHERE ma_chuyen_khoa = chuyen_khoa 
      AND kinh_nghiem >= nam_kinh_nghiem;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS LichHenBacSiTheoNgay $$
CREATE PROCEDURE LichHenBacSiTheoNgay(IN bac_si VARCHAR(10), IN ngay date)
BEGIN
    SELECT lh.* FROM bac_si bs
    JOIN lich_hen lh on lh.ma_bac_si = bs.ma_bac_si
    WHERE bs.ma_bac_si = bac_si AND lh.ngay_hen = ngay;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS LichHenBacSiTheoTrangThai $$
CREATE PROCEDURE LichHenBacSiTheoTrangThai(IN bac_si VARCHAR(10), IN trang_thai VARCHAR(20))
BEGIN
    SELECT lh.* FROM bac_si bs
    JOIN lich_hen lh on lh.ma_bac_si = bs.ma_bac_si
    WHERE bs.ma_bac_si = bac_si AND lh.trang_thai = trang_thai;
END $$
DELIMITER ;

DELIMITER $$
DROP PROCEDURE IF EXISTS DanhSachKhungGioTrong $$
CREATE PROCEDURE DanhSachKhungGioTrong(IN ma_bac_si VARCHAR(10), IN ngay DATE)
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