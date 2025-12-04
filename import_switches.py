import pandas as pd
from app import app
from models import db, Switch

def import_switches_from_excel(excel_file):
    """
    Import switches from Excel file
    
    Expected columns:
    - Switch Location (or Location)
    - IP Address (or IP)
    - Type (or Device Type)
    - Username
    - Password
    
    Section headings (block/floor names) will be detected and used as prefixes
    """
    
    # Read Excel file - skip first row if it's a title, use second row as header
    df = pd.read_excel(excel_file, header=1)
    
    # Drop the first column if it's just serial numbers
    if 'S.NO' in df.columns or 's.no' in df.columns:
        df = df.drop(df.columns[0], axis=1)
    
    # Normalize column names (case-insensitive)
    df.columns = df.columns.str.strip().str.lower()
    
    # Map possible column name variations
    column_mapping = {
        'location': ['switch location', 'location', 'name', 'switch name'],
        'ip': ['ip address', 'ip', 'address'],
        'type': ['type', 'device type', 'device_type', 'vendor'],
        'username': ['username', 'user', 'ssh username'],
        'password': ['password', 'pass', 'ssh password']
    }
    
    # Find actual column names
    columns = {}
    for key, variations in column_mapping.items():
        for col in df.columns:
            if col in variations:
                columns[key] = col
                break
    
    print(f"Detected columns: {columns}")
    print(f"Total rows: {len(df)}")
    
    current_section = ""
    imported_count = 0
    skipped_count = 0
    
    with app.app_context():
        for index, row in df.iterrows():
            # Check if this is a section header (all other fields are empty)
            if pd.notna(row.get(columns.get('location', ''))) and \
               pd.isna(row.get(columns.get('ip', ''))):
                current_section = str(row[columns['location']]).strip()
                print(f"\n--- Section: {current_section} ---")
                continue
            
            # Skip rows with missing critical data
            if pd.isna(row.get(columns.get('ip', ''))) or \
               pd.isna(row.get(columns.get('username', ''))) or \
               pd.isna(row.get(columns.get('password', ''))):
                skipped_count += 1
                continue
            
            # Extract data
            location = str(row[columns['location']]).strip() if pd.notna(row.get(columns.get('location', ''))) else f"Switch-{index}"
            ip_address = str(row[columns['ip']]).strip()
            device_type = str(row[columns['type']]).strip().lower() if pd.notna(row.get(columns.get('type', ''))) else 'cisco_ios'
            username = str(row[columns['username']]).strip()
            password = str(row[columns['password']]).strip()
            
            # Create full name with section prefix
            if current_section:
                full_name = f"{current_section} - {location}"
            else:
                full_name = location
            
            # Map device type to standard values
            device_type_map = {
                'cisco': 'cisco_ios',
                'cisco ios': 'cisco_ios',
                'aruba': 'aruba_os',
                'hp': 'hp_procurve',
                'hp procurve': 'hp_procurve',
                'cambium': 'cambium',
                'tplink': 'tplink',
                'tp-link': 'tplink',
                'dlink': 'dlink',
                'd-link': 'dlink',
            }
            device_type = device_type_map.get(device_type, device_type)
            
            # Check if switch already exists
            existing = Switch.query.filter_by(ip_address=ip_address).first()
            if existing:
                print(f"⚠ Skipping {full_name} ({ip_address}) - already exists")
                skipped_count += 1
                continue
            
            # Create new switch
            switch = Switch(
                name=full_name,
                ip_address=ip_address,
                username=username,
                password=password,
                device_type=device_type
            )
            
            db.session.add(switch)
            print(f"✓ Added: {full_name} ({ip_address}) - {device_type}")
            imported_count += 1
        
        # Commit all changes
        db.session.commit()
    
    print(f"\n{'='*50}")
    print(f"Import completed!")
    print(f"Imported: {imported_count} switches")
    print(f"Skipped: {skipped_count} rows")
    print(f"{'='*50}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python import_switches.py <excel_file.xlsx>")
        print("\nExample: python import_switches.py switches.xlsx")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    
    try:
        import_switches_from_excel(excel_file)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
