from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Создание базы данных
def init_db():
    conn = sqlite3.connect('business_trips.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            organization TEXT NOT NULL,
            address TEXT NOT NULL,
            purpose TEXT NOT NULL,
            ticket_to_type TEXT NOT NULL,
            ticket_to_details TEXT NOT NULL,
            ticket_back_type TEXT NOT NULL,
            ticket_back_details TEXT NOT NULL,
            hotel TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Страны для выбора
COUNTRIES = ['Россия', 'Белоруссия', 'Казахстан', 'Кыргызстан', 'Китай', 'Индия']

# Главная страница - список командировок
@app.route('/')
def index():
    conn = sqlite3.connect('business_trips.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM business_trips')
    trips = cursor.fetchall()
    conn.close()
    return render_template('index.html', trips=trips, countries=COUNTRIES)

# Страница создания/редактирования командировки
@app.route('/trip/<int:trip_id>')
@app.route('/trip/new')
def trip_form(trip_id=None):
    trip = None
    if trip_id:
        conn = sqlite3.connect('business_trips.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM business_trips WHERE id = ?', (trip_id,))
        trip = cursor.fetchone()
        conn.close()
    return render_template('trip_form.html', trip=trip, countries=COUNTRIES)

# Сохранение командировки
@app.route('/save', methods=['POST'])
def save_trip():
    data = request.form
    trip_id = data.get('trip_id')
    
    if trip_id:  # Редактирование существующей
        conn = sqlite3.connect('business_trips.db')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE business_trips SET 
            full_name=?, country=?, city=?, start_date=?, end_date=?, 
            organization=?, address=?, purpose=?,
            ticket_to_type=?, ticket_to_details=?,
            ticket_back_type=?, ticket_back_details=?,
            hotel=?
            WHERE id=?
        ''', (
            data.get('full_name', ''), data.get('country', ''), data.get('city', ''),
            data.get('start_date', ''), data.get('end_date', ''),
            data.get('organization', ''), data.get('address', ''), data.get('purpose', ''),
            data.get('ticket_to_type', ''), data.get('ticket_to_details', ''),
            data.get('ticket_back_type', ''), data.get('ticket_back_details', ''),
            data.get('hotel', ''), trip_id
        ))
        conn.commit()
        conn.close()
    else:  # Создание новой
        conn = sqlite3.connect('business_trips.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO business_trips 
            (full_name, country, city, start_date, end_date, 
            organization, address, purpose,
            ticket_to_type, ticket_to_details,
            ticket_back_type, ticket_back_details, hotel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('full_name', ''), data.get('country', ''), data.get('city', ''),
            data.get('start_date', ''), data.get('end_date', ''),
            data.get('organization', ''), data.get('address', ''), data.get('purpose', ''),
            data.get('ticket_to_type', ''), data.get('ticket_to_details', ''),
            data.get('ticket_back_type', ''), data.get('ticket_back_details', ''),
            data.get('hotel', '')
        ))
        conn.commit()
        conn.close()
    
    return redirect(url_for('index'))

# Удаление командировки
@app.route('/delete/<int:trip_id>')
def delete_trip(trip_id):
    conn = sqlite3.connect('business_trips.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM business_trips WHERE id = ?', (trip_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
