import mysql.connector
import db_config
import os

def apply_sql_file(filename):
    print(f"Applying {filename}...")
    try:
        # Read the SQL file
        with open(filename, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Split into individual statements
        # This is a simple split, might not handle complex triggers but works for standard CREATE/UPDATE
        statements = sql_content.split(';')
        
        with db_config.get_db_connection() as conn:
            cursor = conn.cursor()
            for statement in statements:
                # Remove comments from the statement
                lines = statement.split('\n')
                clean_lines = [line for line in lines if not line.strip().startswith('--')]
                clean_statement = ' '.join(clean_lines).strip()
                
                if not clean_statement:
                    continue
                
                if clean_statement.upper().startswith('USE'):
                    print(f"Skipping USE statement: {clean_statement}")
                    continue
                
                try:
                    cursor.execute(clean_statement)
                    print(f"Successfully executed statement starting with: {clean_statement[:50]}...")
                except mysql.connector.Error as e:
                    print(f"Error executing statement: {e}")
            
            conn.commit()
            print("\n[OK] All statements processed and committed.")
            return True

    except Exception as e:
        print(f"[ERROR] Failed to apply {filename}: {e}")
        return False

if __name__ == "__main__":
    if os.path.exists('update_db_v2.sql'):
        apply_sql_file('update_db_v2.sql')
    else:
        print("[ERROR] update_db_v2.sql not found.")
