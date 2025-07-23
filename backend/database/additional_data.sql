USE phong_kham;

-- Thêm chuyên khoa mới
INSERT INTO chuyen_khoa (ten_chuyen_khoa, mo_ta) VALUES
('Tim mạch', 'Chuyên khoa về bệnh tim và mạch máu'),
('Da liễu', 'Chuyên khoa về da và các bệnh liên quan'),
('Thần kinh', 'Chuyên khoa về hệ thần kinh');

-- Thêm bác sĩ mới
INSERT INTO bac_si (ten_bac_si, ma_chuyen_khoa, so_dien_thoai, kinh_nghiem) VALUES
('Pham Van G', 4, '0912345681', 12),
('Hoang Thi H', 5, '0912345682', 7),
('Nguyen Van I', 6, '0912345683', 9),
('Tran Thi K', 1, '0912345684', 15),
('Le Van L', 2, '0912345685', 6),
('Vo Thi M', 3, '0912345686', 10);

-- Thêm bệnh nhân mới
INSERT INTO benh_nhan (ten_benh_nhan, ngay_sinh, so_dien_thoai, dia_chi, tien_su_benh) VALUES
('Tran Van N', '1988-11-25', '0901234570', '101 Đường D, Hà Nội', 'Tăng huyết áp'),
('Nguyen Thi P', '1992-07-30', '0901234571', '202 Đường E, TP.HCM', 'Không'),
('Le Van Q', '1980-04-12', '0901234572', '303 Đường F, Đà Nẵng', 'Viêm gan B'),
('Pham Thi R', '1998-09-05', '0901234573', '404 Đường G, Hải Phòng', 'Không'),
('Hoang Van S', '1975-12-20', '0901234574', '505 Đường H, Cần Thơ', 'Tiểu đường'),
('Vo Thi T', '1993-06-15', '0901234575', '606 Đường I, Hà Nội', 'Không'),
('Nguyen Van T', '1987-02-14', '0901234576', '707 Đường J, Hà Nội', 'Không'),
('Tran Thi U', '1994-06-22', '0901234577', '808 Đường K, TP.HCM', 'Dị ứng'),
('Le Van V', '1978-09-10', '0901234578', '909 Đường L, Đà Nẵng', 'Tiểu đường'),
('Pham Thi W', '1990-12-05', '0901234579', '1010 Đường M, Hải Phòng', 'Không'),
('Hoang Van X', '1983-03-18', '0901234580', '1111 Đường N, Cần Thơ', 'Tăng huyết áp'),
('Vo Thi Y', '1996-08-30', '0901234581', '1212 Đường P, Hà Nội', 'Không');

-- Thêm thuốc mới
INSERT INTO thuoc (ten_thuoc, don_vi, gia) VALUES
('Aspirin', 'Viên', 6000.0),
('Metformin', 'Viên', 8000.0),
('Loratadine', 'Viên', 5500.0),
('Cefixime', 'Viên', 12000.0),
('Omeprazole', 'Viên', 9000.0),
('Vitamin C', 'Viên', 4000.0);

-- Thêm lịch hẹn mới
SET FOREIGN_KEY_CHECKS = 0;
SELECT * FROM lich_hen;
INSERT INTO lich_hen (ma_benh_nhan, ma_bac_si, ngay_hen, gio_hen, trang_thai) VALUES
(1, 1, '2025-07-15', '15:00:00', 'Đã khám'),
(5, 5, '2025-07-15', '10:00:00', 'Đã khám'),
(6, 6, '2025-07-15', '13:00:00', 'Đã khám'),
(4, 1, '2025-07-16', '09:30:00', 'Đã khám'),
(5, 2, '2025-07-16', '14:30:00', 'Đã khám'),
(6, 3, '2025-07-16', '11:00:00', 'Đã khám'),
(1, 4, '2025-07-17', '08:30:00', 'Đã khám'),
(2, 5, '2025-07-17', '15:00:00', 'Đã khám'),
(3, 6, '2025-07-17', '10:30:00', 'Đã khám'),
(7, 1, '2025-07-18', '08:00:00', 'Đã khám'),
(8, 1, '2025-07-18', '09:00:00', 'Đã khám'),
(9, 1, '2025-07-18', '10:00:00', 'Đã khám'),
(10, 1, '2025-07-19', '08:30:00', 'Đã khám'),
(11, 1, '2025-07-19', '09:30:00', 'Đã khám'),
(12, 1, '2025-07-19', '10:30:00', 'Đã khám'),
(1, 1, '2025-07-20', '08:00:00', 'Đã đặt'),
(7, 1, '2025-07-20', '09:00:00', 'Đã đặt'),
(8, 1, '2025-07-20', '10:00:00', 'Đã hủy'),
(9, 1, '2025-07-21', '08:30:00', 'Đã đặt'),
(10, 1, '2025-07-21', '09:30:00', 'Đã hủy');

-- Thêm phiếu khám mới
INSERT INTO phieu_kham (ma_lich_hen, trieu_chung, chan_doan, ngay_kham) VALUES
(65, 'Đau ngực, khó thở', 'Bệnh tim mạch', '2025-07-15'),
(46, 'Phát ban, ngứa', 'Viêm da dị ứng', '2025-07-15'),
(47, 'Đau đầu, chóng mặt', 'Rối loạn tiền đình', '2025-07-15'),
(48, 'Sốt, đau họng', 'Viêm họng', '2025-07-16'),
(49, 'Đau bụng, tiêu chảy', 'Rối loạn tiêu hóa', '2025-07-16'),
(50, 'Sốt, mệt mỏi', 'Cảm cúm', '2025-07-16'),
(51, 'Tức ngực', 'Tăng huyết áp', '2025-07-17'),
(52, 'Nổi mẩn đỏ', 'Dị ứng da', '2025-07-17'),
(53, 'Đau đầu, mất ngủ', 'Suy nhược thần kinh', '2025-07-17'),
(54, 'Sốt, đau họng', 'Viêm họng cấp', '2025-07-18'),
(55, 'Mệt mỏi, đau đầu', 'Thiếu máu', '2025-07-18'),
(56, 'Đau bụng, buồn nôn', 'Rối loạn tiêu hóa', '2025-07-18'),
(57, 'Ho, khó thở', 'Viêm phế quản', '2025-07-19'),
(58, 'Tức ngực, hồi hộp', 'Rối loạn nhịp tim', '2025-07-19'),
(59, 'Đau lưng, mệt mỏi', 'Thoái hóa cột sống', '2025-07-19');
SELECT * FROM bac_si;
-- Thêm đơn thuốc mới
INSERT INTO don_thuoc (ma_phieu_kham, ma_thuoc, so_luong, lieu_dung, cach_dung) VALUES
(4, 4, 20, '1 viên/lần', 'Uống sau ăn'),
(5, 5, 10, '1 viên/lần', 'Uống trước ăn'),
(6, 6, 15, '1 viên/lần', 'Uống buổi tối'),
(7, 1, 12, '1 viên/lần', 'Uống sau ăn'),
(8, 2, 7, '1 hộp/lần', 'Uống trước ăn'),
(9, 3, 10, '1 viên/lần', 'Uống sau ăn'),
(10, 4, 15, '1 viên/lần', 'Uống sáng tối'),
(11, 5, 8, '1 viên/lần', 'Uống trước ăn'),
(12, 6, 20, '1 viên/lần', 'Uống buổi tối'),
(13, 7, 10, '1 viên/lần', 'Uống sau ăn'),
(14, 8, 14, '1 viên/lần', 'Uống trước ăn'),
(15, 9, 20, '1 viên/lần', 'Uống buổi sáng'),
(16, 7, 12, '1 viên/lần', 'Uống sau ăn'),
(17, 8, 10, '1 viên/lần', 'Uống trước ăn'),
(18, 9, 15, '1 viên/lần', 'Uống buổi tối');


-- Thêm người dùng mới
INSERT INTO nguoi_dung (email, ma_bac_si, ma_benh_nhan, mat_khau, role) VALUES
('bs04@gmail.com', 4, NULL, '123456', 'bac_si'),
('bs05@gmail.com', 5, NULL, '123456', 'bac_si'),
('bs06@gmail.com', 6, NULL, '123456', 'bac_si'),
('bn04@gmail.com', NULL, 4, '123456', 'benh_nhan'),
('bn05@gmail.com', NULL, 5, '123456', 'benh_nhan'),
('bn06@gmail.com', NULL, 6, '123456', 'benh_nhan'),
('bs07@gmail.com', 7, NULL, '123456', 'bac_si'),
('bs08@gmail.com', 8, NULL, '123456', 'bac_si'),
('bs09@gmail.com', 9, NULL, '123456', 'bac_si'),
('bn07@gmail.com', NULL, 7, '123456', 'benh_nhan'),
('bn08@gmail.com', NULL, 8, '123456', 'benh_nhan'),
('bn09@gmail.com', NULL, 9, '123456', 'benh_nhan'),
('bn10@gmail.com', NULL, 10, '123456', 'benh_nhan'),
('bn11@gmail.com', NULL, 11, '123456', 'benh_nhan'),
('bn12@gmail.com', NULL, 12, '123456', 'benh_nhan');