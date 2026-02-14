import db_config

def check_tables():
    print("Checking tables in database...")
    query = "SHOW TABLES"
    try:
        results = db_config.execute_query(query, fetch=True)
        print("Existing tables:")
        for row in results:
            print(f"- {list(row.values())[0]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_tables()
