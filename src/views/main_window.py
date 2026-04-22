import flet as ft
from src.views.login_view import LoginView
from src.views.register_view import RegisterView
from src.views.dashboard_view import DashboardView

def main(page: ft.Page):
    # --- Configuración básica de la ventana ---
    # Aquí definimos cómo se verá la ventana de la aplicación en el ordenador del usuario.
    page.title = "NoxSend Workspace"
    page.padding = 0  # Quitamos los márgenes por defecto para que nuestro diseño ocupe todo el espacio
    page.window_width = 1100
    page.window_height = 700
    
    # Establecemos unos topes mínimos para evitar que el usuario encoja 
    # demasiado la ventana y se rompa nuestro diseño "estilo PS5"
    page.window_min_width = 900
    page.window_min_height = 600

    # --- Sistema de Navegación (Enrutamiento) ---
    # Esta función actúa como un "controlador de tráfico". 
    # Cada vez que le decimos a la app 'page.go("ruta")', pasa por aquí.
    def route_change(e):
        # 1. Limpiamos las pantallas (vistas) anteriores para que no se amontonen unas encima de otras
        page.views.clear()
        
        # 2. Comprobamos a qué "ruta" queremos ir y cargamos su archivo correspondiente
        if page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/register":
            page.views.append(RegisterView(page))
        elif page.route == "/dashboard":
            page.views.append(DashboardView(page))
            
        # 3. Obligamos a la ventana a refrescarse para mostrar la nueva pantalla
        page.update()

    # Vinculamos la acción de cambiar de ruta de la app con nuestra función 'route_change'
    page.on_route_change = route_change
    
    # --- Arranque de la aplicación ---
    # Cuando abrimos el programa por primera vez, le decimos que vaya directamente a iniciar sesión
    page.go("/login")

# Este es el motor de arranque de Python. 
# Si ejecutamos este archivo directamente, lanza la interfaz gráfica de Flet.
if __name__ == "__main__":
    ft.app(target=main)