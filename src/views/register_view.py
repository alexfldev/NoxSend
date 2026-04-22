import flet as ft
from src.controllers.app_controller import AppController

def RegisterView(page: ft.Page):
    controlador = AppController()

    # --- Paleta de colores ---
    BG_ROOT = "#06080a"      
    BG_PANEL = "#0f1115"     
    ACCENT = "#3b82f6"       
    TEXT_MUTED = "grey500"   
    BORDER_COLOR = ft.Colors.with_opacity(0.1, "white")

    # --- Lógica de Registro ---
    def realizar_registro(e):
        if not input_email.value or not input_pass.value or not input_confirm.value:
            page.overlay.append(ft.SnackBar(ft.Text("Vaya, parece que te has dejado algún campo sin rellenar."), bgcolor="orange", open=True))
            page.update()
            return
            
        if input_pass.value != input_confirm.value:
            page.overlay.append(ft.SnackBar(ft.Text("Las contraseñas no coinciden. Dales un repaso rápido."), bgcolor="red", open=True))
            page.update()
            return

        boton_registro_btn.disabled = True
        cargando.visible = True
        page.update()

        exito, msg = controlador.registrar_usuario(input_email.value, input_pass.value)
        
        cargando.visible = False
        if exito:
            page.overlay.append(ft.SnackBar(ft.Text("¡Todo listo! Tu cuenta privada ya está creada. Ya puedes entrar."), bgcolor="green", open=True))
            page.go("/login") 
        else:
            page.overlay.append(ft.SnackBar(ft.Text(f"Hubo un problema: {msg}"), bgcolor="red", open=True))
            boton_registro_btn.disabled = False
        page.update()

    # --- Componentes del formulario ---
    input_email = ft.TextField(
        label="Tu correo electrónico", width=380, border_radius=12, text_size=15, height=60,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.EMAIL_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" 
    )
    
    input_pass = ft.TextField(
        label="Invéntate una contraseña segura", password=True, can_reveal_password=True, width=380, border_radius=12, text_size=15, height=60,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.LOCK_OUTLINED,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" 
    )

    input_confirm = ft.TextField(
        label="Escríbela de nuevo para confirmarla", password=True, can_reveal_password=True, width=380, border_radius=12, text_size=15, height=60,
        bgcolor=BG_ROOT, border_color=BORDER_COLOR, prefix_icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        focused_border_color=ACCENT, cursor_color=ACCENT, color="white" 
    )
    
    cargando = ft.ProgressRing(visible=False, width=24, height=24, color=ACCENT, stroke_width=3)
    
    boton_registro_btn = ft.ElevatedButton(
        "Crear mi cuenta gratis", icon=ft.Icons.ROCKET_LAUNCH, width=380, height=55, 
        bgcolor=ACCENT, color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12)),
        on_click=realizar_registro
    )

    boton_registro = ft.Container(
        content=boton_registro_btn,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=20, color=ft.Colors.with_opacity(0.3, ACCENT)) 
    )

    # --- NUEVO: Panel Explicativo (Corregido) ---
    def PasoExplicativo(icono, titulo, descripcion):
        return ft.Row([
            ft.Container(
                content=ft.Icon(icono, color=ACCENT, size=24),
                bgcolor=ft.Colors.with_opacity(0.1, ACCENT),
                padding=12, border_radius=12
            ),
            ft.Column([
                ft.Text(titulo, weight="bold", color="white", size=14),
                ft.Text(descripcion, color=TEXT_MUTED, size=12, width=320)
            ], spacing=2)
        ], alignment="start", vertical_alignment="center")

    panel_explicativo = ft.Container(
        width=550,
        bgcolor=ft.Colors.with_opacity(0.05, "white"), 
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, "white")),
        border_radius=16,
        padding=30,
        content=ft.Column([
            ft.Text("¿Cómo vas a enviar archivos con NoxSend?", size=18, weight="bold", color="white"),
            ft.Container(height=15), # <-- Esta es la corrección
            PasoExplicativo(ft.Icons.LOCK_OUTLINE, "1. Blíndalos aquí", "Usa esta aplicación de escritorio para encriptar tus archivos antes de que toquen internet."),
            ft.Container(height=5),
            PasoExplicativo(ft.Icons.SHARE_OUTLINED, "2. Comparte la llave", "NoxSend te dará un enlace y una llave privada. Pásaselos a tu contacto por un chat seguro."),
            ft.Container(height=5),
            PasoExplicativo(ft.Icons.WEB_ASSET, "3. El receptor lo abre en la Web", "Tu contacto no necesita instalar nada. Abre el enlace en la web, pone la llave y lo descarga.")
        ], spacing=10)
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
                        
                        ft.Text("Tu privacidad, de vuelta a tus manos.", size=38, weight="black", color="white", style=ft.TextStyle(height=1.1)),
                        ft.Container(height=10),
                        ft.Text("Regístrate en menos de un minuto. Todo el blindaje de seguridad ocurre en tu ordenador, nosotros no nos guardamos ni un solo dato.", size=16, color="white70", width=500),
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
                        ft.Divider(height=20, color=BORDER_COLOR),
                        
                        ft.Container(
                            expand=True, 
                            alignment=ft.alignment.center, 
                            content=ft.Column([
                                ft.Container(
                                    content=ft.Icon(ft.Icons.PERSON_ADD_ALT_1_ROUNDED, color=ACCENT, size=40),
                                    padding=15, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=24, margin=ft.margin.only(bottom=5)
                                ),
                                ft.Text("Nuevo usuario", size=26, weight="black", color="white"),
                                ft.Text("Rellena estos datos para empezar a usar NoxSend", size=14, color=TEXT_MUTED),
                                ft.Container(height=15),
                                
                                input_email, 
                                input_pass,
                                input_confirm,
                                
                                ft.Container(
                                    width=380, 
                                    padding=ft.padding.only(top=5),
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.LIGHTBULB_OUTLINED, color=ft.Colors.AMBER_400, size=16), 
                                        ft.Text("Apunta bien tu contraseña, nosotros no podemos verla ni recuperarla.", color=ft.Colors.AMBER_400, size=12) 
                                    ], alignment="center")
                                ),
                                
                                ft.Container(height=10),
                                boton_registro,
                                ft.Container(height=5),
                                cargando,
                            ], horizontal_alignment="center", spacing=5)
                        ),
                        
                        ft.Column([
                            ft.Divider(height=20, color=BORDER_COLOR),
                            ft.Row([
                                ft.Text("¿Ya tienes una cuenta?", color=TEXT_MUTED, size=13),
                                ft.TextButton(
                                    "Entrar ahora", 
                                    icon=ft.Icons.LOGIN, 
                                    icon_color=ACCENT, 
                                    style=ft.ButtonStyle(color=ACCENT, overlay_color=ft.Colors.with_opacity(0.1, ACCENT)), 
                                    on_click=lambda _: page.go("/login")
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