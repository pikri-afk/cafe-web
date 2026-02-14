import os
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import db_config
from decimal import Decimal

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ============================================
# Helper Functions
# ============================================

def login_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*roles):
    """Decorator to protect routes based on user roles"""
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def decimal_to_float(obj):
    """Convert Decimal objects to float for JSON serialization"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(item) for item in obj]
    return obj

# ============================================
# Authentication Routes
# ============================================

@app.route('/')
def index():
    """Redirect to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username dan password harus diisi'}), 400
        
        # Query user from database
        query = "SELECT id_user, username, password, role, nama_lengkap FROM users WHERE username = %s"
        user = db_config.execute_query(query, (username,), fetch_one=True)
        
        if user and check_password_hash(user['password'], password):
            # Set session
            session.permanent = True
            session['user_id'] = user['id_user']
            session['username'] = user['username']
            session['role'] = user['role']
            session['nama_lengkap'] = user['nama_lengkap']
            
            return jsonify({'success': True, 'message': 'Login berhasil'})
        else:
            return jsonify({'success': False, 'message': 'Username atau password salah'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))

# ============================================
# Dashboard Route
# ============================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard page - redirects based on role"""
    role = session.get('role')
    if role == 'admin' or role == 'manager':
        return render_template('dashboard.html', user=session)
    elif role == 'kasir':
        return render_template('kasir_dashboard.html', user=session)
    elif role == 'customer':
        return render_template('customer_dashboard.html', user=session)
    return render_template('dashboard.html', user=session)

# ============================================
# Menu Routes (CRUD)
# ============================================

@app.route('/menu')
@login_required
def menu():
    """Menu management page"""
    return render_template('menu.html', user=session)

@app.route('/api/menu', methods=['GET'])
@login_required
def get_menu():
    """Get all menu items or search"""
    search = request.args.get('search', '')
    
    if search:
        query = """
            SELECT id_menu, nama_menu, kategori, harga, stok, deskripsi, gambar, status 
            FROM menu 
            WHERE nama_menu LIKE %s OR kategori LIKE %s
            ORDER BY nama_menu
        """
        menu_items = db_config.execute_query(query, (f'%{search}%', f'%{search}%'), fetch=True)
    else:
        query = "SELECT id_menu, nama_menu, kategori, harga, stok, deskripsi, gambar, status FROM menu ORDER BY nama_menu"
        menu_items = db_config.execute_query(query, fetch=True)
    
    return jsonify(decimal_to_float(menu_items))

@app.route('/api/menu/<int:id_menu>', methods=['GET'])
@login_required
def get_menu_item(id_menu):
    """Get single menu item"""
    query = "SELECT * FROM menu WHERE id_menu = %s"
    item = db_config.execute_query(query, (id_menu,), fetch_one=True)
    
    if item:
        return jsonify(decimal_to_float(item))
    return jsonify({'error': 'Menu tidak ditemukan'}), 404

@app.route('/api/menu', methods=['POST'])
@login_required
def add_menu():
    """Add new menu item with optional image"""
    nama_menu = request.form.get('nama_menu')
    kategori = request.form.get('kategori')
    harga = request.form.get('harga')
    stok = request.form.get('stok', 0)
    deskripsi = request.form.get('deskripsi', '')
    status = request.form.get('status', 'tersedia')
    
    # Handle image upload
    gambar_filename = None
    if 'gambar' in request.files:
        file = request.files['gambar']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to avoid name collisions
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            gambar_filename = filename

    query = """
        INSERT INTO menu (nama_menu, kategori, harga, stok, deskripsi, gambar, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (nama_menu, kategori, harga, stok, deskripsi, gambar_filename, status)
    
    try:
        id_menu = db_config.execute_query(query, params)
        return jsonify({'success': True, 'id_menu': id_menu, 'message': 'Menu berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/menu/<int:id_menu>', methods=['POST'])  # Use POST for multipart/form-data with PUT logic
@login_required
def update_menu(id_menu):
    """Update menu item including optional new image"""
    nama_menu = request.form.get('nama_menu')
    kategori = request.form.get('kategori')
    harga = request.form.get('harga')
    stok = request.form.get('stok')
    deskripsi = request.form.get('deskripsi', '')
    status = request.form.get('status', 'tersedia')
    
    # Get existing image
    item = db_config.execute_query("SELECT gambar FROM menu WHERE id_menu = %s", (id_menu,), fetch_one=True)
    gambar_filename = item['gambar'] if item else None

    # Handle image upload
    if 'gambar' in request.files:
        file = request.files['gambar']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            gambar_filename = filename

    query = """
        UPDATE menu 
        SET nama_menu = %s, kategori = %s, harga = %s, stok = %s, 
            deskripsi = %s, gambar = %s, status = %s
        WHERE id_menu = %s
    """
    params = (nama_menu, kategori, harga, stok, deskripsi, gambar_filename, status, id_menu)
    
    try:
        db_config.execute_query(query, params)
        return jsonify({'success': True, 'message': 'Menu berhasil diupdate'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/menu/<int:id_menu>', methods=['DELETE'])
@login_required
def delete_menu(id_menu):
    """Delete menu item"""
    query = "DELETE FROM menu WHERE id_menu = %s"
    
    try:
        db_config.execute_query(query, (id_menu,))
        return jsonify({'success': True, 'message': 'Menu berhasil dihapus'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# Pelanggan Routes (CRUD)
# ============================================

@app.route('/pelanggan')
@login_required
def pelanggan():
    """Customer management page"""
    return render_template('pelanggan.html', user=session)

@app.route('/api/pelanggan', methods=['GET'])
@login_required
def get_pelanggan():
    """Get all customers"""
    search = request.args.get('search', '')
    
    if search:
        query = """
            SELECT id_pelanggan, nama, no_hp, email, alamat, poin_member 
            FROM pelanggan 
            WHERE nama LIKE %s OR no_hp LIKE %s
            ORDER BY nama
        """
        customers = db_config.execute_query(query, (f'%{search}%', f'%{search}%'), fetch=True)
    else:
        query = "SELECT id_pelanggan, nama, no_hp, email, alamat, poin_member FROM pelanggan ORDER BY nama"
        customers = db_config.execute_query(query, fetch=True)
    
    return jsonify(customers)

@app.route('/api/pelanggan', methods=['POST'])
@login_required
def add_pelanggan():
    """Add new customer"""
    data = request.get_json()
    
    query = """
        INSERT INTO pelanggan (nama, no_hp, email, alamat, poin_member)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (
        data['nama'],
        data.get('no_hp', ''),
        data.get('email', ''),
        data.get('alamat', ''),
        data.get('poin_member', 0)
    )
    
    try:
        id_pelanggan = db_config.execute_query(query, params)
        return jsonify({'success': True, 'id_pelanggan': id_pelanggan, 'message': 'Pelanggan berhasil ditambahkan'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/pelanggan/<int:id_pelanggan>', methods=['PUT'])
@login_required
def update_pelanggan(id_pelanggan):
    """Update customer"""
    data = request.get_json()
    
    query = """
        UPDATE pelanggan 
        SET nama = %s, no_hp = %s, email = %s, alamat = %s, poin_member = %s
        WHERE id_pelanggan = %s
    """
    params = (
        data['nama'],
        data.get('no_hp', ''),
        data.get('email', ''),
        data.get('alamat', ''),
        data.get('poin_member', 0),
        id_pelanggan
    )
    
    try:
        db_config.execute_query(query, params)
        return jsonify({'success': True, 'message': 'Pelanggan berhasil diupdate'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/pelanggan/<int:id_pelanggan>', methods=['DELETE'])
@login_required
def delete_pelanggan(id_pelanggan):
    """Delete customer"""
    query = "DELETE FROM pelanggan WHERE id_pelanggan = %s"
    
    try:
        db_config.execute_query(query, (id_pelanggan,))
        return jsonify({'success': True, 'message': 'Pelanggan berhasil dihapus'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# Transaksi Routes (CRUD)
# ============================================

@app.route('/transaksi')
@login_required
def transaksi():
    """Transaction management page"""
    return render_template('transaksi.html', user=session)

@app.route('/api/transaksi', methods=['GET'])
@login_required
def get_transaksi():
    """Get all transactions"""
    tanggal = request.args.get('tanggal', '')
    
    if tanggal:
        query = """
            SELECT t.id_transaksi, t.tanggal, t.total, t.metode_pembayaran, t.status,
                   COALESCE(p.nama, u.nama_lengkap) as nama_pelanggan, u.username
            FROM transaksi t
            LEFT JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
            LEFT JOIN users u ON t.id_user = u.id_user
            WHERE DATE(t.tanggal) = %s
            ORDER BY t.tanggal DESC
        """
        transactions = db_config.execute_query(query, (tanggal,), fetch=True)
    else:
        query = """
            SELECT t.id_transaksi, t.tanggal, t.total, t.metode_pembayaran, t.status,
                   COALESCE(p.nama, u.nama_lengkap) as nama_pelanggan, u.username
            FROM transaksi t
            LEFT JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
            LEFT JOIN users u ON t.id_user = u.id_user
            ORDER BY t.tanggal DESC
            LIMIT 100
        """
        transactions = db_config.execute_query(query, fetch=True)
    
    return jsonify(decimal_to_float(transactions))

@app.route('/api/transaksi/<int:id_transaksi>', methods=['GET'])
@login_required
def get_transaksi_detail(id_transaksi):
    """Get transaction details"""
    # Get transaction header
    query_header = """
        SELECT t.*, COALESCE(p.nama, u.nama_lengkap) as nama_pelanggan, u.username
        FROM transaksi t
        LEFT JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
        LEFT JOIN users u ON t.id_user = u.id_user
        WHERE t.id_transaksi = %s
    """
    header = db_config.execute_query(query_header, (id_transaksi,), fetch_one=True)
    
    # Get transaction details
    query_details = """
        SELECT dt.*, m.nama_menu, m.kategori
        FROM detail_transaksi dt
        JOIN menu m ON dt.id_menu = m.id_menu
        WHERE dt.id_transaksi = %s
    """
    details = db_config.execute_query(query_details, (id_transaksi,), fetch=True)
    
    if header:
        result = decimal_to_float(header)
        result['details'] = decimal_to_float(details)
        return jsonify(result)
    
    return jsonify({'error': 'Transaksi tidak ditemukan'}), 404

@app.route('/api/transaksi', methods=['POST'])
@login_required
def add_transaksi():
    """Add new transaction"""
    data = request.get_json()
    
    try:
        # Insert transaction header
        query_header = """
            INSERT INTO transaksi (id_pelanggan, id_user, total, metode_pembayaran, catatan)
            VALUES (%s, %s, %s, %s, %s)
        """
        params_header = (
            data.get('id_pelanggan'),
            session['user_id'],
            data['total'],
            data.get('metode_pembayaran', 'tunai'),
            data.get('catatan', '')
        )
        
        id_transaksi = db_config.execute_query(query_header, params_header)
        
        # Insert transaction details
        query_detail = """
            INSERT INTO detail_transaksi (id_transaksi, id_menu, jumlah, harga_satuan, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        for item in data['items']:
            params_detail = (
                id_transaksi,
                item['id_menu'],
                item['jumlah'],
                item['harga_satuan'],
                item['subtotal']
            )
            db_config.execute_query(query_detail, params_detail)
        
        return jsonify({'success': True, 'id_transaksi': id_transaksi, 'message': 'Transaksi berhasil ditambahkan'})
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/transaksi/<int:id_transaksi>', methods=['DELETE'])
@login_required
def delete_transaksi(id_transaksi):
    """Delete transaction"""
    query = "UPDATE transaksi SET status = 'dibatalkan' WHERE id_transaksi = %s"
    
    try:
        db_config.execute_query(query, (id_transaksi,))
        return jsonify({'success': True, 'message': 'Transaksi berhasil dibatalkan'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# Cart & Checkout Routes (Session-based)
# ============================================

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get current cart from session"""
    if 'cart' not in session:
        session['cart'] = []
    # Convert Decimal to float for JSON
    cart = decimal_to_float(session['cart'])
    return jsonify({'cart': cart})

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart"""
    data = request.get_json()
    id_menu = data.get('id_menu')
    
    # Get menu item details
    item_query = "SELECT id_menu, nama_menu, harga, gambar FROM menu WHERE id_menu = %s"
    menu_item = db_config.execute_query(item_query, (id_menu,), fetch_one=True)
    
    if not menu_item:
        return jsonify({'success': False, 'message': 'Menu tidak ditemukan'}), 404
        
    if 'cart' not in session:
        session['cart'] = []
        
    cart = session['cart']
    
    # Check if item already in cart
    found = False
    for item in cart:
        if item['id_menu'] == id_menu:
            item['jumlah'] += 1
            item['subtotal'] = float(item['harga']) * item['jumlah']
            found = True
            break
            
    if not found:
        cart.append({
            'id_menu': menu_item['id_menu'],
            'nama_menu': menu_item['nama_menu'],
            'harga': float(menu_item['harga']),
            'jumlah': 1,
            'subtotal': float(menu_item['harga']),
            'gambar': menu_item['gambar']
        })
        
    session['cart'] = cart
    session.modified = True
    return jsonify({'success': True, 'message': 'Item ditambahkan ke keranjang', 'cart': decimal_to_float(cart)})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    """Update item quantity in cart"""
    data = request.get_json()
    id_menu = data.get('id_menu')
    jumlah = data.get('jumlah')
    
    if 'cart' not in session:
        return jsonify({'success': False, 'message': 'Keranjang kosong'}), 400
        
    cart = session['cart']
    for item in cart:
        if item['id_menu'] == id_menu:
            item['jumlah'] = max(0, int(jumlah))
            item['subtotal'] = float(item['harga']) * item['jumlah']
            if item['jumlah'] == 0:
                cart.remove(item)
            break
            
    session['cart'] = cart
    session.modified = True
    return jsonify({'success': True, 'cart': decimal_to_float(cart)})

@app.route('/api/cart/clear', methods=['POST'])
def clear_cart():
    """Clear the cart"""
    session['cart'] = []
    session.modified = True
    return jsonify({'success': True, 'message': 'Keranjang dikosongkan'})

@app.route('/api/checkout', methods=['POST'])
@login_required
def checkout():
    """Process checkout and payment"""
    data = request.get_json()
    metode_pembayaran = data.get('metode_pembayaran', 'tunai')
    cart = session.get('cart', [])
    
    if not cart:
        return jsonify({'success': False, 'message': 'Keranjang kosong'}), 400
        
    total = sum(float(item['subtotal']) for item in cart)
    
    try:
        # Get id_pelanggan if user is a customer
        id_pelanggan = data.get('id_pelanggan')
        if not id_pelanggan and session.get('role') == 'customer':
            pelanggan_query = "SELECT id_pelanggan FROM pelanggan WHERE id_user = %s"
            pelanggan_res = db_config.execute_query(pelanggan_query, (session['user_id'],), fetch_one=True)
            if pelanggan_res:
                id_pelanggan = pelanggan_res['id_pelanggan']

        # 1. Create Transaction Header
        query_transaksi = """
            INSERT INTO transaksi (id_pelanggan, id_user, total, metode_pembayaran, status)
            VALUES (%s, %s, %s, %s, 'selesai')
        """
        params_transaksi = (id_pelanggan, session['user_id'], total, metode_pembayaran) 
        id_transaksi = db_config.execute_query(query_transaksi, params_transaksi)
        
        # 2. Create Transaction Details
        query_detail = """
            INSERT INTO detail_transaksi (id_transaksi, id_menu, jumlah, harga_satuan, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        for item in cart:
            db_config.execute_query(query_detail, (
                id_transaksi, 
                item['id_menu'], 
                int(item['jumlah']), 
                float(item['harga']), 
                float(item['subtotal'])
            ))
            
            # Update Stock
            db_config.execute_query("UPDATE menu SET stok = stok - %s WHERE id_menu = %s", (item['jumlah'], item['id_menu']))
            
        # 3. Create Payment Record
        query_pembayaran = """
            INSERT INTO pembayaran (id_transaksi, metode_pembayaran, total_bayar, status)
            VALUES (%s, %s, %s, 'berhasil')
        """
        db_config.execute_query(query_pembayaran, (id_transaksi, metode_pembayaran, total))
        
        # 4. Clear Cart
        session['cart'] = []
        session.modified = True
        
        return jsonify({
            'success': True, 
            'id_transaksi': id_transaksi, 
            'message': 'Pembayaran berhasil! Pesanan sedang diproses.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# ============================================
# Report Routes
# ============================================

@app.route('/laporan')
@roles_required('admin', 'manager')
def laporan():
    """Reports page"""
    return render_template('laporan.html', user=session)

@app.route('/api/laporan/harian', methods=['GET'])
@roles_required('admin', 'manager')
def laporan_harian():
    """Daily sales report"""
    tanggal = request.args.get('tanggal', datetime.now().strftime('%Y-%m-%d'))
    
    query = """
        SELECT 
            DATE(tanggal) as tanggal,
            COUNT(*) as jumlah_transaksi,
            SUM(total) as total_penjualan
        FROM transaksi
        WHERE DATE(tanggal) = %s AND status = 'selesai'
        GROUP BY DATE(tanggal)
    """
    
    result = db_config.execute_query(query, (tanggal,), fetch_one=True)
    
    if result:
        return jsonify(decimal_to_float(result))
    
    return jsonify({
        'tanggal': tanggal,
        'jumlah_transaksi': 0,
        'total_penjualan': 0
    })

@app.route('/api/laporan/bulanan', methods=['GET'])
@login_required
def laporan_bulanan():
    """Monthly sales report"""
    bulan = request.args.get('bulan', datetime.now().strftime('%Y-%m'))
    
    query = """
        SELECT 
            DATE_FORMAT(tanggal, '%%Y-%%m') as bulan,
            COUNT(*) as jumlah_transaksi,
            SUM(total) as total_penjualan
        FROM transaksi
        WHERE DATE_FORMAT(tanggal, '%%Y-%%m') = %s AND status = 'selesai'
        GROUP BY DATE_FORMAT(tanggal, '%%Y-%%m')
    """
    
    result = db_config.execute_query(query, (bulan,), fetch_one=True)
    
    if result:
        return jsonify(decimal_to_float(result))
    
    return jsonify({
        'bulan': bulan,
        'jumlah_transaksi': 0,
        'total_penjualan': 0
    })

@app.route('/api/laporan/total-pendapatan', methods=['GET'])
@login_required
def total_pendapatan():
    """Total revenue"""
    query = "SELECT SUM(total) as total_pendapatan FROM transaksi WHERE status = 'selesai'"
    result = db_config.execute_query(query, fetch_one=True)
    
    return jsonify(decimal_to_float(result))

# ============================================
# Dashboard Data Routes (for Charts)
# ============================================

@app.route('/api/dashboard/monthly-sales', methods=['GET'])
@login_required
def monthly_sales():
    """Monthly sales data for line chart"""
    query = """
        SELECT 
            DATE_FORMAT(tanggal, '%%Y-%%m') as bulan,
            SUM(total) as total_penjualan
        FROM transaksi
        WHERE status = 'selesai' 
            AND tanggal >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
        GROUP BY DATE_FORMAT(tanggal, '%%Y-%%m')
        ORDER BY bulan
    """
    
    results = db_config.execute_query(query, fetch=True)
    return jsonify(decimal_to_float(results))

@app.route('/api/dashboard/top-menu', methods=['GET'])
@login_required
def top_menu():
    """Top selling menu items for bar chart"""
    limit = request.args.get('limit', 10, type=int)
    
    query = """
        SELECT 
            m.nama_menu,
            SUM(dt.jumlah) as total_terjual
        FROM detail_transaksi dt
        JOIN menu m ON dt.id_menu = m.id_menu
        JOIN transaksi t ON dt.id_transaksi = t.id_transaksi
        WHERE t.status = 'selesai'
        GROUP BY m.id_menu, m.nama_menu
        ORDER BY total_terjual DESC
        LIMIT %s
    """
    
    results = db_config.execute_query(query, (limit,), fetch=True)
    return jsonify(results)

@app.route('/api/dashboard/sales-by-category', methods=['GET'])
@login_required
def sales_by_category():
    """Sales by category for pie chart"""
    query = """
        SELECT 
            m.kategori,
            SUM(dt.subtotal) as total_pendapatan
        FROM detail_transaksi dt
        JOIN menu m ON dt.id_menu = m.id_menu
        JOIN transaksi t ON dt.id_transaksi = t.id_transaksi
        WHERE t.status = 'selesai'
        GROUP BY m.kategori
        ORDER BY total_pendapatan DESC
    """
    
    results = db_config.execute_query(query, fetch=True)
    return jsonify(decimal_to_float(results))

@app.route('/api/dashboard/stats', methods=['GET'])
@login_required
def dashboard_stats():
    """General dashboard statistics"""
    stats = {}
    
    # Total revenue
    query_revenue = "SELECT SUM(total) as total FROM transaksi WHERE status = 'selesai'"
    revenue = db_config.execute_query(query_revenue, fetch_one=True)
    stats['total_pendapatan'] = float(revenue['total']) if revenue['total'] else 0
    
    # Total transactions today
    query_today = """
        SELECT COUNT(*) as total FROM transaksi 
        WHERE DATE(tanggal) = CURDATE() AND status = 'selesai'
    """
    today = db_config.execute_query(query_today, fetch_one=True)
    stats['transaksi_hari_ini'] = today['total']
    
    # Total menu items
    query_menu = "SELECT COUNT(*) as total FROM menu WHERE status = 'tersedia'"
    menu = db_config.execute_query(query_menu, fetch_one=True)
    stats['total_menu'] = menu['total']
    
    # Total customers
    query_customers = "SELECT COUNT(*) as total FROM pelanggan"
    customers = db_config.execute_query(query_customers, fetch_one=True)
    stats['total_pelanggan'] = customers['total']
    
    return jsonify(stats)

@app.route('/api/dashboard/payment-methods', methods=['GET'])
@login_required
def payment_method_stats():
    """Payment method distribution for charts"""
    query = """
        SELECT metode_pembayaran, COUNT(*) as jumlah
        FROM pembayaran
        GROUP BY metode_pembayaran
    """
    results = db_config.execute_query(query, fetch=True)
    return jsonify(results)

@app.route('/api/dashboard/revenue-trend', methods=['GET'])
@login_required
def revenue_trend():
    """Revenue trend for charts"""
    query = """
        SELECT DATE(tanggal_bayar) as tanggal, SUM(total_bayar) as total
        FROM pembayaran
        WHERE status = 'berhasil'
        GROUP BY DATE(tanggal_bayar)
        ORDER BY tanggal ASC
        LIMIT 30
    """
    results = db_config.execute_query(query, fetch=True)
    return jsonify(decimal_to_float(results))

# ============================================
# Main
# ============================================

if __name__ == '__main__':
    # Test database connection
    if db_config.test_connection():
        print("\n" + "="*50)
        print(">>> Cafe Management System")
        print("="*50)
        print(" -  Server running at: http://localhost:5000")
        print(" -  Default login: admin / admin123")
        print("="*50 + "\n")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("\n[ERROR] Failed to start: Database connection error")
        print("Please check your database configuration in db_config.py")
