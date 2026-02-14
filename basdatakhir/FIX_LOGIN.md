# 🔧 FIX LOGIN - Panduan Cepat

## Masalah
Password hash di database tidak valid, sehingga login gagal.

## Solusi

### OPSI 1: Database Baru (RECOMMENDED)
Jika Anda belum banyak menambah data, lebih baik drop dan buat ulang database:

**Via phpMyAdmin:**
1. Buka http://localhost/phpmyadmin
2. Pilih database `cafe_management`
3. Klik tab "Operations"
4. Scroll ke bawah, klik "Drop the database"
5. Konfirmasi
6. Klik "New" untuk buat database baru: `cafe_management`
7. Import file `database_schema.sql` yang sudah diperbaiki

**Via Command Line:**
```bash
mysql -u root -p

DROP DATABASE cafe_management;
CREATE DATABASE cafe_management;
exit;

mysql -u root -p cafe_management < database_schema.sql
```

### OPSI 2: Update Password Saja
Jika sudah ada data penting, jalankan script update:

**Via phpMyAdmin:**
1. Buka http://localhost/phpmyadmin
2. Pilih database `cafe_management`
3. Klik tab "SQL"
4. Copy-paste isi file `update_password.sql`
5. Klik "Go"

**Via Command Line:**
```bash
mysql -u root -p cafe_management < update_password.sql
```

## Setelah Fix

1. Restart aplikasi Flask (Ctrl+C lalu `python app.py`)
2. Refresh browser
3. Login dengan:
   - Username: **admin**
   - Password: **admin123**

## Verifikasi

Jika berhasil, Anda akan masuk ke dashboard dan melihat:
- Statistik penjualan
- 3 grafik (Line, Pie, Bar)
- Menu navigasi lengkap

---

**Password hash yang benar sudah ada di:**
- `database_schema.sql` (untuk database baru)
- `update_password.sql` (untuk update database existing)
