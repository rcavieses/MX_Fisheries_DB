import os
import pandas as pd

def rename_column_in_csv_files(folder_path):
    # Verificar si la carpeta existe
    if not os.path.exists(folder_path):
        print(f"La carpeta {folder_path} no existe.")
        return
    
    # Recorrer todos los archivos en la carpeta
    for filename in os.listdir(folder_path):
        # Verificar si el archivo es un CSV
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            
            # Leer el archivo CSV en un DataFrame
            try:
                df = pd.read_csv(file_path,low_memory=False)
                # Verificar si la columna 'RazÃ³n Social' existe
                if 'Pemisionario o Concesionario' in df.columns:
                    # Renombrar la columna
                    df.rename(columns={'Pemisionario o Concesionario': 'RAZON_SOCIAL'}, inplace=True)
                    # Guardar el archivo con el mismo nombre
                    df.to_csv(file_path, index=False)
                    print(f"La columna 'Pemisionario o Concesionario' ha sido renombrada en el archivo {filename}.")
                else:
                    print(f"El archivo {filename} no tiene la columna 'Pemisionario o Concesionario'.")
            except Exception as e:
                print(f"Error al procesar el archivo {filename}: {e}")

# Definir el path de la carpeta que contiene los archivos CSV
folder_path = 'data/vms'
rename_column_in_csv_files(folder_path)
