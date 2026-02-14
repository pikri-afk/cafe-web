import mysql.connector
from mysql.connector import pooling
from contextlib import contextmanager

# ============================================
# Database Configuration
# ============================================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': '',  # Change this to your MySQL password
    'database': 'cafe_management',
    'port': 3306
}

# ============================================
# Connection Pool
# ============================================
connection_pool = None

def init_pool():
    """Initialize connection pool"""
    global connection_pool
    try:
        connection_pool = pooling.MySQLConnectionPool(
            pool_name="cafe_pool",
            pool_size=5,
            pool_reset_session=True,
            **DB_CONFIG
        )
        print("[OK] Database connection pool initialized")
        return True
    except mysql.connector.Error as err:
        print(f"[ERROR] Error initializing connection pool: {err}")
        return False

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = connection_pool.get_connection()
        yield connection
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if connection:
            connection.rollback()
        raise
    finally:
        if connection and connection.is_connected():
            connection.close()

@contextmanager
def get_db_cursor(dictionary=True):
    """Context manager for database cursor"""
    with get_db_connection() as connection:
        cursor = connection.cursor(dictionary=dictionary)
        try:
            yield cursor
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()

# ============================================
# Helper Functions
# ============================================

def execute_query(query, params=None, fetch=False, fetch_one=False):
    """
    Execute a query and optionally fetch results
    
    Args:
        query: SQL query string
        params: Query parameters (tuple or dict)
        fetch: Whether to fetch all results
        fetch_one: Whether to fetch one result
    
    Returns:
        For INSERT: lastrowid
        For SELECT with fetch: list of results
        For SELECT with fetch_one: single result
        For UPDATE/DELETE: rowcount
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params or ())
        
        if fetch_one:
            return cursor.fetchone()
        elif fetch:
            return cursor.fetchall()
        else:
            # For INSERT, return lastrowid; for UPDATE/DELETE, return rowcount
            return cursor.lastrowid if cursor.lastrowid else cursor.rowcount

def execute_many(query, params_list):
    """
    Execute a query multiple times with different parameters
    
    Args:
        query: SQL query string
        params_list: List of parameter tuples
    
    Returns:
        Number of affected rows
    """
    with get_db_cursor() as cursor:
        cursor.executemany(query, params_list)
        return cursor.rowcount

def test_connection():
    """Test database connection"""
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("[OK] Database connection test successful")
                return True
    except Exception as e:
        print(f"[ERROR] Database connection test failed: {e}")
        return False

# ============================================
# Initialize on import
# ============================================
if __name__ != "__main__":
    init_pool()
