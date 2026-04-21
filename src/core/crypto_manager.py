import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CryptoManager:
    def __init__(self):
        pass

    def cifrar_archivo(self, ruta_archivo: str, password: str) -> str:
        # Cifra el archivo usando AES-256 en modo GCM
        try:
            # Derivamos la clave para que ocupe exactamente 32 bytes (requisito de AES-256)
            key = password.ljust(32)[:32].encode('utf-8')
            aesgcm = AESGCM(key)
            
            # Generamos un Nonce aleatorio de 12 bytes
            nonce = os.urandom(12)
            
            if not os.path.exists(ruta_archivo):
                print(f"Error: Archivo no encontrado en {ruta_archivo}")
                return None
                
            with open(ruta_archivo, "rb") as f:
                datos = f.read()
                
            # Aplicamos la encriptacion
            datos_cifrados = aesgcm.encrypt(nonce, datos, None)
            
            # Escribimos el archivo temporal cifrado anadiendo el Nonce al principio
            ruta_salida = f"{ruta_archivo}.nox"
            with open(ruta_salida, "wb") as f:
                f.write(nonce + datos_cifrados)
                
            print("Cifrado AES-256 completado en memoria local.")
            return ruta_salida
            
        except Exception as e:
            print(f"Error durante el cifrado local: {e}")
            return None