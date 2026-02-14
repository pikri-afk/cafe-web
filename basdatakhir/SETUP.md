# 🚀 Quick Setup Guide - Café Management System

## Langkah 1: Setup Database

### Opsi A: Menggunakan phpMyAdmin (Recommended)
1. Buka XAMPP Control Panel
2. Start **Apache** dan **MySQL**
3. Buka browser, akses: `http://localhost/phpmyadmin`
4. Klik **New** untuk membuat database baru
5. Nama database: `cafe_management`
6. Klik **Create**
7. Pilih database `cafe_management`
8. Klik tab **Import**
9. Pilih file `database_schema.sql`
10. Klik **Go**

### Opsi B: Menggunakan Command Line
```bash
# Masuk ke MySQL
mysql -u root -p

# Buat database
CREATE DATABASE cafe_management;
exit;

# Import schema
mysql -u root -p cafe_management < database_schema.sql
```

## Langkah 2: Konfigurasi Database

Edit file `db_config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Username MySQL Anda
    'password': '',          # Password MySQL Anda (kosong jika default XAMPP)
    'database': 'cafe_management',
    'port': 3306
}
```

## Langkah 3: Install Dependencies Python

Buka Command Prompt atau PowerShell di folder project:

```bash
cd c:\xampp\htdocs\basdatakhir

# Install dependencies
pip install -r requirements.txt
```

**Jika pip belum terinstall:**
```bash
python -m ensurepip --upgrade
```

## Langkah 4: Jalankan Aplikasi

```bash
python app.py
```

**Output yang diharapkan:**
```
✓ Database connection pool initialized
✓ Database connection test successful

==================================================
🚀 Café Management System
==================================================
📍 Server running at: http://localhost:5000
👤 Default login: admin / admin123
==================================================
```

## Langkah 5: Akses Aplikasi

1. Buka browser (Chrome/Firefox/Edge)
2. Akses: `http://localhost:5000`
3. Login dengan:
   - **Username:** `admin`
   - **Password:** `admin123`

## 🎯 Fitur yang Dapat Diuji

### ✅ Dashboard
- Lihat statistik real-time
- Grafik penjualan bulanan
- Menu terlaris
- Penjualan per kategori

### ✅ Menu
- Tambah menu baru
- Edit menu
- Hapus menu
- Cari menu

### ✅ Pelanggan
- Tambah pelanggan
- Edit data pelanggan
- Hapus pelanggan
- Cari pelanggan

### ✅ Transaksi
- Buat transaksi baru
- Tambah multiple items
- Pilih pelanggan
- Pilih metode pembayaran
- Cari transaksi berdasarkan tanggal
- Batalkan transaksi

### ✅ Laporan
- Laporan harian
- Laporan bulanan
- Total pendapatan

## 🐛 Troubleshooting

### Error: "No module named 'flask'"
```bash
pip install Flask
```

### Error: "No module named 'mysql'"
```bash
pip install mysql-connector-python
```

### Error: "Can't connect to MySQL server"
- Pastikan MySQL di XAMPP sudah running
- Cek username/password di `db_config.py`

### Error: "Port 5000 already in use"
Edit `app.py` baris terakhir:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
Lalu akses: `http://localhost:5001`

### Chart tidak muncul
- Pastikan koneksi internet aktif (untuk CDN)
- Buka Developer Tools (F12) untuk cek error

## 📝 Tips

1. **Ubah Password Default**
   - Login sebagai admin
   - Gunakan `generate_hash.py` untuk membuat hash password baru
   - Update di database

2. **Backup Database**
   ```bash
   mysqldump -u root -p cafe_management > backup.sql
   ```

3. **Reset Database**
   - Import ulang `database_schema.sql`

4. **Tambah User Baru**
   ```python
   python generate_hash.py
   # Copy hash yang dihasilkan
   # Insert ke tabel users
   ```

## 🎉 Selamat!

Aplikasi Café Management System siap digunakan!

Untuk dokumentasi lengkap, lihat file `README.md`
