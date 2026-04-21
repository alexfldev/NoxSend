import flet as ft
from src.controllers.app_controller import AppController

def LoginView(page: ft.Page):
    controlador = AppController()

    # --- Paleta de colores ---
    BG_ROOT = "#06080a"      # Fondo principal
    BG_PANEL = "#0f1115"     # Fondo del formulario
    ACCENT = "#3b82f6"       # Color de acento (Azul)
    TEXT_MUTED = "grey500"   # Texto secundario
    BORDER_COLOR = ft.Colors.with_opacity(0.1, "white")

    # --- Lógica de inicio de sesión ---
    def realizar_login(e):
        boton_login_btn.disabled = True
        cargando.visible = True
        page.update()

        exito, msg = controlador.iniciar_sesion(input_email.value, input_pass.value)
        
        cargando.visible = False
        if exito:
            page.go("/dashboard") 
        else:
            page.overlay.append(ft.SnackBar(ft.Text(f"Error: {msg}"), bgcolor="red", open=True))
            boton_login_btn.disabled = False
        page.update()

    # --- Componentes del formulario ---
    input_email = ft.TextField(
        label="Correo electrónico", width=340, border_radius=12,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.EMAIL_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" # COLOR BLANCO AÑADIDO
    )
    
    input_pass = ft.TextField(
        label="Contraseña", password=True, can_reveal_password=True, width=340, border_radius=12,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.LOCK_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" # COLOR BLANCO AÑADIDO
    )
    
    cargando = ft.ProgressRing(visible=False, width=24, height=24, color=ACCENT, stroke_width=3)
    
    boton_login_btn = ft.ElevatedButton(
        "Iniciar sesión", icon=ft.Icons.LOGIN, width=340, height=50,
        bgcolor=ACCENT, color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=realizar_login
    )

    # Efecto de resplandor (glow) del botón principal
    boton_login = ft.Container(
        content=boton_login_btn,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.with_opacity(0.3, ACCENT)) 
    )

    # --- Contenedor de imagen (Showcase) ---
    hueco_foto_app = ft.Container(
        width=550,
        height=320,
        bgcolor=ft.Colors.with_opacity(0.05, "white"), 
        border=ft.border.all(1, ft.Colors.with_opacity(0.2, "white")),
        border_radius=12,
        shadow=ft.BoxShadow(spread_radius=5, blur_radius=30, color=ft.Colors.with_opacity(0.4, "black")),
        content=ft.Column([
            # Barra superior estilo ventana de macOS
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.1, "black"),
                padding=ft.padding.symmetric(horizontal=12, vertical=8),
                content=ft.Row([
                    ft.CircleAvatar(radius=5, bgcolor="#ff5f56"),
                    ft.CircleAvatar(radius=5, bgcolor="#ffbd2e"),
                    ft.CircleAvatar(radius=5, bgcolor="#27c93f"),
                ], spacing=6)
            ),
            # Placeholder
            ft.Container(
                expand=True, alignment=ft.alignment.center,
                content=ft.Column([
                    ft.Icon(ft.Icons.ADD_PHOTO_ALTERNATE_OUTLINED, size=50, color="white54"),
                    ft.Text("Espacio para la imagen de la aplicación.\nAñade 'image_src' en el contenedor cuando esté lista.", text_align="center", color="white54", size=12)
                ], horizontal_alignment="center", alignment="center")
            )
        ], spacing=0)
    )

    # --- Ensamblaje de la vista (Pantalla dividida) ---
    return ft.View(
        "/login",
        padding=0,
        bgcolor=BG_PANEL,
        controls=[
            ft.Row([
                # --- PANEL IZQUIERDO: Información del producto ---
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
                        
                        ft.Text("El estándar en cifrado de extremo a extremo.", size=38, weight="black", color="white", style=ft.TextStyle(height=1.1)),
                        ft.Container(height=10),
                        ft.Text("Protege, envía y gestiona tus archivos de forma local. Tu privacidad garantizada en todo momento.", size=16, color="white70", width=500),
                        ft.Container(height=30),
                        
                        hueco_foto_app, 
                        
                        ft.Container(expand=True),
                    ], horizontal_alignment="start"),
                ),

                # --- PANEL DERECHO: Formulario de inicio de sesión ---
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
                        ft.Divider(height=40, color=BORDER_COLOR),
                        
                        # --- Formulario central ---
                        ft.Container(
                            expand=True, 
                            alignment=ft.alignment.center, 
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, color=ACCENT, size=45),
                                    padding=15, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=20, margin=ft.margin.only(bottom=10)
                                ),
                                ft.Text("Bienvenido", size=26, weight="black", color="white"),
                                ft.Text("Ingresa tus credenciales para continuar", size=14, color=TEXT_MUTED),
                                ft.Container(height=25),
                                
                                input_email, 
                                input_pass,
                                
                                # Botón "¿Olvidaste tu contraseña?" alineado a la derecha del input
                                ft.Container(
                                    width=340, 
                                    alignment=ft.alignment.center_right,
                                    content=ft.TextButton("¿Olvidaste tu contraseña?", style=ft.ButtonStyle(color=TEXT_MUTED, padding=0))
                                ),
                                
                                ft.Container(height=15),
                                boton_login,
                                ft.Container(height=5),
                                cargando,
                            ], horizontal_alignment="center", spacing=5)
                        ),
                        
                        # --- Pie de página y Registro (Fijado abajo) ---
                        ft.Column([
                            ft.Divider(height=30, color=BORDER_COLOR),
                            ft.Row([
                                ft.Text("¿Aún no tienes una cuenta?", color=TEXT_MUTED, size=13),
                                ft.TextButton(
                                    "Crear una cuenta", 
                                    icon=ft.Icons.ARROW_FORWARD_ROUNDED, 
                                    icon_color=ACCENT, 
                                    style=ft.ButtonStyle(color=ACCENT, overlay_color=ft.Colors.with_opacity(0.1, ACCENT)), 
                                    on_click=lambda _: page.go("/register")
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