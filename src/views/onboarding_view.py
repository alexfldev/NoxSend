# src/views/onboarding_view.py
import flet as ft

def OnboardingView(page: ft.Page):
    
    def finalizar_tutorial(e):
        # Cuando termina el tutorial, va al panel principal
        page.go("/dashboard")

    # Contenido del tutorial
    titulo = ft.Text("Bienvenido a NoxSend", size=32, weight=ft.FontWeight.BOLD)
    
    reglas = ft.Column([
        ft.Text("1. Tus archivos se cifran localmente antes de enviarse.", color=ft.Colors.GREY_300),
        ft.Text("2. Nosotros no guardamos las llaves. Si las pierdes, el archivo es irrecuperable.", color=ft.Colors.GREY_300),
        ft.Text("3. Todo queda registrado en tu Boveda Local de Auditoria.", color=ft.Colors.GREY_300)
    ], spacing=10)
    
    boton_comenzar = ft.ElevatedButton("Entendido, comenzar a usar", on_click=finalizar_tutorial, bgcolor=ft.Colors.GREEN_600, color=ft.Colors.WHITE)

    return ft.View(
        "/onboarding",
        controls=[
            ft.Container(
                content=ft.Column(
                    [titulo, ft.Divider(), reglas, ft.Divider(color="transparent"), boton_comenzar],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center,
                expand=True
            )
        ]
    )