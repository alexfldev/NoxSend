# Autor: Alejandro Fevrier Lozano | NoxSend Desktop Client v1.0 (PFC 2026)
# Lógica de interfaz desarrollada con Flet Framework.
import flet as ft
import pyperclip # Recuerda: pip install pyperclip
from src.controllers.app_controller import AppController

def main(page: ft.Page):
    # 1. Configuración de la ventana
    page.title = "NoxSend - Envío Blindado"
    page.window_width = 500
    page.window_height = 700
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    controlador = AppController()
    ruta_seleccionada = [None] 

    # Función para copiar rápido
    def copiar(texto, msg):
        pyperclip.copy(texto)
        page.show_snack_bar(ft.SnackBar(ft.Text(f"{msg} copiado"), bgcolor=ft.Colors.BLUE_700))

    # 2. Componentes UI
    titulo = ft.Text("NoxSend", size=36, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    subtitulo = ft.Text("Selecciona un archivo para blindarlo.", color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)
    texto_archivo = ft.Text("Ningún archivo seleccionado", color=ft.Colors.GREY_500, italic=True)
    
    # 3. Componentes UI
    cargando = ft.ProgressRing(visible=False)
    panel_resultados = ft.Column(visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    texto_id = ft.TextField(label="ID DEL ARCHIVO", read_only=True, width=350)
    texto_llave = ft.TextField(label="LLAVE SECRETA", read_only=True, width=350, color=ft.Colors.GREEN_400, password=True, can_reveal_password=True)
    
    # Añadimos los campos de texto con sus botones de copiar al lado
    panel_resultados.controls.append(
        ft.Row([texto_id, ft.IconButton(ft.Icons.COPY, on_click=lambda _: copiar(texto_id.value, "ID"))], alignment=ft.MainAxisAlignment.CENTER)
    )
    panel_resultados.controls.append(
        ft.Row([texto_llave, ft.IconButton(ft.Icons.COPY, on_click=lambda _: copiar(texto_llave.value, "Llave"))], alignment=ft.MainAxisAlignment.CENTER)
    )

    # --- EVENTOS ---
    def al_seleccionar_archivo(e):
        if e.files:
            ruta_seleccionada[0] = e.files[0].path
            texto_archivo.value = f"📁 {e.files[0].name}"
            texto_archivo.color = ft.Colors.WHITE
            boton_enviar.disabled = False
        page.update()

    def enviar_archivo(e):
        if not ruta_seleccionada[0]: return
        boton_enviar.disabled = True
        cargando.visible = True
        page.update()

        resultado = controlador.enviar_archivo(ruta_seleccionada[0])

        cargando.visible = False
        if resultado:
            id_archivo, llave = resultado
            texto_id.value = id_archivo
            texto_llave.value = llave
            panel_resultados.visible = True
            texto_archivo.value = "✅ ¡Envío completado!"
            texto_archivo.color = ft.Colors.GREEN_400
        page.update()

    # 4. Explorador
    selector_archivos = ft.FilePicker(on_result=al_seleccionar_archivo)
    page.overlay.append(selector_archivos)

    # 5. Botones
    boton_seleccionar = ft.ElevatedButton(
        "1. Elegir Archivo", 
        icon=ft.Icons.FOLDER_OPEN,
        on_click=lambda _: selector_archivos.pick_files()
    )
    
    boton_enviar = ft.ElevatedButton(
        "2. Blindar y Subir", 
        icon=ft.Icons.CLOUD_UPLOAD,
        disabled=True,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        on_click=enviar_archivo
    )

    # 6. Pintar
    page.add(
        titulo, subtitulo, ft.Divider(height=20, color="transparent"),
        boton_seleccionar, texto_archivo, ft.Divider(height=10, color="transparent"),
        boton_enviar, cargando, panel_resultados
    )

if __name__ == "__main__":
    ft.app(target=main)