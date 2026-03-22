import os
import secrets  # Generación de claves segura para criptografía
import string
from supabase import create_client
from dotenv import load_dotenv
from cifrador import cifrar_archivo 

# 1. Configuración de conexión
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def generar_clave_automatica(longitud=16):
    """Genera una cadena aleatoria segura de letras y números."""
    caracteres = string.ascii_letters + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

def enviar_a_la_nube(ruta_original):
    # A. GENERAMOS LA LLAVE SECRETA AUTOMÁTICAMENTE
    password_auto = generar_clave_automatica()
    
    # B. Ciframos el archivo con la llave generada
    ruta_cifrada = cifrar_archivo(ruta_original, password_auto)
    nombre_solo = os.path.basename(ruta_cifrada)
    
    subida_correcta = False

    # C. Subir al Storage (archivos-cifrados)
    with open(ruta_cifrada, "rb") as f:
        try:
            supabase.storage.from_("archivos-cifrados").upload(
                path=nombre_solo,
                file=f,
                file_options={
                    "content-type": "application/octet-stream",
                    "upsert": "true" 
                }
            )
            print(f"📦 Archivo subido al Storage con éxito.")
            subida_correcta = True
        except Exception as e:
            print(f"❌ ERROR EN STORAGE: {e}")

    if not subida_correcta:
        return None

    # D. Obtener la URL pública
    url_publica = supabase.storage.from_("archivos-cifrados").get_public_url(nombre_solo)

    # E. Anotar en la base de datos (Metadatos)
    datos_archivo = {
        "nombre_archivo": nombre_solo,
        "tamano_bytes": os.path.getsize(ruta_cifrada),
        "storage_url": url_publica
    }
    
    try:
        db_res = supabase.table("archivos_seguros").insert(datos_archivo).execute()
        
        # --- SALIDA FINAL PARA EL USUARIO ---
        print("\n" + "═"*40)
        print("🚀 ¡ENVÍO BLINDADO COMPLETADO!")
        print(f"🆔 ID DEL ARCHIVO: {db_res.data[0]['id']}")
        print(f"🔑 LLAVE SECRETA:  {password_auto}")
        print("═"*40)
        print("⚠️  Copia estos datos. Sin la llave, nadie podrá abrirlo.\n")
        
        return db_res.data[0]['id'], password_auto
    except Exception as e:
        print(f"❌ Error al guardar en la base de datos: {e}")
        return None

# --- EJECUCIÓN ---
if __name__ == "__main__":
    if not os.path.exists("prueba.txt"):
        with open("prueba.txt", "w") as f:
            f.write("Si estas leyendo esto eres Alvaro Gonzalez Zerpa.")
            
    # Ahora la función ya no necesita que le pasemos la contraseña
    enviar_a_la_nube("prueba.txt")