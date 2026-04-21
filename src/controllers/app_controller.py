import os
import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone
from src.services.supabase_service import SupabaseService
from src.core.crypto_manager import CryptoManager
from src.services.vault_service import VaultService
from src.models.paquete_metadata import PaqueteMetadata

class AppController:
    def __init__(self):
        self.supabase = SupabaseService()
        self.crypto = CryptoManager()
        self.vault = VaultService()

    def registrar_usuario(self, email, pwd):
        return self.supabase.crear_usuario(email, pwd)

    def iniciar_sesion(self, email, pwd):
        return self.supabase.iniciar_sesion(email, pwd)

    def enviar_archivo(self, ruta_original: str):
        id_archivo = str(uuid.uuid4())
        llave_secreta = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
        
        ruta_cifrada = self.crypto.cifrar_archivo(ruta_original, llave_secreta)
        if not ruta_cifrada: return None

        ahora = datetime.now(timezone.utc)
        paquete = PaqueteMetadata(
            id=id_archivo,
            tamano_bytes=os.path.getsize(ruta_cifrada),
            creado_en=ahora.isoformat(),
            expira_en=(ahora + timedelta(hours=24)).isoformat()
        )

        if self.supabase.subir_archivo_cifrado(id_archivo, ruta_cifrada):
            self.supabase.registrar_metadatos(paquete.to_dict())
            self.vault.registrar_envio(id_archivo, os.path.basename(ruta_original), ahora.strftime("%Y-%m-%d %H:%M"))
            os.remove(ruta_cifrada)
            return id_archivo, llave_secreta
        return None

    def obtener_boveda(self):
        return self.vault.obtener_historial()

    def limpiar_boveda(self):
        self.vault.limpiar_historial()