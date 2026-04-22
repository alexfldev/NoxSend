# src/views/onboarding_view.py
import flet as ft

def OnboardingView(page: ft.Page):
    
    # --- Lógica de navegación ---
    def finalizar_tutorial(e):
        # Cuando el usuario hace clic en el botón, cerramos esta pantalla
        # y le mandamos directamente a su panel de trabajo (NoxDrive)
        page.go("/dashboard")

    # --- Textos humanizados (Más cercanos y fáciles de entender) ---
    titulo = ft.Text("¡Bienvenido a NoxSend!", size=32, weight=ft.FontWeight.BOLD, color="white")
    subtitulo = ft.Text("Antes de empezar, recuerda estas 3 reglas de oro:", size=16, color="white70")
    
    # Usamos filas (Row) para poner un icono al lado de cada frase y que quede más bonito
    reglas = ft.Column([
        ft.Row([
            ft.Icon(ft.Icons.LOCK_OUTLINED, color="#3b82f6"), 
            ft.Text("1. Todo se bloquea en tu propio ordenador antes de salir a internet.", color=ft.Colors.GREY_300)
        ]),
        ft.Row([
            ft.Icon(ft.Icons.KEY_OFF_OUTLINED, color="#3b82f6"), 
            ft.Text("2. No tenemos copia de tus llaves. Si las pierdes, el archivo se pierde.", color=ft.Colors.GREY_300)
        ]),
        ft.Row([
            ft.Icon(ft.Icons.FOLDER_SPECIAL_OUTLINED, color="#3b82f6"), 
            ft.Text("3. Tienes un historial privado en tu 'Bóveda' que solo tú puedes ver (y borrar).", color=ft.Colors.GREY_300)
        ])
    ], spacing=15)
    
    # Un botón principal que invita a la acción
    boton_comenzar = ft.ElevatedButton(
        "Todo claro, ¡vamos allá!", 
        icon=ft.Icons.ROCKET_LAUNCH,
        on_click=finalizar_tutorial, 
        bgcolor="#3b82f6", # Azul eléctrico a juego con el Login
        color="white",
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), padding=20)
    )

    # --- Ensamblaje de la pantalla ---
    return ft.View(
        "/onboarding",
        bgcolor="#0f1115", # Fondo oscuro para mantener la estética global
        controls=[
            ft.Container(
                content=ft.Column(
                    [
                        titulo, 
                        subtitulo,
                        ft.Divider(height=20, color="transparent"), # Espaciador invisible
                        reglas, 
                        ft.Divider(height=30, color="transparent"), # Espaciador invisible
                        boton_comenzar
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center, # Centra la caja en medio de la pantalla
                expand=True # Le dice al contenedor que ocupe toda la ventana
            )
        ]
    )