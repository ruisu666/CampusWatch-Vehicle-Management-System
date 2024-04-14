import mysql.connector
from flask import flash, render_template, Blueprint, session, request, send_file
from app.utils import close_db_connection, get_db_connection

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('/myvehicles')
def vehicles():
    if 'user_role' not in session:
        session['user_role'] = 'user'  
    
    page = int(request.args.get('page', 1))  
    user_id = session.get('user_id') 
    
    vehicles = get_vehicles_for_page(page, user_id)
    
    if vehicles is None:
        flash("Failed to fetch vehicles.", "danger")
        return render_template('vehicles.html', title='Vehicles', vehicles=[], page=page, user_role=session.get('user_role'))
    else:
        return render_template('vehicles.html', title='Vehicles', vehicles=vehicles, page=page, user_role=session.get('user_role'))

def get_vehicles_for_page(page, user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        offset = (page - 1) * 10 
        cursor.execute("SELECT * FROM vehicle WHERE userID = %s LIMIT 10 OFFSET %s", (user_id, offset))
        vehicles = cursor.fetchall()
        return vehicles
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.CR_CONNECTION_ERROR:
            print("Error: XAMPP connection is closed or MySQL service is not running.")
            flash("Error: XAMPP connection is closed or MySQL service is not running.", "danger")
        else:
            print("Error fetching vehicles:", err)
            flash("Error fetching vehicles. Please try again later.", "danger")
        return None
    finally:
        close_db_connection(connection)


