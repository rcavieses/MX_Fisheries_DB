import pandas as pd
import sqlite3

# Conectar a la base de datos
db_path = 'fisheries_database.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Función para cargar datos de VMS en las tablas embarcaciones y vms_datos
def load_vms_data(csv_file, conn):
    try:
        vms_df = pd.read_csv(csv_file, low_memory=False)
        
        for _, row in vms_df.iterrows():
            # Insertar o ignorar embarcación
            cursor.execute('''
            INSERT OR IGNORE INTO embarcaciones (NOMBRE_EMBARCACION, RNP, PUERTO_BASE, RAZON_SOCIAL)
            VALUES (?, ?, ?, ?)
            ''', (row['NOMBRE_EMBARCACION'], row['RNP'], row['PUERTO_BASE'], row['RAZON_SOCIAL']))
            
            # Obtener el id de la embarcación
            cursor.execute('''
            SELECT id FROM embarcaciones WHERE NOMBRE_EMBARCACION = ?
            ''', (row['NOMBRE_EMBARCACION'],))
            embarcacion_id = cursor.fetchone()[0]
            
            # Insertar datos de movimiento en vms_datos
            cursor.execute('''
            INSERT OR IGNORE INTO vms_datos (embarcacion_id, FECHA, Latitud, Longitud, velocidad, Rumbo)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (embarcacion_id, row['FECHA'], row['Latitud'], row['Longitud'], row['velocidad'], row['Rumbo']))
        
        print(f"Datos de '{csv_file}' cargados en las tablas 'embarcaciones' y 'vms_datos'.")
    except Exception as e:
        print(f"Error al cargar '{csv_file}': {e}")

# Lista de archivos a cargar
files_to_load = [
    'data/vms/VMS_2021-01-02_to_2021-12-02.csv',
    'data/vms/VMS_2023-01-01_to_2023-12-01.csv',
    'data/vms/VMS_2023-05-01_to_2023-05-31.csv',
    'data/vms/VMS_2023-10-01_to_2023-10-31.csv'
]

# Cargar cada archivo individualmente
for file_path in files_to_load:
    load_vms_data(file_path, conn)

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()
print("Todos los archivos han sido cargados en la base de datos.")