import sqlite3
import os

class VaultService:
    def __init__(self):
        # Creamos el archivo de base de datos local en la misma carpeta del programa
        self.db_path = "boveda_local.db"
        self._crear_tabla()

    def _crear_tabla(self):
        # Si la tabla no existe, la creamos la primera vez que se abre el programa
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historial_envios (
                id TEXT PRIMARY KEY,
                nombre_archivo TEXT,
                fecha TEXT
            )
        ''')
        conexion.commit()
        conexion.close()

    def registrar_envio(self, id_archivo: str, nombre_archivo: str, fecha: str):
        # Guarda el registro en el disco duro del usuario
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO historial_envios (id, nombre_archivo, fecha) VALUES (?, ?, ?)",
                       (id_archivo, nombre_archivo, fecha))
        conexion.commit()
        conexion.close()

    def obtener_historial(self):
        # Lee todos los envios para mostrarlos en la interfaz
        conexion = sqlite3.connect(self.db_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre_archivo, fecha FROM historial_envios ORDER BY fecha DESC")
        filas = cursor.fetchall()
        conexion.close()
        return filas

    # --- NUEVA FUNCIÓN PARA EL BOTÓN DE VACIAR BÓVEDA ---
    def limpiar_historial(self):
        # Borra todos los registros de la bóveda local garantizando la privacidad
        try:
            conexion = sqlite3.connect(self.db_path)
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM historial_envios")
            conexion.commit()
            conexion.close()
        except Exception as e:
            print(f"Error al limpiar la bóveda local: {e}")