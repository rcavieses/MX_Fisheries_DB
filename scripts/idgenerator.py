import pandas as pd

# Cargar los archivos CSV
permisos_df = pd.read_csv('data/permits/homogenized_permisos.csv',low_memory=False)
avisos_df = pd.read_csv('data/reports/homogenized_avisos.csv',low_memory=False)
vms_df = pd.read_csv('data/vessel_monitor_system/vms_2018_2023.csv',low_memory=False)

# Remover espacios en los valores de la columna RAZON_SOCIAL para evitar problemas de coincidencia
permisos_df['RAZON_SOCIAL'] = permisos_df['RAZON_SOCIAL'].str.strip()
avisos_df['RAZON_SOCIAL'] = avisos_df['RAZON_SOCIAL'].str.strip()
vms_df['RAZON_SOCIAL'] = vms_df['RAZON_SOCIAL'].str.strip()

# Crear un conjunto con todos los valores únicos de RAZON_SOCIAL en los tres archivos
unique_razon_social = set(permisos_df['RAZON_SOCIAL'].dropna()).union(
    set(avisos_df['RAZON_SOCIAL'].dropna()),
    set(vms_df['RAZON_SOCIAL'].dropna())
)

# Crear un diccionario para mapear cada RAZON_SOCIAL a un ID único
razon_social_id_map = {razon_social: idx for idx, razon_social in enumerate(unique_razon_social, start=1)}

# Agregar una nueva columna 'RAZON_SOCIAL_ID' en cada DataFrame usando el diccionario de mapeo
permisos_df['RAZON_SOCIAL_ID'] = permisos_df['RAZON_SOCIAL'].map(razon_social_id_map)
avisos_df['RAZON_SOCIAL_ID'] = avisos_df['RAZON_SOCIAL'].map(razon_social_id_map)
vms_df['RAZON_SOCIAL_ID'] = vms_df['RAZON_SOCIAL'].map(razon_social_id_map)

# Guardar los DataFrames actualizados en nuevos archivos CSV
permisos_df.to_csv('data/permits/permisos_with_id.csv', index=False)
avisos_df.to_csv('data/reports/avisos_with_id.csv', index=False)
vms_df.to_csv('data/vessel_monitor_system/vms_with_id.csv', index=False)

print("IDs únicos asignados y archivos guardados con la columna 'RAZON_SOCIAL_ID'")
