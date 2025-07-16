USE phong_kham;

DELIMITER $$
DROP TRIGGER IF EXISTS CapNhatTrangThaiDaKham $$
CREATE TRIGGER CapNhatTrangThaiDaKham
before INSERT on phieu_kham
for each row
begin
    update lich_hen
    SET trang_thai = 'Đã khám'
    WHERE ma_lich_hen = NEW.ma_lich_hen;
end $$
DELIMITER ;

DELIMITER $$
DROP TRIGGER IF EXISTS CapNhatTrangThaiDaDat $$
CREATE TRIGGER CapNhatTrangThaiDaDat
before insert on lich_hen
for each row
begin
    SET NEW.trang_thai = 'Đã đặt';
end $$
DELIMITER ;

DELIMITER $$
DROP TRIGGER IF EXISTS CapNhatTrangThaiDaHuy $$
CREATE TRIGGER CapNhatTrangThaiDaHuy
BEFORE DELETE ON lich_hen
FOR EACH ROW
BEGIN
    IF EXISTS (SELECT 1 FROM phieu_kham WHERE ma_lich_hen = OLD.ma_lich_hen) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Không thể xóa lịch hẹn đã có phiếu khám';
    ELSE
        UPDATE lich_hen
        SET trang_thai = 'Đã hủy'
        WHERE ma_lich_hen = OLD.ma_lich_hen;
    END IF;
END $$
DELIMITER ;


