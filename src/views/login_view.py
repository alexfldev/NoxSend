import flet as ft

def get_login_view(page: ft.Page, al_completar_login):
    
    def intentar_login(e):
        # En el futuro aquí validaremos la contraseña local
        # Por ahora, simplemente le decimos a la app principal que nos deje pasar
        al_completar_login()

    return ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.SHIELD_MOON, size=80, color=ft.Colors.BLUE_400),
            ft.Text("NoxSend", size=40, weight=ft.FontWeight.BOLD),
            ft.Text("Autenticación Zero-Knowledge", color=ft.Colors.GREY_400),
            ft.Container(height=20),
            ft.TextField(label="Email / Usuario", width=350, prefix_icon=ft.Icons.PERSON),
            ft.TextField(label="Contraseña Maestra", width=350, password=True, can_reveal_password=True, prefix_icon=ft.Icons.VPN_KEY),
            ft.Text("⚠️ Tu clave no se envía al servidor. Si la pierdes, no hay recuperación.", color=ft.Colors.RED_400, size=12),
            ft.Container(height=10),
            ft.ElevatedButton(
                "DESBLOQUEAR BÓVEDA", 
                on_click=intentar_login, 
                bgcolor=ft.Colors.BLUE_700, 
                color=ft.Colors.WHITE, 
                width=350, 
                height=50
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.center
    )