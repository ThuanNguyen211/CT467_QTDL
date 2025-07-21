USE phong_kham;

INSERT INTO chuyen_khoa (ten_chuyen_khoa, mo_ta) VALUES
('Nội khoa', 'Chuyên khoa nội'),
('Ngoại khoa', 'Chuyên khoa ngoại'),
('Nhi khoa', 'Chuyên khoa nhi');

INSERT INTO bac_si (ten_bac_si, ma_chuyen_khoa, so_dien_thoai, kinh_nghiem) VALUES
('Nguyen Van A', 1, '0912345678', 10),
('Tran Thi B', 2, '0912345679', 8),
('Le Van C', 3, '0912345680', 5);

INSERT INTO benh_nhan (ten_benh_nhan, ngay_sinh, so_dien_thoai, dia_chi, tien_su_benh) VALUES
('Pham Thi D', '1990-05-15', '0901234567', '123 Đường A, Hà Nội', 'Không'),
('Hoang Van E', '1985-08-20', '0901234568', '456 Đường B, TP.HCM', 'Tiểu đường'),
('Nguyen Thi F', '1995-03-10', '0901234569', '789 Đường C, Đà Nẵng', 'Không');

INSERT INTO thuoc (ten_thuoc, don_vi, gia) VALUES
('Paracetamol', 'Viên', 5000.0),
('Amoxicillin', 'Hộp', 25000.0),
('Ibuprofen', 'Viên', 7000.0);

INSERT INTO lich_hen (ma_benh_nhan, ma_bac_si, ngay_hen, gio_hen, trang_thai) VALUES
(1, 1,'2025-07-12', '09:00:00', 'Đã đặt'),
(2, 2,'2025-07-13', '14:00:00', 'Đã khám'),
(3, 3,'2025-07-14', '10:00:00', 'Đã hủy');

INSERT INTO phieu_kham (ma_lich_hen, trieu_chung, chan_doan, ngay_kham) VALUES
(1, 'Sốt, ho', 'Cảm lạnh', '2025-07-12'),
(2, 'Đau bụng', 'Viêm dạ dày', '2025-07-13'),
(3, 'Sốt cao', 'Nhiễm virus', '2025-07-14');

INSERT INTO don_thuoc (ma_phieu_kham, ma_thuoc, so_luong, lieu_dung, cach_dung) VALUES
(1, 1, 10, '1 viên/lần', 'Uống sau ăn'),
(2, 2, 5, '1 hộp/lần', 'Uống trước ăn'),
(3, 1, 15, '1 viên/lần', 'Uống sau ăn');

INSERT INTO nguoi_dung (email, ma_bac_si, ma_benh_nhan, mat_khau, role) VALUES
('bs01@gmail.com', 1, NULL, '123456', 'bac_si'),
('bn01@gmail.com', NULL, 1, '123456', 'benh_nhan'),
('bs02@gmail.com', 2, NULL, '123456', 'bac_si');