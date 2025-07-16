USE phong_kham;

DELIMITER $$
DROP PROCEDURE IF EXISTS TraCuuBacSi $$
CREATE PROCEDURE TraCuuBacSi(IN chuyen_khoa INT, IN nam_kinh_nghiem INT)
BEGIN
    SELECT * FROM bac_si 
    WHERE ma_chuyen_khoa = chuyen_khoa 
      AND kinh_nghiem >= nam_kinh_nghiem;
END $$
DELIMITER ;