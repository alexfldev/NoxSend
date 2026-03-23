import os
from src.controllers.app_controller import AppController

if __name__ == "__main__":
    print("Iniciando NoxSend...")
    
    # Preparamos un archivo de prueba en la carpeta temp
    os.makedirs("temp", exist_ok=True)
    ruta_prueba = "temp/prueba.txt"
    
    if not os.path.exists(ruta_prueba):
        with open(ruta_prueba, "w") as f:
            f.write("Si estas leyendo esto eres Alvaro Gonzalez Zerpa.")
            
    # Instanciamos el controlador y ejecutamos
    app = AppController()
    app.enviar_archivo(ruta_prueba)