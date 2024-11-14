import os
import pandas as pd
from datetime import datetime

# Directorio donde están los archivos
folder_path = 'MX_Fisheries_DB/data/vms'

# Función para renombrar archivos basados en el rango de fechas
def rename_files_by_date(folder_path):
    # Lista de archivos en la carpeta
    for filename in os.listdir(folder_path):
        # Solo procesar archivos CSV
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            
            # Intentar abrir el archivo y extraer las fechas
            try:
                df = pd.read_csv(file_path, encoding='ISO-8859-1', low_memory=False)
                
                # Identificar posibles columnas de fecha
                date_columns = [col for col in df.columns if 'fecha' in col.lower() or 'inicio' in col.lower() or 'fin' in col.lower()]
                
                if len(date_columns) >= 1:
                    # Convertir columnas de fecha al formato datetime
                    df[date_columns[0]] = pd.to_datetime(df[date_columns[0]], errors='coerce')
                    
                    # Obtener el rango de fechas
                    min_date = df[date_columns[0]].min().strftime('%Y-%m-%d')
                    max_date = df[date_columns[0]].max().strftime('%Y-%m-%d')
                    
                    # Crear un nuevo nombre basado en el rango de fechas
                    new_filename = f"VMS_{min_date}_to_{max_date}.csv"
                    new_file_path = os.path.join(folder_path, new_filename)
                    
                    # Renombrar el archivo
                    os.rename(file_path, new_file_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                else:
                    print(f"No date column found in '{filename}'")
            
            except Exception as e:
                print(f"Error processing file '{filename}': {e}")

# Ejecutar la función
rename_files_by_date(folder_path)