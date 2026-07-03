# verdant_app/app.py

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.exceptions import BadRequestKeyError
import logging

# Import from local modules
from config import Config
from business_logic import SERVICES, MATERIAL_CATEGORIES, generate_random_hash, validate_email, get_current_timestamp
from database import init_db, insert_client, insert_address, insert_project, get_all_clients, get_client_by_id

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database by calling the function directly.
# This is the correct, modern approach for one-time initialization.
init_db()

# Configure logging for the application
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/')
def home():
    """Renders the homepage or dashboard."""
    return render_template('index.html', services=SERVICES)

@app.route('/services')
def show_services():
    """Renders a page displaying all available services."""
    return render_template('services.html', services=SERVICES)

@app.route('/materials')
def show_materials():
    """Renders a page displaying all available materials categorized."""
    return render_template('materials.html', material_categories=MATERIAL_CATEGORIES)

@app.route('/clients')
def list_clients():
    """Displays a list of all clients."""
    clients = get_all_clients()
    return render_template('clients.html', clients=clients)

@app.route('/clients/<client_id>')
def view_client(client_id):
    """Displays details for a single client."""
    client = get_client_by_id(client_id)
    if client:
        return render_template('client_detail.html', client=client)
    else:
        flash("Client not found.", "danger")
        return redirect(url_for('list_clients'))

@app.route('/clients/new', methods=['GET', 'POST'])
def new_client():
    """Handles the creation of a new client."""
    if request.method == 'POST':
        try:
            # Extract form data
            client_name = request.form['client_name'].strip()
            client_number = request.form['client_number'].strip()
            client_email = request.form['client_email'].strip()
            street = request.form['street'].strip()
            unit = request.form.get('unit', '').strip()
            city = request.form['city'].strip()
            state = request.form['state'].strip()
            zip_code = request.form['zip_code'].strip()

            # Server-side validation
            if not all([client_name, client_number, client_email, street, city, state, zip_code]):
                flash("Please fill out all required fields.", "danger")
                return redirect(url_for('new_client'))
            
            if not validate_email(client_email):
                flash("Invalid email address format.", "danger")
                return redirect(url_for('new_client'))

            # Generate unique IDs
            client_id = generate_random_hash(10)
            address_id = generate_random_hash(11)

            # Insert address first
            inserted_address_id = insert_address(street, unit, city, state, zip_code, address_id)
            if not inserted_address_id:
                flash("Failed to create client address due to a database error.", "danger")
                return redirect(url_for('new_client'))
            
            # Then insert client
            if insert_client(client_name, client_number, client_email, client_id, inserted_address_id):
                flash(f"Client '{client_name}' created successfully!", "success")
                return redirect(url_for('list_clients'))
            else:
                flash("Failed to create client due to a database error.", "danger")
                return redirect(url_for('new_client'))

        except BadRequestKeyError as e:
            flash(f"Missing form field: {e}", "danger")
            return redirect(url_for('new_client'))
        except Exception as e:
            logging.error(f"Error processing new client form: {e}")
            flash("An unexpected error occurred. Please try again.", "danger")
            return redirect(url_for('new_client'))

    return render_template('new_client.html')

@app.route('/projects/new', methods=['GET', 'POST'])
def new_project():
    """Handles the creation of a new project."""
    if request.method == 'POST':
        try:
            project_name = request.form['project_name'].strip()
            client_id = request.form['client_id'].strip()
            scope_of_work = request.form['scope_of_work'].strip()
            labor_bid = request.form['labor_bid'].strip()
            material_cost_estimate = request.form['material_cost_estimate'].strip()
            start_date = request.form['start_date'].strip()
            notes = request.form.get('notes', '').strip()

            # Basic validation
            if not all([project_name, client_id, scope_of_work, labor_bid, material_cost_estimate, start_date]):
                flash("Please fill out all required project fields.", "danger")
                return redirect(url_for('new_project'))

            project_id = generate_random_hash(12)
            
            if insert_project(
                project_name=project_name, 
                material_cost_estimate=material_cost_estimate, 
                labor_bid=labor_bid, 
                project_status='Pending', 
                scope_of_work=scope_of_work, 
                client=client_id,
                start_date=start_date,
                notes=notes,
                project_id=project_id,
                date_created=get_current_timestamp()
            ):
                flash(f"Project '{project_name}' created successfully!", "success")
                return redirect(url_for('list_projects'))
            else:
                flash("Failed to create project due to a database error.", "danger")
                return redirect(url_for('new_project'))

        except BadRequestKeyError as e:
            flash(f"Missing form field: {e}", "danger")
            return redirect(url_for('new_project'))
        except Exception as e:
            logging.error(f"Error processing new project form: {e}")
            flash("An unexpected error occurred. Please try again.", "danger")
            return redirect(url_for('new_project'))
    
    # Pass clients to the template for a dropdown menu
    clients = get_all_clients()
    return render_template('new_project.html', clients=clients)

@app.route('/projects')
def list_projects():
    """Displays a list of all projects. (Dummy function for now)"""
    # This function would call a database function to retrieve project data.
    projects = []  # Placeholder for project data from the database
    return render_template('projects.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
