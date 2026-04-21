import flet as ft
from src.controllers.app_controller import AppController

def RegisterView(page: ft.Page):
    controlador = AppController()

    # --- Paleta de colores (Idéntica al Login) ---
    BG_ROOT = "#06080a"      
    BG_PANEL = "#0f1115"     
    ACCENT = "#3b82f6"       
    TEXT_MUTED = "grey500"   
    BORDER_COLOR = ft.Colors.with_opacity(0.1, "white")

    # --- Lógica de Registro ---
    def realizar_registro(e):
        if not input_email.value or not input_pass.value or not input_confirm.value:
            page.overlay.append(ft.SnackBar(ft.Text("Por favor, rellena todos los campos."), bgcolor="orange", open=True))
            page.update()
            return
            
        if input_pass.value != input_confirm.value:
            page.overlay.append(ft.SnackBar(ft.Text("Las contraseñas no coinciden. Revisa tu clave maestra."), bgcolor="red", open=True))
            page.update()
            return

        boton_registro_btn.disabled = True
        cargando.visible = True
        page.update()

        exito, msg = controlador.registrar_usuario(input_email.value, input_pass.value)
        
        cargando.visible = False
        if exito:
            page.overlay.append(ft.SnackBar(ft.Text("¡Bóveda creada con éxito! Ya puedes iniciar sesión."), bgcolor="green", open=True))
            page.go("/login") 
        else:
            page.overlay.append(ft.SnackBar(ft.Text(f"Error: {msg}"), bgcolor="red", open=True))
            boton_registro_btn.disabled = False
        page.update()

    # --- Componentes del formulario ---
    input_email = ft.TextField(
        label="Correo electrónico", width=380, border_radius=12, text_size=15, height=60,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.EMAIL_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT
    )
    
    input_pass = ft.TextField(
        label="Crea tu Contraseña Maestra", password=True, can_reveal_password=True, width=380, border_radius=12, text_size=15, height=60,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.LOCK_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT
    )

    input_confirm = ft.TextField(
        label="Confirma tu Contraseña", password=True, can_reveal_password=True, width=380, border_radius=12, text_size=15, height=60,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        focused_border_color=ACCENT, cursor_color=ACCENT
    )
    
    cargando = ft.ProgressRing(visible=False, width=24, height=24, color=ACCENT, stroke_width=3)
    
    boton_registro_btn = ft.ElevatedButton(
        "Crear mi Bóveda", icon=ft.Icons.SHIELD, width=380, height=55,
        bgcolor=ACCENT, color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=realizar_registro
    )

    boton_registro = ft.Container(
        content=boton_registro_btn,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.with_opacity(0.3, ACCENT)) 
    )

    # --- Contenedor de imagen (Mantenemos la coherencia visual) ---
    hueco_foto_app = ft.Container(
        width=550, height=320,
        bgcolor=ft.Colors.with_opacity(0.05, "white"), 
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, "white")),
        border_radius=12,
        shadow=ft.BoxShadow(spread_radius=5, blur_radius=30, color=ft.Colors.with_opacity(0.4, "black")),
        content=ft.Column([
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.1, "black"),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                content=ft.Row([
                    ft.CircleAvatar(radius=5, bgcolor="#ff5f56"),
                    ft.CircleAvatar(radius=5, bgcolor="#ffbd2e"),
                    ft.CircleAvatar(radius=5, bgcolor="#27c93f"),
                ], spacing=6)
            ),
            ft.Container(
                expand=True, alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_OUTLINED, size=50, color="white54"),
                    ft.Text("Espacio para la imagen de la aplicación.\nAñade 'image_src' en el contenedor cuando esté lista.", text_align="center", color="white54", size=12)
                ], horizontal_alignment="center", alignment="center")
            )
        ], spacing=0)
    )

    # --- Ensamblaje de la vista ---
    return ft.View(
        "/register",
        padding=0,
        bgcolor=BG_PANEL,
        controls=[
            ft.Row([
                # --- PANEL IZQUIERDO ---
                ft.Container(
                    expand=5,
                    bgcolor=BG_ROOT,
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left, end=ft.alignment.bottom_right,
                        colors=["#1e3a8a", "#0ea5e9"] 
                    ),
                    padding=60, 
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.SHIELD, color="white", size=28),
                            ft.Text("NOXSEND", size=20, weight="black", color="white", style=ft.TextStyle(letter_spacing=1)),
                        ]),
                        
                        ft.Container(expand=True),
                        
                        ft.Text("Toma el control absoluto de tus datos.", size=38, weight="black", color="white", style=ft.TextStyle(height=1.1)),
                        ft.Container(height=10),
                        ft.Text("Crea tu bóveda personal en segundos. Al ser una arquitectura Zero-Knowledge, la seguridad empieza en tu propio dispositivo.", size=16, color="white70", width=500),
                        ft.Container(height=30),
                        
                        hueco_foto_app, 
                        
                        ft.Container(expand=True),
                    ], horizontal_alignment="start"),
                ),

                # --- PANEL DERECHO: Formulario de Registro ---
                ft.Container(
                    expand=4,
                    bgcolor=BG_PANEL,
                    padding=ft.padding.symmetric(horizontal=50, vertical=40),
                    content=ft.Column([
                        # Cabecera superior
                        ft.Row([
                            ft.Text("WORKSPACE", size=11, weight="black", color=TEXT_MUTED, style=ft.TextStyle(letter_spacing=2)),
                            ft.Row([
                                ft.Icon(ft.Icons.CIRCLE, color="green400", size=10),
                                ft.Text("Servidor Operativo", size=10, color=TEXT_MUTED, weight="bold")
                            ])
                        ], alignment="spaceBetween"),
                        ft.Divider(height=20, color=BORDER_COLOR),
                        
                        # --- Formulario central ---
                        ft.Container(
                            expand=True, 
                            alignment=ft.alignment.center, 
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, color=ACCENT, size=40),
                                    padding=15, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=24, margin=ft.margin.only(bottom=5)
                                ),
                                ft.Text("Crear Auditoría", size=26, weight="black", color="white"),
                                ft.Text("Configura tus credenciales de acceso", size=14, color=TEXT_MUTED),
                                ft.Container(height=15),
                                
                                input_email, 
                                input_pass,
                                input_confirm,
                                
                                ft.Container(
                                    width=380, 
                                    padding=ft.padding.only(top=5),
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.RED_400, size=16),
                                        ft.Text("Crea una contraseña fuerte. No podremos recuperarla.", color=ft.Colors.RED_400, size=12)
                                    ], alignment="center")
                                ),
                                
                                ft.Container(height=10),
                                boton_registro,
                                ft.Container(height=5),
                                cargando,
                            ], horizontal_alignment="center", spacing=5)
                        ),
                        
                        # --- Pie de página y Login (Fijado abajo) ---
                        ft.Column([
                            ft.Divider(height=20, color=BORDER_COLOR),
                            ft.Row([
                                ft.Text("¿Ya tienes una bóveda creada?", color=TEXT_MUTED, size=13),
                                ft.TextButton(
                                    "Iniciar sesión", 
                                    icon=ft.Icons.LOGIN, 
                                    icon_color=ACCENT, 
                                    style=ft.ButtonStyle(color=ACCENT, overlay_color=ft.Colors.with_opacity(0.1, ACCENT)), 
                                    on_click=lambda _: page.go("/login")
                                )
                            ], alignment="center", spacing=5),
                            ft.Container(height=10),
                            ft.Text("NoxSend Workspace © 2024", size=11, color=ft.Colors.with_opacity(0.3, "white"), text_align="center")
                        ], horizontal_alignment="center", spacing=0)
                        
                    ], alignment="spaceBetween") 
                )
            ], expand=True, spacing=0)
        ]
    )