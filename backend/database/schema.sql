DROP SCHEMA phong_kham;

CREATE DATABASE phong_kham;

USE phong_kham;

CREATE TABLE chuyen_khoa (
    ma_chuyen_khoa VARCHAR(10) PRIMARY KEY,
    ten_chuyen_khoa VARCHAR(100) NOT NULL,
    mo_ta TEXT
);

CREATE TABLE bac_si (
    ma_bac_si VARCHAR(10) PRIMARY KEY,
    ten_bac_si VARCHAR(100) NOT NULL,
    ma_chuyen_khoa VARCHAR(10),
    so_dien_thoai VARCHAR(20),
    kinh_nghiem INT,
    FOREIGN KEY (ma_chuyen_khoa) REFERENCES chuyen_khoa(ma_chuyen_khoa)
);

CREATE TABLE benh_nhan (
    ma_benh_nhan VARCHAR(10) PRIMARY KEY,
    ten_benh_nhan VARCHAR(100) NOT NULL,
    ngay_sinh DATE,
    so_dien_thoai VARCHAR(20),
    dia_chi VARCHAR(255),
    tien_su_benh TEXT
);

CREATE TABLE lich_hen (
    ma_lich_hen VARCHAR(10) PRIMARY KEY,
    ma_benh_nhan VARCHAR(10),
    ma_bac_si VARCHAR(10),
    ngay_hen DATE,
    gio_hen TIME,
    trang_thai VARCHAR(20),
    FOREIGN KEY (ma_benh_nhan) REFERENCES benh_nhan(ma_benh_nhan),
    FOREIGN KEY (ma_bac_si) REFERENCES bac_si(ma_bac_si)
);

CREATE TABLE phieu_kham (
    ma_phieu_kham VARCHAR(10) PRIMARY KEY,
    ma_lich_hen VARCHAR(10),
    trieu_chung TEXT,
    chan_doan TEXT,
    ngay_kham DATE,
    FOREIGN KEY (ma_lich_hen) REFERENCES lich_hen(ma_lich_hen)
);

CREATE TABLE thuoc (
    ma_thuoc VARCHAR(10) PRIMARY KEY,
    ten_thuoc VARCHAR(100) NOT NULL,
    don_vi VARCHAR(50),
    gia FLOAT
);

CREATE TABLE don_thuoc (
    ma_don_thuoc VARCHAR(10) PRIMARY KEY,
    ma_phieu_kham VARCHAR(10),
    ma_thuoc VARCHAR(10),
    so_luong INT,
    lieu_dung VARCHAR(100),
    cach_dung VARCHAR(255),
    FOREIGN KEY (ma_phieu_kham) REFERENCES phieu_kham(ma_phieu_kham),
    FOREIGN KEY (ma_thuoc) REFERENCES thuoc(ma_thuoc)
);

CREATE TABLE nguoi_dung (
    email VARCHAR(20) PRIMARY KEY,
    ma_bac_si VARCHAR(10),
    ma_benh_nhan VARCHAR(10),
    mat_khau VARCHAR(255) NOT NULL,
    role ENUM('bac_si', 'benh_nhan') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bac_si FOREIGN KEY (ma_bac_si) REFERENCES bac_si(ma_bac_si) ON DELETE CASCADE,
    CONSTRAINT fk_benh_nhan FOREIGN KEY (ma_benh_nhan) REFERENCES benh_nhan(ma_benh_nhan) ON DELETE SET NULL
);