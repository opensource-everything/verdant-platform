# verdant_app/database.py

import sqlite3
import os
import time
import logging

from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DATABASE_FILE = Config.DATABASE_FILENAME

# Define the database schema as a separate data structure for readability
DB_SCHEMA = [
    {
        'table_name': 'dim_client',
        'attributes': """
            client_key INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id TEXT UNIQUE NOT NULL,
            client_name TEXT NOT NULL,
            address_id TEXT,
            phone_number TEXT,
            email TEXT,
            description TEXT,
            date_created TEXT NOT NULL,
            date_updated TEXT,
            date_last_accessed TEXT,
            metadata TEXT
        """
    },
    {
        'table_name': 'dim_address',
        'attributes': """
            address_key INTEGER PRIMARY KEY AUTOINCREMENT,
            address_id TEXT UNIQUE NOT NULL,
            street TEXT NOT NULL,
            unit TEXT,
            city TEXT NOT NULL,
            state TEXT NOT NULL,
            zip_code TEXT NOT NULL,
            country TEXT,
            latitude REAL,
            longitude REAL,
            date_created TEXT NOT NULL,
            date_updated TEXT,
            metadata TEXT
        """
    },
    {
        'table_name': 'dim_project',
        'attributes': """
            project_key INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT UNIQUE NOT NULL,
            project_name TEXT NOT NULL,
            material_cost_estimate TEXT,
            material_cost_actual TEXT,
            labor_bid TEXT,
            labor_cost_actual TEXT,
            project_status TEXT,
            scope_of_work TEXT,
            client TEXT NOT NULL,
            service TEXT,
            material TEXT,
            notes TEXT,
            start_date TEXT,
            date_created TEXT NOT NULL,
            date_updated TEXT,
            metadata TEXT
        """
    },
    {
        'table_name': 'dim_tag',
        'attributes': """
            tag_key INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_id TEXT UNIQUE NOT NULL,
            tag_name TEXT NOT NULL,
            description TEXT,
            date_created TEXT NOT NULL
        """
    }
    # Add other tables here following the same format
]

def create_table_string(table_name, table_attrs):
    """Constructs a CREATE TABLE SQL statement."""
    return f'CREATE TABLE IF NOT EXISTS {table_name} ( {table_attrs} );'

def init_db():
    """Initializes the database by creating all tables if they don't exist."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        for table in DB_SCHEMA:
            create_sql = create_table_string(table['table_name'], table['attributes'])
            cursor.execute(create_sql)
        conn.commit()
        logging.info("Database tables initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database error during initialization: {e}")
    finally:
        if conn:
            conn.close()

def insert_client(client_name: str, client_number: str, client_email: str, client_id: str, address_id: str, description: str = 'NA'):
    """Inserts a new client into the dim_client table."""
    date_created = time.time()
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dim_client (client_id, client_name, phone_number, email, address_id, description, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (client_id, client_name, client_number, client_email, address_id, description, date_created))
            conn.commit()
        logging.info(f"Client '{client_name}' inserted successfully with ID: {client_id}")
        return True
    except sqlite3.IntegrityError as e:
        logging.error(f"Database Integrity Error: {e} - Client ID '{client_id}' already exists.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error inserting client: {e}")
        return False

def insert_address(street: str, unit: str, city: str, state: str, zip_code: str, address_id: str) -> str | None:
    """Inserts an address and returns its ID."""
    date_created = time.time()
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dim_address (address_id, street, unit, city, state, zip_code, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (address_id, street, unit, city, state, zip_code, date_created))
            conn.commit()
        logging.info(f"Address '{street}, {city}' inserted successfully with ID: {address_id}")
        return address_id
    except sqlite3.IntegrityError as e:
        logging.error(f"Database Integrity Error: {e} - Address ID '{address_id}' already exists.")
        return None
    except Exception as e:
        logging.error(f"Unexpected error inserting address: {e}")
        return None

def insert_project(project_name: str, **kwargs):
    """Inserts a new project into the dim_project table."""
    project_id = kwargs.get('project_id')
    date_created = time.time()
    date_updated = 'NA'
    
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO dim_project (project_id, project_name, material_cost_estimate, material_cost_actual, 
                                        labor_bid, labor_cost_actual, project_status, scope_of_work, client, 
                                        service, material, notes, start_date, date_created)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project_id,
                project_name,
                kwargs.get('material_cost_estimate'),
                kwargs.get('material_cost_actual', 'NA'),
                kwargs.get('labor_bid'),
                kwargs.get('labor_cost_actual', 'NA'),
                kwargs.get('project_status'),
                kwargs.get('scope_of_work'),
                kwargs.get('client'),
                kwargs.get('service'),
                kwargs.get('material'),
                kwargs.get('notes'),
                kwargs.get('start_date'),
                date_created
            ))
            conn.commit()
        logging.info(f"Project '{project_name}' inserted successfully with ID: {project_id}")
        return True
    except sqlite3.IntegrityError as e:
        logging.error(f"Database Integrity Error: {e} - Project ID '{project_id}' already exists.")
        return False
    except Exception as e:
        logging.error(f"Unexpected error inserting project: {e}")
        return False

# You can add similar insert functions for other tables (dim_tag, etc.)
# ...

def get_all_clients():
    """Fetches all clients from the database."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row  # This allows fetching rows as dictionaries
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dim_client ORDER BY date_created DESC")
        clients = cursor.fetchall()
        return [dict(row) for row in clients]
    except sqlite3.Error as e:
        logging.error(f"Database error fetching clients: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_client_by_id(client_id: str):
    """Fetches a single client by their ID."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dim_client WHERE client_id = ?", (client_id,))
        client = cursor.fetchone()
        return dict(client) if client else None
    except sqlite3.Error as e:
        logging.error(f"Database error fetching client by ID: {e}")
        return None
    finally:
        if conn:
            conn.close()