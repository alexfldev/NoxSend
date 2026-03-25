import os
import secrets
import string
import uuid
from datetime import datetime, timedelta, timezone
from src.services.supabase_service import SupabaseService
from src.core.crypto_manager import CryptoManager
from src.models.paquete_metadata import PaqueteMetadata

class AppController:
    def __init__(self):
        """Inicializa el controlador y conecta con los servicios y el núcleo."""

        # Instanciamos los módulos de  arquitectura
        self.supabase = SupabaseService()
        self.crypto = CryptoManager()

    def generar_clave_automatica(self, longitud=16) -> str:
        """Genera una cadena aleatoria segura de letras y números."""
        caracteres = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(longitud))

    def enviar_archivo(self, ruta_original: str):
        print("Iniciando proceso Zero-Knowledge...")
        
        # 1. Generamos Identificador Único (UUID) y Llave
        id_archivo = str(uuid.uuid4())
        llave_secreta = self.generar_clave_automatica()
        
        # 2. Ciframos el archivo (Delegamos al core de cifrado)
        ruta_cifrada = self.crypto.cifrar_archivo(ruta_original, llave_secreta)
        
        if not ruta_cifrada or not os.path.exists(ruta_cifrada):
            print("❌ Error crítico: No se pudo cifrar el archivo localmente.")
            return None

        # 3. Preparamos los Metadatos usando nuestra DataClass
        tamano = os.path.getsize(ruta_cifrada)
        ahora = datetime.now(timezone.utc)
        expira = ahora + timedelta(hours=24) # Caducidad automática a las 24h
        
        paquete = PaqueteMetadata(
            id=id_archivo,
            tamano_bytes=tamano,
            creado_en=ahora.isoformat(),
            expira_en=expira.isoformat()
        )

        # 4. Subir al Storage (Usando el UUID para ocultar el nombre original)
        subida_ok = self.supabase.subir_archivo_cifrado(id_archivo, ruta_cifrada)
        
        if not subida_ok:
            return None

        # 5. Anotar en la Base de Datos (Convertimos la dataclass a diccionario)
        registro_ok = self.supabase.registrar_metadatos(paquete.to_dict())
        
        if not registro_ok:
            return None
            
        # 6. Limpieza de seguridad: Borramos el archivo .nox local
        try:
            os.remove(ruta_cifrada)
        except OSError:
            pass 

        # --- SALIDA FINAL PARA EL USUARIO ---
        print("\n" + "═"*55)
        print(" ¡ENVÍO BLINDADO COMPLETADO!")
        print(f" ID DEL ARCHIVO: {id_archivo}")
        print(f" LLAVE SECRETA:  {llave_secreta}")
        print("\n Simulación de enlace para el receptor:")
        print(f"   https://noxsend.com/recibir?id={id_archivo}#{llave_secreta}")
        print("═"*55)
        print(" Copia estos datos. Ni siquiera nosotros podemos abrirlo.\n")
        
        return id_archivo, llave_secreta