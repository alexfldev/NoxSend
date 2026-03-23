import os
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseService:
    def __init__(self):
        """Inicializa la conexión a Supabase usando las variables ocultas del .env"""
        load_dotenv()
        # Buscamos el NOMBRE de la variable, no el valor
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("⚠️ Faltan las credenciales de Supabase en el archivo .env")
            
        # Cliente oficial de Supabase
        self.cliente: Client = create_client(url, key)
        self.bucket_nombre = "archivos-cifrados"
        self.tabla_nombre = "archivos_seguros" 

    def subir_archivo_cifrado(self, id_archivo: str, ruta_archivo_local: str) -> bool:
        """Sube el archivo al Storage. OJO: Usa el ID como nombre para no revelar el nombre original."""
        try:
            with open(ruta_archivo_local, "rb") as f:
                self.cliente.storage.from_(self.bucket_nombre).upload(
                    path=id_archivo,
                    file=f,
                    file_options={"content-type": "application/octet-stream", "upsert": "true"}
                )
            print(f"📦 Blob subido al Storage con éxito (ID: {id_archivo}).")
            return True
        except Exception as e:
            print(f"❌ ERROR EN STORAGE: {e}")
            return False

    def registrar_metadatos(self, datos_paquete: dict) -> bool:
        """Guarda la información pública (tamaño, caducidad) en PostgreSQL."""
        try:
            self.cliente.table(self.tabla_nombre).insert(datos_paquete).execute()
            print("✅ Metadatos registrados en la base de datos.")
            return True
        except Exception as e:
            print(f"❌ Error al guardar metadatos en la base de datos: {e}")
            return False