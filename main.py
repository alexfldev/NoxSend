import flet as ft
from src.views.main_window import main

if __name__ == "__main__":
    print("🚀 Iniciando Interfaz Gráfica de NoxSend...")
    # Esto le dice a Flet que abra la ventana que acabamos de diseñar
    ft.app(target=main)