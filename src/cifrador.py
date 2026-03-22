import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def cifrar_archivo(ruta_archivo, password):
    # 1. Convertimos la contraseña en una llave de 32 bytes (AES-256)
    # Para el MVP, la ajustamos a 32 caracteres (rellenando con espacios si hace falta)
    key = password.ljust(32)[:32].encode()
    aesgcm = AESGCM(key)
    
    # 2. Creamos un "Nonce" (un número aleatorio único para este archivo)
    # Es vital para que el cifrado no sea siempre igual
    nonce = os.urandom(12)
    
    # 3. Leemos el archivo original
    with open(ruta_archivo, "rb") as f:
        datos = f.read()
        
    # 4. CIFRAMOS
    datos_cifrados = aesgcm.encrypt(nonce, datos, None)
    
    # 5. Guardamos el archivo cifrado (Metemos el nonce al principio para poder descifrar luego)
    ruta_salida = ruta_archivo + ".nox"
    with open(ruta_salida, "wb") as f:
        f.write(nonce + datos_cifrados)
        
    print(f"✅ Archivo cifrado con éxito: {ruta_salida}")
    return ruta_salida

# --- PRUEBA RÁPIDA ---
if __name__ == "__main__":
    # Crea un archivo de texto de prueba rápido
    with open("prueba.txt", "w") as f:
        f.write("Este es un mensaje secreto de NoxSend.")
    
    # Lo ciframos con una contraseña
    cifrar_archivo("prueba.txt", "mi_clave_secreta_123")