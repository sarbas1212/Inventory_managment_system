import psycopg2

def reset_auth():
    try:
        conn = psycopg2.connect(
            dbname="inventory_db",
            user="postgres",
            password="admin123",
            host="localhost"
        )
        conn.autocommit = True
        cur = conn.cursor()

        tables_to_drop = [
            "django_admin_log",
            "auth_group_permissions",
            "auth_user_groups",
            "auth_user_user_permissions",
            "auth_group",
            "auth_permission",
            "auth_user",
            "accounts_customuser_groups",
            "accounts_customuser_user_permissions",
            "accounts_customuser",
            "accounts_ledger_ledgerentry",
            "accounts_ledger_voucher",
            "accounts_ledger_ledger",
            "accounts_ledger_ledger_id_seq",
            "accounts_ledger_ledgerentry_id_seq",
            "accounts_ledger_voucher_id_seq"
        ]

        for table in tables_to_drop:
            try:
                cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Error dropping {table}: {e}")

        cur.execute("DELETE FROM django_migrations WHERE app IN ('admin', 'auth', 'accounts', 'accounts_ledger')")
        print("Cleared relevant migration history")

        cur.close()
        conn.close()
        print("Auth reset complete.")
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    reset_auth()
