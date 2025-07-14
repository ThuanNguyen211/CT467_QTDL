DELIMITER $$
CREATE TRIGGER cap_nhat_trang_thai_da_kham
before INSERT on phieu_kham
for each row
begin
    update lich_hen
    SET trang_thai = 'Đã khám'
    WHERE ma_lich_hen = NEW.ma_lich_hen;
end $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER cap_nhat_trang_thai_da_dat
before insert on lich_hen
for each row
begin
    SET NEW.trang_thai = 'Đã đặt';
end $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER cap_nhat_trang_thai_da_huy
BEFORE UPDATE ON lich_hen
FOR EACH ROW
BEGIN
    IF NEW.trang_thai = 'Hủy' THEN
        SET NEW.trang_thai = 'Đã hủy';
    END IF;
END$$
DELIMITER ;




