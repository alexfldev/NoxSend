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
        # Instanciamos los módulos de arquitectura
        self.supabase = SupabaseService()
        self.crypto = CryptoManager()

    def generar_clave_automatica(self, longitud=32) -> str:
        """
        Genera una clave aleatoria segura. 
        Para AES-256 es recomendable usar 32 bytes de entropía.
        """
        caracteres = string.ascii_letters + string.digits
        return ''.join(secrets.choice(caracteres) for _ in range(longitud))

    def enviar_archivo(self, ruta_original: str, gan_lat=None, gan_lng=None, exp_time=24, exp_unit="Horas"):
        """
        Orquesta el proceso de envío con parámetros opcionales de seguridad.
        """
        print(f"Iniciando proceso Zero-Knowledge para: {os.path.basename(ruta_original)}")
        
        # 1. Generamos Identificador Único (UUID) y Llave desechable
        id_archivo = str(uuid.uuid4())
        llave_secreta = self.generar_clave_automatica()
        
        # 2. Ciframos el archivo localmente
        # Pasamos la llave generada al CryptoManager
        ruta_cifrada = self.crypto.cifrar_archivo(ruta_original, llave_secreta)
        
        if not ruta_cifrada or not os.path.exists(ruta_cifrada):
            print("❌ Error crítico: No se pudo cifrar el archivo localmente.")
            return None

        # 3. Lógica de Expiración (Opcional)
        ahora = datetime.now(timezone.utc)
        try:
            valor_tiempo = int(exp_time)
            if exp_unit == "Días":
                delta = timedelta(days=valor_tiempo)
            elif exp_unit == "Horas":
                delta = timedelta(hours=valor_tiempo)
            else:
                # Si son 'Descargas', por ahora ponemos un default de 1 semana 
                # hasta que implementes el contador en el backend
                delta = timedelta(days=7)
            
            fecha_expiracion = ahora + delta
        except (ValueError, TypeError):
            # Fallback a 24 horas si hay error en el input
            fecha_expiracion = ahora + timedelta(hours=24)

        # 4. Preparamos los Metadatos (Incluyendo G.A.N. si existen)
        tamano = os.path.getsize(ruta_cifrada)
        
        # Asegúrate de que tu DataClass 'PaqueteMetadata' acepte estos nuevos campos:
        # gan_lat, gan_lng y requiere_gan
        paquete = PaqueteMetadata(
            id=id_archivo,
            tamano_bytes=tamano,
            creado_en=ahora.isoformat(),
            expira_en=fecha_expiracion.isoformat(),
            requiere_gan=True if gan_lat and gan_lng else False,
            gan_lat=float(gan_lat) if gan_lat else None,
            gan_lng=float(gan_lng) if gan_lng else None
        )

        # 5. Subida al Storage (Cifrado de extremo a extremo)
        # El servidor recibe el archivo ya cifrado (.nox)
        subida_ok = self.supabase.subir_archivo_cifrado(id_archivo, ruta_cifrada)
        
        if not subida_ok:
            print("❌ Error: Fallo en la subida al Storage.")
            return None

        # 6. Registro en la Base de Datos (PostgreSQL)
        # Guardamos la política de seguridad (G.A.N y Expiración)
        registro_ok = self.supabase.registrar_metadatos(paquete.to_dict())
        
        if not registro_ok:
            print("❌ Error: No se pudieron registrar los metadatos en la DB.")
            return None
            
        # 7. Limpieza de seguridad: Borramos el rastro cifrado local
        try:
            os.remove(ruta_cifrada)
        except OSError:
            pass 

        # --- REPORTE TÁCTICO FINAL ---
        print("\n" + "═"*60)
        print(" 🛡️  SISTEMA NOXSEND: ENVÍO COMPLETADO")
        print(f" ID:    {id_archivo}")
        print(f" LLAVE: {llave_secreta}")
        if paquete.requiere_gan:
            print(f" G.A.N: Bloqueado a coordenadas [{gan_lat}, {gan_lng}]")
        print(f" EXP:   Caduca el {fecha_expiracion.strftime('%d/%m/%Y a las %H:%M')}")
        print("═"*60 + "\n")
        
        return id_archivo, llave_secreta