import os
from supabase import create_client
from dotenv import load_dotenv
from cifrador import cifrar_archivo 

# 1. Configuración de conexión
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def enviar_a_la_nube(ruta_original, password):
    # A. Ciframos el archivo (esto crea el archivo .nox localmente)
    ruta_cifrada = cifrar_archivo(ruta_original, password)
    nombre_solo = os.path.basename(ruta_cifrada)
    
    subida_correcta = False

    # B. Subir al Storage (TODO EN MINÚSCULAS)
    with open(ruta_cifrada, "rb") as f:
        try:
            # Usamos el nombre exacto de tu web: archivos-cifrados
            supabase.storage.from_("archivos-cifrados").upload(
                path=nombre_solo,
                file=f,
                file_options={"content-type": "application/octet-stream"}
            )
            print(f"📦 Archivo subido al Storage con éxito.")
            subida_correcta = True
        except Exception as e:
            print(f"❌ ERROR CRÍTICO EN STORAGE: {e}")
            print("El archivo NO se ha subido. Revisa el nombre del bucket o las Policies.")

    # C. Si la subida falló, paramos aquí para no crear datos falsos
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
        
        print(f"\n🚀 ¡AHORA SÍ: MISIÓN CUMPLIDA!")
        print(f"ID del archivo: {db_res.data[0]['id']}")
        print(f"Archivo cifrado, subido y registrado correctamente.")
        return db_res.data[0]['id']
    except Exception as e:
        print(f"❌ Error al guardar en la base de datos: {e}")
        return None

# --- EJECUCIÓN ---
if __name__ == "__main__":
    if not os.path.exists("prueba.txt"):
        with open("prueba.txt", "w") as f:
            f.write("Este es el contenido secreto de NoxSend.")
            
    enviar_a_la_nube("prueba.txt", "clave-secreta-del-pfc")