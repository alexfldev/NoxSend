import os
from supabase import create_client, Client
from dotenv import load_dotenv

class SupabaseService:
    def __init__(self):
        load_dotenv()
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("Error: Credenciales no configuradas.")
        self.cliente: Client = create_client(url, key)
        self.bucket_nombre = "archivos-cifrados"
        self.tabla_nombre = "archivos_seguros"

    def crear_usuario(self, email: str, password: str):
        try:
            self.cliente.auth.sign_up({"email": email, "password": password})
            return True, "Registro exitoso"
        except Exception as e:
            return False, str(e)

    def iniciar_sesion(self, email: str, password: str):
        try:
            self.cliente.auth.sign_in_with_password({"email": email, "password": password})
            return True, "Login correcto"
        except Exception:
            return False, "Credenciales incorrectas"

    def subir_archivo_cifrado(self, id_archivo, ruta_local):
        try:
            with open(ruta_local, "rb") as f:
                self.cliente.storage.from_(self.bucket_nombre).upload(path=id_archivo, file=f)
            return True
        except: return False

    def registrar_metadatos(self, datos):
        try:
            self.cliente.table(self.tabla_nombre).insert(datos).execute()
            return True
        except: return False