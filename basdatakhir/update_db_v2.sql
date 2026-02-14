-- ============================================
-- Database Enhancement: Payment Table
-- ============================================

USE cafe_management;

-- Create pembayaran table if it doesn't exist
CREATE TABLE IF NOT EXISTS pembayaran (
    id_pembayaran INT AUTO_INCREMENT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    metode_pembayaran ENUM('tunai', 'transfer', 'dana', 'ovo', 'gopay') NOT NULL,
    total_bayar DECIMAL(10, 2) NOT NULL,
    tanggal_bayar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('berhasil', 'gagal', 'pending') DEFAULT 'berhasil',
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Ensure gambar column exists in menu (should already be there based on schema)
-- ALTER TABLE menu ADD COLUMN IF NOT EXISTS gambar VARCHAR(255) AFTER deskripsi;

-- Sample data updates for menu images (placeholder names)
UPDATE menu SET gambar = 'espresso.jpg' WHERE nama_menu = 'Espresso';
UPDATE menu SET gambar = 'cappuccino.jpg' WHERE nama_menu = 'Cappuccino';
UPDATE menu SET gambar = 'latte.jpg' WHERE nama_menu = 'Latte';
UPDATE menu SET gambar = 'americano.jpg' WHERE nama_menu = 'Americano';
UPDATE menu SET gambar = 'mocha.jpg' WHERE nama_menu = 'Mocha';
UPDATE menu SET gambar = 'greentea.jpg' WHERE nama_menu = 'Green Tea Latte';
UPDATE menu SET gambar = 'chocolate.jpg' WHERE nama_menu = 'Chocolate';
UPDATE menu SET gambar = 'icedcoffee.jpg' WHERE nama_menu = 'Iced Coffee';
UPDATE menu SET gambar = 'croissant.jpg' WHERE nama_menu = 'Croissant';
UPDATE menu SET gambar = 'sandwich.jpg' WHERE nama_menu = 'Sandwich';
UPDATE menu SET gambar = 'pasta.jpg' WHERE nama_menu = 'Pasta Carbonara';
UPDATE menu SET gambar = 'nasigoreng.jpg' WHERE nama_menu = 'Nasi Goreng';
UPDATE menu SET gambar = 'frenchfries.jpg' WHERE nama_menu = 'French Fries';
UPDATE menu SET gambar = 'chickenwings.jpg' WHERE nama_menu = 'Chicken Wings';
UPDATE menu SET gambar = 'donut.jpg' WHERE nama_menu = 'Donut';
UPDATE menu SET gambar = 'cheesecake.jpg' WHERE nama_menu = 'Cheesecake';
UPDATE menu SET gambar = 'tiramisu.jpg' WHERE nama_menu = 'Tiramisu';
UPDATE menu SET gambar = 'icecream.jpg' WHERE nama_menu = 'Ice Cream';
