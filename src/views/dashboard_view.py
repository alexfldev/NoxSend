import flet as ft
import os
import shutil
from src.controllers.app_controller import AppController

def DashboardView(page: ft.Page):
    # FORZAMOS EL MODO OSCURO GLOBAL
    page.theme_mode = ft.ThemeMode.DARK 
    page.update()

    controlador = AppController()
    ruta_seleccionada = [None]

    # --- CONFIGURACIÓN DE LÍMITES Y URL ---
    LIMITE_GB = 1
    LIMITE_BYTES = LIMITE_GB * 1024 * 1024 * 1024 
    WEB_URL = "https://www.noxsend.com" 

    # --- PALETA "ESTILO PS5" ---
    BG_ROOT = "#0b0e14"
    BG_PANEL = "#121620"
    BG_CARD = "#1a1f2e"
    ACCENT = "#5c3cfa" 
    ACCENT_GLOW = "#3a86ff" 
    TEXT_MUTED = "grey500"
    BORDER_COLOR = ft.Colors.with_opacity(0.15, "white")
    BORDER_GLOW = ft.Colors.with_opacity(0.3, ACCENT_GLOW)

    txt_archivos_protegidos = ft.Text("0", size=24, weight="black", color="white")
    txt_espacio_libre = ft.Text("0 GB", size=24, weight="black", color="white")
    
    # LA SOLUCIÓN: Definimos el título aquí arriba para que todas las funciones lo vean
    header_title = ft.Text("PANEL PRINCIPAL", size=13, weight="black", color="white")

    def copiar(texto, msg):
        page.set_clipboard(texto)
        page.overlay.append(ft.SnackBar(ft.Text(f"{msg} copiado al portapapeles"), bgcolor=ACCENT, open=True))
        page.update()

    def cambiar_pestana(e):
        view_home.visible = False
        view_transfer.visible = False
        view_vault.visible = False
        
        for btn in sidebar_menu.controls:
            if isinstance(btn, ft.IconButton):
                btn.icon_color = "grey600"
                btn.bgcolor = ft.Colors.TRANSPARENT
            
        e.control.icon_color = "white"
        e.control.bgcolor = ft.Colors.with_opacity(0.1, "white")
        
        if e.control.data == "home": view_home.visible = True
        elif e.control.data == "transfer": view_transfer.visible = True
        elif e.control.data == "vault": view_vault.visible = True
        
        header_title.value = e.control.tooltip.upper()
        page.update()

    # Función para saltar directo a NoxDrive desde el botón del Home
    def ir_a_transferencia(e):
        view_home.visible = False
        view_transfer.visible = True
        view_vault.visible = False
        
        for btn in sidebar_menu.controls:
            if isinstance(btn, ft.IconButton):
                btn.icon_color = "grey600"
                btn.bgcolor = ft.Colors.TRANSPARENT
        
        sidebar_menu.controls[1].icon_color = "white"
        sidebar_menu.controls[1].bgcolor = ft.Colors.with_opacity(0.1, "white")
        header_title.value = "NOXDRIVE (BLINDAJE)"
        page.update()

    def SidebarIcon(icon, tab_name, tooltip, is_active=False, is_pro=False):
        return ft.IconButton(
            icon=icon, icon_size=22, icon_color="white" if is_active else "grey600",
            bgcolor=ft.Colors.with_opacity(0.1, "white") if is_active else ft.Colors.TRANSPARENT,
            tooltip=tooltip + (" (Próximamente)" if is_pro else ""), data=tab_name, 
            on_click=cambiar_pestana if not is_pro else lambda _: None,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=14)), width=50, height=50, disabled=is_pro
        )

    sidebar_menu = ft.Column([
        SidebarIcon(ft.Icons.SPACE_DASHBOARD_ROUNDED, "home", "Panel Principal", True),
        SidebarIcon(ft.Icons.SHIELD_ROUNDED, "transfer", "NoxDrive (Blindaje)"),
        SidebarIcon(ft.Icons.STORAGE_ROUNDED, "vault", "Mi Bóveda"),
        ft.Divider(height=20, color=BORDER_COLOR),
        SidebarIcon(ft.Icons.MAIL_ROUNDED, "mail", "NoxMail", is_pro=True),
        SidebarIcon(ft.Icons.PASSWORD_ROUNDED, "pass", "NoxPass", is_pro=True),
    ], spacing=10, horizontal_alignment="center")

    sidebar = ft.Container(
        width=85, bgcolor=BG_ROOT, border=ft.border.only(right=ft.border.BorderSide(1, BORDER_COLOR)),
        padding=ft.padding.symmetric(vertical=25),
        content=ft.Column([
            ft.Container(content=ft.Icon(ft.Icons.SECURITY, color=ACCENT, size=32), padding=10),
            ft.Container(height=10), sidebar_menu, ft.Container(expand=True),
            ft.Container(content=ft.Text("AF", weight="bold", color="white", size=12), bgcolor=ACCENT, width=40, height=40, border_radius=12, alignment=ft.alignment.center, margin=ft.margin.only(top=10))
        ], horizontal_alignment="center")
    )

    def TutorialStep(numero, titulo, desc):
        return ft.Row([
            ft.Container(content=ft.Text(numero, weight="black", color=ACCENT), width=30, height=30, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=8, alignment=ft.alignment.center),
            ft.Column([ft.Text(titulo, weight="bold", color="white", size=14), ft.Text(desc, color=TEXT_MUTED, size=12)], spacing=2)
        ], alignment="start")

    # --- VISTA 1: HOME ---
    view_home = ft.Container(
        visible=True, expand=True, padding=40, alignment=ft.alignment.top_center,
        content=ft.Container(
            width=1100, 
            content=ft.Column([
                ft.Container(
                    bgcolor=ACCENT, border_radius=24, padding=40,
                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ACCENT_GLOW, ACCENT]),
                    content=ft.Row([
                        ft.Column([
                            ft.Text("Bienvenido a NoxSend Workspace", size=28, weight="black", color="white"),
                            ft.Text("Tu suite de privacidad y cifrado Zero-Knowledge.", color="white70", size=14),
                            ft.Container(height=10),
                            ft.ElevatedButton("Blindar mi primer archivo", icon=ft.Icons.SHIELD, color="black", bgcolor="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=ir_a_transferencia)
                        ]),
                        ft.Icon(ft.Icons.VERIFIED_USER, size=100, color="white24")
                    ], alignment="spaceBetween")
                ),
                ft.Container(height=30),
                ft.Row([
                    ft.Column([
                        ft.Text("Métricas de Seguridad", size=18, weight="bold", color="white"),
                        ft.Row([
                            ft.Container(content=ft.Column([ft.Icon(ft.Icons.STORAGE, color=ACCENT_GLOW), ft.Text("Espacio Libre PC", color=TEXT_MUTED, size=12), txt_espacio_libre]), bgcolor=BG_CARD, padding=25, border_radius=20, border=ft.border.all(1, BORDER_COLOR), expand=1),
                            ft.Container(content=ft.Column([ft.Icon(ft.Icons.SHIELD, color=ACCENT), ft.Text("Archivos Protegidos", color=TEXT_MUTED, size=12), txt_archivos_protegidos]), bgcolor=BG_CARD, padding=25, border_radius=20, border=ft.border.all(1, BORDER_COLOR), expand=1),
                        ]),
                    ], expand=2),
                    ft.Column([
                        ft.Text("¿Cómo funciona NoxSend?", size=18, weight="bold", color="white"),
                        ft.Container(
                            bgcolor=BG_CARD, padding=25, border_radius=20, border=ft.border.all(1, BORDER_COLOR), expand=1,
                            content=ft.Column([
                                TutorialStep("1", "Blindaje Local", "Tu PC lo encripta en NoxDrive."),
                                TutorialStep("2", "Dile a tu contacto", f"Que entre en {WEB_URL}"),
                                TutorialStep("3", "Pásale la Llave", "Le pedirá el ID y la Llave para abrirlo.")
                            ], spacing=20)
                        )
                    ], expand=1)
                ], spacing=30)
            ], scroll="auto") 
        )
    )

    # --- VISTA 2: TRANSFERENCIA ---
    banner_explicativo_transfer = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.1, ACCENT), 
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, ACCENT)), 
        border_radius=16, 
        padding=20,
        margin=ft.margin.only(top=10, bottom=25),
        content=ft.Row([
            ft.Container(content=ft.Icon(ft.Icons.HELP_OUTLINE, color=ACCENT_GLOW, size=28), padding=ft.padding.only(right=10)),
            ft.Column([
                ft.Text("Guía rápida de envío seguro:", weight="bold", color="white", size=15),
                ft.Text("1. Selecciona tu archivo confidencial y elige el tiempo de autodestrucción (Ej: 24 Horas).", color="white70", size=13),
                ft.Text("2. Al pulsar 'Blindar', tu ordenador lo encriptará y te devolverá un ID público y una Llave secreta.", color="white70", size=13),
                ft.Text(f"3. Pásale a tu contacto el ID, la Llave y el enlace ({WEB_URL}). Ellos lo desencriptarán allí.", color="white70", size=13)
            ], spacing=4, expand=True)
        ], vertical_alignment="start")
    )

    icon_status = ft.Icon(ft.Icons.SHIELD_OUTLINED, color=ACCENT_GLOW, size=50)
    text_status = ft.Text("Selecciona tu archivo confidencial", size=16, weight="bold", color="white")
    subtext_status = ft.Text(f"Máximo {LIMITE_GB} GB por envío", size=12, color=TEXT_MUTED)

    icono_archivo = ft.Icon(ft.Icons.INSERT_DRIVE_FILE_OUTLINED, color="white", size=30)
    texto_nombre_archivo = ft.Text("", size=14, weight="bold", color="white", width=250, no_wrap=True)
    texto_peso_archivo = ft.Text("", size=11, color=TEXT_MUTED)
    
    tarjeta_archivo_vista = ft.Container(
        visible=False, bgcolor=ft.Colors.with_opacity(0.05, "white"), border_radius=12, padding=15,
        border=ft.border.all(1, ft.Colors.with_opacity(0.1, "white")),
        content=ft.Row([
            ft.Container(content=icono_archivo, bgcolor=ft.Colors.with_opacity(0.2, ACCENT), padding=10, border_radius=8),
            ft.Column([texto_nombre_archivo, texto_peso_archivo], spacing=2, expand=True),
            ft.Icon(ft.Icons.CHECK_CIRCLE, color="green400", size=20)
        ], alignment="spaceBetween", vertical_alignment="center")
    )

    drop_zone = ft.Container(
        content=ft.Column([
            ft.Container(content=icon_status, padding=20, border_radius=50, bgcolor=ft.Colors.with_opacity(0.1, ACCENT_GLOW)),
            text_status, subtext_status
        ], alignment="center", horizontal_alignment="center", spacing=10),
        height=220, expand=True, bgcolor=ft.Colors.with_opacity(0.3, BG_ROOT), 
        border=ft.border.all(2, BORDER_GLOW), border_radius=24, alignment=ft.alignment.center
    )

    cargando = ft.ProgressRing(visible=False, width=30, height=30, color=ACCENT)
    texto_id = ft.TextField(label="ID SEGUIMIENTO (Público)", read_only=True, border_radius=12, text_size=12, color="white", bgcolor=BG_ROOT)
    texto_llave = ft.TextField(label="LLAVE MAESTRA (Privada)", read_only=True, password=True, can_reveal_password=True, border_radius=12, color="green400", bgcolor=BG_ROOT)
    texto_codigo_cifrado = ft.Text("", font_family="Courier", color="green400", size=11, selectable=True)
    
    opciones_tiempo = ft.Dropdown(
        width=300, border_color=BORDER_COLOR, border_radius=12,
        options=[
            ft.dropdown.Option("1", "1 Hora"),
            ft.dropdown.Option("24", "24 Horas"),
            ft.dropdown.Option("168", "7 Días"),
        ],
        value="24", text_size=13
    )

    def cerrar_auditoria(e):
        page.close(dialogo_prueba)
        page.update()

    dialogo_prueba = ft.AlertDialog(
        modal=False, title=ft.Row([ft.Icon(ft.Icons.TERMINAL, color="green400"), ft.Text("Auditoría de Carga Útil", weight="bold", color="white")]),
        content=ft.Container(width=550, height=250, bgcolor="black", padding=15, border_radius=10, border=ft.border.all(1, ft.Colors.with_opacity(0.3, "green400")), content=ft.Column([ft.Text("Esto es exactamente lo único que recibe el servidor.", color="white70", size=12), ft.Divider(color="white24"), ft.Container(content=texto_codigo_cifrado, expand=True)], scroll="auto")),
        actions=[ft.TextButton("Cerrar", on_click=cerrar_auditoria, style=ft.ButtonStyle(color=TEXT_MUTED))], bgcolor=BG_CARD
    )

    def abrir_prueba_cifrado(e):
        page.open(dialogo_prueba)
        page.update()

    boton_prueba_cifrado = ft.ElevatedButton("Auditoría: Ver Carga Cifrada", icon=ft.Icons.SHIELD_MOON, bgcolor=ft.Colors.with_opacity(0.1, "white"), color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=abrir_prueba_cifrado)

    panel_resultados = ft.Container(
        visible=False, padding=25, border_radius=24, bgcolor=ft.Colors.with_opacity(0.05, ACCENT), border=ft.border.all(1, ft.Colors.with_opacity(0.3, ACCENT)),
        content=ft.Column([
            ft.Text("¡BLINDAJE COMPLETADO!", weight="black", size=14, color=ACCENT_GLOW),
            ft.Row([texto_id, ft.IconButton(ft.Icons.COPY, icon_color=ACCENT_GLOW, on_click=lambda _: copiar(texto_id.value, "ID"))], alignment="center"),
            ft.Row([texto_llave, ft.IconButton(ft.Icons.COPY, icon_color=ACCENT_GLOW, on_click=lambda _: copiar(texto_llave.value, "Llave"))], alignment="center"),
            
            ft.Container(
                bgcolor=ft.Colors.with_opacity(0.1, "white"), border_radius=10, padding=15, margin=ft.margin.only(top=10, bottom=10),
                content=ft.Column([
                    ft.Text("Dile a tu contacto que abra esta web:", color="white70", size=12, text_align="center"),
                    ft.Row([
                        ft.Icon(ft.Icons.LANGUAGE, color="white54", size=16),
                        ft.Text(WEB_URL, color="white", weight="bold", selectable=True),
                        ft.IconButton(ft.Icons.COPY, icon_size=16, icon_color="white54", on_click=lambda _: copiar(WEB_URL, "Enlace web"))
                    ], alignment="center")
                ], horizontal_alignment="center")
            ),
            
            boton_prueba_cifrado 
        ], horizontal_alignment="center", spacing=10)
    )

    def al_seleccionar(e):
        if e.files:
            ruta = e.files[0].path
            ruta_seleccionada[0] = ruta
            try:
                peso_bytes = os.path.getsize(ruta)
                peso_mb = peso_bytes / (1024 * 1024)
                
                texto_nombre_archivo.value = e.files[0].name
                texto_peso_archivo.value = f"{peso_mb:.2f} MB"
                
                if peso_bytes > LIMITE_BYTES:
                    tarjeta_archivo_vista.border = ft.border.all(1, "red400")
                    icono_archivo.color = "red400"
                    texto_peso_archivo.value += f" (Supera límite de {LIMITE_GB} GB)"
                    boton_enviar.disabled = True
                else:
                    tarjeta_archivo_vista.border = ft.border.all(1, ACCENT)
                    icono_archivo.color = ACCENT_GLOW
                    boton_enviar.disabled = False
                
                drop_zone.visible = False
                tarjeta_archivo_vista.visible = True
            except:
                texto_nombre_archivo.value = "Error al leer archivo"
                boton_enviar.disabled = True
            page.update()

    def ejecutar_envio(e):
        if not ruta_seleccionada[0]: return
        boton_enviar.disabled = True
        cargando.visible = True
        page.update()
        
        horas = int(opciones_tiempo.value)
        res = controlador.enviar_archivo(ruta_seleccionada[0], horas)
        
        cargando.visible = False
        
        if res:
            id_arc, key, muestra_cifrada = res 
            texto_id.value = id_arc
            texto_llave.value = key
            texto_codigo_cifrado.value = muestra_cifrada 
            
            panel_resultados.visible = True
            sincronizar_datos_reales() 
        page.update()

    selector = ft.FilePicker(on_result=al_seleccionar)
    page.overlay.append(selector)

    boton_seleccionar = ft.ElevatedButton("Examinar mi Equipo", icon=ft.Icons.FOLDER_OPEN, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=ft.Colors.with_opacity(0.1, "white"), color="white"), on_click=lambda _: selector.pick_files())
    boton_enviar = ft.ElevatedButton("Blindar y Enviar Enlace Seguro", icon=ft.Icons.SHIELD, disabled=True, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=ACCENT, color="white", padding=20), on_click=ejecutar_envio, expand=True)

    tarjeta_paso1 = ft.Container(
        bgcolor=BG_CARD, padding=35, border_radius=24, border=ft.border.all(1, BORDER_GLOW), expand=5,
        content=ft.Column([
            ft.Text("Paso 1: Añadir Archivo", size=20, weight="bold", color="white"),
            ft.Text("Sube y blinda archivos confidenciales. Nada sale de tu dispositivo sin cifrar.", color=TEXT_MUTED, size=13),
            ft.Container(height=20),
            drop_zone,
            tarjeta_archivo_vista,
            ft.Container(height=10),
            ft.Row([boton_seleccionar], alignment="center")
        ], horizontal_alignment="center")
    )

    tarjeta_paso2 = ft.Container(
        bgcolor=BG_CARD, padding=35, border_radius=24, border=ft.border.all(1, BORDER_COLOR), expand=5,
        content=ft.Column([
            ft.Text("Paso 2: Configuración y Envío", size=20, weight="bold", color="white"),
            ft.Container(height=20),
            
            ft.Container(
                padding=20, border_radius=16, border=ft.border.all(1, BORDER_COLOR), bgcolor=ft.Colors.with_opacity(0.2, BG_ROOT),
                content=ft.Column([
                    ft.Text("Tiempo de Vida (Autodestrucción)", weight="bold", size=13, color="white"),
                    ft.Row([ft.Icon(ft.Icons.TIMER_OUTLINED, color=ACCENT_GLOW), opciones_tiempo], alignment="start")
                ])
            ),
            ft.Container(height=10),
            
            ft.Container(
                padding=15, border_radius=12, bgcolor=ft.Colors.with_opacity(0.1, "amber"),
                content=ft.Row([
                    ft.Icon(ft.Icons.LOCK, color="amber", size=20),
                    ft.Text("Cifrado Zero-Knowledge activado. NoxSend nunca tiene acceso a la llave.", color="amber", size=11, expand=True)
                ], vertical_alignment="center")
            ),
            ft.Container(height=20),
            
            ft.Row([boton_enviar], alignment="center"),
            ft.Row([cargando], alignment="center"),
            panel_resultados
        ])
    )

    view_transfer = ft.Container(
        visible=False, expand=True, padding=40, alignment=ft.alignment.top_center,
        content=ft.Container(
            width=1100,
            content=ft.Column([
                ft.Text("NoxDrive (Módulo de Blindaje)", size=28, weight="black", color="white"),
                banner_explicativo_transfer, 
                ft.Row([tarjeta_paso1, tarjeta_paso2], alignment="start", vertical_alignment="start", spacing=30) 
            ], scroll="auto") 
        )
    )

    # --- VISTA 3: BÓVEDA ---
    banner_explicativo = ft.Container(
        bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border=ft.border.all(1, ft.Colors.with_opacity(0.3, ACCENT)), border_radius=16, padding=25,
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_OUTLINE, color=ACCENT_GLOW, size=32),
            ft.Column([
                ft.Text("¿Para qué sirve tu Bóveda Local?", weight="bold", color="white", size=16),
                ft.Text("Es tu historial privado. NoxSend NO guarda las llaves maestras por seguridad (Zero-Knowledge). Aquí puedes consultar qué ID corresponde a cada archivo que enviaste. Si pulsas 'Vaciar Bóveda', destruirás este historial garantizando que no quede rastro en tu ordenador (Anti-forense).", color="white70", size=13, width=800)
            ], spacing=4)
        ], vertical_alignment="start")
    )

    estado_vacio = ft.Container(
        visible=False, padding=60, alignment=ft.alignment.center,
        content=ft.Column([
            ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, size=60, color="white24"),
            ft.Text("Tu Bóveda está vacía", size=18, weight="bold", color="white54"),
            ft.Text("Los archivos que blindes aparecerán aquí como registro.", size=13, color=TEXT_MUTED)
        ], horizontal_alignment="center", spacing=10)
    )

    tabla_historial = ft.DataTable(
        border_radius=15, heading_row_color=ft.Colors.with_opacity(0.05, "white"),
        columns=[
            ft.DataColumn(ft.Text("NOMBRE DEL ARCHIVO ORIGINAL", size=11, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("ID PÚBLICO (NUBE)", size=11, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("FECHA DE ENVÍO", size=11, weight="bold", color=TEXT_MUTED)),
        ], rows=[]
    )

    def vaciar_boveda_click(e):
        controlador.vaciar_boveda() 
        sincronizar_datos_reales()
        page.overlay.append(ft.SnackBar(ft.Text("Historial local destruido. Rastro eliminado."), bgcolor="red", open=True))
        page.update()

    boton_vaciar_boveda = ft.ElevatedButton("Vaciar Bóveda (Anti-Forense)", icon=ft.Icons.DELETE_FOREVER, bgcolor=ft.Colors.RED_700, color="white", on_click=vaciar_boveda_click)

    def sincronizar_datos_reales():
        boveda = controlador.obtener_boveda()
        tabla_historial.rows.clear()
        
        if not boveda or len(boveda) == 0:
            tabla_historial.visible = False
            estado_vacio.visible = True
        else:
            tabla_historial.visible = True
            estado_vacio.visible = False
            for reg in boveda:
                tabla_historial.rows.append(ft.DataRow(cells=[
                    ft.DataCell(ft.Text(reg[1], weight="bold", color="white")), 
                    ft.DataCell(ft.Row([ft.Icon(ft.Icons.CLOUD_DONE_OUTLINED, size=14, color=ACCENT_GLOW), ft.Text(reg[0][:15] + "...", color=ACCENT_GLOW)])), 
                    ft.DataCell(ft.Text(reg[2], size=12, color=TEXT_MUTED))
                ]))
                
        txt_archivos_protegidos.value = str(len(boveda))
        try:
            total, used, free = shutil.disk_usage(os.getcwd())
            txt_espacio_libre.value = f"{free / (1024 ** 3):.1f} GB"
        except:
            txt_espacio_libre.value = "-- GB"
        try: page.update()
        except: pass

    view_vault = ft.Container(
        visible=False, expand=True, padding=40, alignment=ft.alignment.top_center,
        content=ft.Container(
            width=1100,
            content=ft.Column([
                ft.Row([
                    ft.Column([ft.Text("Mi Bóveda", size=28, weight="black", color="white"), ft.Text("Auditoría local de privacidad.", color=TEXT_MUTED, size=14)], expand=True),
                    boton_vaciar_boveda 
                ], alignment="spaceBetween"),
                ft.Container(height=20),
                banner_explicativo,
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column([estado_vacio, tabla_historial], scroll="auto", horizontal_alignment="center"), 
                    bgcolor=BG_CARD, padding=25, border_radius=24, border=ft.border.all(1, BORDER_COLOR), expand=True, alignment=ft.alignment.top_center
                )
            ])
        )
    )
    
    sincronizar_datos_reales()

    return ft.View(
        "/dashboard", padding=0, bgcolor=BG_PANEL,
        controls=[
            ft.Row([
                sidebar,
                ft.Container(expand=True, content=ft.Column([
                    ft.Container(padding=ft.padding.symmetric(horizontal=40, vertical=20), border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER_COLOR)), content=ft.Row([header_title, ft.Row([ft.Icon(ft.Icons.FINGERPRINT, color=ACCENT_GLOW, size=16), ft.Text("Conexión Cifrada", size=12, weight="bold", color=TEXT_MUTED)])], alignment="spaceBetween")),
                    ft.Stack([view_home, view_transfer, view_vault], expand=True)
                ]))
            ], expand=True, spacing=0)
        ]
    )