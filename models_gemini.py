import time
import os
import re
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# --- Configuration ---
APP_DATABASE_FILENAME = 'verdant_app_MAR_17_2025_v3.db'
DATABASE_URL = f"sqlite:///{APP_DATABASE_FILENAME}"

# --- Setup SQLAlchemy Engine and Session ---
# Use connect_args={"check_same_thread": False} for SQLite in non-threaded environments like a web app
# but for a simple script, we can omit it.
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()



# --- Table Mixins ---

class MetadataMixin:
    metadata_ = Column(Text)

class DescriptionMixin:
    description = Column(Text)

class TimestampMixin:
    date_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    date_last_accessed = Column(DateTime)

class SoftDeleteMixin:
    is_deleted = Column(Boolean, default=False, nullable=False)
    deleted_at = Column(DateTime, nullable=True)

class AuditMixin:
    created_by = Column(String)   # user_id
    updated_by = Column(String)

class StandardMixin(TimestampMixin, SoftDeleteMixin, AuditMixin, MetadataMixin, DescriptionMixin):
    pass



# ----------------------------------------------------------------------
# 🧱 Database Model Definitions (SQLAlchemy ORM)
# ----------------------------------------------------------------------

# --- Dimension Tables ---

class Address(Base, StandardMixin):
    __tablename__ = 'dim_address'
    address_key = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(String, unique=True)
    street = Column(Text)
    unit = Column(Text)
    city = Column(Text)
    state = Column(Text)
    zip_code = Column(Text)
    country = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)

    # Relationships (Optional but good practice)
    properties = relationship("DimProperty", back_populates="address")


class Client(Base, StandardMixin):
    __tablename__ = 'dim_client'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True)
    name = Column(Text)
    address_id = Column(Text) # Note: In a real ORM setup, this would be a ForeignKey
    phone_number = Column(Text)
    email = Column(Text)

    # Relationships (You can define relationships here if you had ForeignKeys)


class Property(Base, StandardMixin):
    __tablename__ = 'dim_property'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    owner_id = Column(Integer) # In a real ORM, this would be a ForeignKey to DimClient
    address_key = Column(Integer, ForeignKey('dim_address.address_key'))
    address = relationship("DimAddress", back_populates="properties")


class SiteBasename(Base, StandardMixin):
    __tablename__ = 'dim_site_basename'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    url_basename = Column(Text)

class Website(Base, StandardMixin):
    __tablename__ = 'dim_website'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    url_suffix = Column(Text)

class PendingDownloads(Base, StandardMixin):
    __tablename__ = 'dim_pending_downloads'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    url = Column(Text)

class User(Base, StandardMixin):
    __tablename__ = 'dim_user'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    username = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    email = Column(Text)
    phone_number = Column(Text)
    role = Column(Text)
    bio = Column(Text)


class Employee(Base, StandardMixin):
    __tablename__ = 'dim_employee'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    username = Column(Text)
    first_name = Column(Text)
    last_name = Column(Text)
    role = Column(Text)
    position = Column(Text)
    hire_date = Column(Text)
    salary = Column(Text)
    email = Column(Text)
    birthday = Column(Text)
    phone = Column(Text)


class Project(Base, StandardMixin):
    __tablename__ = 'dim_project'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True)
    name = Column(Text)
    material_cost_estimate = Column(Text)
    material_cost_actual = Column(Text)
    labor_bid = Column(Text)
    labor_cost_actual = Column(Text)
    project_status = Column(Text)
    scope_of_work = Column(Text)
    client = Column(Text)
    service = Column(Text)
    material = Column(Text)
    material_cost = Column(Text)
    notes = Column(Text)
    start_date = Column(Text) # NOTE: Original was missing type
    assigned_team = Column(Text)

class Tag(Base, StandardMixin):
    __tablename__ = 'dim_tag'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    color = Column(Text)

class Team(Base, StandardMixin):
    __tablename__ = 'dim_team'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    color = Column(Text)
    employee_ids = Column(Text)

class Task(Base, StandardMixin):
    __tablename__ = 'dim_task'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    priority = Column(Text)
    status = Column(Text)
    assigned_team = Column(Text)
    created_by = Column(Text) # user or employee id

class Folder(Base, StandardMixin):
    __tablename__ = 'dim_tag'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    color = Column(Text)

class File(Base, StandardMixin):
    __tablename__ = 'dim_file'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    color = Column(Text)

class Ledger(Base, StandardMixin):
    __tablename__ = 'dim_ledger'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    color = Column(Text)

class Person(Base, StandardMixin):
    __tablename__ = 'dim_person'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    age = Column(Text)
    socials = Column(Text)
    phone_numbers = Column(Text)


class Service(Base, StandardMixin):
    __tablename__ = 'dim_service'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    base_price = Column(Text)
    service_type = Column(Text)
    task_ids = Column(Text)

class Tenant(Base, StandardMixin):
    __tablename__ = 'dim_tenant'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    address = Column(Text)
    category = Column(Text)
    task_ids = Column(Text)

class Transaction(Base, StandardMixin):
    __tablename__ = 'dim_transaction'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    amount = Column(Text)
    category = Column(Text)
    task_ids = Column(Text)

class Item(Base, StandardMixin):
    __tablename__ = 'dim_item'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    sales_price = Column(Text)
    category = Column(Text)
    cost = Column(Text)
    task_ids = Column(Text)

class Inventory(Base, StandardMixin):
    __tablename__ = 'dim_inventory'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    total_items = Column(Text)
    item_id = Column(Text)
    price_cost = Column(Text)
    task_ids = Column(Text)

class Store(Base, StandardMixin):
    __tablename__ = 'dim_store'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    store = Column(Text)
    store = Column(Text)

class Vendor(Base, StandardMixin):
    __tablename__ = 'dim_vendor'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    category = Column(Text)
    industry = Column(Text)


# --- Fact Tables ---

class CustomerOrder(Base, StandardMixin):
    __tablename__ = 'fact_customer_orders'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    order_price = Column(Text)
    item_ids = Column(Text)
    customer_id = Column(Text)

class StoreInventory(Base, StandardMixin):
    __tablename__ = 'fact_store_inventory'
    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Text)
    name = Column(Text)
    store_id = Column(Text)
    inventory_id = Column(Text)



# ... (Define other Dim and Fact tables similarly, e.g., FactTransaction, DimProduct, etc.)

# NOTE: For brevity, only the classes corresponding to the original insert functions are fully shown,
# but the complete schema would require defining classes for ALL tables in `store_struct`.
# The `Base.metadata.create_all(engine)` call below will automatically create the tables defined as classes.

# ----------------------------------------------------------------------
# ⚙️ Initialization and Utility Functions
# ----------------------------------------------------------------------

def create_database_tables():
    """Creates all tables defined in the Base metadata."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created (or already exist).")

# Simple hash generator (dummy implementation for functionality)
def generate_random_hash(length):
    import uuid
    return str(uuid.uuid4().hex)[:length]

# ----------------------------------------------------------------------
# 🚀 Refactored ORM Insert Methods
# ----------------------------------------------------------------------

def get_db():
    """Dependency for getting a session (similar to FastAPI pattern)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def insert_employee(employee_id, username, first_name, last_name, role, position, hire_date, salary, email, birthday, phone):
    """Inserts employee into the dim_employee table using SQLAlchemy ORM."""
    print(f"Inserting employee: {first_name} {last_name}, ID: {employee_id}")
    db = next(get_db())
    date_created = str(time.time())
    date_updated = 'NA'

    new_employee = DimEmployee(
        employee_id=employee_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        role=role,
        position=position,
        hire_date=hire_date,
        salary=salary,
        email=email,
        birthday=birthday,
        phone=phone,
        date_created=date_created,
        date_updated=date_updated
    )

    try:
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
    except Exception as e:
        db.rollback()
        # SQLAlchemy exceptions are different, e.g., IntegrityError is under sqlalchemy.exc
        print(f"Error while inserting employee: {e}")
    finally:
        db.close()


def insert_user(user_id, username, first_name, last_name, role, bio, desc, email, phone_number, metadata):
    """Inserts user into the dim_user table using SQLAlchemy ORM."""
    print(f"Inserting user: {first_name} {last_name}, ID: {user_id}")
    db = next(get_db())
    date_created = str(time.time())
    date_updated = 'NA'

    new_user = DimUser(
        user_id=user_id, username=username, first_name=first_name, last_name=last_name,
        role=role, bio=bio, desc=desc, email=email, phone_number=phone_number,
        date_created=date_created, date_updated=date_updated, metadata_=metadata
    )

    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while inserting user: {e}")
    finally:
        db.close()


def insert_project(project_name, material_cost_estimate, material_cost_actual, labor_bid, labor_cost_actual,
                   project_status, scope_of_work, client, service, material, project_id, notes, start_date, metadata):
    """Inserts project into the dim_project table using SQLAlchemy ORM."""
    print(f"Inserting project: {project_name}, ID: {project_id}")
    db = next(get_db())
    date_created = str(time.time())
    date_updated = 'NA'
    
    # material_cost in the original schema was redundant, removing it from instantiation
    new_project = DimProject(
        project_id=project_id,
        project_name=project_name,
        material_cost_estimate=material_cost_estimate,
        material_cost_actual=material_cost_actual,
        labor_bid=labor_bid,
        labor_cost_actual=labor_cost_actual,
        project_status=project_status,
        scope_of_work=scope_of_work,
        client=client,
        service=service,
        material=material,
        notes=notes,
        start_date=start_date,
        date_created=date_created,
        date_updated=date_updated,
        metadata_=metadata
    )

    try:
        db.add(new_project)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while inserting project: {e}")
    finally:
        db.close()


def insert_tag(tag_name, description, tag_id):
    """Inserts a tag into the dim_tag table using SQLAlchemy ORM."""
    print(f"Inserting tag: {tag_name}, ID: {tag_id}")
    db = next(get_db())
    date_created = str(time.time())

    new_tag = DimTag(
        tag_name=tag_name,
        description=description,
        tag_id=tag_id,
        date_created=date_created
    )

    try:
        db.add(new_tag)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while inserting tag: {e}")
    finally:
        db.close()


def insert_client(client_name, client_number, client_email, client_id, address_id, description='NA'):
    """Inserts client into dim_client table using SQLAlchemy ORM."""
    print(f"Inserting client: {client_name}, ID: {client_id}")
    db = next(get_db())
    date_created = str(time.time())
    date_updated = 'NA'
    date_last_accessed = 'NA'

    new_client = DimClient(
        client_name=client_name,
        phone_number=client_number,
        email=client_email,
        client_id=client_id,
        address_id=address_id,
        description=description,
        date_created=date_created,
        date_updated=date_updated,
        date_last_accessed=date_last_accessed
    )

    try:
        db.add(new_client)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while inserting client: {e}")
    finally:
        db.close()


def insert_address(street, unit, city, state, zip_code):
    """Inserts address into dim_address and returns address_id using SQLAlchemy ORM."""
    db = next(get_db())
    address_id = generate_random_hash(11)
    date_created = str(time.time())

    new_address = DimAddress(
        address_id=address_id,
        street=street,
        unit=unit,
        city=city,
        state=state,
        zip_code=zip_code,
        date_created=date_created
    )
    
    try:
        db.add(new_address)
        db.commit()
        db.refresh(new_address) # Get the address_key
        return new_address.address_id
    except Exception as e:
        db.rollback()
        print(f"Error while inserting address: {e}")
        return None
    finally:
        db.close()


def insert_client_property(property_id, property_name, property_type, client_id, address_key):
    """Inserts property into dim_property using SQLAlchemy ORM."""
    print(f"Inserting property: {property_name}, ID: {property_id}")
    db = next(get_db())
    date_created = str(time.time())
    date_updated = 'NA'

    new_property = DimProperty(
        # Assuming property_id in the original schema was the primary key
        # In SQLAlchemy, we often use the auto-increment key. Using owner_id instead of client_id based on schema.
        # NOTE: The original `dim_property` was inconsistent. I've mapped `client_id` to `owner_id` and added a dummy `property_type` for the insert function call.
        property_name=property_name,
        owner_id=client_id, # Reusing client_id as owner_id
        address_key=address_key,
        date_created=date_created,
        date_updated=date_updated
    )

    try:
        db.add(new_property)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while inserting property: {e}")
    finally:
        db.close()


def insert_service(service_name, service_price, description, service_id, service_type):
    """Inserts service into dim_service table using SQLAlchemy ORM."""
    print(f"Inserting service: {service_name}, ID: {service_id}")
    db = next(get_db())
    date_created = str(time.time())
    date_updated = 'NA'
    date_last_accessed = 'NA'
    metadata = 'NA'
    task_ids = 'NA'

    new_service = DimService(
        service_id=service_id,
        service_name=service_name,
        base_price=service_price,
        service_type=service_type,
        description=description,
        task_ids=task_ids,
        date_created=date_created,
        date_updated=date_updated,
        date_last_accessed=date_last_accessed,
        metadata_=metadata
    )

    try:
        db.add(new_service)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error while inserting service: {e}")
    finally:
        db.close()

# NOTE: I removed the original `insert_table_attrs` utility as its functionality is entirely
# replaced by the idiomatic ORM approach of instantiating an object and calling `session.add(obj)`.

# ----------------------------------------------------------------------
# 🧪 Example Usage (Testing the Refactor)
# ----------------------------------------------------------------------

if __name__ == '__main__':
    # 1. Initialize Database
    create_database_tables()
    
    # 2. Example Inserts
    
    # Insert an Address
    address_id = insert_address(
        street="123 Evergreen Lane",
        unit="Apt 2B",
        city="Verdantville",
        state="CA",
        zip_code="90210"
    )
    
    # Insert a Client
    client_id = generate_random_hash(10)
    insert_client(
        client_name="Acme Landscaping Co.",
        client_number="555-1234",
        client_email="acme@corp.com",
        client_id=client_id,
        address_id=address_id,
        description="Major commercial client"
    )

    # Insert a Project
    project_id = generate_random_hash(10)
    insert_project(
        project_name="Spring Garden Renovation",
        material_cost_estimate="1500.00",
        material_cost_actual="1450.00",
        labor_bid="3000.00",
        labor_cost_actual="2800.00",
        project_status="Completed",
        scope_of_work="Full landscape overhaul",
        client="Acme Landscaping Co.",
        service="softscape",
        material="plants, soil, mulch",
        project_id=project_id,
        notes="Client happy with final result.",
        start_date="2025-03-01",
        metadata="NA"
    )
    
    # Insert an Employee
    insert_employee(
        employee_id=generate_random_hash(10),
        username="jdoe",
        first_name="John",
        last_name="Doe",
        role="Foreman",
        position="Senior Landscaper",
        hire_date="2020-05-15",
        salary="60000",
        email="jdoe@verdant.com",
        birthday="1985-01-01",
        phone="555-5555"
    )

    print("\nExample data inserted using SQLAlchemy ORM.")
