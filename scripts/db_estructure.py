import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('pesca_db.sqlite')
cursor = conn.cursor()

# Crear la tabla Permisionarios
cursor.execute('''
CREATE TABLE IF NOT EXISTS Permisionarios (
    RAZON_SOCIAL_ID INTEGER PRIMARY KEY,
    Razon_Social TEXT NOT NULL,
    RNP TEXT,
    ID_Estado INTEGER,
    Nombre_Estado TEXT,
    ID_Municipio INTEGER,
    Municipio TEXT,
    ID_Localidad INTEGER,
    Localidad TEXT
)
''')

# Crear la tabla Especies
cursor.execute('''
CREATE TABLE IF NOT EXISTS Especies (
    EspecieID INTEGER PRIMARY KEY,
    NOMBRE_PRINCIPAL TEXT NOT NULL
)
''')

# Crear la tabla PermisosPesca
cursor.execute('''
CREATE TABLE IF NOT EXISTS PermisosPesca (
    PermisoID INTEGER PRIMARY KEY,
    RAZON_SOCIAL_ID INTEGER,
    Tipo_Embarcacion TEXT,
    Zona_de_Operacion TEXT,
    Puerto_Base TEXT,
    Pesqueria TEXT,
    Fecha_Inicio DATE,
    Fecha_Termino DATE,
    Artes_de_Pesca TEXT,
    Descripcion_Artes_de_Pesca TEXT,
    Observaciones TEXT,
    Subserie TEXT,
    FOREIGN KEY (RAZON_SOCIAL_ID) REFERENCES Permisionarios(RAZON_SOCIAL_ID)
)
''')

# Crear la tabla Embarcaciones (usando los nombres de embarcación del archivo VMS)
cursor.execute('''
CREATE TABLE IF NOT EXISTS Embarcaciones (
    EmbarcacionID INTEGER PRIMARY KEY,
    Nombre_Embarcacion TEXT NOT NULL,
    RAZON_SOCIAL_ID INTEGER,
    FOREIGN KEY (RAZON_SOCIAL_ID) REFERENCES Permisionarios(RAZON_SOCIAL_ID)
)
''')

# Crear la tabla OficinasPesca
cursor.execute('''
CREATE TABLE IF NOT EXISTS OficinasPesca (
    OficinaID INTEGER PRIMARY KEY,
    Nombre_Oficina TEXT NOT NULL,
    Ubicacion TEXT,
    Estado TEXT,
    Clave_Sitio_Desembarque TEXT,
    Nombre_Sitio_Desembarque TEXT
)
''')

# Crear la tabla AvisosArribo
cursor.execute('''
CREATE TABLE IF NOT EXISTS AvisosArribo (
    ArriboID INTEGER PRIMARY KEY,
    Fecha_Arribo DATE,
    OficinaID INTEGER,
    RAZON_SOCIAL_ID INTEGER,
    EspecieID INTEGER,
    Peso_Desembarcado_KG FLOAT,
    Precio_Pesos FLOAT,
    Litoral TEXT,
    Lugar_Captura TEXT,
    Numero_Embarcaciones INTEGER,
    FOREIGN KEY (OficinaID) REFERENCES OficinasPesca(OficinaID),
    FOREIGN KEY (RAZON_SOCIAL_ID) REFERENCES Permisionarios(RAZON_SOCIAL_ID),
    FOREIGN KEY (EspecieID) REFERENCES Especies(EspecieID)
)
''')

# Crear la tabla Capturas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Capturas (
    CapturaID INTEGER PRIMARY KEY,
    EspecieID INTEGER,
    OficinaID INTEGER,
    Fecha_Captura DATE,
    Peso_KG FLOAT,
    Valor FLOAT,
    Mes INTEGER,
    Año INTEGER,
    FOREIGN KEY (EspecieID) REFERENCES Especies(EspecieID),
    FOREIGN KEY (OficinaID) REFERENCES OficinasPesca(OficinaID)
)
''')

# Crear la tabla VMS (con relación a EmbarcacionID)
cursor.execute('''
CREATE TABLE IF NOT EXISTS VMS (
    VMSID INTEGER PRIMARY KEY,
    EmbarcacionID INTEGER,
    Fecha DATE,
    Latitud FLOAT,
    Longitud FLOAT,
    Velocidad FLOAT,
    Rumbo TEXT,
    FOREIGN KEY (EmbarcacionID) REFERENCES Embarcaciones(EmbarcacionID)
)
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Estructura de la base de datos creada exitosamente.")
