# Sistem Informasi Manajemen Café

Aplikasi web lengkap untuk manajemen café dengan fitur autentikasi, CRUD, laporan, dan visualisasi data interaktif.

## 🚀 Fitur Utama

### 1. **Autentikasi & Keamanan**
- Login dengan username dan password
- Session management
- Password hashing (PBKDF2-SHA256)
- Protected routes

### 2. **Dashboard Interaktif**
- Statistik real-time (pendapatan, transaksi, menu, pelanggan)
- Grafik penjualan bulanan (Line Chart)
- Grafik menu terlaris (Bar Chart)
- Grafik penjualan per kategori (Pie Chart)
- Visualisasi menggunakan Chart.js

### 3. **Manajemen Menu**
- CRUD lengkap untuk menu café
- Kategori: Minuman, Makanan, Snack, Dessert
- Pencarian menu berdasarkan nama
- Tracking stok dan harga
- Status ketersediaan

### 4. **Manajemen Pelanggan**
- CRUD data pelanggan
- Informasi kontak lengkap
- Sistem poin member
- Pencarian pelanggan

### 5. **Manajemen Transaksi**
- Buat transaksi baru dengan multiple items
- Pilih pelanggan (opsional)
- Metode pembayaran: Tunai, Kartu, E-Wallet
- Pencarian transaksi berdasarkan tanggal
- View detail transaksi
- Batalkan transaksi

### 6. **Laporan Penjualan**
- Laporan harian
- Laporan bulanan
- Total pendapatan keseluruhan
- Filter berdasarkan tanggal/bulan

## 🛠️ Teknologi

**Backend:**
- Python Flask 3.0.0
- MySQL (via mysql-connector-python)
- Werkzeug (password hashing)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Chart.js 4.4.0
- Google Fonts (Poppins)

**Database:**
- MySQL 8.0+

## 📋 Persyaratan Sistem

- Python 3.8+
- MySQL Server 8.0+
- XAMPP (atau MySQL standalone)
- Browser modern (Chrome, Firefox, Edge)

## 🔧 Instalasi

### 1. Setup Database

```bash
# Jalankan MySQL server (via XAMPP atau standalone)
# Buka MySQL command line atau phpMyAdmin

# Import database schema
mysql -u root -p < database_schema.sql
```

Atau melalui phpMyAdmin:
1. Buka http://localhost/phpmyadmin
2. Buat database baru: `cafe_management`
3. Import file `database_schema.sql`

### 2. Konfigurasi Database

Edit file `db_config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Sesuaikan dengan username MySQL Anda
    'password': '',          # Sesuaikan dengan password MySQL Anda
    'database': 'cafe_management',
    'port': 3306
}
```

### 3. Install Dependencies Python

```bash
# Buka terminal di folder project
cd c:\xampp\htdocs\basdatakhir

# Install dependencies
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

## 👤 Login Default

```
Username: admin
Password: admin123
```

**PENTING:** Segera ubah password default setelah login pertama!

## 📁 Struktur Folder

```
basdatakhir/
├── app.py                      # Aplikasi Flask utama
├── db_config.py                # Konfigurasi database
├── database_schema.sql         # Schema database
├── requirements.txt            # Dependencies Python
├── README.md                   # Dokumentasi
├── templates/                  # Template HTML
│   ├── login.html             # Halaman login
│   ├── dashboard.html         # Dashboard dengan charts
│   ├── menu.html              # Manajemen menu
│   ├── pelanggan.html         # Manajemen pelanggan
│   ├── transaksi.html         # Manajemen transaksi
│   └── laporan.html           # Laporan penjualan
└── static/                     # File statis
    ├── css/
    │   └── style.css          # Custom CSS
    └── js/
        └── main.js            # (opsional)
```

## 🎨 Desain UI/UX

- **Tema Warna:** Coklat, krem, hitam elegan (café theme)
- **Font:** Poppins (modern & clean)
- **Responsif:** Mobile-friendly
- **Animasi:** Smooth transitions & hover effects
- **Card Layout:** Modern card-based design
- **Icons:** Font Awesome

## 📊 Database Schema

### Tabel Utama:

1. **users** - Data pengguna dan autentikasi
2. **menu** - Menu café (nama, kategori, harga, stok)
3. **pelanggan** - Data pelanggan
4. **transaksi** - Header transaksi
5. **detail_transaksi** - Detail item transaksi

### Relasi:
- `transaksi.id_pelanggan` → `pelanggan.id_pelanggan`
- `transaksi.id_user` → `users.id_user`
- `detail_transaksi.id_transaksi` → `transaksi.id_transaksi`
- `detail_transaksi.id_menu` → `menu.id_menu`

## 🔒 Keamanan

- ✅ Password hashing dengan PBKDF2-SHA256
- ✅ Session-based authentication
- ✅ Protected routes dengan decorator
- ✅ SQL injection prevention (parameterized queries)
- ✅ Input validation di frontend dan backend

## 🐛 Troubleshooting

### Error: "Database connection failed"
- Pastikan MySQL server berjalan
- Cek kredensial di `db_config.py`
- Pastikan database `cafe_management` sudah dibuat

### Error: "Module not found"
- Jalankan: `pip install -r requirements.txt`

### Port 5000 sudah digunakan
- Edit `app.py`, ubah port di baris terakhir:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```

### Chart tidak muncul
- Pastikan koneksi internet aktif (untuk CDN Chart.js)
- Cek console browser untuk error JavaScript

## 📝 Catatan Pengembangan

### Menambah User Baru
Gunakan password hashing:

```python
from werkzeug.security import generate_password_hash

password_hash = generate_password_hash('password_baru')
# Insert ke database dengan password_hash
```

### Backup Database

```bash
mysqldump -u root -p cafe_management > backup.sql
```

### Restore Database

```bash
mysql -u root -p cafe_management < backup.sql
```

## 🎯 Fitur Mendatang (Opsional)

- [ ] Export laporan ke PDF/Excel
- [ ] Notifikasi stok menipis
- [ ] Multi-role access (admin, kasir, manager)
- [ ] Dashboard analytics lebih detail
- [ ] Upload gambar menu
- [ ] Sistem diskon dan promo

## 📄 Lisensi

Project ini dibuat untuk keperluan pembelajaran dan pengembangan.

## 👨‍💻 Pengembang

Dibuat dengan ❤️ menggunakan Flask, MySQL, dan Chart.js

---

**Selamat menggunakan Sistem Informasi Manajemen Café!** ☕
