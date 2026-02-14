import mysql.connector
import db_config
import os

def apply_sql_file(filename):
    print(f"Applying {filename}...")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        statements = sql_content.split(';')
        
        with db_config.get_db_connection() as conn:
            cursor = conn.cursor()
            for statement in statements:
                lines = statement.split('\n')
                clean_lines = [line for line in lines if not line.strip().startswith('--')]
                clean_statement = ' '.join(clean_lines).strip()
                
                if not clean_statement or clean_statement.upper().startswith('USE'):
                    continue
                
                try:
                    cursor.execute(clean_statement)
                    print(f"Executed: {clean_statement[:50]}...")
                except mysql.connector.Error as e:
                    print(f"Error: {e}")
            
            conn.commit()
            print("\n[OK] Migration completed.")
            return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

if __name__ == "__main__":
    apply_sql_file('update_db_v3.sql')
