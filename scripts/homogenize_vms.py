import os
import pandas as pd
from datetime import datetime

# Directorio donde están los archivos VMS
folder_path = 'data/vms'

# Define el mapeo de columnas estandarizadas
column_map = {
    'NOMBRE_EMBARCACION': 'Nombre',
    'RNPA': 'NRP',
    'FECHA': 'Fecha',
    'Latitud': 'Latitud',
    'Longitud': 'Longitud',
    'PUERTO_BASE': 'Puerto_Base',
    'RNPA': 'RNPA UNIDAD ECONOMICA',
    'RAZON_SOCIAL': 'RazÃ³n Social',
    'RNPA': 'RNP_TITULAR',
    'PUERTO_BASE':'Puerto Base',
    'RAZON_SOCIAL':'RazÃÂ³n Social',
    'FECHA':'Fecha',
    'velocidad':'Velocidad',
    'Rumbo':'Rumbo',
    'RAZON_SOCIAL':'RazÃÂÃÂ³n Social',
    'RAZON_SOCIAL':'Razón Social'
}

# Función para homogenizar columnas y renombrar archivo basado en rango de fechas
def homogenize_and_rename_files(folder_path, column_map):
    for filename in os.listdir(folder_path):
        # Solo procesar archivos CSV
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            
            try:
                # Cargar el archivo
                df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)
                
                # Crear un mapeo inverso para renombrar columnas
                reverse_map = {v: k for k, v in column_map.items()}
                df = df.rename(columns=reverse_map)
                
                # Identificar la columna de fecha
                date_columns = [col for col in df.columns if 'fecha' in col.lower() or 'inicio' in col.lower() or 'fin' in col.lower()]
                if date_columns:
                    df[date_columns[0]] = pd.to_datetime(df[date_columns[0]], errors='coerce')
                    
                    # Obtener el rango de fechas
                    min_date = df[date_columns[0]].min().strftime('%Y-%m-%d')
                    max_date = df[date_columns[0]].max().strftime('%Y-%m-%d')
                    
                    # Definir el nuevo nombre del archivo basado en el rango de fechas
                    new_filename = f"VMS_{min_date}_to_{max_date}.csv"
                    new_file_path = os.path.join(folder_path, new_filename)
                    
                    # Guardar el archivo homogenizado y renombrado
                    df.to_csv(new_file_path, index=False, encoding='utf-8')
                    print(f"Renamed and saved '{filename}' as '{new_filename}'")
                else:
                    print(f"No date column found in '{filename}'")
            
            except Exception as e:
                print(f"Error processing file '{filename}': {e}")

# Ejecutar la función
homogenize_and_rename_files(folder_path, column_map)
