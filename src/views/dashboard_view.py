import flet as ft
import os
import shutil
from src.controllers.app_controller import AppController

def DashboardView(page: ft.Page):
    controlador = AppController()
    ruta_seleccionada = [None]

    # --- CONFIGURACIÓN DE LÍMITES ---
    LIMITE_GB = 1
    LIMITE_BYTES = LIMITE_GB * 1024 * 1024 * 1024 

    # --- PALETA PROTON ---
    BG_ROOT = "#0f1115"
    BG_PANEL = "#16191f"
    BG_CARD = "#1c2028"
    ACCENT = "#6d4aff"
    TEXT_MUTED = "grey500"
    BORDER_COLOR = ft.Colors.with_opacity(0.1, "white")

    txt_archivos_protegidos = ft.Text("0", size=24, weight="black", color="white")
    txt_espacio_libre = ft.Text("0 GB", size=24, weight="black", color="white")

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

    def TutorialStepModal(icono, titulo, desc):
        return ft.Row([
            ft.Container(content=ft.Icon(icono, color=ACCENT, size=24), bgcolor=ft.Colors.with_opacity(0.1, ACCENT), padding=12, border_radius=12),
            ft.Column([
                ft.Text(titulo, weight="bold", color="white", size=14),
                ft.Text(desc, color=TEXT_MUTED, size=12, width=380) 
            ], spacing=2)
        ], alignment="start", vertical_alignment="center")

    def cerrar_tutorial(e):
        page.close(dialogo_tutorial)
        page.update()

    dialogo_tutorial = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.Icons.MENU_BOOK, color=ACCENT), ft.Text("Guía de Seguridad NoxSend", weight="black", color="white")], alignment="start"),
        content=ft.Container(
            width=500,
            content=ft.Column([
                ft.Text("Así es como garantizamos la privacidad Zero-Knowledge:", color=TEXT_MUTED, size=13),
                ft.Divider(height=20, color=BORDER_COLOR),
                TutorialStepModal(ft.Icons.LOCK, "1. Cifrado Local", "Todo ocurre en tu dispositivo. Usamos AES-256-GCM."),
                TutorialStepModal(ft.Icons.CLOUD_UPLOAD, "2. Subida Segura", "El archivo blindado se sube a nuestra nube. Solo es ruido."),
                TutorialStepModal(ft.Icons.VPN_KEY, "3. La Llave Maestra", "El sistema genera una llave que NUNCA se envía."),
                TutorialStepModal(ft.Icons.SHARE, "4. Compartir", "Pásale el ID y la Llave al destinatario por otro canal.")
            ], tight=True, spacing=15)
        ),
        actions=[
            ft.ElevatedButton("Empezar a Blindar", bgcolor=ACCENT, color="white", on_click=cerrar_tutorial, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        bgcolor=BG_CARD,
        shape=ft.RoundedRectangleBorder(radius=20)
    )

    def show_tutorial(e):
        page.open(dialogo_tutorial)

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
            ft.IconButton(icon=ft.Icons.HELP_OUTLINE, icon_color="grey500", tooltip="Centro de Ayuda", on_click=show_tutorial),
            ft.Container(content=ft.Text("AF", weight="bold", color="white", size=12), bgcolor=ACCENT, width=40, height=40, border_radius=12, alignment=ft.alignment.center, margin=ft.margin.only(top=10))
        ], horizontal_alignment="center")
    )

    def TutorialStep(numero, titulo, desc):
        return ft.Row([
            ft.Container(content=ft.Text(numero, weight="black", color=ACCENT), width=30, height=30, bgcolor=ft.Colors.with_opacity(0.1, ACCENT), border_radius=8, alignment=ft.alignment.center),
            ft.Column([ft.Text(titulo, weight="bold", color="white", size=14), ft.Text(desc, color=TEXT_MUTED, size=12)], spacing=2)
        ], alignment="start")

    view_home = ft.Container(
        visible=True, expand=True, padding=40, alignment=ft.alignment.top_center,
        content=ft.Container(
            width=1100, 
            content=ft.Column([
                ft.Container(
                    bgcolor=ACCENT, border_radius=24, padding=40,
                    gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=[ACCENT, "#4328b7"]),
                    content=ft.Row([
                        ft.Column([
                            ft.Text("Bienvenido a NoxSend Workspace", size=28, weight="black", color="white"),
                            ft.Text("Tu suite de privacidad y cifrado Zero-Knowledge.", color="white70", size=14),
                            ft.Container(height=10),
                            ft.ElevatedButton("Ver el Tutorial", icon=ft.Icons.PLAY_ARROW, color="black", bgcolor="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=show_tutorial)
                        ]),
                        ft.Icon(ft.Icons.VERIFIED_USER, size=100, color="white24")
                    ], alignment="spaceBetween")
                ),
                ft.Container(height=30),
                ft.Row([
                    ft.Column([
                        ft.Text("Métricas de Seguridad", size=18, weight="bold", color="white"),
                        ft.Row([
                            ft.Container(content=ft.Column([ft.Icon(ft.Icons.STORAGE, color=ACCENT), ft.Text("Espacio Libre PC", color=TEXT_MUTED, size=12), txt_espacio_libre]), bgcolor=BG_CARD, padding=25, border_radius=20, border=ft.border.all(1, BORDER_COLOR), expand=1),
                            ft.Container(content=ft.Column([ft.Icon(ft.Icons.SHIELD, color="green400"), ft.Text("Archivos Protegidos", color=TEXT_MUTED, size=12), txt_archivos_protegidos]), bgcolor=BG_CARD, padding=25, border_radius=20, border=ft.border.all(1, BORDER_COLOR), expand=1),
                        ]),
                    ], expand=2),
                    ft.Column([
                        ft.Text("¿Cómo funciona NoxSend?", size=18, weight="bold", color="white"),
                        ft.Container(
                            bgcolor=BG_CARD, padding=25, border_radius=20, border=ft.border.all(1, BORDER_COLOR), expand=1,
                            content=ft.Column([
                                TutorialStep("1", "Sube un archivo", "Ve a NoxDrive y selecciona cualquier documento."),
                                TutorialStep("2", "Cifrado Local", "Tu PC lo encripta antes de enviarlo a la nube."),
                                TutorialStep("3", "Comparte la Llave", "Pásale la llave por otra vía al destinatario.")
                            ], spacing=20)
                        )
                    ], expand=1)
                ], spacing=30)
            ])
        )
    )

    # --- TRANSFERENCIA ---
    icon_status = ft.Icon(ft.Icons.FILE_UPLOAD_OUTLINED, color="grey600", size=60)
    text_status = ft.Text("Arrastra tu archivo aquí", size=20, weight="bold", color="white")
    subtext_status = ft.Text(f"Máximo {LIMITE_GB} GB por envío", size=13, color=TEXT_MUTED)

    drop_zone = ft.Container(
        content=ft.Column([icon_status, text_status, subtext_status], alignment="center", horizontal_alignment="center", spacing=10),
        height=250, expand=True, bgcolor=BG_CARD, border=ft.border.all(2, ft.Colors.with_opacity(0.2, "white")), border_radius=24,
        alignment=ft.alignment.center, animate=ft.Animation(400, "decelerate")
    )

    cargando = ft.ProgressRing(visible=False, width=40, height=40, color=ACCENT)
    texto_id = ft.TextField(label="ID SEGUIMIENTO (Público)", read_only=True, border_radius=12, text_size=12, color="white", bgcolor=BG_ROOT)
    texto_llave = ft.TextField(label="LLAVE MAESTRA (Privada)", read_only=True, password=True, can_reveal_password=True, border_radius=12, color="green400", bgcolor=BG_ROOT)
    texto_codigo_cifrado = ft.Text("", font_family="Courier", color="green400", size=11, selectable=True)
    
    # --- NUEVO: DROPDOWN DE EXPIRACIÓN ---
    opciones_tiempo = ft.Dropdown(
        label="Autodestrucción",
        width=170,
        bgcolor=BG_ROOT, color="white", border_color=BORDER_COLOR, border_radius=12,
        options=[
            ft.dropdown.Option("1", "En 1 Hora"),
            ft.dropdown.Option("24", "En 24 Horas"),
            ft.dropdown.Option("168", "En 7 Días"),
        ],
        value="24", text_size=13
    )

    def cerrar_auditoria(e):
        page.close(dialogo_prueba)
        page.update()

    dialogo_prueba = ft.AlertDialog(
        modal=False,
        title=ft.Row([ft.Icon(ft.Icons.TERMINAL, color="green400"), ft.Text("Auditoría de Carga Útil", weight="bold", color="white")]),
        content=ft.Container(width=550, height=250, bgcolor="black", padding=15, border_radius=10, border=ft.border.all(1, ft.Colors.with_opacity(0.3, "green400")), content=ft.Column([ft.Text("Esto es exactamente lo único que recibe el servidor.", color="white70", size=12), ft.Divider(color="white24"), ft.Container(content=texto_codigo_cifrado, expand=True)], scroll="auto")),
        actions=[ft.TextButton("Cerrar", on_click=cerrar_auditoria, style=ft.ButtonStyle(color=TEXT_MUTED))], bgcolor=BG_CARD
    )

    def abrir_prueba_cifrado(e):
        page.open(dialogo_prueba)
        page.update()

    boton_prueba_cifrado = ft.ElevatedButton("Inspeccionar Carga", icon=ft.Icons.TROUBLESHOOT, bgcolor=BG_ROOT, color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)), on_click=abrir_prueba_cifrado)

    panel_resultados = ft.Container(
        visible=False, padding=25, border_radius=24, bgcolor=ft.Colors.with_opacity(0.05, ACCENT), border=ft.border.all(1, ft.Colors.with_opacity(0.3, ACCENT)),
        content=ft.Column([
            ft.Text("¡BLINDAJE COMPLETADO!", weight="black", size=14, color=ACCENT),
            ft.Row([texto_id, ft.IconButton(ft.Icons.COPY, icon_color=ACCENT, on_click=lambda _: copiar(texto_id.value, "ID"))], alignment="center"),
            ft.Row([texto_llave, ft.IconButton(ft.Icons.COPY, icon_color=ACCENT, on_click=lambda _: copiar(texto_llave.value, "Llave"))], alignment="center"),
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
                if peso_bytes > LIMITE_BYTES:
                    text_status.value = "ARCHIVO DEMASIADO GRANDE"
                    subtext_status.value = f"{peso_mb:.2f} MB (Máximo {LIMITE_GB} GB)"
                    text_status.color = "red400"
                    icon_status.name = ft.Icons.ERROR_OUTLINE
                    icon_status.color = "red400"
                    drop_zone.border = ft.border.all(2, "red400")
                    drop_zone.bgcolor = ft.Colors.with_opacity(0.05, "red")
                    boton_enviar.disabled = True
                else:
                    text_status.value = e.files[0].name
                    subtext_status.value = f"{peso_mb:.2f} MB - Listo para cifrar"
                    text_status.color = "white"
                    icon_status.name = ft.Icons.LOCK
                    icon_status.color = ACCENT
                    drop_zone.border = ft.border.all(2, ACCENT)
                    drop_zone.bgcolor = ft.Colors.with_opacity(0.05, ACCENT)
                    boton_enviar.disabled = False
            except:
                text_status.value = "Error al leer archivo"
                boton_enviar.disabled = True
            page.update()

    def ejecutar_envio(e):
        if not ruta_seleccionada[0]: return
        boton_enviar.disabled = True
        cargando.visible = True
        page.update()
        
        # AQUÍ LE PASAMOS LAS HORAS AL CONTROLADOR
        horas = int(opciones_tiempo.value)
        res = controlador.enviar_archivo(ruta_seleccionada[0], horas)
        
        cargando.visible = False
        
        if res:
            id_arc, key, muestra_cifrada = res 
            texto_id.value = id_arc
            texto_llave.value = key
            texto_codigo_cifrado.value = muestra_cifrada 
            
            panel_resultados.visible = True
            text_status.value = "TRANSFERENCIA COMPLETADA"
            icon_status.name = ft.Icons.CHECK_CIRCLE
            icon_status.color = "green400"
            sincronizar_datos_reales() 
        page.update()

    selector = ft.FilePicker(on_result=al_seleccionar)
    page.overlay.append(selector)

    boton_seleccionar = ft.ElevatedButton("1. Buscar Archivo", icon=ft.Icons.FOLDER, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=BG_CARD, color="white"), on_click=lambda _: selector.pick_files())
    boton_enviar = ft.ElevatedButton("2. Encriptar y Enviar", icon=ft.Icons.SECURITY, disabled=True, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12), bgcolor=ACCENT, color="white"), on_click=ejecutar_envio)

    view_transfer = ft.Container(
        visible=False, expand=True, padding=40, alignment=ft.alignment.top_center,
        content=ft.Container(
            width=1100,
            content=ft.Column([
                ft.Text("NoxDrive (Módulo de Blindaje)", size=28, weight="black", color="white"),
                ft.Text("Sube archivos confidenciales. El cifrado ocurre en tu dispositivo.", color=TEXT_MUTED, size=14),
                ft.Container(height=20),
                ft.Row([
                    ft.Column([
                        drop_zone,
                        ft.Container(height=10),
                        # AQUÍ SE MUESTRAN LOS 3 ELEMENTOS EN FILA
                        ft.Row([boton_seleccionar, opciones_tiempo, boton_enviar], spacing=15),
                        ft.Container(height=10),
                        cargando,
                        panel_resultados
                    ], expand=6),
                    ft.Container(
                        bgcolor=BG_CARD, padding=30, border_radius=24, border=ft.border.all(1, BORDER_COLOR), expand=4,
                        content=ft.Column([
                            ft.Icon(ft.Icons.INFO_OUTLINE, color=ACCENT, size=30),
                            ft.Text("Privacidad Absoluta", size=16, weight="bold", color="white"),
                            ft.Text("NoxSend no puede ver tus archivos. Aplicamos criptografía AES-256.", color=TEXT_MUTED, size=13),
                        ])
                    )
                ], alignment="start", vertical_alignment="start") 
            ])
        )
    )

    # --- BÓVEDA ---
    tabla_historial = ft.DataTable(
        border_radius=15, heading_row_color=ft.Colors.with_opacity(0.05, "white"),
        columns=[
            ft.DataColumn(ft.Text("NOMBRE DEL ARCHIVO", size=11, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("ID PÚBLICO", size=11, weight="bold", color=TEXT_MUTED)),
            ft.DataColumn(ft.Text("FECHA", size=11, weight="bold", color=TEXT_MUTED)),
        ], rows=[]
    )

    def vaciar_boveda_click(e):
        controlador.vaciar_boveda() 
        sincronizar_datos_reales()
        page.overlay.append(ft.SnackBar(ft.Text("Bóveda vaciada correctamente (Anti-forense)."), bgcolor="red", open=True))
        page.update()

    boton_vaciar_boveda = ft.ElevatedButton("Vaciar Bóveda", icon=ft.Icons.DELETE_FOREVER, bgcolor=ft.Colors.RED_700, color="white", on_click=vaciar_boveda_click)

    def sincronizar_datos_reales():
        boveda = controlador.obtener_boveda()
        tabla_historial.rows.clear()
        for reg in boveda:
            tabla_historial.rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(reg[1], weight="bold", color="white")), 
                ft.DataCell(ft.Text(reg[0][:12] + "...", color=ACCENT)), 
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
                    ft.Column([ft.Text("Mi Bóveda", size=28, weight="black", color="white"), ft.Text("Auditoría de todos los archivos que has protegido.", color=TEXT_MUTED, size=14)], expand=True),
                    boton_vaciar_boveda 
                ], alignment="spaceBetween"),
                ft.Container(height=20),
                ft.Container(content=ft.Column([tabla_historial], scroll="auto"), bgcolor=BG_CARD, padding=25, border_radius=24, border=ft.border.all(1, BORDER_COLOR), expand=True)
            ])
        )
    )
    
    sincronizar_datos_reales()
    header_title = ft.Text("PANEL PRINCIPAL", size=13, weight="black", color="white")

    return ft.View(
        "/dashboard", padding=0, bgcolor=BG_PANEL,
        controls=[
            ft.Row([
                sidebar,
                ft.Container(expand=True, content=ft.Column([
                    ft.Container(padding=ft.padding.symmetric(horizontal=40, vertical=20), border=ft.border.only(bottom=ft.border.BorderSide(1, BORDER_COLOR)), content=ft.Row([header_title, ft.Row([ft.Icon(ft.Icons.FINGERPRINT, color="grey500", size=16), ft.Text("Conexión Cifrada", size=12, weight="bold", color=TEXT_MUTED)])], alignment="spaceBetween")),
                    ft.Stack([view_home, view_transfer, view_vault], expand=True)
                ]))
            ], expand=True, spacing=0)
        ]
    )