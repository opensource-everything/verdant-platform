from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3, time, os, secrets, time, random, re 
from datetime import datetime
import subprocess

from models import *

app = Flask(__name__)


'''


 ██████╗██████╗ ███████╗ █████╗ ████████╗███████╗    ████████╗ █████╗ ██████╗ ██╗     ███████╗███████╗
██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗██║     ██╔════╝██╔════╝
██║     ██████╔╝█████╗  ███████║   ██║   █████╗         ██║   ███████║██████╔╝██║     █████╗  ███████╗
██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██╔══╝         ██║   ██╔══██║██╔══██╗██║     ██╔══╝  ╚════██║
╚██████╗██║  ██║███████╗██║  ██║   ██║   ███████╗       ██║   ██║  ██║██████╔╝███████╗███████╗███████║
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚══════╝


'''



# 
# SQL Row insertion 
# 


'''
legacy code -
soon to be depricated or seperated into its own module

used to be the old way of inserting subjects to
make subject profiles
essentially creating a dossier of known people
linking all social media accounts
and know information about an individual



'''
def insert_subjects():

    folder = r'H:\archives\Laptop\2023\INDEX REBORN V2'
    files = os.listdir(folder)
    full_names = []

    for f in files:
        names = f[:f.rfind('[')]
        names = [n for n in names.split(' ') if n]
        full_names.append(' '.join(names))

    filtered_list = list(set(filter_strings_without_numbers(full_names)))
    # print(filtered_list)

    name_list = []

    for name in filtered_list:
        full_name = name.split(' ')

        first_name = full_name[0]
        last_name = full_name[-1]
        try:
            middle_name = full_name[-2]
            if first_name in middle_name:
                middle_name = None
            new_name_list = [n for n in list(set([first_name, middle_name, last_name]))[::-1] if n]
            name_list.append(new_name_list)
        except: pass



    '''
    subject_key INTEGER PRIMARY KEY,
    subject_id TEXT,
    first_name TEXT,
    middle_name TEXT,
    last_name TEXT,
    social_links TEXT,
    role TEXT,
    birthday TEXT,
    phone TEXT
    '''

    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()

    table_attrs_dict = {}
    table_data = []

    for name in sorted(name_list):
        first_name = name[0]
        last_name = name[-1]
        role = 'slut'
        # social_links = []
        # print(first_name, last_name)


        table_attrs_dict = {
                'table_name': 'dim_subject',
                'table_attrs': {
                    'subject_id': generate_random_hash(16),
                    'first_name': first_name,
                    'last_name': last_name,
                    'role': role
                }

        }

        table_data.append(table_attrs_dict)


    for tr in table_data:
        table_name = tr['table_name']
        table_attrs = tr['table_attrs']

        subject_id = table_attrs['subject_id']
        first_name = table_attrs['first_name']
        last_name = table_attrs['last_name']
        role = table_attrs['role']

        sql_statement = construct_insert_statement(table_name, table_attrs)

        c.execute(sql_statement, (subject_id, first_name, last_name, role))
        print(sql_statement)

    conn.commit()
    conn.close()






'''
 Generates a psudo folder_schema
 to populate the folder table in the database

inserting my favorite folders from extgernal drives
has them hardcoded
as the


'''

def insert_folders_into_schema():
    favorite_folders = [
    r'C:\EasyDiffusion\profile\Stable Diffusion UI',
    r'H:\archives\Laptop\2023\304',
    r'E:\Volumes\Dump\304'
    ]

    # print(favorite_folders)

    folder_schema = []


    for f in favorite_folders:
        sub_files = os.listdir(f)

        folder_store = {}
        folders = []
        files = []
        for _ in sub_files:
            file_path = os.path.join(f,_)

            if os.path.isfile(file_path):
                files.append(file_path)
                # print(file_path)
                # folder_schema.append({})

            if os.path.isdir(file_path):
                folders.append(file_path)
                # print(file_path)

        folder_store[f] = [folders, files]



    # Check the folder_store 
    # Prints a randomly chosen value from the folder_store, as a basic check
    for d in folder_store.values():
        rand_file = random.choice(d[1])
        print(rand_file)
        print(len(d[1]))
        # os.startfile(rand_file)
        # print(d[1])

    # print(folder_store.values())

    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()

    rows = [
        {
            'folder_id':generate_random_hash(12),
            'folder_name':os.path.basename(f),
            'folder_path':f,
            'creation_date':os.stat(f).st_ctime
        } for f in favorite_folders
    ]

    table_name = 'dim_folder'
    table_attrs = [
        'folder_id',
        'folder_name',
        'creation_date',
        'folder_path'
    ]

    sql_statement = construct_insert_statement(table_name, table_attrs)

    for r in rows:
        folder_id = r['folder_id']
        folder_name = r['folder_name']
        folder_path = r['folder_path']
        create_date = r['creation_date']
        # print(r['folder_id'])
        # print(r['folder_name'])
        # print(r['creation_date'])
        # print(r['folder_path'])
        # print()
        c.execute(sql_statement, (folder_id, folder_name, create_date, folder_path))

    conn.commit()
    conn.close()

    # Generating a hash string for file and attempt table insertion
    # folder_id = generate_random_hash(12)
    # table_name = 'dim_file'
    # c.execute(f'INSERT INTO {table_name}')




'''


██████╗  ██████╗ ██╗   ██╗████████╗██╗███╗   ██╗ ██████╗ 
██╔══██╗██╔═══██╗██║   ██║╚══██╔══╝██║████╗  ██║██╔════╝ 
██████╔╝██║   ██║██║   ██║   ██║   ██║██╔██╗ ██║██║  ███╗
██╔══██╗██║   ██║██║   ██║   ██║   ██║██║╚██╗██║██║   ██║
██║  ██║╚██████╔╝╚██████╔╝   ██║   ██║██║ ╚████║╚██████╔╝
╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ 


'''



@app.route('/', methods=['GET'])
def index():
    # conn = sqlite3.connect('products.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM products")
    # products = c.fetchall()
    # conn.close()

    # Retrieve table data
    clients = retrieve_tables('dim_client')
    properties = retrieve_tables('dim_property')
    services = retrieve_tables('dim_service')
    tags = retrieve_tables('dim_tag')

    # services = retrieve_tables('dim_service')

    # tasks = retrieve_tables('dim_task')
    # products = retrieve_tables('dim_product')

    # Render table data
    # return render_template('index.html', products=products, clients=clients, services=services, tasks=tasks)
    # return render_template('index_kimi_v2.html')
    return render_template('index_v1.html',
        clients=clients,
        properties=properties,
        services=services,
        tags=tags
    )
    '''

    '''
    # Base Page Render
    # return render_template('index.html')


@app.route('/nav', methods=['GET'])
def navigaton():
    # conn = sqlite3.connect('products.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM products")
    # products = c.fetchall()
    # conn.close()
    return render_template('navigaton_test.html')

@app.route('/dash', methods=['GET'])
def dashboard_test():
    # conn = sqlite3.connect('products.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM products")
    # products = c.fetchall()
    # conn.close()
    return render_template('dashboard-main.html')

@app.route('/home-test', methods=['GET'])
def home_test():
    return render_template('index_v1.html')


'''
Working as of 10-30-24
Expansion needed

'''

@app.route('/folders', methods=['GET'])
def folders_dashboard():
    conn = sqlite3.connect(APP_DATABASE_FILENAME)
    c = conn.cursor()
    c.execute("SELECT * FROM dim_folder")
    folders = c.fetchall()
    conn.close()
    return render_template('folders_dashboard.html', folders=folders)


@app.route('/CMS_dashboard', methods=['GET'])
def CMS_dashboard():
    # conn = sqlite3.connect('products.db')
    # c = conn.cursor()
    # c.execute("SELECT * FROM products")
    # products = c.fetchall()
    # conn.close()
    return render_template('CMS_dashboard.html')




# 
# Navigation Routes
# 

@app.route('/tagging', methods=['GET'])
def tagging():

    # start_index = 140
    # offset = 30
    # files = retrieve_tables('dim_filename', db_filename='file_tagging_app.db')[start_index:start_index+offset]
    # files = retrieve_tables('dim_tag', mode='random', random_limit='100')
    tags = retrieve_tables('dim_tag')
    # print(type(files))

    return render_template('tagging.html', tags=tags)

# Tags pages
'''
from flask import render_template, request, redirect, url_for, jsonify
from your_app import db, Tag
from your_utils import generate_color_from_name  # or inline the function
'''

@app.route('/tags')
def tag_manager():
    tags = Tag.query.all()
    return render_template('tag_manager.html', tags=tags)

'''

@app.route('/tags/add', methods=['POST'])
def add_tag():
    name = request.form.get('tag_name', '').strip()
    if not name:
        return redirect(url_for('tag_manager'))
    
    existing = Tag.query.filter_by(name=name).first()
    if existing:
        return redirect(url_for('tag_manager'))

    color = generate_color_from_name(name)
    new_tag = Tag(name=name, color=color)
    db.session.add(new_tag)
    db.session.commit()
    return redirect(url_for('tag_manager'))
'''

@app.route('/tags/<int:tag_id>/update', methods=['POST'])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    data = request.get_json()
    name = data.get('name', '').strip()
    color = data.get('color', '').strip()

    if not name or not color.startswith('#') or len(color) != 7:
        return jsonify({"error": "Invalid data"}), 400

    # Ensure name uniqueness (ignore self)
    if Tag.query.filter(Tag.name == name, Tag.id != tag_id).first():
        return jsonify({"error": "Name already exists"}), 400

    tag.name = name
    tag.color = color
    db.session.commit()
    return jsonify(tag.to_dict()), 200

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('tag_manager'))
# Tags end


@app.route('/file_tracker', methods=['GET'])
def file_tracker():
    return render_template('file_tracker.html')

@app.route('/media', methods=['GET'])
def media():
    return render_template('media_track.html')

@app.route('/workflow_automation', methods=['GET'])
def workflow_automation():
    return render_template('workflow_automation_dashboard.html')

@app.route('/projects', methods=['GET'])
def projects_board():
    return render_template('projects-dashboard.html')

@app.route('/projects-dash', methods=['GET'])
def projects_dashboard():
    return render_template('projects-dashboard-modern.html')

@app.route('/ledger-personal', methods=['GET'])
def personal_ledger():
    return render_template('ledger-personal.html')








'''

███████╗ ██████╗ ██████╗ ███╗   ███╗███████╗
██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔════╝
█████╗  ██║   ██║██████╔╝██╔████╔██║███████╗
██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║╚════██║
██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████║
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝

'''


from flask import request, redirect, url_for, render_template, flash
from datetime import datetime
import hashlib
import re
import logging
import uuid

# Assuming your User model and database session are imported
# from your_models import User, db_session

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''
    Process POST requests from signup form
    Creates new user account in database
    '''
    if request.method == 'POST':
        try:
            # Gather form data
            username = request.form.get('username', '').strip()
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone_number = request.form.get('phone_number', '').strip()
            role = request.form.get('role', 'user').strip()
            bio = request.form.get('bio', '').strip()
            
            # --- Validation ---
            errors = []
            
            # Username validation
            if not username:
                errors.append('Username is required')
            elif len(username) < 3:
                errors.append('Username must be at least 3 characters')
            elif not re.match(r'^[a-zA-Z0-9_]+$', username):
                errors.append('Username can only contain letters, numbers, and underscores')
            
            # Email validation
            if not email:
                errors.append('Email is required')
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                errors.append('Invalid email format')
            
            # Password validation
            if not password:
                errors.append('Password is required')
            elif len(password) < 8:
                errors.append('Password must be at least 8 characters')
            elif not re.search(r'[A-Z]', password):
                errors.append('Password must contain at least one uppercase letter')
            elif not re.search(r'[a-z]', password):
                errors.append('Password must contain at least one lowercase letter')
            elif not re.search(r'[0-9]', password):
                errors.append('Password must contain at least one number')
            
            if password != confirm_password:
                errors.append('Passwords do not match')
            
            # Name validation
            if not first_name:
                errors.append('First name is required')
            if not last_name:
                errors.append('Last name is required')
            
            # Phone validation (optional but validate if provided)
            if phone_number and not re.match(r'^[\d\s\-+()]{10,15}$', phone_number):
                errors.append('Invalid phone number format')
            
            # Check if username already exists
            # existing_user = db_session.query(User).filter_by(username=username).first()
            # if existing_user:
            #     errors.append('Username already taken')
            
            # Check if email already exists
            # existing_email = db_session.query(User).filter_by(email=email).first()
            # if existing_email:
            #     errors.append('Email already registered')
            
            # If validation errors, return to form with error messages
            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('signup.html', 
                                     form_data=request.form)
            
            # --- Create user ---
            # Generate unique user ID (could be UUID or custom)
            user_id = str(uuid.uuid4())  # Or generate_product_id(15) if you have that function
            
            # Hash password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            # Create user object
            user = User(
                id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number if phone_number else None,
                role=role,
                bio=bio if bio else None
            )
            
            # Add user to database
            # db_session.add(user)
            # db_session.commit()
            
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            logging.error(f"Error creating user account: {str(e)}")
            db_session.rollback()  # if using SQLAlchemy
            flash('An error occurred while creating your account. Please try again.', 'error')
            return render_template('signup.html', 
                                 form_data=request.form)
    else:
        # GET request - render empty form
        return render_template('signup.html')


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    '''
    Process Post Requests from page forms 
    inserts new data into databases
    '''
    if request.method == 'POST':
        # Gather form data with default values
        product_data = {
            'product_name': request.form.get('product_name', 'NA'),
            'cost': request.form.get('cost', 'NA'),
            'price': request.form.get('price', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get product ID
        product_data['product_id'] = generate_product_id(15) if 'use_random_id' in request.form else request.form.get('product_id', 'NA')

        # Insert product using dictionary unpacking
        insert_product(**product_data)

        # Redirect to index page
        return redirect(url_for('index'))
    else:
        # Render empty form
        return render_template('add_product.html')



@app.route('/add_service', methods=['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        # Gather form data with default values
        service_data = {
            'service_name': request.form.get('service_name', 'NA'),
            'service_price': request.form.get('service_price', 'NA'),
            'service_type': request.form.get('service_type', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get service ID
        service_data['service_id'] = generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')

        # Insert service using dictionary unpacking
        insert_service(**service_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_service.html')

@app.route('/add_profile', methods=['GET', 'POST'])
def add_profile():
    if request.method == 'POST':
        # Gather form data with default values
        service_data = {
            'service_name': request.form.get('service_name', 'NA'),
            'service_price': request.form.get('service_price', 'NA'),
            'service_type': request.form.get('service_type', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get service ID
        service_data['service_id'] = generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')

        # Insert service using dictionary unpacking
        insert_service(**service_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_service.html')

@app.route('/add_supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        # Gather form data with default values
        service_data = {
            'service_name': request.form.get('service_name', 'NA'),
            'service_price': request.form.get('service_price', 'NA'),
            'service_type': request.form.get('service_type', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get service ID
        service_data['service_id'] = generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')

        # Insert service using dictionary unpacking
        insert_service(**service_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_service.html')

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        # Gather form data with default values
        service_data = {
            'service_name': request.form.get('service_name', 'NA'),
            'service_price': request.form.get('service_price', 'NA'),
            'service_type': request.form.get('service_type', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get service ID
        service_data['service_id'] = generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')

        # Insert service using dictionary unpacking
        insert_service(**service_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_service.html')

@app.route('/add_url', methods=['GET', 'POST'])
def add_url():
    if request.method == 'POST':
        # Gather form data with default values
        service_data = {
            'service_name': request.form.get('service_name', 'NA'),
            'service_price': request.form.get('service_price', 'NA'),
            'service_type': request.form.get('service_type', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get service ID
        service_data['service_id'] = generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')

        # Insert service using dictionary unpacking
        insert_service(**service_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_service.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Gather form data with default values
        service_data = {
            'service_name': request.form.get('service_name', 'NA'),
            'service_price': request.form.get('service_price', 'NA'),
            'service_type': request.form.get('service_type', 'NA'),
            'description': request.form.get('description', 'NA'),
        }

        # Generate or get service ID
        service_data['service_id'] = generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')

        # Insert service using dictionary unpacking
        insert_service(**service_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_service.html')

# Assuming your utility functions are available:
# from your_utils import generate_random_hash, insert_table_attrs
# from flask import request, redirect, url_for, render_template, flash

@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        # Gather form data with default values
        property_data = {
            'property_name': request.form.get('property_name', 'NA'),
            'category': request.form.get('category', 'NA'),
            'property_address': request.form.get('property_address', 'NA'),
            'property_zipcode': request.form.get('property_zipcode', 'NA'),
            'property_city': request.form.get('property_city', 'NA'),
            'property_state': request.form.get('property_state', 'NA'),
            'owner_name': request.form.get('owner_name', 'NA'),
            'contact_phone': request.form.get('contact_phone', 'NA'),
            'email': request.form.get('email', 'NA'),
            'description': request.form.get('description', 'NA'),
            # Optional: include property_price if available in your form
            'property_price': request.form.get('property_price', 'NA')
        }
        
        # Consolidate Generate or get property ID logic into the dictionary
        # Note: I'm standardizing the key to 'property_ID' as used in your original block
        if 'use_random_id' in request.form:
            property_data['property_ID'] = generate_random_hash(11)
        else:
            property_data['property_ID'] = request.form.get('property_id', 'NA')
            
        # 1. Define table name
        table_name = 'dim_property' # ASSUMPTION: Check if your property table name is different

        # 2. Use the generalized insert method
        # This replaces: insert_property(**property_data)
        insert_table_attrs(
            table_name, 
            list(property_data.keys()), 
            list(property_data.values())
        )
        
        flash("Property added successfully!", "success")
        return redirect(url_for('index'))
    else:
        # For GET requests, generate a default random property ID
        default_property_id = generate_random_hash(11)
        return render_template('add_property.html', property_id=default_property_id)


@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        # Gather form data with default values
        category_data = {
            'category_ID': generate_random_hash(11) if 'use_random_id' in request.form else request.form.get('random_id', 'NA'),
            'category': request.form.get('category_name', 'NA'),
            'description': request.form.get('description', 'NA'),
            'parent_category_id': request.form.get('parent_category_id', 'NA'),
            'created_at': int(time.time())  # Store timestamp for record creation
        }

        # Define table name
        table_name = 'dim_category'

        # Use the generalized insert method
        insert_table_attrs(table_name, list(category_data.keys()), list(category_data.values()))

        return redirect(url_for('index'))
    else:
        current_date = datetime.today().strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
        return render_template('add_category.html', current_date=current_date)

@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if request.method == 'POST':
        # Gather form data with default values
        category_data = {
            'category_ID': generate_random_hash(11) if 'use_random_id' in request.form else request.form.get('random_id', 'NA'),
            'category': request.form.get('category_name', 'NA'),
            'description': request.form.get('description', 'NA'),
            'parent_category_id': request.form.get('parent_category_id', 'NA'),
            'created_at': int(time.time())  # Store timestamp for record creation
        }

        # Define table name
        table_name = 'dim_category'

        # Use the generalized insert method
        insert_table_attrs(table_name, list(category_data.keys()), list(category_data.values()))

        return redirect(url_for('index'))
    else:
        current_date = datetime.today().strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
        return render_template('add_category.html', current_date=current_date)

# Add project route
@app.route('/add_project', methods=['GET', 'POST'])
def add_project_route():
    if request.method == 'POST':
        # Gather form data with default values
        project_data = {
            # 1. Generate/Get project_id, similar to category_ID logic
            'project_id': generate_random_hash(11) if 'use_random_id' in request.form else request.form.get('project_id', 'NA'),
            
            'project_name': request.form.get('project_name', 'NA'),
            'project_status': request.form.get('project_status', 'NA'),
            'material_cost_estimate': request.form.get('material_cost_estimate', 'NA'),
            'material_cost_actual': request.form.get('material_cost_actual', 'NA'),
            'labor_bid': request.form.get('labor_bid', 'NA'),
            'labor_cost_actual': request.form.get('labor_cost_actual', 'NA'),
            'scope_of_work': request.form.get('scope_of_work', 'NA'),
            'client': request.form.get('project_client', 'NA'),
            'service': request.form.get('project_service', 'NA'),
            'material': request.form.get('project_material', 'NA'),
            'notes': request.form.get('notes', 'NA'),
            'start_date': request.form.get('start_date', 'NA')
        }

        # Set timestamps and metadata (Converted to integer timestamp like the first method)
        now_timestamp = int(time.time())
        project_data['date_created'] = now_timestamp
        project_data['date_updated'] = now_timestamp
        project_data['metadata'] = 'NA'

        # 2. Define table name
        table_name = 'dim_project' # Assuming the project data goes into a table named 'dim_project'

        # 3. Use the generalized insert method
        insert_table_attrs(table_name, list(project_data.keys()), list(project_data.values()))
        
        # Removed insert_project(**project_data)
        
        flash("Project added successfully!", "success")
        return redirect(url_for('index'))
    else:
        # GET request logic (remains the same)
        clients = retrieve_tables('dim_client')
        default_project_id = generate_random_hash(11)
        return render_template('add_project.html', project_id=default_project_id, clients=clients)

'''
2025 updated client insertion techinique

client insertions start
'''
# Assuming your utility functions are available:
# from your_utils import generate_random_hash, insert_table_attrs

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        # 1. Generate IDs needed for this transaction
        client_id = generate_random_hash(11) if 'use_random_id' in request.form else request.form.get('client_id', 'NA')
        # Generate address_id upfront, as the generalized insert_table_attrs 
        # doesn't return the last inserted ID.
        address_id = generate_random_hash(11)


        # 2. Insert Address
        # Define table name
        address_table = 'dim_address' # ASSUMPTION: Update if table name is different
        
        address_data = {
            'address_id': address_id, # Include the generated ID
            'street': request.form.get('street', 'NA'),
            'unit': request.form.get('unit', 'NA'),
            'city': request.form.get('city', 'NA'),
            'state': request.form.get('state', 'NA'),
            'zip_code': request.form.get('zip_code', 'NA')
        }
        
        # Use the generalized insert method
        insert_table_attrs(
            address_table, 
            list(address_data.keys()), 
            list(address_data.values())
        )
        # address_id is now already defined from the generation step


        # 3. Insert Client
        # Define table name
        client_table = 'dim_client' # ASSUMPTION: Update if table name is different
        
        client_data = {
            'client_name': request.form.get('client_name', 'NA'),
            'client_number': request.form.get('client_number', 'NA'),
            'client_email': request.form.get('client_email', 'NA'),
            'description': request.form.get('description', 'NA'),
            'client_id': client_id,
            'address_id': address_id # Use the generated address_id
        }
        
        # Use the generalized insert method
        insert_table_attrs(
            client_table, 
            list(client_data.keys()), 
            list(client_data.values())
        )


        # 4. Insert Property (if provided)
        if request.form.get('property_id'):
            # Define table name
            property_table = 'dim_property' # ASSUMPTION: Update if table name is different
            
            property_data = {
                'property_id': request.form.get('property_id'),
                'property_name': request.form.get('property_name', 'NA'),
                'property_type': request.form.get('property_type', 'NA'),
                'client_id': client_id
            }
            
            # Use the generalized insert method
            insert_table_attrs(
                property_table, 
                list(property_data.keys()), 
                list(property_data.values())
            )


        print(address_id)
        print()

        return redirect(url_for('index'))

    return render_template('add_client.html')


'''
End of client insertion

'''
'''
Adding Items for tables Forms
'''

@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Gather form data for employee
        employee_data = {
            'employee_id': generate_random_hash(11) if 'use_random_id' in request.form else request.form.get('employee_id', 'NA'),
            'username': request.form.get('username', 'NA'), # Add these fields to your HTML form
            'first_name': request.form.get('first_name', 'NA'),
            'last_name': request.form.get('last_name', 'NA'),
            'role': request.form.get('role', 'NA'),
            'position': request.form.get('position', 'NA'),
            'hire_date': request.form.get('hire_date', 'NA'),
            'salary': request.form.get('salary', 'NA'),
            'email': request.form.get('email', 'NA'),
            'birthday': request.form.get('birthday', 'NA'),
            'phone': request.form.get('phone', 'NA'),
        }
        # Insert employee using the function defined above
        insert_employee(
            employee_data['employee_id'], employee_data['username'], employee_data['first_name'],
            employee_data['last_name'], employee_data['role'], employee_data['position'],
            employee_data['hire_date'], employee_data['salary'], employee_data['email'],
            employee_data['birthday'], employee_data['phone']
        )


        return redirect(url_for('index'))
    else:
        # Render the employee form
        return render_template('add_employee.html') # Make sure this template exists and has the correct fields


# Add task route
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        # Gather form data with default values
        task_data = {
            'task_name': request.form.get('task_name', 'NA'),
            'status': request.form.get('status', 'NA'),
            'assigned_to': request.form.get('assigned_to', 'NA'),
            'created_by': request.form.get('created_by', 'NA'),
            'description': request.form.get('description', 'NA'),
            'task_id': generate_random_hash(10) if 'use_random_id' in request.form else request.form.get('task_id', 'NA')
        }

        # Insert task using dictionary unpacking
        insert_task(**task_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_task.html')


@app.route('/add_material', methods=['GET', 'POST'])
def add_material():
    if request.method == 'POST':
        # Gather form data with default values
        material_data = {
            'material_name': request.form.get('material_name', 'NA'),
            'material_price': request.form.get('material_price', 'NA'),
            'description': request.form.get('description', 'NA'),
            'service_id': generate_service_id() if 'use_random_id' in request.form else request.form.get('service_id', 'NA')
        }

        # Insert material data using dictionary unpacking
        insert_service(**material_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_material.html')



# Add expense route
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        # Gather form data with default values
        expense_data = {
            'item_name': request.form.get('item_name', 'NA'),
            'item_price': request.form.get('item_price', 'NA'),
            'description': request.form.get('description', 'NA'),
            'item_id': generate_random_hash(16) if 'use_random_id' in request.form else request.form.get('item_id', 'NA')
        }

        # Insert expense using dictionary unpacking
        insert_service(**expense_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_expense.html')



# add expense route
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user_id = generate_random_hash(15) if 'use_random_id' in request.form else request.form.get('user_id', 'NA')
        username = request.form.get('username', 'NA')
        first_name = request.form.get('first_name', 'NA')
        last_name = request.form.get('last_name', 'NA')
        role = request.form.get('role', 'NA')
        bio = request.form.get('bio', 'NA')
        desc = request.form.get('desc', 'NA')
        email = request.form.get('email', 'NA')
        phone_number = request.form.get('phone_number', 'NA')
        metadata = request.form.get('metadata', 'NA')
        date_created = time.time()
        date_updated = 'NA'

        insert_user(user_id, username, first_name, last_name, role, bio, desc, email, phone_number, date_created, date_updated, metadata)
        return redirect(url_for('index'))
    else:
        return render_template('add_user.html') # Make sure this template exists and has the correct fields

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']


        if use_random_id:
            user_id = generate_random_hash(15)
        else:
            user_id = request.form['user_id']


        insert_user(username, first_name, last_name, role, metadata)

        return redirect(url_for('index'))
    else:
        return render_template('add_user.html')

# add expense route
@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        team_name = request.form['team_name']
        first_name = request.form['first_name']
        last_name = request.form['last_name']


        if use_random_id:
            order_id = generate_random_hash(15)
        else:
            order_id = request.form['order_id']


        insert_user(username, first_name, last_name, role, metadata)

        return redirect(url_for('index'))
    else:
        return render_template('add_user.html')



@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    if request.method == 'POST':
        service_name = request.form['service_name']
        service_price = request.form['service_price']
        description = request.form['description']

        if use_random_id:
            service_id = generate_random_hash(15)
        else:
            service_id = request.form['service_id']


        insert_service(service_name, service_price, description, service_id)

        return redirect(url_for('index'))
    else:
        return render_template('add_subject.html')

@app.route('/add_login', methods=['GET', 'POST'])
def add_login():
    if request.method == 'POST':
        # Gather form data with default values
        login_data = {
            'login_ID': generate_random_hash(15) if 'use_random_id' in request.form else request.form.get('tag_id', 'NA'),
            'email': request.form.get('email', 'NA'),
            'username': request.form.get('username', 'NA'),
            'password': request.form.get('password', 'NA'),
            'platform_url': request.form.get('platform_url', 'NA'),
            'created_at': int(time.time())  # Store timestamp for record creation
        }

        # Define table name
        table_name = 'dim_login'

        # Use the generalized insert method
        insert_table_attrs(table_name, list(login_data.keys()), list(login_data.values()))

        return redirect(url_for('index'))
    else:
        current_date = datetime.today().strftime('%Y-%m-%d')  # Format as 'YYYY-MM-DD'
        return render_template('add_login.html', current_date=current_date)


@app.route('/add_tag', methods=['GET', 'POST'])
def add_tag():
    if request.method == 'POST':
        # Gather form data with default values
        tag_data = {
            'tag_name': request.form.get('tag_name', 'NA'),
            'description': request.form.get('description', 'NA'),
            'tag_id': generate_random_hash(15) if 'tag_id' in request.form else request.form.get('tag_id', 'NA')
        }

        # Insert tag using dictionary unpacking
        insert_tag(**tag_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_tag.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Gather form data with default values
        login_data = {
            'email': request.form.get('tag_name', 'NA'),
            'password': request.form.get('description', 'NA'),
            'remember-check': generate_random_hash(15) if 'password' in request.form else request.form.get('password', 'NA')
        }

        # Insert tag using dictionary unpacking
        insert_tag(**login_data)

        return redirect(url_for('index'))
    else:
        return render_template('login.html')

'''
Add items to tables 
'''
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        # Gather form data with default values
        post_data = {
            'post_title': request.form.get('tag_name', 'NA'),
            'description': request.form.get('description', 'NA'),
            'created_by': request.form.get('description', 'NA'),
            'scheduled_post_date': request.form.get('description', 'NA'),
            'media': request.form.get('description', 'NA'),
            'tag_id': generate_random_hash(15) if 'tag_id' in request.form else request.form.get('tag_id', 'NA')
        }

        # Insert tag using dictionary unpacking
        insert_tag(**tag_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_tag.html')


# add expense route
@app.route('/add_drive', methods=['GET', 'POST'])
def add_drive():
    if request.method == 'POST':
        drive_name = request.form['drive_name']
        drive_size = request.form['drive_size']
        description = request.form['description']
        description = request.form['description']

        if use_random_id:
            drive_id = generate_random_hash(15)
        else:
            drive_id = request.form['random_id']


        insert_service(service_name, service_price, description, service_id)

        return redirect(url_for('index'))
    else:
        return render_template('add_drive.html')

# Add folder route
@app.route('/add_folder', methods=['GET', 'POST'])
def add_folder():
    if request.method == 'POST':
        # Gather form data with default values
        folder_data = {
            'folder_path': request.form.get('folder_path', 'NA'),
            'folder_name': request.form.get('folder_name', 'NA'),
            'description': request.form.get('description', 'NA'),
            'category_name': request.form.get('category_name', 'NA'),
            'folder_id': id_generator() if 'use_random_id' in request.form else request.form.get('folder_id', 'NA')
        }

        # Ensure folder_id is provided if required
        if not folder_data['folder_id']:
            flash("Folder ID is required", "error")
            return redirect(url_for('add_folder'))

        # Insert folder data using dictionary unpacking
        insert_folder(**folder_data)

        return redirect(url_for('index'))
    else:
        return render_template('add_folder.html')


@app.route('/launch_stable_diffusion', methods=['POST'])
def launch_stable_diffusion():
    try:
        # subprocess.Popen([])
        os.startfile(r"E:\Archives\AI\New Working\EasyDiffusion\Start Stable Diffusion UI Shortcut.lnk")

          # Change this for your OS
        return jsonify({"status": "success", "message": "Application launched!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/launch_easy_diffusion', methods=['POST'])
def launch_easy_diffusion():
    try:
        # subprocess.Popen([])
        os.startfile(r"E:\Archives\AI\New Working\stable-diffusion-webui\webui-user shortcut.lnk")

          # Change this for your OS
        return jsonify({"status": "success", "message": "Application launched!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/launch_photoshop', methods=['POST'])
def launch_photoshop():
    try:
        # subprocess.Popen([])
        os.startfile(r"E:\Archives\AI\New Versions\EasyDiffusion\Start Stable Diffusion UI_shortcut.lnk")

          # Change this for your OS
        return jsonify({"status": "success", "message": "Application launched!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/launch_photo_ai', methods=['POST'])
def launch_photo_ai():
    try:
        # subprocess.Popen([])
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Topaz Photo AI\Topaz Photo AI.lnk")

          # Change this for your OS
        return jsonify({"status": "success", "message": "Application launched!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/launch_after_effects', methods=['POST'])
def launch_after_effects():
    try:
        # subprocess.Popen([])
        os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Topaz Photo AI\Topaz Photo AI.lnk")

          # Change this for your OS
        return jsonify({"status": "success", "message": "Application launched!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500





def table_tests():
    # insert_folders_into_schema()
    # insert_subjects()
    pass



'''

███████╗███╗   ██╗████████╗██████╗ ██╗   ██╗    ██████╗  ██████╗ ██╗███╗   ██╗████████╗
██╔════╝████╗  ██║╚══██╔══╝██╔══██╗╚██╗ ██╔╝    ██╔══██╗██╔═══██╗██║████╗  ██║╚══██╔══╝
█████╗  ██╔██╗ ██║   ██║   ██████╔╝ ╚████╔╝     ██████╔╝██║   ██║██║██╔██╗ ██║   ██║   
██╔══╝  ██║╚██╗██║   ██║   ██╔══██╗  ╚██╔╝      ██╔═══╝ ██║   ██║██║██║╚██╗██║   ██║   
███████╗██║ ╚████║   ██║   ██║  ██║   ██║       ██║     ╚██████╔╝██║██║ ╚████║   ██║   
╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝       ╚═╝      ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   


'''

if __name__ == '__main__':

    # Create database tables if it doesn't exist
    # 

    # create_product_table()
    # create_landscape_app_tables()

    initialize_database_tables()
    # insert_table_attrs()
    # table_tests()

    app.run(debug=True)
