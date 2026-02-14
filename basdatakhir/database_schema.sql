-- ============================================
-- Sistem Informasi Manajemen Café
-- Database Schema
-- ============================================

-- Create database
CREATE DATABASE IF NOT EXISTS cafe_management;
USE cafe_management;

-- ============================================
-- Table: users
-- Purpose: Store user authentication data
-- ============================================
CREATE TABLE users (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'kasir', 'manager') DEFAULT 'kasir',
    nama_lengkap VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: menu
-- Purpose: Store café menu items
-- ============================================
CREATE TABLE menu (
    id_menu INT AUTO_INCREMENT PRIMARY KEY,
    nama_menu VARCHAR(100) NOT NULL,
    kategori ENUM('Minuman', 'Makanan', 'Snack', 'Dessert') NOT NULL,
    harga DECIMAL(10, 2) NOT NULL,
    stok INT DEFAULT 0,
    deskripsi TEXT,
    gambar VARCHAR(255),
    status ENUM('tersedia', 'habis') DEFAULT 'tersedia',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_kategori (kategori),
    INDEX idx_nama (nama_menu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: pelanggan
-- Purpose: Store customer information
-- ============================================
CREATE TABLE pelanggan (
    id_pelanggan INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    no_hp VARCHAR(20),
    email VARCHAR(100),
    alamat TEXT,
    poin_member INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_nama (nama),
    INDEX idx_no_hp (no_hp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: transaksi
-- Purpose: Store transaction headers
-- ============================================
CREATE TABLE transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATETIME DEFAULT CURRENT_TIMESTAMP,
    id_pelanggan INT,
    id_user INT,
    total DECIMAL(10, 2) NOT NULL,
    metode_pembayaran ENUM('tunai', 'kartu', 'e-wallet') DEFAULT 'tunai',
    status ENUM('selesai', 'dibatalkan') DEFAULT 'selesai',
    catatan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tanggal (tanggal),
    INDEX idx_pelanggan (id_pelanggan),
    FOREIGN KEY (id_pelanggan) REFERENCES pelanggan(id_pelanggan) ON DELETE SET NULL,
    FOREIGN KEY (id_user) REFERENCES users(id_user) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Table: detail_transaksi
-- Purpose: Store transaction line items
-- ============================================
CREATE TABLE detail_transaksi (
    id_detail INT AUTO_INCREMENT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    id_menu INT NOT NULL,
    jumlah INT NOT NULL,
    harga_satuan DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    catatan TEXT,
    INDEX idx_transaksi (id_transaksi),
    INDEX idx_menu (id_menu),
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi) ON DELETE CASCADE,
    FOREIGN KEY (id_menu) REFERENCES menu(id_menu) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================
-- Sample Data
-- ============================================

-- Insert admin user (password: admin123 - hashed with werkzeug)
-- Hash generated with: generate_password_hash('admin123')
INSERT INTO users (username, password, role, nama_lengkap) VALUES
('admin', 'scrypt:32768:8:1$Z1AeWgz7PZKfaqgM$5d2e45970e483694341b91bc28ac76fce188a5896d8e48fbaa8172ae762ba048af8402320169fa4265aee6f938b0d9a64695e9d0a817762f9971c383c76f47b1', 'admin', 'Administrator'),
('kasir1', 'scrypt:32768:8:1$Z1AeWgz7PZKfaqgM$5d2e45970e483694341b91bc28ac76fce188a5896d8e48fbaa8172ae762ba048af8402320169fa4265aee6f938b0d9a64695e9d0a817762f9971c383c76f47b1', 'kasir', 'Kasir Satu');

-- Insert sample menu items
INSERT INTO menu (nama_menu, kategori, harga, stok, deskripsi, status) VALUES
('Espresso', 'Minuman', 15000.00, 100, 'Kopi espresso klasik', 'tersedia'),
('Cappuccino', 'Minuman', 25000.00, 100, 'Espresso dengan susu foam', 'tersedia'),
('Latte', 'Minuman', 28000.00, 100, 'Espresso dengan steamed milk', 'tersedia'),
('Americano', 'Minuman', 20000.00, 100, 'Espresso dengan air panas', 'tersedia'),
('Mocha', 'Minuman', 30000.00, 100, 'Latte dengan cokelat', 'tersedia'),
('Green Tea Latte', 'Minuman', 28000.00, 80, 'Latte dengan matcha', 'tersedia'),
('Chocolate', 'Minuman', 25000.00, 90, 'Cokelat panas premium', 'tersedia'),
('Iced Coffee', 'Minuman', 22000.00, 100, 'Kopi dingin segar', 'tersedia'),
('Croissant', 'Makanan', 18000.00, 50, 'Croissant butter premium', 'tersedia'),
('Sandwich', 'Makanan', 35000.00, 40, 'Sandwich ayam dengan sayuran', 'tersedia'),
('Pasta Carbonara', 'Makanan', 45000.00, 30, 'Pasta dengan saus carbonara', 'tersedia'),
('Nasi Goreng', 'Makanan', 38000.00, 35, 'Nasi goreng spesial café', 'tersedia'),
('French Fries', 'Snack', 20000.00, 60, 'Kentang goreng crispy', 'tersedia'),
('Chicken Wings', 'Snack', 32000.00, 45, 'Sayap ayam goreng pedas', 'tersedia'),
('Donut', 'Dessert', 12000.00, 70, 'Donut dengan berbagai topping', 'tersedia'),
('Cheesecake', 'Dessert', 28000.00, 25, 'Cheesecake New York style', 'tersedia'),
('Tiramisu', 'Dessert', 32000.00, 20, 'Tiramisu klasik Italia', 'tersedia'),
('Ice Cream', 'Dessert', 18000.00, 50, 'Es krim vanilla premium', 'tersedia');

-- Insert sample customers
INSERT INTO pelanggan (nama, no_hp, email, poin_member) VALUES
('Budi Santoso', '081234567890', 'budi@email.com', 150),
('Siti Nurhaliza', '081234567891', 'siti@email.com', 200),
('Ahmad Rizki', '081234567892', 'ahmad@email.com', 80),
('Dewi Lestari', '081234567893', 'dewi@email.com', 120),
('Eko Prasetyo', '081234567894', 'eko@email.com', 50),
('Fitri Handayani', '081234567895', 'fitri@email.com', 180),
('Gunawan', '081234567896', 'gunawan@email.com', 90),
('Hana Permata', '081234567897', 'hana@email.com', 110);

-- Insert sample transactions
INSERT INTO transaksi (tanggal, id_pelanggan, id_user, total, metode_pembayaran, status) VALUES
('2026-01-01 10:30:00', 1, 1, 53000.00, 'tunai', 'selesai'),
('2026-01-01 14:15:00', 2, 1, 78000.00, 'kartu', 'selesai'),
('2026-01-02 09:20:00', 3, 1, 45000.00, 'e-wallet', 'selesai'),
('2026-01-02 11:45:00', 4, 1, 96000.00, 'tunai', 'selesai'),
('2026-01-03 13:30:00', 5, 1, 62000.00, 'kartu', 'selesai'),
('2026-01-05 10:00:00', 1, 1, 83000.00, 'tunai', 'selesai'),
('2026-01-08 15:20:00', 6, 1, 55000.00, 'e-wallet', 'selesai'),
('2026-01-10 12:30:00', 2, 1, 120000.00, 'kartu', 'selesai'),
('2026-01-12 09:45:00', 7, 1, 70000.00, 'tunai', 'selesai'),
('2026-01-15 14:00:00', 3, 1, 88000.00, 'e-wallet', 'selesai'),
('2026-01-18 11:15:00', 8, 1, 95000.00, 'tunai', 'selesai'),
('2026-01-20 16:30:00', 4, 1, 65000.00, 'kartu', 'selesai'),
('2026-01-22 10:20:00', 5, 1, 110000.00, 'tunai', 'selesai'),
('2026-01-25 13:45:00', 6, 1, 75000.00, 'e-wallet', 'selesai'),
('2026-01-28 15:00:00', 1, 1, 92000.00, 'kartu', 'selesai'),
('2026-01-30 12:00:00', 2, 1, 105000.00, 'tunai', 'selesai');

-- Insert sample transaction details
INSERT INTO detail_transaksi (id_transaksi, id_menu, jumlah, harga_satuan, subtotal) VALUES
-- Transaction 1
(1, 2, 1, 25000.00, 25000.00),
(1, 9, 1, 18000.00, 18000.00),
(1, 15, 1, 12000.00, 12000.00),
-- Transaction 2
(2, 3, 2, 28000.00, 56000.00),
(2, 10, 1, 35000.00, 35000.00),
-- Transaction 3
(3, 11, 1, 45000.00, 45000.00),
-- Transaction 4
(4, 5, 2, 30000.00, 60000.00),
(4, 16, 1, 28000.00, 28000.00),
(4, 1, 1, 15000.00, 15000.00),
-- Transaction 5
(5, 12, 1, 38000.00, 38000.00),
(5, 13, 1, 20000.00, 20000.00),
-- Transaction 6
(6, 4, 2, 20000.00, 40000.00),
(6, 14, 1, 32000.00, 32000.00),
(6, 15, 1, 12000.00, 12000.00),
-- Transaction 7
(7, 3, 1, 28000.00, 28000.00),
(7, 9, 1, 18000.00, 18000.00),
(7, 15, 1, 12000.00, 12000.00),
-- Transaction 8
(8, 11, 2, 45000.00, 90000.00),
(8, 7, 1, 25000.00, 25000.00),
-- Transaction 9
(9, 10, 2, 35000.00, 70000.00),
-- Transaction 10
(10, 5, 2, 30000.00, 60000.00),
(10, 17, 1, 32000.00, 32000.00),
-- Transaction 11
(11, 12, 2, 38000.00, 76000.00),
(11, 8, 1, 22000.00, 22000.00),
-- Transaction 12
(12, 2, 2, 25000.00, 50000.00),
(12, 13, 1, 20000.00, 20000.00),
-- Transaction 13
(13, 11, 2, 45000.00, 90000.00),
(13, 6, 1, 28000.00, 28000.00),
-- Transaction 14
(14, 3, 2, 28000.00, 56000.00),
(14, 8, 1, 22000.00, 22000.00),
-- Transaction 15
(15, 5, 2, 30000.00, 60000.00),
(15, 16, 1, 28000.00, 28000.00),
-- Transaction 16
(16, 11, 2, 45000.00, 90000.00),
(16, 18, 1, 18000.00, 18000.00);

-- ============================================
-- Views for Reporting
-- ============================================

-- View: Daily Sales Summary
CREATE OR REPLACE VIEW v_daily_sales AS
SELECT 
    DATE(tanggal) as tanggal,
    COUNT(*) as jumlah_transaksi,
    SUM(total) as total_penjualan
FROM transaksi
WHERE status = 'selesai'
GROUP BY DATE(tanggal)
ORDER BY tanggal DESC;

-- View: Monthly Sales Summary
CREATE OR REPLACE VIEW v_monthly_sales AS
SELECT 
    DATE_FORMAT(tanggal, '%Y-%m') as bulan,
    COUNT(*) as jumlah_transaksi,
    SUM(total) as total_penjualan
FROM transaksi
WHERE status = 'selesai'
GROUP BY DATE_FORMAT(tanggal, '%Y-%m')
ORDER BY bulan DESC;

-- View: Top Selling Menu
CREATE OR REPLACE VIEW v_top_menu AS
SELECT 
    m.id_menu,
    m.nama_menu,
    m.kategori,
    SUM(dt.jumlah) as total_terjual,
    SUM(dt.subtotal) as total_pendapatan
FROM detail_transaksi dt
JOIN menu m ON dt.id_menu = m.id_menu
JOIN transaksi t ON dt.id_transaksi = t.id_transaksi
WHERE t.status = 'selesai'
GROUP BY m.id_menu, m.nama_menu, m.kategori
ORDER BY total_terjual DESC;

-- View: Sales by Category
CREATE OR REPLACE VIEW v_sales_by_category AS
SELECT 
    m.kategori,
    SUM(dt.jumlah) as total_item,
    SUM(dt.subtotal) as total_pendapatan
FROM detail_transaksi dt
JOIN menu m ON dt.id_menu = m.id_menu
JOIN transaksi t ON dt.id_transaksi = t.id_transaksi
WHERE t.status = 'selesai'
GROUP BY m.kategori
ORDER BY total_pendapatan DESC;

-- ============================================
-- End of Schema
-- ============================================
