import flet as ft
from src.views.onboarding_view import get_onboarding_view
from src.views.login_view import get_login_view
from src.views.dashboard_view import get_dashboard_view

def main(page: ft.Page):
    # 1. Configuración de la ventana principal
    page.title = "NoxSend - Zero Knowledge"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1000
    page.window_height = 700
    page.window_min_width = 800
    page.window_min_height = 600

    # 2. Rutas (El GPS de nuestra aplicación)
    def ir_al_dashboard():
        page.clean()
        vista_dashboard = get_dashboard_view(page)
        page.add(vista_dashboard)
        page.update()

    def ir_al_login():
        page.clean()
        vista_login = get_login_view(page, al_completar_login=ir_al_dashboard)
        page.add(vista_login)
        page.update()

    # 3. Arranque de la App (Mostramos el Onboarding/Tutorial primero)
    # Al terminar el tutorial, llamará a "ir_al_login"
    vista_tutorial = get_onboarding_view(page, al_completar_tutorial=ir_al_login)
    page.add(vista_tutorial)

if __name__ == "__main__":
    ft.app(target=main)