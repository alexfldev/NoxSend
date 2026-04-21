import flet as ft
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView

def main(page: ft.Page):
    page.title = "NoxSend Workspace"
    page.padding = 0
    page.window_width = 1100
    page.window_height = 700
    page.window_min_width = 900
    page.window_min_height = 600

    def route_change(e):
        page.views.clear()
        
        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/register":
            page.views.append(RegisterView(page))
        elif page.route == "/dashboard":
            page.views.append(DashboardView(page))
            
        page.update()

    page.on_route_change = route_change
    page.go("/login")

if __name__ == "__main__":
    ft.app(target=main)