"""
Database migration script to add switch_name and switch_ip columns to Alert table
and make switch_id nullable for preserving historical alerts.
"""
import sqlite3
from datetime import datetime

def migrate_database():
    print("Starting database migration...")
    
    # Connect to the database
    conn = sqlite3.connect('instance/network_monitor.db')
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(alert)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'switch_name' in columns and 'switch_ip' in columns:
            print("✓ Migration already applied. Database is up to date.")
            return
        
        print("Creating new alert table with updated schema...")
        
        # Create new table with updated schema
        cursor.execute("""
            CREATE TABLE alert_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                switch_id INTEGER,
                switch_name VARCHAR(100),
                switch_ip VARCHAR(50),
                alert_type VARCHAR(50) NOT NULL,
                severity VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                acknowledged BOOLEAN DEFAULT 0,
                FOREIGN KEY (switch_id) REFERENCES switch(id) ON DELETE SET NULL
            )
        """)
        
        print("Copying existing alert data...")
        
        # Copy data from old table to new table, populating switch_name and switch_ip
        cursor.execute("""
            INSERT INTO alert_new (id, switch_id, switch_name, switch_ip, alert_type, severity, message, timestamp, acknowledged)
            SELECT 
                a.id, 
                a.switch_id,
                s.name,
                s.ip_address,
                a.alert_type,
                a.severity,
                a.message,
                a.timestamp,
                a.acknowledged
            FROM alert a
            LEFT JOIN switch s ON a.switch_id = s.id
        """)
        
        # Drop old table
        cursor.execute("DROP TABLE alert")
        
        # Rename new table
        cursor.execute("ALTER TABLE alert_new RENAME TO alert")
        
        # Commit changes
        conn.commit()
        
        print("✓ Database migration completed successfully!")
        print("✓ Alert table now supports historical data for deleted switches")
        
    except Exception as e:
        print(f"✗ Migration failed: {str(e)}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
