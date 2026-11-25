import os
import time
import psycopg2

# Esperar unos segundos a que la base de datos arranca por completo
time.sleep(3)

try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "mi_base_datos"),
        user=os.getenv("DB_USER", "mi_usuario"),
        password=os.getenv("DB_PASSWORD", "mi_password")
    )
    cursor = connection.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print(f" ¡Conexión exitosa a la base de datos! Versión: {db_version}")
    cursor.close()
    connection.close()
except Exception as error:
    print(f" Error al conectar a la base de datos: {error}")