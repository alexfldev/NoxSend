# NÚCLEO DE SEGURIDAD NOXSEND - PROPIEDAD DE ALEJANDRO FEVRIER
# Implementación de cifrado simétrico AES-256-GCM Zero-Knowledge.
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoManager:
    def __init__(self):
        """Inicializa el motor criptográfico Zero-Knowledge."""
        pass

    def cifrar_archivo(self, ruta_archivo: str, password: str) -> str:
        """
        Cifra un archivo local usando AES-256-GCM.
        """
        try:
            # 1. Derivación de la llave
            key = password.ljust(32)[:32].encode('utf-8')
            aesgcm = AESGCM(key)
            
            # 2. Vector de Inicialización (Nonce) - 12 bytes aleatorios para GCM
            nonce = os.urandom(12)
            
            if not os.path.exists(ruta_archivo):
                print(f"❌ ❌ Error: No se encuentra el archivo en {ruta_archivo}❌ ❌ ")
                return None
                
            with open(ruta_archivo, "rb") as f:
                datos = f.read()
                
            # 3. Cifrado
            datos_cifrados = aesgcm.encrypt(nonce, datos, None)
            
            # 4. Empaquetado final (Nonce + Ciphertext)
            ruta_salida = f"{ruta_archivo}.nox"
            with open(ruta_salida, "wb") as f:
                f.write(nonce + datos_cifrados)
                
            print(f"🔒 Cifrado AES-256 completado con éxito en memoria local.")
            return ruta_salida
            
        except Exception as e:
            print(f"❌ ❌ Error crítico durante el cifrado local: {e}❌ ❌ ")
            return None