import pandas as pd
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('pesca_db.sqlite')

# 1. Cargar datos para la tabla Permisionarios desde homogenized_permisos.csv
permisos_df = pd.read_csv('data/permits/permisos_with_id.csv',low_memory=False)
permisos_df['RAZON_SOCIAL_ID'] = permisos_df['RAZON_SOCIAL'].factorize()[0] + 1
permisos_df[['RAZON_SOCIAL_ID', 'RAZON_SOCIAL', 'RNP', 'ID_ESTADO', 'NOMBRE_ESTADO', 'ID_MUNICIPIO', 'MUNICIPIO', 'ID_LOCALIDAD', 'LOCALIDAD']].to_sql('Permisionarios', conn, if_exists='replace', index=False)

# 2. Cargar datos para la tabla Especies desde homogenized_avisos.csv
avisos_df = pd.read_csv('data/reports/avisos_with_id.csv',low_memory=False)
especies_df = avisos_df[['NOMBRE_PRINCIPAL']].drop_duplicates().reset_index(drop=True)
especies_df['EspecieID'] = especies_df['NOMBRE_PRINCIPAL'].factorize()[0] + 1
especies_df[['EspecieID', 'NOMBRE_PRINCIPAL']].to_sql('Especies', conn, if_exists='replace', index=False)

# 3. Cargar datos para la tabla PermisosPesca desde homogenized_permisos.csv
permisos_df['PermisoID'] = permisos_df.index + 1
permisos_df.to_sql('PermisosPesca', conn, if_exists='replace', index=False)

# 4. Cargar datos para la tabla Embarcaciones desde VMS_2018-01-01_to_2018-10-01.csv
vms_df = pd.read_csv('data/vessel_monitor_system/vms_with_id.csv',low_memory=False)
vms_df['EmbarcacionID'] = vms_df['NOMBRE_EMBARCACION'].factorize()[0] + 1
embarcaciones_df = vms_df[['EmbarcacionID', 'NOMBRE_EMBARCACION']].drop_duplicates().rename(columns={'NOMBRE_EMBARCACION': 'Nombre_Embarcacion'})
embarcaciones_df = embarcaciones_df.merge(permisos_df[['RAZON_SOCIAL', 'RAZON_SOCIAL_ID']], left_on='Nombre_Embarcacion', right_on='RAZON_SOCIAL', how='left')
embarcaciones_df.to_sql('Embarcaciones', conn, if_exists='replace', index=False)

# 5. Cargar datos para la tabla OficinasPesca desde homogenized_avisos.csv
oficinas_df = avisos_df[['CLAVE_OFICINA', 'NOMBRE_OFICINA', 'NOMBRE_ESTADO', 'CLAVE_SITIO_DESEMBARQUE', 'NOMBRE_SITIO_DESEMBARQUE']].drop_duplicates().rename(columns={
    'CLAVE_OFICINA': 'OficinaID',
    'NOMBRE_OFICINA': 'Nombre_Oficina',
    'NOMBRE_ESTADO': 'Estado',
    'CLAVE_SITIO_DESEMBARQUE': 'Clave_Sitio_Desembarque',
    'NOMBRE_SITIO_DESEMBARQUE': 'Nombre_Sitio_Desembarque'
})
oficinas_df.to_sql('OficinasPesca', conn, if_exists='replace', index=False)

# 6. Cargar datos para la tabla AvisosArribo desde homogenized_avisos.csv
avisos_df['ArriboID'] = avisos_df.index + 1

# Realizar el merge para asegurar que RAON_SOCIAL_ID esté presente
avisos_df = avisos_df.merge(permisos_df[['RAZON_SOCIAL', 'RAZON_SOCIAL_ID']], on='RAZON_SOCIAL', how='left')
avisos_df = avisos_df.merge(especies_df[['NOMBRE_PRINCIPAL', 'EspecieID']], on='NOMBRE_PRINCIPAL', how='left')

# Seleccionar y renombrar columnas antes de cargar en AvisosArribo
avisos_df[['ArriboID', 'FECHA_AVISO', 'CLAVE_OFICINA', 'RAZON_SOCIAL_ID', 'EspecieID', 'PESO_DESEMBARCADO_KILOGRAMOS', 'PRECIO_PESOS', 'LITORAL', 'NOMBRE_LUGARCAPTURA', 'NUMERO_EMBARCACIONES']].rename(columns={
    'FECHA_AVISO': 'Fecha_Arribo',
    'CLAVE_OFICINA': 'OficinaID',
    'PESO_DESEMBARCADO_KILOGRAMOS': 'Peso_Desembarcado_KG',
    'PRECIO_PESOS': 'Precio_Pesos',
    'NOMBRE_LUGARCAPTURA': 'Lugar_Captura'
}).to_sql('AvisosArribo', conn, if_exists='replace', index=False)

# 7. Cargar datos para la tabla Capturas desde homogenized_avisos.csv
avisos_df['Mes'] = pd.to_datetime(avisos_df['FECHA_AVISO']).dt.month
avisos_df['Año'] = pd.to_datetime(avisos_df['FECHA_AVISO']).dt.year
avisos_df[['ArriboID', 'EspecieID', 'CLAVE_OFICINA', 'FECHA_AVISO', 'PESO_DESEMBARCADO_KILOGRAMOS', 'PRECIO_PESOS', 'Mes', 'Año']].rename(columns={
    'ArriboID': 'CapturaID',
    'CLAVE_OFICINA': 'OficinaID',
    'FECHA_AVISO': 'Fecha_Captura',
    'PESO_DESEMBARCADO_KILOGRAMOS': 'Peso_KG',
    'PRECIO_PESOS': 'Valor'
}).to_sql('Capturas', conn, if_exists='replace', index=False)

# 8. Cargar datos para la tabla VMS desde VMS_2018-01-01_to_2018-10-01.csv
vms_df = vms_df.merge(embarcaciones_df[['Nombre_Embarcacion', 'EmbarcacionID']], left_on='NOMBRE_EMBARCACION', right_on='Nombre_Embarcacion', how='left')
vms_df['VMSID'] = vms_df.index + 1
vms_df[['VMSID', 'EmbarcacionID', 'FECHA', 'Latitud', 'Longitud', 'velocidad', 'Rumbo']].rename(columns={
    'FECHA': 'Fecha',
    'velocidad': 'Velocidad'
}).to_sql('VMS', conn, if_exists='replace', index=False)

# Guardar y cerrar conexión
conn.commit()
conn.close()

print("Datos cargados exitosamente en la base de datos.")
