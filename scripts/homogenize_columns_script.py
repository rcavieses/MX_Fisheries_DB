
import pandas as pd

# Define file paths
vms_file = 'data/vms/01 - 01 -15 ENE  2023.csv'
avisos_file = 'data/reports/AVISOS_MAYORES_2017_2023.csv'
permisos_file = 'data/permits/permisos_pesca_comercial.csv'

# Define the standard column mapping for each unique column
column_map = {
    'LITORAL': 'LITORAL',
    'SUBSERIE': 'SUBSERIE',
    'ID_ESTADO': 'ID_ESTADO',
    'CLAVE_LUGARCAPTURA': 'CLAVE LUGARCAPTURA',
    'NOMBRE_SITIO_DESEMBARQUE': 'NOMBRE SITIO DESEMBARQUE',
    'PERMISO': 'PERMISO',
    'RNPA': 'RNPA UNIDAD ECONOMICA',
    'NOMBRE_ESTADO': 'NOMBRE ESTADO',
    'RNPA': 'RNP_TITULAR',
    'OBSERVACIONES': 'OBSERVACIONES',
    'EMBARCACION': 'EMBARCACION_O_NUMERO_DE_EMBARCACIONES',
    'MUNICIPIO': 'MUNICIPIO',
    'NOMBRE_LUGARCAPTURA': 'NOMBRE LUGARCAPTURA',
    'RAZON_SOCIAL': 'UNIDAD ECONOMICA',
    'FECHA_TERMINO': 'FECHA_TERMINO',
    'Puerto_Base': 'Puerto_Base',
    'CLAVE_OFICINA': 'CLAVE OFICINA',
    'RAZON_SOCIAL': 'Razón Social',
    'Velocidad': 'Velocidad',
    'Longitud': 'Longitud',
    'CLAVE_ESPECIE': 'CLAVE ESPECIE',
    'ZONA_DE_OPERACION': 'ZONA_DE_OPERACION',
    'RNPA': 'RNP',
    'NOMBRE_ESTADO': 'ESTADO',
    'RAZON_SOCIAL': 'RAZON_SOCIAL',
    'PESQUERIA': 'PESQUERIA',
    'Fecha': 'Fecha',
    'NOMBRE_OFICINA': 'NOMBRE OFICINA',
    'ARTES_DE_PESCA': 'ARTES_DE_PESCA',
    'Rumbo': 'Rumbo',
    'PRECIO_PESOS': 'PRECIO_PESOS',
    'FECHA_AVISO': 'FECHA AVISO',
    'RAZON_SOCIAL': 'Nombre',
    'NOMBRE_ESPECIE': 'NOMBRE ESPECIE',
    'ID_LOCALIDAD': 'ID_LOCALIDAD',
    'YEAR_CORTE': 'YEAR CORTE',
    'Latitud': 'Latitud',
    'TIPO_EMBARCACION': 'TIPO_EMBARCACION',
    'FECHA_INICIO': 'FECHA_INICIO',
    'NUMERO_EMBARCACIONES': 'NUMERO EMBARCACIONES',
    'LOCALIDAD': 'LOCALIDAD',
    'DESCRIPCION_ARTES_DE_PESCA': 'DESCRIPCION_ARTES_DE_PESCA',
    'NOMBRE_PRINCIPAL': 'NOMBRE PRINCIPAL',
    'FOLIO_AVISO': 'FOLIO AVISO',
    'Unnamed_0': 'Unnamed: 0',
    'PUERTO_BASE': 'PUERTO_BASE',
    'PESO_DESEMBARCADO_KILOGRAMOS': 'PESO DESEMBARCADO_KILOGRAMOS',
    'ID_MUNICIPIO': 'ID_MUNICIPIO',
    'CLAVE_SITIO_DESEMBARQUE': 'CLAVE SITIO DESEMBARQUE'
}

# Load each file and rename columns
def homogenize_and_save(file_path, output_path, column_map):
    # Load file
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    
    # Create a reverse map for renaming
    reverse_map = {v: k for k, v in column_map.items()}
    
    # Rename columns
    df = df.rename(columns=reverse_map)
    
    # Save the file
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"File saved to {output_path}")

# Process each file with the homogenized column names
homogenize_and_save(vms_file, 'homogenized_vms.csv', column_map)
homogenize_and_save(avisos_file, 'homogenized_avisos.csv', column_map)
homogenize_and_save(permisos_file, 'homogenized_permisos.csv', column_map)
