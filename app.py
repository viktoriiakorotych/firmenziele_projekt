from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Mdhdfj36487Gtd.",  
        database="firmenziele_db"  
    )
    return connection

# Index-Route (Homepage)
@app.route('/')
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT 
        z.id_goals,  
        a.department_name AS abteilung,
        z.statement AS ziel,
        z.criteria AS kriterien,
        zb.score AS bewertung,
        zb.comment AS kommentar,
        z.last_modified_date AS zuletzt_geaendert,
        b.user_name AS aenderer,
        z.measure_success AS anregung
    FROM 
        Ziele z
    LEFT JOIN 
        Abteilung a ON z.id_department = a.id_department
    LEFT JOIN 
        Zielbewertungen zb ON z.id_goals = zb.goals_id
    LEFT JOIN 
        Benutzer b ON z.modified_by = b.id_user;
    '''

    cursor.execute(query)
    goals = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('index.html', goals=goals)

# Route für das Abrufen der Score-Historie als JSON (API)
@app.route('/api/score_history/<int:id>')
def score_history(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT gh.last_modified_date, gh.new_score
    FROM Zielhistorie gh
    WHERE gh.id_goals = %s
    ORDER BY gh.last_modified_date ASC;
    '''

    cursor.execute(query, (id,))
    score_history = cursor.fetchall()
    cursor.close()
    connection.close()

    # Daten als JSON zurückgeben
    return jsonify(score_history)

# Create-Route
@app.route('/create', methods=('GET', 'POST'))
def create():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Holen der Abteilungen und Benutzer für die Dropdown-Menüs
    cursor.execute('SELECT id_department, department_name FROM Abteilung')
    departments = cursor.fetchall()
    cursor.execute('SELECT id_user, user_name FROM Benutzer')
    users = cursor.fetchall()

    # Wenn das Formular abgesendet wurde (POST)
    if request.method == 'POST':
        statement = request.form['statement']
        criteria = request.form['criteria']
        status_from = int(request.form['status_from'])
        measure_success = request.form['measure_success']
        id_department = request.form['id_department']
        modified_by = request.form['modified_by']

        # Validierung der Bewertung (status_from)
        if status_from < 1 or status_from > 10:
            return "Bewertung muss zwischen 1 und 10 liegen", 400

        # Ziel-Daten in die Datenbank einfügen
        cursor.execute(
            'INSERT INTO Ziele (statement, criteria, status_from, measure_success, id_department, last_modified_date, modified_by) '
            'VALUES (%s, %s, %s, %s, %s, NOW(), %s)',
            (statement, criteria, status_from, measure_success, id_department, modified_by)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    # Wenn es eine GET-Anfrage ist (Seite wird aufgerufen)
    cursor.close()
    connection.close()

    # Leeres goal-Objekt für den Fall, dass ein neues Ziel erstellt wird
    goal = {
        'statement': '',
        'criteria': '',
        'status_from': 1,  # Standardwert für Bewertung
        'measure_success': '',
        'id_department': None,
        'modified_by': None
    }

    return render_template('create.html', departments=departments, users=users, goal=goal)

# Edit-Route
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute('SELECT * FROM Ziele WHERE id_goals = %s', (id,))
    goal = cursor.fetchone()

    cursor.execute('SELECT id_department, department_name FROM Abteilung')
    departments = cursor.fetchall()
    cursor.execute('SELECT id_user, user_name FROM Benutzer')
    users = cursor.fetchall()

    if request.method == 'POST':
        statement = request.form['statement']
        criteria = request.form['criteria']
        status_from = int(request.form['status_from'])
        measure_success = request.form['measure_success']
        id_department = request.form['id_department']
        modified_by = request.form['modified_by']

        if status_from < 1 or status_from > 10:
            return "Bewertung muss zwischen 1 und 10 liegen", 400

        cursor.execute(
            'UPDATE Ziele SET statement = %s, criteria = %s, status_from = %s, measure_success = %s, id_department = %s, last_modified_date = NOW(), modified_by = %s '
            'WHERE id_goals = %s',
            (statement, criteria, status_from, measure_success, id_department, modified_by, id)
        )

        cursor.execute(
            'INSERT INTO Zielhistorie (id_goals, previous_score, new_score, change_description, last_modified_date, modified_by) '
            'VALUES (%s, %s, %s, %s, NOW(), %s)',
            (id, goal['status_from'], status_from, 'Ziel bearbeitet', modified_by)
        )

        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('index'))

    return render_template('edit.html', goal=goal, departments=departments, users=users)

# Delete-Route
@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Ziele WHERE id_goals = %s', (id,))
    connection.commit()
    cursor.close()
    connection.close()
    return redirect(url_for('index'))

# Historie-Route
@app.route('/history/<int:id>')
def history(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = '''
    SELECT gh.id_goals_history, gh.last_modified_date AS aenderungsdatum, 
           b.user_name AS aenderer, gh.new_score AS bewertung, 
           gh.change_description AS kommentar, z.measure_success AS anregung
    FROM Zielhistorie gh
    LEFT JOIN Ziele z ON gh.id_goals = z.id_goals
    LEFT JOIN Benutzer b ON gh.modified_by = b.id_user
    WHERE z.id_goals = %s
    ORDER BY gh.last_modified_date DESC;
    '''
    
    cursor.execute(query, (id,))
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return render_template('history.html', history=history)

# Delete History Entry Route
@app.route('/delete_history/<int:history_id>', methods=('POST',))
def delete_history(history_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('DELETE FROM Zielhistorie WHERE id_goals_history = %s', (history_id,))
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(request.referrer)

@app.route('/api/score_history_all')
def score_history_all():
    abteilung = request.args.get('abteilung', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Grundlegende SQL-Abfrage
    query = '''
    SELECT z.statement AS zielname, gh.last_modified_date, gh.new_score
    FROM Zielhistorie gh
    LEFT JOIN Ziele z ON gh.id_goals = z.id_goals
    LEFT JOIN Abteilung a ON z.id_department = a.id_department
    WHERE 1 = 1
    '''

    # Füge Filterbedingungen hinzu, falls gesetzt
    params = []
    if abteilung:
        query += ' AND a.department_name = %s'
        params.append(abteilung)
    
    if date_from:
        query += ' AND gh.last_modified_date >= %s'
        params.append(date_from)
    
    if date_to:
        query += ' AND gh.last_modified_date <= %s'
        params.append(date_to)

    query += ' ORDER BY gh.last_modified_date ASC'

    cursor.execute(query, tuple(params))
    score_history_all = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(score_history_all)



@app.route('/chart_view_all')
def chart_view_all():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Alle Abteilungen für das Dropdown abrufen
    cursor.execute('SELECT department_name FROM Abteilung')
    departments = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('chart_all.html', departments=departments)

@app.route('/history_overview')
def history_overview():
    return render_template('history.html')


if __name__ == "__main__":
    app.run(debug=True)
