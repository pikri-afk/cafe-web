import db_config

def debug_data():
    with db_config.get_db_cursor() as cursor:
        print("--- USERS ---")
        cursor.execute("SELECT id_user, username, role, nama_lengkap FROM users")
        for row in cursor.fetchall():
            print(row)
            
        print("\n--- PELANGGAN ---")
        cursor.execute("SELECT id_pelanggan, nama, email FROM pelanggan")
        for row in cursor.fetchall():
            print(row)
            
        print("\n--- TRANSAKSI (Recent) ---")
        cursor.execute("SELECT id_transaksi, id_pelanggan, id_user, total FROM transaksi ORDER BY id_transaksi DESC LIMIT 5")
        for row in cursor.fetchall():
            print(row)

if __name__ == "__main__":
    debug_data()
