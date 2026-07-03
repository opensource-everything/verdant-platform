# models.py

from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSON  # Use JSON if on Postgres


from typing import Optional
from datetime import datetime
from dataclasses import dataclass
import time

# --- Configuration ---
APP_DATABASE_FILENAME = 'verdant_app_MAR_17_2025_v3.db'
DATABASE_URL = f"sqlite:///{APP_DATABASE_FILENAME}"

# --- SQLAlchemy Setup ---
Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False) # Set echo=True for SQL debugging
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Functional Mixins ---
# For SQLite, fall back to Text (store as JSON string)

class MetadataMixin:
    metadata_ = Column(Text)  # Avoid 'metadata' (SQLAlchemy reserved word)

class DescriptionMixin:
    description = Column(Text)  # Avoid 'metadata' (SQLAlchemy reserved word)

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

class StandardMixin(TimestampMixin, SoftDeleteMixin, AuditMixin):
    pass

# --- Dataclasses (Optional, for input/output validation or API schemas) ---
# These are not strictly necessary for ORM operations but can be helpful for structure.

# Related to people
@dataclass
class ClientData:
    client_name: str
    phone_number: str = 'NA'
    email: str = 'NA'
    client_id: str = None # Will be generated if None
    address_id: str = 'NA' # Or handle address creation/linking separately


@dataclass
class UserData:
    username: str
    first_name: str
    last_name: str
    user_id: Optional[str] = None # Will be generated if None
    email: Optional[str] = None # Will be generated if None
    phone_number: Optional[str] = None # Will be generated if None
    role: Optional[str] = None # Will be generated if None
    bio: Optional[str] = None # Will be generated if None

@dataclass
class EmployeeData:
    first_name: str
    last_name: str
    username: str
    employee_id: str = None # Will be generated if None
    role: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[str] = None
    salary: Optional[str] = None
    email: Optional[str] = None
    birthday: Optional[str] = None
    phone: Optional[str] = None

# Business objects
@dataclass
class ProjectData:
    project_name: str
    project_id: str = None # Will be generated if None
    material_cost_estimate: float = None
    material_cost_actual: float = None
    labor_bid: float = None
    labor_cost_actual: float = None
    project_status: Optional[str] = None
    scope_of_work: Optional[str] = None
    client: Optional[str] = None # client_id
    service: Optional[str] = None # service_id
    material: Optional[str] = None # material_id
    notes: Optional[str] = None
    start_date: datetime = None # Or str if passed from form

@dataclass
class ProductData:
    product_name: str
    product_id: str = None # Will be generated if None

@dataclass
class ServiceData:
    service_name: str
    service_id: str = None # Will be generated if None

@dataclass
class ProductData:
    product_name: str
    product_id: str = None # Will be generated if None

@dataclass
class TeamData:
    team_name: str
    team_id: str = None # Will be generated if None

@dataclass
class LedgerData:
    ledger_name: str
    ledger_id: str = None # Will be generated if None
    inflow: float = 0.0
    outflow: float = 0.0
    category: Optional[str] = None
    currency: Optional[str] = None
    transaction_id: Optional[str] = None
    client_id: Optional[str] = None

@dataclass
class PropertyData:
    property_name: str
    property_id: str = None # Will be generated if None

@dataclass
class FileData:
    file_name: str
    file_id: str = None # Will be generated if None

@dataclass
class FolderData:
    folder_name: str
    folder_id: str = None # Will be generated if None
    folder_path: str



# --- SQLAlchemy Models ---
class Client(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_client'

    client_key = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(String, unique=True, nullable=False) # Use String if it's a hash
    client_name = Column(String, nullable=False)
    address_id = Column(String, ForeignKey('dim_address.address_id')) # Reference other table
    phone_number = Column(String)
    email = Column(String)

    # Relationship: A client can have many properties (if property links back to client_id)
    # properties = relationship("Property", back_populates="client")

    def __repr__(self):
        return f"<Client(name='{self.client_name}', id='{self.client_id}')>"

class Address(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_address'

    address_key = Column(Integer, primary_key=True, autoincrement=True)
    address_id = Column(String, unique=True, nullable=False)
    street = Column(String)
    unit = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    # Relationship: An address can belong to many clients/properties (or one, depending on your logic)
    # Example assuming one address per client for simplicity
    # client = relationship("Client", back_populates="address") # Adjust back_populates if needed

    def __repr__(self):
        return f"<Address(street='{self.street}', city='{self.city}')>"

class Project(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_project's

    project_key = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String, unique=True, nullable=False)
    project_name = Column(String, nullable=False)
    material_cost_estimate = Column(Float)
    material_cost_actual = Column(Float)
    labor_bid = Column(Float)
    labor_cost_actual = Column(Float)
    project_status = Column(String) # Consider using Enum for statuses
    scope_of_work = Column(Text)
    client = Column(String) # Store client_id as string for now, or link via ForeignKey
    service = Column(String) # Store service_id as string for now, or link via ForeignKey
    material = Column(String) # Store material_id as string for now, or link via ForeignKey
    material_cost = Column(Float) # Added based on table definition
    notes = Column(Text)
    start_date = Column(DateTime) # Use DateTime type

    # Relationships (if foreign keys are properly defined)
    # client_rel = relationship("Client", foreign_keys=[client]) # Example, adjust if client column is FK
    # service_rel = relationship("Service", foreign_keys=[service]) # Example
    # material_rel = relationship("Material", foreign_keys=[material]) # Example

    def __repr__(self):
        return f"<Project(name='{self.project_name}', id='{self.project_id}')>"

class User(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_user'

    user_key = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False) # Consider making unique if intended as an ID
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    phone_number = Column(String)
    role = Column(String)
    bio = Column(Text)

    def __repr__(self):
        return f"<User(username='{self.username}', id='{self.user_id}')>"

class Employee(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_employee'

    employee_key = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, nullable=False) # Consider making unique if intended as an ID
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String)
    position = Column(String)
    hire_date = Column(String) # Consider DateTime if format is consistent
    salary = Column(String) # Consider Float if it's a number
    email = Column(String)
    birthday = Column(String) # Consider Date if format is consistent
    phone = Column(String)

    def __repr__(self):
        return f"<Employee(name='{self.first_name} {self.last_name}', id='{self.employee_id}')>"

class Service(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_service'

    service_key = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String, nullable=False) # Consider making unique if intended as an ID
    service_name = Column(String, nullable=False)
    base_price = Column(String) # Consider Float if it's a number
    service_type = Column(String)
    description = Column(Text)
    task_ids = Column(Text) # Store as comma-separated string or JSON
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_last_accessed = Column(DateTime)
    metadata_ = Column(Text)

    def __repr__(self):
        return f"<Service(name='{self.service_name}', id='{self.service_id}')>"

class Ledger(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_ledger'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)
    transaction_id = Column(String) # Consider Float if it's a number
    category = Column(String)
    currency = Column(Text)
    inflow = Column(Text) # Store as comma-separated string or JSON
    outflow = Column(Text) # Store as comma-separated string or JSON

    def __repr__(self):
        return f"<Ledger(name='{self.ledger_name}', id='{self.ledger_id}')>"



class Product(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_product'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)
    sales_price = Column(String) # Consider Float if it's a number
    sku = Column(String)
    available_stock = Column(String) # Consider Integer if it's a number
    price_per_unit = Column(String) # Consider Float if it's a number
    cost_per_unit = Column(String) # Consider Float if it's a number
    supplier_id = Column(String) # Store supplier_id as string for now, or link via ForeignKey
    availability_status = Column(Boolean, default=True) # Use Boolean type
    our_cost = Column(String) # Consider Float if it's a number

    def __repr__(self):
        return f"<Product(name='{self.product_name}', id='{self.product_id}')>"

class Tag(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_tag'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)

    def __repr__(self):
        return f"<Tag(name='{self.name}', id='{self.id}')>"

class Task(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_task'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Task(name='{self.task_name}', id='{self.task_id}')>"

class Department(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin, DescriptionMixin):
    __tablename__ = 'dim_department'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    def __repr__(self):
        return f"<Tag(name='{self.department_name}', id='{self.department_id}')>"

class Team(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_team'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)
    description = Column(Text)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    date_last_accessed = Column(DateTime)
    metadata_ = Column(Text)

    def __repr__(self):
        return f"<Tag(name='{self.team_name}', id='{self.team_id}')>"

class Folder(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_folder'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Folder(name='{self.tag_name}', id='{self.tag_id}')>"


class BackupPaths(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_backup_paths'

    path_key = Column(Integer, primary_key=True, autoincrement=True)
    path_id = Column(String, nullable=False) # Consider making unique if intended as an ID
    path_name = Column(String, nullable=False)

    def __repr__(self):
        return f"<BackupPath(name='{self.path_name}', id='{self.path_id}')>"


class File(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_file'

    file_key = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(String, nullable=False) # Consider making unique if intended as an ID
    filename = Column(String, nullable=False)

    def __repr__(self):
        return f"<File(name='{self.tag_name}', id='{self.tag_id}')>"

class Property(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_property'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, unique=True, nullable=False) # Adjusted to be unique and primary key
    name = Column(String, nullable=False)
    owner_id = Column(Integer) # Or String, depending on how owner is represented
    address_key = Column(Integer, ForeignKey('dim_address.address_key')) # Corrected FK reference

    # Relationship: A property belongs to an address
    address = relationship("Address", back_populates="properties")

    def __repr__(self):
        return f"<Property(name='{self.property_name}', id='{self.property_id}')>"

# Add back_populates to Address if Property links to it
Address.properties = relationship("Property", back_populates="address")

# Add other models as needed based on store_struct...

class Date(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_date'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Date(name='{self.date_name}', id='{self.date_id}')>"

class Timestamp(Base, TimestampMixin, SoftDeleteMixin, MetadataMixin):
    __tablename__ = 'dim_timestamp'

    key = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String, nullable=False) # Consider making unique if intended as an ID
    name = Column(String, nullable=False)

    def __repr__(self):
        return f"<Timestamp(name='{self.timestamp_name}', id='{self.timestamp_id}')>"


# --- CRUD Operations (Using SQLAlchemy Session) ---

def create_client(db_session, client_data: ClientData):
    """Creates a new client record using ClientData."""
    from utils import generate_random_hash # Import ID generator here to avoid circular imports if needed
    if not client_data.client_id:
        client_data.client_id = generate_random_hash(11)

    db_client = Client(
        client_name=client_data.client_name,
        phone_number=client_data.phone_number,
        email=client_data.email,
        client_id=client_data.client_id,
        address_id=client_data.address_id,
        description=client_data.description,
        date_created=datetime.utcnow()
    )
    db_session.add(db_client)
    db_session.commit()
    db_session.refresh(db_client)
    return db_client

def create_project(db_session, project_data: ProjectData):
    """Creates a new project record using ProjectData."""
    from utils import generate_random_hash
    if not project_data.project_id:
        project_data.project_id = generate_random_hash(12)

    db_project = Project(
        project_name=project_data.project_name,
        project_id=project_data.project_id,
        material_cost_estimate=project_data.material_cost_estimate,
        material_cost_actual=project_data.material_cost_actual,
        labor_bid=project_data.labor_bid,
        labor_cost_actual=project_data.labor_cost_actual,
        project_status=project_data.project_status,
        scope_of_work=project_data.scope_of_work,
        client=project_data.client,
        service=project_data.service,
        material=project_data.material,
        notes=project_data.notes,
        start_date=project_data.start_date,
        metadata=project_data.metadata,
        date_created=datetime.utcnow()
    )
    db_session.add(db_project)
    db_session.commit()
    db_session.refresh(db_project)
    return db_project

# Get by IDs
def get_client_by_id(db_session, client_id: str):
    """Retrieves a client by client_id."""
    return db_session.query(Client).filter(Client.client_id == client_id).first()

def get_project_by_id(db_session, project_id: str):
    """Retrieves a project by project_id."""
    return db_session.query(Project).filter(Project.project_id == project_id).first()

def get_tag_by_id(db_session, project_id: str):
    """Retrieves a project by project_id."""
    return db_session.query(Project).filter(Project.project_id == project_id).first()



# Get all rows
def get_all_clients(db_session):
    """Retrieves all clients."""
    return db_session.query(Client).all()

def get_all_projects(db_session):
    """Retrieves all projects."""
    return db_session.query(Project).all()

def get_all_tags(db_session):
    """Retrieves all tags."""
    return db_session.query(Tag).all()

def get_all_folders(db_session):
    """Retrieves all tags."""
    return db_session.query(Folder).all()

def get_all_files(db_session):
    """Retrieves all tags."""
    return db_session.query(File).all()

def get_all_timestamps(db_session):
    """Retrieves all tags."""
    return db_session.query(Timstamp).all()

def get_all_dates(db_session):
    """Retrieves all tags."""
    return db_session.query(Tag).all()

def get_all_services(db_session):
    """Retrieves all services."""
    return db_session.query(Service).all()

# Add other CRUD functions as needed...

# --- Helper Functions ---
def create_tables():
    """Creates database tables based on models."""
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully (if they didn't exist).")

def get_db_session():
    """Provides a database session."""
    return SessionLocal()


# --- Legacy Functions (Converted to SQLAlchemy, if needed elsewhere) ---
# Example conversion of insert_client
def legacy_insert_client_sqlalchemy(client_name, client_number, client_email, client_id, address_id, description='NA'):
    """Legacy function converted to use SQLAlchemy session internally."""
    from utils import generate_random_hash
    if not client_id:
        client_id = generate_random_hash(11)

    db = get_db_session()
    try:
        db_client = Client(
            client_name=client_name,
            phone_number=client_number,
            email=client_email,
            client_id=client_id,
            address_id=address_id,
            description=description,
            date_created=datetime.utcnow()
        )
        db.add(db_client)
        db.commit()
        db.refresh(db_client)
        print(f"Inserting client: {client_name}, ID: {client_id}")
        return db_client
    except Exception as e:
        db.rollback()
        print(f"Unexpected error while inserting client: {e}")
        raise # Re-raise to handle in calling function if needed
    finally:
        db.close()

# Example conversion of insert_project
def legacy_insert_project_sqlalchemy(project_name, material_cost_estimate, material_cost_actual, labor_bid, labor_cost_actual,
                                     project_status, scope_of_work, client, service, material, project_id, notes, start_date, metadata):
    """Legacy function converted to use SQLAlchemy session internally."""
    from utils import generate_random_hash
    if not project_id:
        project_id = generate_random_hash(12)

    db = get_db_session()
    try:
        # Parse start_date if it's a string
        parsed_start_date = None
        if start_date and start_date != 'NA':
             try:
                 parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
             except ValueError:
                 print(f"Invalid date format for start date: {start_date}")
                 # Handle error appropriately, maybe return None or raise

        db_project = Project(
            project_name=project_name,
            project_id=project_id,
            material_cost_estimate=float(material_cost_estimate) if material_cost_estimate != 'NA' else None,
            material_cost_actual=float(material_cost_actual) if material_cost_actual != 'NA' else None,
            labor_bid=float(labor_bid) if labor_bid != 'NA' else None,
            labor_cost_actual=float(labor_cost_actual) if labor_cost_actual != 'NA' else None,
            project_status=project_status,
            scope_of_work=scope_of_work,
            client=client,
            service=service,
            material=material,
            notes=notes,
            start_date=parsed_start_date,
            metadata=metadata,
            date_created=datetime.utcnow()
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        print(project_name, project_id)
        return db_project
    except Exception as e:
        db.rollback()
        print(f"Unexpected error while inserting project: {e}")
        raise
    finally:
        db.close()

# ... Convert other legacy insert functions similarly if needed ...
