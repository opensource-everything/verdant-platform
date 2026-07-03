import random
import string
import sqlite3
import time
import os

'''

██████╗  █████╗ ████████╗ █████╗     ███████╗ ██████╗██╗  ██╗███████╗███╗   ███╗ █████╗ ███████╗
██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔════╝██╔════╝██║  ██║██╔════╝████╗ ████║██╔══██╗██╔════╝
██║  ██║███████║   ██║   ███████║    ███████╗██║     ███████║█████╗  ██╔████╔██║███████║███████╗
██║  ██║██╔══██║   ██║   ██╔══██║    ╚════██║██║     ██╔══██║██╔══╝  ██║╚██╔╝██║██╔══██║╚════██║
██████╔╝██║  ██║   ██║   ██║  ██║    ███████║╚██████╗██║  ██║███████╗██║ ╚═╝ ██║██║  ██║███████║
╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝

'''


def generate_random_hash(length):
    # Define the characters pool (alphanumeric)
    characters = string.ascii_letters + string.digits
    
    # Generate the hash by choosing 'length' number of random characters
    random_hash = ''.join(random.choice(characters) for i in range(length))
    
    return random_hash


random_hash_filename = generate_random_hash(5)
APP_DATABASE_FILENAME = f'verdant_app_DEC_15_2025_v5.db'
APP_DATABASE_FILENAME = os.path.join('dbs', APP_DATABASE_FILENAME)

material_categories = {
    'general': ['material', 'tools', 'parts', 'plants', 'trees', 'shrubs'],
    'plant': ['plants', 'trees', 'shrubs', 'flowers', 'groundcover', 'vines'],
    'hardscape': ['pavers', 'stones', 'gravel', 'mulch', 'sand', 'bricks', 'concrete', 'retaining walls', 'bricks', 'driveway pavers'],
    'soil': ['topsoil', 'compost', 'mulch', 'fertilizers', 'soil amendments', 'soil conditioners', 'peat moss'],
    'irrigation': ['sprinklers', 'drip irrigation systems', 'hoses', 'timers', 'pipes and fittings', 'valves', 'irrigation controllers'],
    'tool': ['shovels', 'rakes', 'pruners', 'wheelbarrows', 'lawn mowers', 'trimmers', 'leaf blowers', 'chainsaw', 'hedge trimmers', 'edgers'],
    'outdoor_features': ['patios', 'decks', 'pergolas', 'gazebos', 'outdoor_kitchens', 'fire pits', 'water features', 'retaining walls', 'fencing'],
    'lighting': ['landscape lighting', 'pathway lighting', 'accent lighting', 'outdoor string lights', 'deck lights'],
    'weed_control': ['herbicides', 'pesticides', 'weed barriers', 'organic control products', 'pre-emergent herbicides'],
    'lawn_care': ['grass seed', 'sod', 'lawn fertilizers', 'lawn aeration tools', 'lawn mowers', 'weed and feed products'],
    'decorative': ['statues', 'garden ornaments', 'planters', 'birdbaths', 'trellises', 'fountains'],
    'seasonal_item': ['snow removal equipment', 'de-icing products', 'salt spreaders', 'snow shovels'],
    'safety_gear': ['gloves', 'safety glasses', 'ear protection', 'work boots', 'knee pads', 'high-visibility vests']
}


services = {
    'maintenance': [
        'lawn care and mowing', 
        'fertilization and weed control', 
        'aeration and dethatching', 
        'seasonal cleanups', 
        'pruning and trimming', 
        'leaf removal', 
    ],

    'hardscape': [
        'landscape design consultation', 
        'custom landscape design', 
        'hardscape design', 
        'retaining wall', 
        'driveways and paving', 
        'outdoor kitchen and fireplace', 
        'fencing', 
        'walkway', 
        'deck', 
        'patio', 
        'outdoor lighting', 
        'gazebo and arbor construction',
        'shed and storage building',
    ],

    'softscape': [
        'lawn installation and seeding', 
        'flower beds and planting', 
        'tree and shrub planting', 
        'seasonal planting', 
        'mulching and edging',
    ],

    'irrigation systems': [
        'irrigation system design', 
        'irrigation system installation', 
        'irrigation maintenance and repair',
    ],

    'sustainability services': [
        'xeriscaping', 
        'native plant landscaping', 
        'green roof and vertical gardens', 
        'rain gardens',
    ],

    'outdoor structures': [
        'outdoor kitchen and fireplace',
        'gazebo and arbor construction',
        'shed and storage building',
    ],

    'water features': [
        'pond design and installation',
        'waterfall and fountain installation',
        'poolscapes',
    ],

    'snow removal': [
        'snow plowing and salting',
        'sidewalk shoveling',
    ],

    'pest control': [
        'pest and insect management',
    ],

    'consulting and education': [
        'landscape planning and budgeting',
        'sustainability consulting',
        'plant care and gardening classes',
    ],

    'lawn equipment services': [
        'lawn mower maintenance and repair',
        'power washing',
    ]
}


'''
Our motto is you should be able to transform any space you have

'''

store_struct = [
    #
    # Business Fact Tables
    #
    {
        'table_name': 'fact_transaction',
        'attributes': '''
            transaction_key INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            item_id TEXT,
            timestamp_id TEXT,
            amount TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'fact_sales',
        'attributes': '''
            sales_key INTEGER PRIMARY KEY AUTOINCREMENT,
            sales_id TEXT,
            item_id TEXT,
            customer_id TEXT,
            timestamp_id TEXT,
            amount TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'fact_sales_ledger',
        'attributes': '''
            ledger_key INTEGER PRIMARY KEY AUTOINCREMENT,
            ledger_id TEXT,
            item_id TEXT,
            payment_id TEXT,
            transaction_id TEXT,
            timestamp_id TEXT,
            debit TEXT,
            credit TEXT,
            balance TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'fact_stock_portfilo_ledger',
        'attributes': '''
            stock_portfolio_key INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            item_id TEXT,
            timestamp_id TEXT,
            debit TEXT,
            credit TEXT,
            balance TEXT
        '''
    },

    # Service and Client Facts
    {
        'table_name': 'fact_service_transaction',
        'attributes': '''
            transaction_key INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            customer_id TEXT,
            service_id TEXT,
            date_id TEXT,
            employee_id TEXT,
            amount TEXT,
            recurring_charge_frequency TEXT,
            timestamp_id TEXT
        '''
    },

    {
        'table_name': 'fact_client_workscopes',
        'attributes': '''
            project_key INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT,
            service_ids TEXT,
            address_id TEXT,
            status TEXT,
            start_date TEXT,
            end_date TEXT,
            bid_at TEXT,
            updated_at TEXT,
            created_at TEXT,
            actual_cost TEXT
        '''
    },

    {
        'table_name': 'fact_client_projects',
        'attributes': '''
            client_project_key INTEGER PRIMARY KEY AUTOINCREMENT,
            client_project_id TEXT,
            project_id TEXT,
            client_id TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        '''
    },

    #
    # Inventory and Product Management
    #
    {
        'table_name': 'fact_inventory',
        'attributes': '''
            inventory_key INTEGER PRIMARY KEY AUTOINCREMENT,
            inventory_id TEXT,
            product_id TEXT,
            warehouse_location TEXT,
            current_quantity TEXT,
            min_quantity TEXT,
            max_quantity TEXT,
            last_updated TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'fact_store_inventory',
        'attributes': '''
            store_inventory_key INTEGER PRIMARY KEY AUTOINCREMENT,
            store_inventory_id TEXT,
            inventory_id TEXT,
            store_id TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            product_ids TEXT
        '''
    },

    #
    # User and File Management Facts
    #
    {
        'table_name': 'fact_user_file_storage',
        'attributes': '''
            user_key INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            file_storage_ids TEXT,
            last_accessed TEXT,
            storage_size TEXT
        '''
    },

    {
        'table_name': 'fact_tagged_folders',
        'attributes': '''
            tagged_folder_key INTEGER PRIMARY KEY AUTOINCREMENT,
            tagged_folder_id TEXT,
            folder_id TEXT,
            tag_id TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'fact_user_drives',
        'attributes': '''
            user_drive_key INTEGER PRIMARY KEY AUTOINCREMENT,
            user_drive_id TEXT,
            drive_ids TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            max_drives TEXT
        '''
    },


    {
        'table_name': 'fact_retail_properties',
        'attributes': '''
            client_key INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT,
            address_id TEXT,
            phone_number TEXT,
            email TEXT,
            description TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        '''
    },

    #
    # User types
    #
    # Dimension Tables
    #
    {
        'table_name': 'dim_client',
        'attributes': '''
            client_key INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT UNIQUE,
            client_name TEXT,
            address_id TEXT,
            phone_number TEXT,
            email TEXT,
            description TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'dim_address',
        'attributes': '''
            address_key INTEGER PRIMARY KEY AUTOINCREMENT,
            address_id TEXT UNIQUE,
            street TEXT,
            unit TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            date_created TEXT,
            date_updated TEXT,
            metadata TEXT
        '''
    },


    {
        'table_name': 'dim_user',
        'attributes': '''
            user_key INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            description TEXT,
            phone_number TEXT,
            role TEXT,
            bio TEXT,
            desc TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'dim_employee',
        'attributes': '''
            employee_key INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT,
            username TEXT,
            description TEXT,
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            position TEXT,
            hire_date TEXT,
            salary TEXT,
            email TEXT,
            birthday TEXT,
            phone TEXT
        '''
    },



    # Business objects
    {
        'table_name': 'dim_payment',
        'attributes': '''
            pay_key INTEGER PRIMARY KEY AUTOINCREMENT,
            payment_id TEXT,
            payment_amount TEXT,
            date_created TEXT,
            date_updated TEXT,
            status TEXT,
            issued_by TEXT,
            issued_to TEXT,
            comment TEXT,
            metadata TEXT
        '''
    },

    # New addition table working on as of NOv 18
    # fix the attributes
    {
        'table_name': 'dim_ledger',
        'attributes': '''
            ledger_key INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            item_id TEXT,
            date TEXT,
            description TEXT,
            category TEXT,
            inflow TEXT,
            outflow TEXT,
            balance TEXT,
            account_type TEXT
        '''
    },

    {
        'table_name': 'dim_service',
        'attributes': '''
            service_key INTEGER PRIMARY KEY AUTOINCREMENT,
            service_id TEXT,
            service_name TEXT,
            base_price TEXT,
            service_type TEXT,
            description TEXT,
            task_ids TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'dim_supplier',
        'attributes': '''
            supplier_key INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id TEXT,
            supplier_name TEXT,
            contact_name TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            description TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            zip_code TEXT,
            country TEXT,
            rating TEXT,
            lead_time_days TEXT,
            sales_price TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'dim_product',
        'attributes': '''
            product_key INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT,
            product_name TEXT,
            description TEXT,
            sales_price TEXT,
            sku TEXT,
            available_stock TEXT,
            price_per_unit TEXT,
            cost_per_unit TEXT,
            supplier_id TEXT,
            date_created TEXT,
            date_updated TEXT,
            date_last_accessed TEXT,
            availability_status TEXT,
            our_cost TEXT,
            metadata TEXT
        '''
    },



    {
        'table_name': 'dim_project',
        'attributes': '''
            project_key INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT UNIQUE,
            project_name TEXT,
            material_cost_estimate TEXT,
            material_cost_actual TEXT,
            labor_bid TEXT,
            labor_cost_actual TEXT,
            project_status TEXT,
            scope_of_work TEXT,
            client TEXT,
            service TEXT,
            material TEXT,
            material_cost TEXT,
            notes TEXT,
            start_date TEXT,
            date_created TEXT,
            date_updated TEXT,
            metadata TEXT
        '''
    },

    # Properties
    {
        'table_name': 'dim_property',
        'attributes': '''
            property_id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_name TEXT,
            category TEXT,
            property_address TEXT,
            property_zipcode TEXT,
            property_city TEXT,
            property_state TEXT,
            owner_name TEXT,
            contact_phone TEXT,
            email TEXT,
            description TEXT,
            property_price TEXT,
            date_created TEXT,
            date_updated TEXT
        '''
    },

    # Base objects
    {
        'table_name': 'dim_timestamp',
        'attributes': '''
            timestamp_key INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp_id TEXT,
            timestamp TEXT
        '''
    },

    {
        'table_name': 'dim_tag',
        'attributes': '''
            tag_key INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id TEXT,
            tag_name TEXT,
            description TEXT,
            date_created TEXT
        '''
    },

    {
        'table_name': 'dim_dates',
        'attributes': '''
            date_key INTEGER PRIMARY KEY AUTOINCREMENT,
            date_id TEXT,
            year TEXT,
            quarter TEXT,
            month TEXT,
            day TEXT,
            week TEXT,
            day_of_week TEXT
        '''
    },

    {
        'table_name': 'dim_file',
        'attributes': '''
            file_key INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id TEXT,
            filename TEXT,
            file_path TEXT,
            date_created TEXT,
            date_updated TEXT,
            file_byte_ids TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'dim_item',
        'attributes': '''
            item_key INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT,
            item_name TEXT,
            price TEXT,
            date_created TEXT,
            date_updated TEXT,
            metadata TEXT
        '''
    },

    {
        'table_name': 'dim_folder',
        'attributes': '''
            folder_key INTEGER PRIMARY KEY AUTOINCREMENT,
            folder_id TEXT,
            folder_path TEXT,
            folder_name TEXT,
            description TEXT,
            category_name TEXT,
            date_created TEXT,
            date_updated TEXT,
            metadata TEXT
        '''
    }
]

# Assuming store_struct is defined above this function
# Assuming APP_DATABASE_FILENAME is a string pointing to your database file

def initialize_database_tables():
    """
    Creates all tables defined in the store_struct list in the SQLite database.
    """
    try:
        # 1. Establish database connection
        conn = sqlite3.connect(APP_DATABASE_FILENAME)
        cursor = conn.cursor()

        print(f"--- Initializing Database: {APP_DATABASE_FILENAME} ---")
        
        # 2. Iterate through each table definition
        for table_def in store_struct:
            table_name = table_def['table_name']
            # Clean up the multiline string attributes by stripping whitespace/comments
            attributes = table_def['attributes'].strip()
            
            # Special Fix for 'dim_ledger': Remove duplicate PRIMARY KEY definition
            if table_name == 'dim_ledger':
                # Remove the duplicate 'payment_key...' which causes an error
                attributes = attributes.split('payment_key INTEGER PRIMARY KEY AUTOINCREMENT')[0].strip()

            print(attributes)
            
            # Construct the final SQL statement
            sql_statement = f'CREATE TABLE IF NOT EXISTS {table_name} ({attributes})'

            # 3. Execute the SQL statement
            cursor.execute(sql_statement)
            print(f"Created/Verified table: {table_name}")

        # 4. Commit changes and close connection
        conn.commit()
        print("--- Database initialization complete. ---")

    except sqlite3.Error as e:
        print(f"An SQLite error occurred: {e}")
    finally:
        if conn:
            conn.close()



def insert_employee(employee_id, username, first_name, last_name, role, position, hire_date, salary, email, birthday, phone):
    """Inserts employee into the dim_employee table."""
    date_created = time.time()
    date_updated = 'NA' # Or calculate if needed
    print(f"Inserting employee: {first_name} {last_name}, ID: {employee_id}")
    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_employee (
                    employee_id, username, first_name, last_name, role, position, hire_date, salary, email, birthday, phone, date_created, date_updated
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                employee_id, username, first_name, last_name, role, position, hire_date, salary, email, birthday, phone, date_created, date_updated
            ))
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - Employee ID '{employee_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting employee: {e}")


def insert_user(user_id, username, first_name, last_name, role, bio, desc, email, phone_number, date_created, date_updated, metadata):
    """Inserts user into the dim_user table."""
    date_created = time.time()
    date_updated = 'NA' # Or calculate if needed
    print(f"Inserting user: {first_name} {last_name}, ID: {user_id}")
    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_user (
                    user_id, username, first_name, last_name, role, bio, desc, email, phone_number, date_created, date_updated, metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, username, first_name, last_name, role, bio, desc, email, phone_number, date_created, date_updated, metadata
            ))
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - User ID '{user_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting user: {e}")


def insert_project(project_name, material_cost_estimate, material_cost_actual, labor_bid, labor_cost_actual,
                   project_status, scope_of_work, client, service, material, project_id, date_created, date_updated, notes, start_date, metadata):
    """Inserts project into the dim_project table."""
    date_created = time.time()
    date_updated = 'NA'

    print(project_name, project_id)

    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_project (
                    project_id,
                    project_name,
                    material_cost_estimate,
                    material_cost_actual,
                    labor_bid,
                    labor_cost_actual,
                    project_status,
                    scope_of_work,
                    client,
                    service,
                    material,
                    notes,
                    start_date,
                    date_created,
                    metadata
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id,
                project_name,
                material_cost_estimate,
                material_cost_actual,
                labor_bid,
                labor_cost_actual,
                project_status,
                scope_of_work,
                client,
                service,
                material,
                notes,
                start_date,
                date_created,
                metadata
            ))
            conn.commit()

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - Project ID '{project_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting project: {e}")



def insert_tag(tag_name, description, tag_id):
    """Inserts a tag into the dim_tag table."""
    date_created = time.time()

    print(tag_name, tag_id)

    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_tag (tag_name, description, tag_id, date_created)
                VALUES (?, ?, ?, ?)
            """, (tag_name, description, tag_id, date_created))
            conn.commit()

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - Tag ID '{tag_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting tag: {e}")


'''
2025 Feb insertion techinques for clients

start of client insertion methods

'''

def insert_client(client_name, client_number, client_email, client_id, address_id, description='NA'):
    """Inserts client into dim_client table."""
    date_created = time.time()

    print(client_name, client_number, client_id)

    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_client (client_name, phone_number, email, client_id, address_id, description, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (client_name, client_number, client_email, client_id, address_id, description, date_created))
            conn.commit()

    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - Client ID '{client_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting client: {e}")


def insert_address(street, unit, city, state, zip_code):
    """Inserts address into dim_address and returns address_id."""
    address_id = generate_random_hash(11)
    created_at = time.time()

    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_address (address_id, street, unit, city, state, zip_code, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (address_id, street, unit, city, state, zip_code, created_at))
            conn.commit()
        return address_id
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - Address ID '{address_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting address: {e}")
    return None  # Return None if insertion fails


def insert_client_property(property_id, property_name, property_type, client_id):
    """Inserts property into dim_property and links it to a client."""
    created_at = time.time()

    try:
        with sqlite3.connect(APP_DATABASE_FILENAME) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO dim_property (property_id, property_name, property_type, client_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (property_id, property_name, property_type, client_id, created_at))
            conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error: {e} - Property ID '{property_id}' might already exist.")
    except Exception as e:
        print(f"Unexpected error while inserting property: {e}")







def insert_category(category_name, parent_category_id, description, random_id):
    db_name = APP_DATABASE_FILENAME
    table_name = 'dim_category'
    current_time = time.time()

    attrs = ['parent_category_id', 'description', 'category_name', 'category_id', 'date_created']
    values = [parent_category_id, description, category_name, random_id, current_time]

    insert_table_attrs(table_name=table_name, table_attrs=attrs, values=values)



def insert_folder(folder_path, folder_name, description, category_name, folder_id):
    table_name = 'dim_folder'
    current_time = time.time()

    attrs = ['folder_id', 'folder_path', 'folder_name', 'description', 'category_name', 'date_created']
    values = [folder_id, folder_path, folder_name, description, category_name, current_time]

    insert_table_attrs(table_name=table_name, table_attrs=attrs, values=values)
    '''
    try:
    except:
        print(len(attrs), len(values))
    '''



def insert_service(service_name, service_price, description, service_id, service_type):
    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()
    c.execute("INSERT INTO dim_service (service_name, base_price, description, service_id, service_type) VALUES (?, ?, ?, ?, ?)", (service_name, service_price, description, service_id, service_type))
    conn.commit()
    conn.close()



def insert_task(task_name, status, assigned_to, created_by, description, task_id):
    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()
    insert_statement = construct_insert_statement('dim_task', [task_name, status, assigned_to, created_by, description, task_id])

    # New Refactored
    # STATUS: Working on this as of 11-13-25
    # Testing phase
    c.execute(insert_statement, (task_name, status, assigned_to, created_by, description, task_id))

    # Old attempting to refactor
    # c.execute("INSERT INTO dim_task (task_name, status, assigned_to, created_by, description, task_id) VALUES (?,?,?,?,?,?)", (task_name, status, assigned_to, created_by, description, task_id))
    conn.commit()
    conn.close()



# Function to insert product into database
def insert_product(product_name, cost, price, description, product_id):
    # conn = sqlite3.connect('products.db')
    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()


    try:
        c.execute("INSERT INTO dim_product (product_name, our_cost, sales_price, description, product_id) VALUES (?, ?, ?, ?, ?)", (product_name, cost, price, description, product_id))

        conn.commit()
    except sqlite3.IntegrityError:
        # Handle unique constraint error
        print(f"Product with ID '{product_id}' already exists.")
    finally:
        conn.close()

'''
End of use case DB insertion methods
'''


# Other Database Utility Functions



def construct_insert_statement(table_name, table_attrs):
    qmarks = ['?' for x in range(len(table_attrs))] 
    marks = f"({', '.join(qmarks)})"
    attrs = f"({', '.join(table_attrs)})"
    tuple_attrs = tuple(table_attrs)
    sql_statement = f'INSERT INTO {table_name} {attrs} VALUES {marks}'
    return sql_statement



# NEW VERSION 
def insert_table_attrs(table_name=None, table_attrs=None, values=None, database_filename=APP_DATABASE_FILENAME):

    if table_attrs is None or values is None:
        raise ValueError("table_attrs and values must be provided")
    if len(table_attrs) != len(values):
        raise ValueError("The number of attributes and values must match")

    print(len(table_attrs))
    print(len(values))

    # Establish database connection
    conn = sqlite3.connect(database_filename)
    c = conn.cursor()

    # Construct placeholders and SQL statement
    placeholders = ', '.join(['?'] * len(table_attrs))
    columns = ', '.join(table_attrs)
    sql_statement = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

    # Execute SQL statement with provided values
    c.execute(sql_statement, values)
    conn.commit()
    conn.close()


# NEW WORKING VERSION 
def retrieve_tables(table_name, mode='all', random_limit='30'):
    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()
    if mode == 'all':
        c.execute(f"SELECT * FROM {table_name}")
    elif mode == 'random':
        c.execute(f"SELECT * FROM {table_name} ORDER BY RANDOM() LIMIT {random_limit}")
    table_rows = c.fetchall()
    conn.close()

    return table_rows



def initial_insert_subjects_into_db(db_filename, names_list):

    for name in names_list:
        names = name.split(' ')
        if len(names) < 2:
            first_name = names[0] 
        elif len(names) == 2:
            first_name, last_name = names
        elif len(names) > 3:
            first_name, last_name, middle_name = None, None, None
        elif len(names) > 2:
            first_name, middle_name, last_name = names
        elif len(names) == 1 or len(names) < 2:
            first_name, last_name, middle_name = None, None, None


        subject_id = generate_random_hash(10)
        try:
            print(first_name, middle_name, last_name, subject_id)
        except:
            pass


def extract_names(directory):
    import re
    # Set to store unique names
    unique_names = set()

    # Regular expression pattern to match the filename format, ignoring file extension
    pattern = r"([\w+\s]*)\[\d+\]"

    # Iterate through files in the directory
    for filename in os.listdir(directory):
        # Split the filename and extension
        name_part, _ = os.path.splitext(filename)
        match = re.match(pattern, name_part)
        if match:
            # print(match.group(1))
            first_name = match.group(1)
            # Add the name to the set (automatically handles duplicates)
            unique_names.add(f"{first_name.rstrip()}")
        else:
            continue

    # Convert set to sorted list
    return sorted(list(unique_names))

# database utilities


'''
LEGACY CODE will be depricated soon
12/15/2025
NOT NEEDED
Table Creation

def create_landscape_app_tables():
    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()

    table_digest(c)

    # table_name = 'dim_network_drives'
    # table_attrs = 'drive_ID, drive_name, drive_path'
    # generated_hash = generate_random_hash(8)

    # drive_letters = {'Nexus2':'E:', 'Nexus1':'H:', 'MEDIA':'G:', 'STOCK':'D:', 'Windows':'C:'}
    # (generated_hash, 'E:')
    # c.execute(f'INSERT INTO {table_name} {table_attrs} VALUES (?,?,?)', ())

    conn.commit()
    conn.close()

# Create all tables defined in store_struct
def table_digest(c):
    for t in store_struct:

        table_name = t['table_name']
        attrs = t['attributes']
        # print(table_name, attrs)

        table_string = create_table_string(table_name, attrs)
        c.execute(table_string)
'''

# LEGACY CODE
# Function to create database table if it doesn't exist
def create_product_table():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
                 id INTEGER PRIMARY KEY,
                 product_name TEXT NOT NULL,
                 description TEXT,
                 product_id TEXT UNIQUE NOT NULL)''')
    conn.commit()
    conn.close()




def create_table_string(table_name, table_attrs):
    return f'''CREATE TABLE IF NOT EXISTS {table_name} ( {table_attrs} )'''






'''
input a list of strings
get only strings with no numbers
'''

def filter_strings_without_numbers(input_list):
    pattern = re.compile(r'\d')
    return [string for string in input_list if not pattern.search(string) and '.jp' not in string and '.p' not in string and '.d' not in string and '.t' not in string]

def id_generator():
    return generate_random_hash(11)

def generate_service_id():
    return generate_random_hash(11)

def get_index_data():
    folder = r'A:\INDEX second_gen'
    names_list = extract_names(folder)
    initial_insert_subjects_into_db(APP_DATABASE_FILENAME, names_list)
    # print(names_list)


def main():
    initialize_database_tables()

if __name__ == '__main__':
    pass
    # main()
