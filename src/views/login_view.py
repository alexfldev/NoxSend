import flet as ft
from src.controllers.app_controller import AppController

def LoginView(page: ft.Page):
    controlador = AppController()

    # --- Paleta de colores ---
    BG_ROOT = "#06080a"      
    BG_PANEL = "#0f1115"     
    ACCENT = "#3b82f6"       
    TEXT_MUTED = "grey500"   
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
            page.overlay.append(ft.SnackBar(ft.Text(f"Vaya, algo ha fallado: {msg}"), bgcolor="red", open=True))
            boton_login_btn.disabled = False
        page.update()

    # --- Componentes del formulario ---
    input_email = ft.TextField(
        label="Tu correo", width=340, border_radius=12,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.EMAIL_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" 
    )
    
    input_pass = ft.TextField(
        label="Tu contraseña", password=True, can_reveal_password=True, width=340, border_radius=12,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.LOCK_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" 
    )
    
    cargando = ft.ProgressRing(visible=False, width=24, height=24, color=ACCENT, stroke_width=3)
    
    boton_login_btn = ft.ElevatedButton(
        "Entrar", icon=ft.Icons.LOGIN, width=340, height=50,
        bgcolor=ACCENT, color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=realizar_login
    )

    boton_login = ft.Container(
        content=boton_login_btn,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.with_opacity(0.3, ACCENT)) 
    )

    # --- NUEVO: Panel Explicativo (ALTO CONTRASTE BLANCO) ---
    def PasoExplicativo(icono, titulo, descripcion):
        return ft.Row([
            ft.Container(
                content=ft.Icon(icono, color="white", size=24), # Icono Blanco puro
                bgcolor=ft.Colors.with_opacity(0.2, "white"),   # Fondo del icono blanco translúcido
                padding=12, border_radius=12
            ),
            ft.Column([
                ft.Text(titulo, weight="bold", color="white", size=14),
                ft.Text(descripcion, color="white70", size=12, width=320) # Texto secundario en blanco al 70%
            ], spacing=2)
        ], alignment="start", vertical_alignment="center")

    panel_explicativo = ft.Container(
        width=550,
        bgcolor=ft.Colors.with_opacity(0.15, "white"), # Fondo de la caja más blanco
        border=ft.border.all(1, ft.Colors.with_opacity(0.4, "white")), # Borde blanco más visible
        border_radius=16,
        padding=30,
        content=ft.Column([
            ft.Text("¿Cómo vas a enviar archivos con NoxSend?", size=18, weight="bold", color="white"),
            ft.Container(height=15),
            PasoExplicativo(ft.Icons.LOCK_OUTLINE, "1. Blíndalos aquí", "Usa esta aplicación de escritorio para encriptar tus archivos antes de que toquen internet."),
            ft.Container(height=5),
            PasoExplicativo(ft.Icons.SHARE_OUTLINED, "2. Comparte la llave", "NoxSend te dará un enlace y una llave privada. Pásaselos a tu contacto por un chat seguro."),
            ft.Container(height=5),
            PasoExplicativo(ft.Icons.WEB_ASSET, "3. El receptor lo abre en la Web", "Tu contacto no necesita instalar nada. Abre el enlace en la web, pone la llave y lo descarga.")
        ], spacing=10)
    )

    # --- Ensamblaje de la vista ---
    return ft.View(
        "/login",
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
                        
                        ft.Text("Envía tus archivos bajo llave.", size=38, weight="black", color="white", style=ft.TextStyle(height=1.1)),
                        ft.Container(height=10),
                        ft.Text("Tus fotos y documentos se bloquean en tu ordenador antes de salir. Nadie, ni siquiera nosotros, podrá verlos.", size=16, color="white", width=500), # Cambiado a blanco puro
                        ft.Container(height=30),
                        
                        panel_explicativo, 
                        
                        ft.Container(expand=True),
                    ], horizontal_alignment="start"),
                ),

                # --- PANEL DERECHO ---
                ft.Container(
                    expand=4,
                    bgcolor=BG_PANEL,
                    padding=ft.padding.symmetric(horizontal=50, vertical=40),
                    content=ft.Column([
                        ft.Row([
                            ft.Text("TU ESPACIO SEGURO", size=11, weight="black", color=TEXT_MUTED, style=ft.TextStyle(letter_spacing=2)),
                            ft.Row([
                                ft.Icon(ft.Icons.CIRCLE, color="green400", size=10),
                                ft.Text("Sistema en línea", size=10, color=TEXT_MUTED, weight="bold")
                            ])
                        ], alignment="spaceBetween"),
                        ft.Divider(height=40, color=BORDER_COLOR),
                        
                        ft.Container(
                            expand=True, 
                            alignment=ft.alignment.center, 
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.WAVING_HAND, color=ACCENT, size=40),
                                    padding=15, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=20, margin=ft.margin.only(bottom=10)
                                ),
                                ft.Text("¡Hola de nuevo!", size=26, weight="black", color="white"),
                                ft.Text("Pon tus datos para entrar", size=14, color=TEXT_MUTED),
                                ft.Container(height=25),
                                
                                input_email, 
                                input_pass,
                                
                                ft.Container(
                                    width=340, 
                                    alignment=ft.alignment.center_right,
                                    content=ft.TextButton("¿Has olvidado tu contraseña?", style=ft.ButtonStyle(color=TEXT_MUTED, padding=0))
                                ),
                                
                                ft.Container(height=15),
                                boton_login,
                                ft.Container(height=5),
                                cargando,
                            ], horizontal_alignment="center", spacing=5)
                        ),
                        
                        ft.Column([
                            ft.Divider(height=30, color=BORDER_COLOR),
                            ft.Row([
                                ft.Text("¿Todavía no tienes cuenta?", color=TEXT_MUTED, size=13),
                                ft.TextButton(
                                    "Regístrate gratis", 
                                    icon=ft.Icons.ARROW_FORWARD_ROUNDED, 
                                    icon_color=ACCENT, 
                                    style=ft.ButtonStyle(color=ACCENT, overlay_color=ft.Colors.with_opacity(0.1, ACCENT)), 
                                    on_click=lambda _: page.go("/register")
                                )
                            ], alignment="center", spacing=5),
                            ft.Container(height=10),
                            ft.Text("NoxSend © 2026", size=11, color=ft.Colors.with_opacity(0.3, "white"), text_align="center")
                        ], horizontal_alignment="center", spacing=0)
                        
                    ], alignment="spaceBetween") 
                )
            ], expand=True, spacing=0)
        ]
    )