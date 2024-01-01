import sqlite3
import random
from datetime import datetime, timedelta

# Connect to the SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('progreso.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Sample data for 'sucursal', 'movimiento', and 'tipo_de_movimiento'
sucursales = ['Oficina Central', 'La Guardia', 'Mairana', 'Mercado El Torno', 'Cabezas', 'Vallegrande', 'Mora']
movimientos = ['Captaciones', 'Colocaciones']
captaciones_tipos = ['Caja de Ahorro', 'Deposito a Plazo Fijo', 'Tarjeta de Debito']
colocaciones_tipos = ['Microcreditos', 'Credito de Consumo', 'Credito de Vivienda', 'Credito Banca Comunal', 'Credito Grupo Solidario', 'Credito Productivo']

# Function to generate random datetime within a given range
def random_date(start_date, end_date):
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Function to generate random transactions
def generate_random_transactions(num_transactions):
    for _ in range(num_transactions):
        fecha = random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
        sucursal = random.choice(sucursales)
        movimiento = random.choice(movimientos)
        if movimiento == 'Captaciones':
            tipo_movimiento = random.choice(captaciones_tipos)
        else:
            tipo_movimiento = random.choice(colocaciones_tipos)
        monto = random.randint(1000, 50000)
        
        cursor.execute('''
            INSERT INTO movimientos (movimiento, tipo_de_movimiento, sucursal, monto, fecha)
            VALUES (?, ?, ?, ?, ?)
        ''', (movimiento, tipo_movimiento, sucursal, monto, fecha))

# Generate random transactions for two years with a range of 50 to 100 transactions per day
start_date = datetime(2022, 1, 1)
end_date = datetime(2023, 12, 31)

for day in range((end_date - start_date).days):
    num_transactions = random.randint(50, 100)
    generate_random_transactions(num_transactions)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully.")
