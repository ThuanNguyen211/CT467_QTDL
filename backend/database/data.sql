USE phong_kham;

INSERT INTO chuyen_khoa (ma_chuyen_khoa, ten_chuyen_khoa, mo_ta, so_dien_thoai, kinh_nghiem) VALUES
('CK01', 'Nội khoa', 'Chuyên khoa nội', '0987654321', 15),
('CK02', 'Ngoại khoa', 'Chuyên khoa ngoại', '0987654322', 10),
('CK03', 'Nhi khoa', 'Chuyên khoa nhi', '0987654323', 8);

INSERT INTO bac_si (ma_bac_si, ten_bac_si, ma_chuyen_khoa, so_dien_thoai, kinh_nghiem) VALUES
('BS01', 'Nguyen Van A', 'CK01', '0912345678', 10),
('BS02', 'Tran Thi B', 'CK02', '0912345679', 8),
('BS03', 'Le Van C', 'CK03', '0912345680', 5);

INSERT INTO benh_nhan (ma_benh_nhan, ten_benh_nhan, ngay_sinh, so_dien_thoai, dia_chi, tien_su_benh) VALUES
('BN01', 'Pham Thi D', '1990-05-15', '0901234567', '123 Đường A, Hà Nội', 'Không'),
('BN02', 'Hoang Van E', '1985-08-20', '0901234568', '456 Đường B, TP.HCM', 'Tiểu đường'),
('BN03', 'Nguyen Thi F', '1995-03-10', '0901234569', '789 Đường C, Đà Nẵng', 'Không');

INSERT INTO thuoc (ma_thuoc, ten_thuoc, don_vi, gia) VALUES
('TH01', 'Paracetamol', 'Viên', 5000.0),
('TH02', 'Amoxicillin', 'Hộp', 25000.0),
('TH03', 'Ibuprofen', 'Viên', 7000.0);

INSERT INTO lich_hen (ma_lich_hen, ma_benh_nhan, ma_bac_si, ngay_hen, gio_hen, trang_thai) VALUES
('LH01', 'BN01', 'BS01', '2025-07-12', '09:00:00', 'Chưa khám'),
('LH02', 'BN02', 'BS02', '2025-07-13', '14:00:00', 'Chưa khám'),
('LH03', 'BN03', 'BS03', '2025-07-14', '10:00:00', 'Chưa khám');

INSERT INTO phieu_kham (ma_phieu_kham, ma_lich_hen, trieu_chung, chan_doan, ngay_kham) VALUES
('PK01', 'LH01', 'Sốt, ho', 'Cảm lạnh', '2025-07-12'),
('PK02', 'LH02', 'Đau bụng', 'Viêm dạ dày', '2025-07-13'),
('PK03', 'LH03', 'Sốt cao', 'Nhiễm virus', '2025-07-14');

INSERT INTO don_thuoc (ma_don_thuoc, ma_phieu_kham, ma_thuoc, so_luong, lieu_dung, cach_dung) VALUES
('DT01', 'PK01', 'TH01', 10, '1 viên/lần', 'Uống sau ăn'),
('DT02', 'PK02', 'TH02', 5, '1 hộp/lần', 'Uống trước ăn'),
('DT03', 'PK03', 'TH01', 15, '1 viên/lần', 'Uống sau ăn');

INSERT INTO nguoi_dung (email, ma_bac_si, ma_benh_nhan, mat_khau, role) VALUES
('bs01@gmail.com', 'BS01', NULL, '123456', 'bac_si'),
('bn01@gmail.com', NULL, 'BN01', '123456', 'benh_nhan'),
('bs02@gmail.com', 'BS02', NULL, '123456', 'bac_si');