# TÀI LIỆU API HỆ THỐNG QUẢN LÝ PHÒNG KHÁM

## 1. Người dùng (User)

### Lấy danh sách người dùng

- **GET** `/users`
- **Response:**

```json
[
  {
    "email": "string",
    "ma_bac_si": "string|null",
    "ma_benh_nhan": "string|null",
    "role": "string",
    "created_at": "datetime"
  }
]
```

### Thêm người dùng

- **POST** `/users`
- **Request:**

```json
{
  "email": "string",
  "ma_bac_si": "string|null",
  "ma_benh_nhan": "string|null",
  "mat_khau": "string",
  "role": "string"
}
```

- **Response:** `{ "message": "Thêm người dùng thành công" }`

### Đăng nhập

- **POST** `/users/login`
- **Request:**

```json
{
  "email": "string",
  "mat_khau": "string"
}
```

- **Response:** Thông tin người dùng hoặc lỗi

### Cập nhật người dùng

- **PUT** `/users/<email>`
- **Request:**

```json
{
  "ma_bac_si": "string|null",
  "ma_benh_nhan": "string|null",
  "mat_khau": "string",
  "role": "string"
}
```

- **Response:** `{ "message": "Cập nhật người dùng thành công" }`

### Xóa người dùng

- **DELETE** `/users/<email>`
- **Response:** `{ "message": "Xóa người dùng thành công" }`

---

## 2. Bệnh nhân (Patient)

### Lấy danh sách bệnh nhân

- **GET** `/patients`
- **Response:** Danh sách bệnh nhân

### Lấy thông tin bệnh nhân

- **GET** `/patients/<ma_benh_nhan>`
- **Response:** Thông tin bệnh nhân

### Thêm bệnh nhân

- **POST** `/patients`
- **Request:**

```json
{
  "ten_benh_nhan": "string",
  "ngay_sinh": "string",
  "so_dien_thoai": "string",
  "dia_chi": "string",
  "tien_su_benh": "string"
}
```

- **Response:** `{ "message": "Thêm bệnh nhân thành công" }`

### Cập nhật bệnh nhân

- **PUT** `/patients/<ma_benh_nhan>`
- **Request:**

```json
{
  "ten_benh_nhan": "string",
  "ngay_sinh": "string",
  "so_dien_thoai": "string",
  "dia_chi": "string",
  "tien_su_benh": "string"
}
```

- **Response:** `{ "message": "Cập nhật bệnh nhân thành công" }`

### Xóa bệnh nhân

- **DELETE** `/patients/<ma_benh_nhan>`
- **Response:** `{ "message": "Xóa bệnh nhân thành công" }`

---

## 3. Bác sĩ (Doctor)

### Lấy danh sách bác sĩ

- **GET** `/doctors`
- **Response:** Danh sách bác sĩ

### Lấy thông tin bác sĩ

- **GET** `/doctors/<ma_bac_si>`
- **Response:** Thông tin bác sĩ

### Thêm bác sĩ

- **POST** `/doctors`
- **Request:**

```json
{
  "ten_bac_si": "string",
  "ma_chuyen_khoa": "string",
  "so_dien_thoai": "string",
  "kinh_nghiem": "string"
}
```

- **Response:** `{ "message": "Thêm bác sĩ thành công" }`

### Cập nhật bác sĩ

- **PUT** `/doctors/<ma_bac_si>`
- **Request:**

```json
{
  "ten_bac_si": "string",
  "ma_chuyen_khoa": "string",
  "so_dien_thoai": "string",
  "kinh_nghiem": "string"
}
```

- **Response:** `{ "message": "Cập nhật bác sĩ thành công" }`

### Xóa bác sĩ

- **DELETE** `/doctors/<ma_bac_si>`
- **Response:** `{ "message": "Xóa bác sĩ thành công" }`

---

## 4. Chuyên khoa (Specialty)

### Lấy danh sách chuyên khoa

- **GET** `/specialty`
- **Response:** Danh sách chuyên khoa

### Lấy thông tin chuyên khoa

- **GET** `/specialty/<ma_chuyen_khoa>`
- **Response:** Thông tin chuyên khoa

### Thêm chuyên khoa

- **POST** `/specialty`
- **Request:**

```json
{
  "ten_chuyen_khoa": "string",
  "mo_ta": "string"
}
```

- **Response:** `{ "message": "Thêm chuyên khoa thành công" }`

### Cập nhật chuyên khoa

- **PUT** `/specialty/<ma_chuyen_khoa>`
- **Request:**

```json
{
  "ten_chuyen_khoa": "string",
  "mo_ta": "string"
}
```

- **Response:** `{ "message": "Cập nhật chuyên khoa thành công" }`

### Xóa chuyên khoa

- **DELETE** `/specialty/<ma_chuyen_khoa>`
- **Response:** `{ "message": "Xóa chuyên khoa thành công" }`

---

## 5. Lịch hẹn (Booking)

### Lấy danh sách lịch hẹn

- **GET** `/bookings`
- **Response:** Danh sách lịch hẹn

### Thêm lịch hẹn

- **POST** `/bookings`
- **Request:**

```json
{
  "ma_benh_nhan": "string",
  "ma_bac_si": "string",
  "ngay_hen": "string",
  "gio_hen": "string",
  "trang_thai": "string"
}
```

- **Response:** `{ "message": "Đặt lịch hẹn thành công" }`

### Cập nhật lịch hẹn

- **PUT** `/bookings/<ma_lich_hen>`
- **Request:**

```json
{
  "ma_bac_si": "string",
  "ngay_hen": "string",
  "gio_hen": "string",
  "trang_thai": "string"
}
```

- **Response:** `{ "message": "Cập nhật lịch hẹn thành công" }`

### Xóa lịch hẹn

- **DELETE** `/bookings/<ma_lich_hen>`
- **Response:** `{ "message": "Xóa lịch hẹn thành công" }`

---

## 6. Phiếu khám (Medical Exam)

### Lấy danh sách phiếu khám

- **GET** `/medical_exams`
- **Response:** Danh sách phiếu khám

### Thêm phiếu khám

- **POST** `/medical_exams`
- **Request:**

```json
{
  "ma_lich_hen": "string",
  "trieu_chung": "string",
  "chan_doan": "string",
  "ngay_kham": "string"
}
```

- **Response:** `{ "message": "Thêm phiếu khám thành công" }`

### Cập nhật phiếu khám

- **PUT** `/medical_exams/<ma_phieu_kham>`
- **Request:**

```json
{
  "trieu_chung": "string",
  "chan_doan": "string",
  "ngay_kham": "string"
}
```

- **Response:** `{ "message": "Cập nhật phiếu khám thành công" }`

### Xóa phiếu khám

- **DELETE** `/medical_exams/<ma_phieu_kham>`
- **Response:** `{ "message": "Xóa phiếu khám thành công" }`

---

## 7. Đơn thuốc (Prescription)

### Lấy danh sách đơn thuốc

- **GET** `/prescriptions`
- **Response:** Danh sách đơn thuốc

### Thêm đơn thuốc

- **POST** `/prescriptions`
- **Request:**

```json
{
  "ma_phieu_kham": "string",
  "ma_thuoc": "string",
  "so_luong": "int",
  "lieu_dung": "string",
  "cach_dung": "string"
}
```

- **Response:** `{ "message": "Thêm đơn thuốc thành công" }`

### Cập nhật đơn thuốc

- **PUT** `/prescriptions/<ma_don_thuoc>`
- **Request:**

```json
{
  "ma_thuoc": "string",
  "so_luong": "int",
  "lieu_dung": "string",
  "cach_dung": "string"
}
```

- **Response:** `{ "message": "Cập nhật đơn thuốc thành công" }`

### Xóa đơn thuốc

- **DELETE** `/prescriptions/<ma_don_thuoc>`
- **Response:** `{ "message": "Xóa đơn thuốc thành công" }`

---

## 8. Thuốc (Medicine)

### Lấy danh sách thuốc

- **GET** `/medicines`
- **Response:** Danh sách thuốc

### Lấy thông tin thuốc

- **GET** `/medicines/<ma_thuoc>`
- **Response:** Thông tin thuốc

### Thêm thuốc

- **POST** `/medicines`
- **Request:**

```json
{
  "ten_thuoc": "string",
  "don_vi": "string",
  "gia": "int"
}
```

- **Response:** `{ "message": "Thêm thuốc thành công" }`

### Cập nhật thuốc

- **PUT** `/medicines/<ma_thuoc>`
- **Request:**

```json
{
  "ten_thuoc": "string",
  "don_vi": "string",
  "gia": "int"
}
```

- **Response:** `{ "message": "Cập nhật thuốc thành công" }`

### Xóa thuốc

- **DELETE** `/medicines/<ma_thuoc>`
- **Response:** `{ "message": "Xóa thuốc thành công" }`

---

**Lưu ý:**

- Một số endpoint có thể yêu cầu xác thực.
- Các trường dữ liệu có thể thay đổi tùy vào logic thực tế.
- Tham khảo code backend/routes để biết chi tiết hơn về từng API.
