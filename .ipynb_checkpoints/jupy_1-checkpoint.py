# Connect to database
conn = sqlite3.connect('progreso.db')

# Query everything from movimientos table
query = 'SELECT * FROM movimientos'
df = pd.read_sql_query(query, conn)

#convertir la columna FECHAS a formato datetime
df['fecha'] = pd.to_datetime(df['fecha'])
df['Ano'] = df['fecha'].dt.year
df['Mes'] = df['fecha'].dt.month
df['Dia'] = df['fecha'].dt.day
df['Hora'] = df['fecha'].dt.hour
df['NombreDia'] = df['fecha'].dt.day_name()

print(df)

