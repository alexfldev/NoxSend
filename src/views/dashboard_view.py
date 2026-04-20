import flet as ft
import pyperclip
import time 
import random 
import urllib.request
import urllib.parse 
import json
import webbrowser
from src.controllers.app_controller import AppController

def get_dashboard_view(page: ft.Page):
    controlador = AppController()
    ruta_seleccionada = [None]
    gps_lat = [None]
    gps_lng = [None]
    
    # Variable para controlar si ya hemos mostrado el tutorial del mando
    tutorial_mando_mostrado = [False]
    
    estado_usuario = {
        "usuario": "Alejandro_Dev",
        "email": "alejandro@noxsend.com",
        "email_oculto": True,
        "2fa_activo": False,
        "notif_escritorio": True,
        "notif_sonido": False
    }

    def copiar(texto, msg):
        pyperclip.copy(texto)
        page.open(ft.SnackBar(ft.Text(f"{msg} copiado al portapapeles", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_700))

    # ==========================================
    # 0. MODAL: TUTORIAL CENTRO DE MANDO (PRIMER ACCESO)
    # ==========================================
    dialogo_tutorial_mando = ft.AlertDialog(
        modal=True,
        title=ft.Row([ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_400), ft.Text("PROTOCOLO DE BLINDAJE")]),
        content=ft.Container(
            content=ft.Column([
                ft.Text("Bienvenido al Centro de Mando. Sigue estos 3 pasos para enviar un archivo de forma segura:", size=13, color=ft.Colors.GREY_300),
                ft.Container(height=15),
                ft.Row([ft.Container(ft.Text("1", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), bgcolor=ft.Colors.BLUE_400, border_radius=15, width=24, height=24, alignment=ft.alignment.center), ft.Text("Selecciona tu archivo. Se cifrará en tu PC con AES-256.", size=12, expand=True)]),
                ft.Container(height=5),
                ft.Row([ft.Container(ft.Text("2", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), bgcolor=ft.Colors.BLUE_400, border_radius=15, width=24, height=24, alignment=ft.alignment.center), ft.Text("Pulsa 'Blindar y Subir'. Solo subiremos ruido ininteligible a la nube.", size=12, expand=True)]),
                ft.Container(height=5),
                ft.Row([ft.Container(ft.Text("3", weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), bgcolor=ft.Colors.BLUE_400, border_radius=15, width=24, height=24, alignment=ft.alignment.center), ft.Text("Copia el enlace y la Llave Maestra para pasársela al receptor.", size=12, expand=True)]),
                ft.Container(height=20),
                ft.Container(
                    content=ft.Row([ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER_400, size=20), ft.Text("Si pierdes la llave, el archivo será irrecuperable. Nosotros no la guardamos, el servidor es ciego.", size=11, color=ft.Colors.AMBER_400, weight=ft.FontWeight.BOLD, expand=True)]),
                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.AMBER_400), padding=10, border_radius=8, border=ft.border.all(1, ft.Colors.AMBER_900)
                )
            ], tight=True),
            width=500, padding=10
        ),
        actions=[
            ft.ElevatedButton("ENTENDIDO, INICIAR PROTOCOLO", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=lambda e: page.close(dialogo_tutorial_mando))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # ==========================================
    # 1. PESTAÑA 0: INICIO (DASHBOARD 70/30 PROFESIONAL)
    # ==========================================
    cabecera_inicio = ft.Row([
        ft.Column([
            ft.Text("Central de Inteligencia", size=32, weight=ft.FontWeight.BOLD),
            ft.Text(f"Agente: {estado_usuario['usuario']} | Monitoreo global y estado del sistema", color=ft.Colors.GREY_500, size=14)
        ], expand=True),
        ft.ElevatedButton("NUEVO BLINDAJE", icon=ft.Icons.SHIELD, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, height=50, on_click=lambda e: cambiar_pestana_manual(1))
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def crear_tarjeta_metrica(titulo, valor, icono, color_acento):
        return ft.Container(
            content=ft.Row([
                ft.Container(content=ft.Icon(icono, color=color_acento, size=24), padding=12, bgcolor=ft.Colors.with_opacity(0.1, color_acento), border_radius=10),
                ft.Column([
                    ft.Text(titulo, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
                    ft.Text(valor, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ], spacing=0)
            ]),
            expand=True, padding=20, bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE), border_radius=12, border=ft.border.all(1, ft.Colors.BLUE_GREY_900)
        )

    fila_metricas = ft.Row([
        crear_tarjeta_metrica("ARCHIVOS BLINDADOS", "3 Activos", ft.Icons.CLOUD_DONE_OUTLINED, ft.Colors.BLUE_400),
        crear_tarjeta_metrica("PURGAS DE RED", "12 Destruidos", ft.Icons.AUTO_DELETE_OUTLINED, ft.Colors.RED_400),
        crear_tarjeta_metrica("ANCLAJES G.A.N.", "2 Geovallados", ft.Icons.LOCATION_ON_OUTLINED, ft.Colors.PURPLE_400),
    ], spacing=20)

    noticias_ciberseguridad = [
        {"titulo": "Campaña de malware suplantando a la Agencia Tributaria", "fuente": "INCIBE - Avisos", "fecha": "Hoy, 10:30", "desc": "Se ha detectado una campaña masiva de phishing que suplanta a la Agencia Tributaria para instalar troyanos bancarios.", "img": "https://images.unsplash.com/photo-1563986768494-4dee2763ff0f?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80", "url": "https://www.incibe.es/"},
        {"titulo": "Vulnerabilidad crítica Zero-Day en routers VPN", "fuente": "The Hacker News", "fecha": "Ayer", "desc": "Un fallo crítico (CVSS 9.8) permite a atacantes remotos tomar el control total de dispositivos sin autenticación previa.", "img": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80", "url": "https://thehackernews.com/"},
        {"titulo": "NoxSend Beta: Protocolo G.A.N. en pruebas", "fuente": "NoxSend Dev Blog", "fecha": "Hace 2 días", "desc": "La próxima actualización permitirá restringir la apertura de archivos basándose en coordenadas GPS. El servidor es ciego a la ubicación.", "img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80", "url": ""}
    ]

    def crear_tarjeta_noticia(noticia):
        return ft.Container(
            content=ft.Row([
                ft.Image(src=noticia["img"], width=120, height=90, fit=ft.ImageFit.COVER, border_radius=8),
                ft.Column([
                    ft.Text(f"{noticia['fuente']} • {noticia['fecha']}", size=11, color=ft.Colors.BLUE_400, weight=ft.FontWeight.BOLD),
                    ft.Text(noticia["titulo"], weight=ft.FontWeight.BOLD, size=15, color=ft.Colors.WHITE),
                    ft.Text(noticia["desc"], size=12, color=ft.Colors.GREY_400, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                ], expand=True, spacing=4)
            ]),
            padding=15, bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE), border=ft.border.all(1, ft.Colors.BLUE_GREY_900), border_radius=12,
            margin=ft.margin.only(bottom=15), ink=True, on_click=lambda e: webbrowser.open(noticia["url"]) if noticia["url"] else None
        )

    columna_izq = ft.Column([
        fila_metricas,
        ft.Container(height=20),
        ft.Row([ft.Icon(ft.Icons.NEWSPAPER, size=18, color=ft.Colors.BLUE_300), ft.Text("FEED DE CIBERSEGURIDAD", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300)]),
        ft.Container(height=5),
        ft.Column([crear_tarjeta_noticia(n) for n in noticias_ciberseguridad], spacing=0)
    ], expand=7) 

    banner_estado = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.VERIFIED_USER_OUTLINED, color=ft.Colors.GREEN_400, size=28), ft.Text("SISTEMA SEGURO", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.GREEN_400)]),
            ft.Text("Conexión Zero-Knowledge activa. Claves locales.", size=12, color=ft.Colors.GREY_400)
        ]),
        padding=20, bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.GREEN_400), border=ft.border.all(1, ft.Colors.GREEN_900), border_radius=12
    )

    def crear_tarjeta_curiosidad(titulo, texto):
        return ft.Container(
            content=ft.Column([
                ft.Text(titulo, weight=ft.FontWeight.BOLD, size=13, color=ft.Colors.WHITE),
                ft.Text(texto, size=12, color=ft.Colors.GREY_400)
            ]), padding=15, bgcolor=ft.Colors.BLACK45, border=ft.border.all(1, ft.Colors.BLUE_GREY_900), border_radius=10, margin=ft.margin.only(bottom=10)
        )

    columna_der = ft.Column([
        banner_estado,
        ft.Container(height=20),
        ft.Row([ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=18, color=ft.Colors.AMBER_400), ft.Text("CULTURA HACKER", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)]),
        ft.Container(height=5),
        crear_tarjeta_curiosidad("Entropía AES-256", "Harían falta 77 cuatrillones de años con toda la población mundial usando superordenadores para descifrar tu llave."),
        crear_tarjeta_curiosidad("El concepto 'ZK'", "Ideado en 1985 por Micali y Rackoff. Permite demostrar que sabes la llave sin revelarla jamás al servidor central."),
        crear_tarjeta_curiosidad("Enlaces Fragmentados", "En NoxSend, la llave viaja en el '#' de la URL. El navegador no envía esta parte al servidor. Somos matemáticamente ciegos.")
    ], expand=3) 

    vista_inicio = ft.Container(
        content=ft.Column([
            cabecera_inicio,
            ft.Container(height=30),
            ft.Row([columna_izq, columna_der], vertical_alignment=ft.CrossAxisAlignment.START, spacing=30)
        ], scroll=ft.ScrollMode.AUTO),
        padding=40, expand=True, alignment=ft.alignment.top_left
    )

    # ==========================================
    # 2. COMPONENTES COMPARTIDOS Y MODALES
    # ==========================================
    def generar_hex_dump():
        hex_chars = "0123456789ABCDEF"
        dump = ""
        for i in range(8):
            linea = " ".join("".join(random.choices(hex_chars, k=2)) for _ in range(12))
            dump += f"0x{(i*12):04X} | {linea}\n"
        return dump

    texto_payload = ft.Text(generar_hex_dump(), font_family="Consolas", size=11, color=ft.Colors.GREEN_400)
    visor_payload = ft.Container(
        content=ft.Column([
            ft.Row([ft.Icon(ft.Icons.WIFI_TETHERING_ERROR_ROUNDED, color=ft.Colors.RED_400, size=16), ft.Text("DATOS EN TRÁNSITO: INTERCEPTACIÓN DE RED", size=10, color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD)]),
            ft.Container(bgcolor=ft.Colors.GREY_800, height=1), 
            texto_payload,
        ]),
        bgcolor=ft.Colors.BLACK, padding=15, border_radius=5, border=ft.border.all(1, ft.Colors.RED_900)
    )

    dialogo_auditoria = ft.AlertDialog(
        title=ft.Row([ft.Icon(ft.Icons.GAVEL, color=ft.Colors.BLUE_400), ft.Text("Certificado de Privacidad")]),
        content=ft.Container(
            content=ft.Column([
                ft.Text("ARQUITECTURA DE CONOCIMIENTO CERO", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.BLUE_400),
                ft.Container(height=10),
                ft.Text("El cifrado se realiza íntegramente en su dispositivo. La Llave Maestra nunca sale de su equipo.", size=12, color=ft.Colors.BLUE_400),
                ft.Container(height=10),
                visor_payload,
            ], tight=True, scroll=ft.ScrollMode.AUTO),
            width=600, padding=10
        ),
        actions=[ft.TextButton("Cerrar Auditoría", style=ft.ButtonStyle(color=ft.Colors.BLUE_400), on_click=lambda e: page.close(dialogo_auditoria))]
    )

    # ==========================================
    # 3. PESTAÑA 1: CENTRO DE MANDO (CON OPCIONES INTEGRADAS)
    # ==========================================
    ancho_main = 650 

    texto_archivo = ft.Text("Ningún archivo seleccionado", color=ft.Colors.GREY_500, size=14, weight=ft.FontWeight.W_500)
    zona_drop = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.CLOUD_UPLOAD_OUTLINED, size=70, color=ft.Colors.BLUE_400),
            ft.Text("Haz clic aquí para blindar un archivo", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Cifrado local asegurado. Client-side encryption.", color=ft.Colors.GREY_500, size=12),
            ft.Container(height=10),
            texto_archivo
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=ancho_main, padding=50, border=ft.border.all(2, ft.Colors.BLUE_GREY_700), border_radius=15, ink=True, 
        on_click=lambda _: selector_archivos_mando.pick_files(),
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLUE_200)
    )

    # --- CONTROLES DE SEGURIDAD AVANZADA (ANTIGUO "PREMIUM") ---
    txt_busqueda = ft.TextField(hint_text="Ej: Madrid, o Calle Serrano...", expand=True, height=45, text_size=13, border_color=ft.Colors.BLUE_GREY_700)
    txt_lat = ft.TextField(label="Latitud", width=150, height=45, text_size=12, border_color=ft.Colors.BLUE_GREY_700)
    txt_lng = ft.TextField(label="Longitud", width=150, height=45, text_size=12, border_color=ft.Colors.BLUE_GREY_700)
    texto_destino_fijado = ft.Text("", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREEN_400)
    
    tarjeta_anclaje = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.GREEN_400), texto_destino_fijado, ft.Container(expand=True),
            ft.IconButton(ft.Icons.EDIT, icon_color=ft.Colors.GREY_500, tooltip="Cambiar destino", on_click=lambda _: resetear_busqueda())
        ]), bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400), padding=15, border_radius=8, visible=False, border=ft.border.all(1, ft.Colors.GREEN_800)
    )

    fila_busqueda = ft.Row([txt_busqueda], visible=True)
    fila_manual = ft.Row([txt_lat, txt_lng, ft.IconButton(icon=ft.Icons.MAP, icon_color=ft.Colors.BLUE_400, tooltip="Abrir Google Maps", on_click=lambda _: webbrowser.open("https://www.google.com/maps"))], visible=True)

    def resetear_busqueda():
        gps_lat[0] = None; gps_lng[0] = None
        txt_busqueda.value = ""; txt_lat.value = ""; txt_lng.value = ""
        tarjeta_anclaje.visible = False
        fila_busqueda.visible = True; fila_manual.visible = True
        page.update()

    def buscar_coordenadas(e):
        if not txt_busqueda.value: return
        btn_buscar.icon = ft.Icons.HOURGLASS_TOP
        page.update()
        try:
            query = urllib.parse.quote(txt_busqueda.value)
            req = urllib.request.Request(f"https://nominatim.openstreetmap.org/search?q={query}&format=json&limit=1", headers={'User-Agent': 'NoxSend_PFC_App/1.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data:
                    gps_lat[0] = data[0]["lat"][:8]; gps_lng[0] = data[0]["lon"][:8]
                    nombre_corto = data[0]['display_name'].split(',')[0]
                    texto_destino_fijado.value = f"Anclado a: {nombre_corto}"
                    fila_busqueda.visible = False; fila_manual.visible = False
                    tarjeta_anclaje.visible = True
                else:
                    page.open(ft.SnackBar(ft.Text("❌ Destino no encontrado. Introduce Lat/Lng manualmente.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700))
        except Exception:
            page.open(ft.SnackBar(ft.Text("❌ Error de red al buscar en OpenStreetMap.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700))
        btn_buscar.icon = ft.Icons.SEARCH
        page.update()

    btn_buscar = ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.BLUE_400, tooltip="Buscar ubicación", on_click=buscar_coordenadas)
    fila_busqueda.controls.append(btn_buscar)

    txt_tiempo = ft.TextField(value="24", width=100, height=45, text_align=ft.TextAlign.CENTER, border_color=ft.Colors.BLUE_GREY_700)
    drop_unidad = ft.Dropdown(width=200, border_color=ft.Colors.BLUE_GREY_700, options=[ft.dropdown.Option("Horas"), ft.dropdown.Option("Días"), ft.dropdown.Option("Descargas")], value="Horas")

    opciones_avanzadas = ft.Column([
        ft.Text("Destino Autorizado (Opcional)", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400),
        fila_busqueda, fila_manual, tarjeta_anclaje,
        ft.Container(height=5),
        ft.Text("Precisión del perímetro (Metros)", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_400),
        ft.Slider(min=10, max=1000, divisions=99, label="{value} m", value=50, active_color=ft.Colors.BLUE_400),
    ], visible=False)

    def toggle_gps(e):
        opciones_avanzadas.visible = switch_gps.value
        if not switch_gps.value: resetear_busqueda()
        page.update()

    switch_gps = ft.Switch(label="Activar Geo-Fencing (G.A.N.)", value=False, active_color=ft.Colors.BLUE_400, on_change=toggle_gps)

    # Panel Desplegable de Opciones Avanzadas en el Mando
    panel_opciones_seguridad = ft.ExpansionTile(
        title=ft.Text("Opciones de Seguridad Avanzadas", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300),
        subtitle=ft.Text("Configurar G.A.N. y Autodestrucción (Opcional)"),
        leading=ft.Icon(ft.Icons.TUNE, color=ft.Colors.BLUE_300),
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Protocolo Geo-Acuse Notarial (G.A.N.)", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.BLUE_400),
                    ft.Text("Añade una cerradura física. El archivo exigirá que el receptor esté en el perímetro GPS.", color=ft.Colors.GREY_400, size=12),
                    ft.Container(content=switch_gps, padding=10, border_radius=8, bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE)),
                    opciones_avanzadas,
                    ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=15)), 
                    ft.Row([ft.Icon(ft.Icons.TIMER, color=ft.Colors.RED_400), ft.Text("Límite de Autodestrucción", weight=ft.FontWeight.BOLD, size=14, color=ft.Colors.RED_400)]),
                    ft.Text("El archivo cifrado será purgado de la nube al superar el límite.", color=ft.Colors.GREY_400, size=12),
                    ft.Row([txt_tiempo, drop_unidad]),
                ]),
                padding=20,
                bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE),
                border_radius=8,
                border=ft.border.all(1, ft.Colors.BLUE_GREY_900)
            )
        ]
    )
    # --- FIN CONTROLES SEGURIDAD ---

    texto_terminal = ft.Text("", font_family="Consolas", color=ft.Colors.GREEN_400, size=12)
    consola_auditoria = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("AUDITORÍA DE CIFRADO ZERO-KNOWLEDGE", size=10, color=ft.Colors.GREY_500, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.Icon(ft.Icons.SHIELD, color=ft.Colors.BLUE_500, size=14)
            ]),
            ft.Container(bgcolor=ft.Colors.GREY_800, height=1, width=ancho_main), 
            texto_terminal,
            ft.ProgressBar(color=ft.Colors.GREEN_400, bgcolor=ft.Colors.GREY_900)
        ]),
        width=ancho_main, bgcolor=ft.Colors.BLACK, padding=20, border_radius=10, border=ft.border.all(1, ft.Colors.GREY_900), visible=False
    )

    texto_id = ft.TextField(label="ID de Recuperación (PÚBLICO)", read_only=True, expand=True, border_color=ft.Colors.BLUE_GREY_700)
    texto_llave = ft.TextField(label="LLAVE MAESTRA (¡TOP SECRET!)", read_only=True, expand=True, color=ft.Colors.GREEN_400, password=True, can_reveal_password=True, border_color=ft.Colors.BLUE_GREY_700)
    
    tarjeta_resultados = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400), ft.Text("ARCHIVO BLINDADO Y SUBIDO", weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400)]),
                ft.Container(bgcolor=ft.Colors.GREY_800, height=1, width=ancho_main), 
                ft.Row([texto_id, ft.IconButton(ft.Icons.COPY, icon_color=ft.Colors.BLUE_400, tooltip="Copiar ID", on_click=lambda _: copiar(texto_id.value, "ID"))]),
                ft.Row([texto_llave, ft.IconButton(ft.Icons.COPY, icon_color=ft.Colors.GREEN_400, tooltip="Copiar Llave", on_click=lambda _: copiar(texto_llave.value, "Llave"))]),
                ft.Container(height=10),
                ft.ElevatedButton("COPIAR ENLACE NOXSEND (WEB)", icon=ft.Icons.LINK, width=ancho_main, height=50, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=lambda _: copiar(f"https://noxsend.com/download?id={texto_id.value}", "Enlace")),
            ]),
            padding=30, bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.GREEN_400),
        ), width=ancho_main, visible=False
    )

    boton_enviar = ft.ElevatedButton("BLINDAR Y SUBIR", icon=ft.Icons.SHIELD, disabled=True, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, width=ancho_main, height=55)
    
    def ejecutar_boton_nuclear(e):
        ruta_seleccionada[0] = None
        texto_archivo.value = "Ningún archivo seleccionado"
        texto_archivo.color = ft.Colors.GREY_500
        zona_drop.visible = True
        panel_opciones_seguridad.visible = True
        tarjeta_resultados.visible = False
        consola_auditoria.visible = True
        boton_enviar.disabled = True
        boton_nuclear.visible = False
        texto_terminal.color = ft.Colors.RED_500
        texto_terminal.value = "> [ALERTA] INICIANDO PROTOCOLO DE PURGA...\n> Vaciando punteros de memoria (RAM)...\n> Sobrescribiendo bloques con 0x00...\n> PAYLOAD ABORTADO Y DESTRUIDO CON ÉXITO."
        page.update()

    boton_nuclear = ft.ElevatedButton("BOTÓN NUCLEAR (CANCELAR SUBIDA)", icon=ft.Icons.WARNING_ROUNDED, bgcolor=ft.Colors.RED_900, color=ft.Colors.WHITE, width=ancho_main, height=45, visible=False, on_click=ejecutar_boton_nuclear)

    def al_seleccionar_archivo_mando(e):
        if e.files:
            ruta_seleccionada[0] = e.files[0].path
            texto_archivo.value = f"📁 {e.files[0].name}"
            texto_archivo.color = ft.Colors.BLUE_300
            boton_enviar.disabled = False
            boton_nuclear.visible = True 
            tarjeta_resultados.visible = False 
            consola_auditoria.visible = False
            zona_drop.border = ft.border.all(2, ft.Colors.BLUE_400) 
            texto_terminal.color = ft.Colors.GREEN_400 
            texto_terminal.value = ""
        page.update()

    selector_archivos_mando = ft.FilePicker(on_result=al_seleccionar_archivo_mando)
    page.overlay.append(selector_archivos_mando)

    def enviar_archivo(e):
        if not ruta_seleccionada[0]: return
        boton_enviar.disabled = True
        boton_nuclear.disabled = True 
        zona_drop.visible = False
        panel_opciones_seguridad.visible = False
        consola_auditoria.visible = True
        texto_terminal.color = ft.Colors.GREEN_400
        
        texto_terminal.value = "> Iniciando protocolo NoxSend Engine...\n"
        
        lat_final = gps_lat[0] if gps_lat[0] else txt_lat.value
        lng_final = gps_lng[0] if gps_lng[0] else txt_lng.value
        if switch_gps.value and lat_final and lng_final:
            texto_terminal.value += f"> [PREMIUM] Restricción G.A.N. activada: {lat_final}, {lng_final}\n"
        
        texto_terminal.value += f"> [PREMIUM] Autodestrucción fijada en: {txt_tiempo.value} {drop_unidad.value}\n"
        page.update()
        time.sleep(0.5)

        texto_terminal.value += "> Generando CSPRNG Key y cifrando con AES-256-GCM...\n"
        page.update()

        try:
            resultado = controlador.enviar_archivo(
                ruta_seleccionada[0], 
                gan_lat=lat_final if switch_gps.value else None,
                gan_lng=lng_final if switch_gps.value else None,
                exp_time=txt_tiempo.value,
                exp_unit=drop_unidad.value
            )
            
            if resultado:
                id_archivo, llave = resultado
                texto_id.value = id_archivo
                texto_llave.value = llave
                
                consola_auditoria.visible = False
                tarjeta_resultados.visible = True
                zona_drop.visible = True
                panel_opciones_seguridad.visible = True
                zona_drop.border = ft.border.all(2, ft.Colors.BLUE_GREY_700) 
                texto_archivo.value = "Ningún archivo seleccionado"
                texto_archivo.color = ft.Colors.GREY_500
                boton_nuclear.visible = False 
                boton_nuclear.disabled = False
            else:
                texto_terminal.value += "\n[ERROR] Fallo de conexión con Supabase Storage."
                texto_terminal.color = ft.Colors.RED_400
                boton_enviar.disabled = False
                boton_nuclear.disabled = False
                zona_drop.visible = True
                panel_opciones_seguridad.visible = True
        except Exception as error_real:
            texto_terminal.value += f"\n[FATAL EXCEPTION]:\n{str(error_real)}"
            texto_terminal.color = ft.Colors.RED_400
            boton_enviar.disabled = False
            boton_nuclear.disabled = False
            zona_drop.visible = True
            panel_opciones_seguridad.visible = True

        page.update()

    boton_enviar.on_click = enviar_archivo

    vista_centro_mando = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Centro de Mando", size=32, weight=ft.FontWeight.BOLD),
                ft.Container(ft.Text("AES-256-GCM", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK), bgcolor=ft.Colors.GREEN_400, padding=5, border_radius=5)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=ancho_main),
            ft.Text("Cifrado de extremo a extremo activo. Listo para transmisión.", color=ft.Colors.GREY_500),
            ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, width=ancho_main, margin=ft.margin.symmetric(vertical=10)), 
            zona_drop,
            panel_opciones_seguridad, 
            ft.Container(height=5),
            boton_enviar,
            boton_nuclear,
            consola_auditoria,
            tarjeta_resultados
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO),
        expand=True, padding=ft.padding.only(top=40), alignment=ft.alignment.top_center
    )

    # ==========================================
    # 4. PESTAÑA 2: BÓVEDA LOCAL
    # ==========================================
    historial_dummy = [
        {"id": "8f9a2b4...", "nombre": "Contrato_NDAs_2026.pdf", "fecha": "Hoy, 10:45", "estado": "Activo", "color": ft.Colors.GREEN_400},
        {"id": "1c3x9z2...", "nombre": "Backups_BBDD.zip", "fecha": "Ayer, 18:20", "estado": "Destruido", "color": ft.Colors.RED_400},
        {"id": "7m2p8l1...", "nombre": "Nominas_Febrero.xlsx", "fecha": "12 Abr, 09:15", "estado": "Destruido", "color": ft.Colors.RED_400},
    ]

    filas_tabla = []
    for item in historial_dummy:
        filas_tabla.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(item["id"], font_family="Consolas", color=ft.Colors.BLUE_300)),
                ft.DataCell(ft.Text(item["nombre"])),
                ft.DataCell(ft.Text(item["fecha"], color=ft.Colors.GREY_400)),
                ft.DataCell(ft.Container(ft.Text(item["estado"], size=10, weight=ft.FontWeight.BOLD), bgcolor=ft.Colors.with_opacity(0.2, item["color"]), border_radius=4, padding=ft.padding.symmetric(horizontal=6, vertical=2))),
            ])
        )

    tabla_historial = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID PÚBLICO")),
            ft.DataColumn(ft.Text("ARCHIVO ORIGINAL")),
            ft.DataColumn(ft.Text("FECHA ENVÍO")),
            ft.DataColumn(ft.Text("ESTADO")),
        ],
        rows=filas_tabla,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_800),
        border_radius=10,
        heading_row_color=ft.Colors.BLUE_GREY_900,
        expand=True
    )

    vista_boveda = ft.Container(
        content=ft.Column([
            ft.Text("Auditoría de Bóveda", size=32, weight=ft.FontWeight.BOLD),
            ft.Text("Registro inmutable de tus transferencias. (Datos guardados en SQLite local).", color=ft.Colors.GREY_500),
            ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=15)), 
            tabla_historial
        ]),
        padding=40, width=800, alignment=ft.alignment.top_center
    )

    # ==========================================
    # 5. PESTAÑA 3: AJUSTES (ESTILO DISCORD MEJORADO)
    # ==========================================
    
    input_nuevo_nombre = ft.TextField(label="Nuevo nombre de usuario", value=estado_usuario["usuario"], border_color=ft.Colors.BLUE_GREY_700)
    
    def guardar_nombre(e):
        estado_usuario["usuario"] = input_nuevo_nombre.value
        texto_usuario.value = estado_usuario["usuario"]
        page.close(dlg_editar_nombre)
        page.open(ft.SnackBar(ft.Text("✅ Nombre actualizado", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_700))
        page.update()

    dlg_editar_nombre = ft.AlertDialog(
        title=ft.Text("Cambiar nombre"), content=input_nuevo_nombre,
        actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_editar_nombre)), ft.ElevatedButton("Guardar", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=guardar_nombre)]
    )

    input_pass = ft.TextField(label="Contraseña maestra", password=True, can_reveal_password=True, border_color=ft.Colors.BLUE_GREY_700)
    def verificar_y_revelar(e):
        estado_usuario["email_oculto"] = False
        texto_email.value = estado_usuario["email"]
        btn_revelar.text = "Ocultar"
        input_pass.value = "" 
        page.close(dlg_revelar_email)
        page.update()

    dlg_revelar_email = ft.AlertDialog(
        title=ft.Row([ft.Icon(ft.Icons.SECURITY, color=ft.Colors.RED_400), ft.Text("Verificación requerida")]),
        content=ft.Column([ft.Text("Introduce tu contraseña maestra:", size=12), input_pass], tight=True),
        actions=[ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_revelar_email)), ft.ElevatedButton("Verificar", bgcolor=ft.Colors.RED_700, color=ft.Colors.WHITE, on_click=verificar_y_revelar)]
    )
    
    dlg_pass = ft.AlertDialog(
        title=ft.Text("Cambiar Contraseña"),
        content=ft.Column([
            ft.TextField(label="Contraseña Actual", password=True, can_reveal_password=True, border_color=ft.Colors.BLUE_GREY_700),
            ft.TextField(label="Nueva Contraseña", password=True, can_reveal_password=True, border_color=ft.Colors.BLUE_GREY_700)
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: page.close(dlg_pass)), 
            ft.ElevatedButton("Actualizar", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, on_click=lambda e: [page.close(dlg_pass), page.open(ft.SnackBar(ft.Text("🔒 Contraseña actualizada", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_700))])
        ]
    )

    def al_seleccionar_avatar(e):
        if e.files:
            icono_avatar.name = ft.Icons.CHECK
            icono_avatar.color = ft.Colors.GREEN_400
            page.open(ft.SnackBar(ft.Text(f"📸 Avatar actualizado a {e.files[0].name}", color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN_700))
            page.update()

    selector_avatar = ft.FilePicker(on_result=al_seleccionar_avatar)
    page.overlay.append(selector_avatar)

    def toggle_email(e):
        if estado_usuario["email_oculto"]:
            page.open(dlg_revelar_email)
        else:
            estado_usuario["email_oculto"] = True
            texto_email.value = "ale********@noxsend.com"
            btn_revelar.text = "Revelar"
        page.update()

    texto_usuario = ft.Text(estado_usuario["usuario"], size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD)
    texto_email = ft.Text("ale********@noxsend.com", size=16, color=ft.Colors.WHITE)
    btn_revelar = ft.ElevatedButton("Revelar", color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_800, on_click=toggle_email)
    icono_avatar = ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=40)

    contenido_perfil = ft.Column([
        ft.Text("Mi Cuenta", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(
            bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE), border_radius=10, border=ft.border.all(1, ft.Colors.BLUE_GREY_900),
            content=ft.Column([
                ft.Stack([
                    ft.Container(height=100, bgcolor=ft.Colors.BLUE_800, border_radius=ft.border_radius.only(top_left=10, top_right=10)),
                    ft.Container(
                        content=ft.CircleAvatar(radius=40, bgcolor=ft.Colors.BLUE_GREY_900, content=icono_avatar),
                        margin=ft.margin.only(top=50, left=20), tooltip="Cambiar Avatar",
                        ink=True, on_click=lambda _: selector_avatar.pick_files()
                    ),
                    ft.Container(content=ft.ElevatedButton("Editar Perfil", bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE), alignment=ft.alignment.top_right, margin=ft.margin.only(top=110, right=20))
                ], height=160),
                
                ft.Container(
                    bgcolor=ft.Colors.BLACK45, border_radius=8, padding=20, margin=20,
                    content=ft.Column([
                        ft.Row([
                            ft.Column([ft.Text("NOMBRE DE USUARIO", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500), texto_usuario], expand=True),
                            ft.ElevatedButton("Editar", color=ft.Colors.WHITE, bgcolor=ft.Colors.BLUE_GREY_800, on_click=lambda _: page.open(dlg_editar_nombre))
                        ]),
                        ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=10)),
                        ft.Row([
                            ft.Column([ft.Text("CORREO ELECTRÓNICO", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500), texto_email], expand=True),
                            btn_revelar
                        ]),
                    ])
                )
            ])
        )
    ])

    def revocar_dispositivo(e):
        e.control.parent.visible = False
        page.open(ft.SnackBar(ft.Text("🚫 Acceso revocado remotamente.", color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700))
        page.update()

    contenido_privacidad = ft.Column([
        ft.Text("Privacidad y Seguridad", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=10)),
        
        ft.Text("Gestión de Contraseñas", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
        ft.Row([
            ft.Text("Cambia tu contraseña maestra de cifrado.", size=12, color=ft.Colors.GREY_500, expand=True),
            ft.ElevatedButton("Cambiar Contraseña", bgcolor=ft.Colors.BLUE_GREY_800, color=ft.Colors.WHITE, on_click=lambda _: page.open(dlg_pass))
        ]),
        
        ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=20)),
        
        ft.Text("Dispositivos Conectados", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
        ft.Text("Aquí tienes todos los dispositivos en los que has iniciado sesión.", size=12, color=ft.Colors.GREY_500),
        ft.Container(height=10),
        ft.Container(
            bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE), border_radius=8, padding=15, border=ft.border.all(1, ft.Colors.GREEN_900),
            content=ft.Row([
                ft.Icon(ft.Icons.COMPUTER, color=ft.Colors.GREEN_400),
                ft.Column([ft.Text("Linux - App de Escritorio", weight=ft.FontWeight.BOLD), ft.Text("Madrid, España • Activo ahora", size=11, color=ft.Colors.GREEN_400)], expand=True),
                ft.Text("Actual", size=11, color=ft.Colors.GREY_500)
            ])
        ),
        ft.Container(height=5),
        ft.Container(
            bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE), border_radius=8, padding=15, border=ft.border.all(1, ft.Colors.BLUE_GREY_900),
            content=ft.Row([
                ft.Icon(ft.Icons.PHONE_IPHONE, color=ft.Colors.GREY_400),
                ft.Column([ft.Text("Safari en iPhone 14 Pro", weight=ft.FontWeight.BOLD), ft.Text("Sevilla, España • Hace 2 horas", size=11, color=ft.Colors.GREY_500)], expand=True),
                ft.IconButton(ft.Icons.CLOSE, icon_color=ft.Colors.RED_400, tooltip="Cerrar sesión", on_click=revocar_dispositivo)
            ])
        ),
    ])

    contenido_notificaciones = ft.Column([
        ft.Text("Notificaciones", size=24, weight=ft.FontWeight.BOLD),
        ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=10)),
        ft.Text("Personaliza cómo te avisa NoxSend de los eventos importantes.", size=12, color=ft.Colors.GREY_500),
        ft.Container(height=10),
        ft.Switch(label="Notificaciones de escritorio (Nuevas descargas, alertas GAN)", value=True, active_color=ft.Colors.BLUE_400),
        ft.Switch(label="Sonidos de alerta", value=False, active_color=ft.Colors.BLUE_400),
        ft.Switch(label="Emails de seguridad (Nuevos inicios de sesión)", value=True, active_color=ft.Colors.BLUE_400),
    ])

    area_contenido_ajustes = ft.Container(content=contenido_perfil, expand=True, padding=ft.padding.only(left=40))

    def cambiar_seccion(e, seccion):
        if seccion == "perfil": area_contenido_ajustes.content = contenido_perfil
        elif seccion == "privacidad": area_contenido_ajustes.content = contenido_privacidad
        elif seccion == "notificaciones": area_contenido_ajustes.content = contenido_notificaciones
        page.update()

    menu_lateral_discord = ft.Container(
        width=250, padding=20, bgcolor=ft.Colors.with_opacity(0.01, ft.Colors.WHITE),
        border=ft.border.only(right=ft.border.BorderSide(1, ft.Colors.BLUE_GREY_900)),
        content=ft.Column([
            ft.Text("AJUSTES DE USUARIO", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
            ft.TextButton("Mi Cuenta", width=210, style=ft.ButtonStyle(alignment=ft.alignment.center_left, color=ft.Colors.GREY_300), on_click=lambda e: cambiar_seccion(e, "perfil")),
            ft.TextButton("Privacidad y Seguridad", width=210, style=ft.ButtonStyle(alignment=ft.alignment.center_left, color=ft.Colors.GREY_300), on_click=lambda e: cambiar_seccion(e, "privacidad")),
            ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=10)),
            ft.Text("AJUSTES DE LA APP", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_500),
            ft.TextButton("Notificaciones", width=210, style=ft.ButtonStyle(alignment=ft.alignment.center_left, color=ft.Colors.GREY_300), on_click=lambda e: cambiar_seccion(e, "notificaciones")),
            ft.Container(bgcolor=ft.Colors.BLUE_GREY_800, height=1, margin=ft.margin.symmetric(vertical=10)),
            ft.TextButton("Cerrar Sesión", width=210, style=ft.ButtonStyle(alignment=ft.alignment.center_left, color=ft.Colors.RED_400), icon=ft.Icons.LOGOUT, icon_color=ft.Colors.RED_400),
        ])
    )

    vista_ajustes = ft.Row([menu_lateral_discord, area_contenido_ajustes], expand=True)

    # ==========================================
    # 7. ENSAMBLAJE FINAL Y NAVEGACIÓN
    # ==========================================
    
    area_contenido_principal = ft.Container(content=vista_inicio, expand=True)

    def cambiar_pestana(e):
        indice = e.control.selected_index
        if indice == 0: 
            area_contenido_principal.content = vista_inicio 
        elif indice == 1: 
            area_contenido_principal.content = vista_centro_mando
            if not tutorial_mando_mostrado[0]:
                tutorial_mando_mostrado[0] = True
                page.open(dialogo_tutorial_mando)
        elif indice == 2: 
            area_contenido_principal.content = vista_boveda
        elif indice == 3: 
            area_contenido_principal.content = vista_ajustes 
        
        area_contenido_principal.opacity = 0
        page.update()
        time.sleep(0.05)
        area_contenido_principal.opacity = 1
        page.update()

    def cambiar_pestana_manual(indice):
        rail_navegacion.selected_index = indice
        class DummyEvent:
            pass
        e = DummyEvent()
        e.control = rail_navegacion
        cambiar_pestana(e)

    rail_navegacion = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME_OUTLINED, selected_icon=ft.Icons.HOME, label="Inicio"),
            ft.NavigationRailDestination(icon=ft.Icons.ROCKET_LAUNCH_OUTLINED, selected_icon=ft.Icons.ROCKET_LAUNCH, label="Mando"),
            ft.NavigationRailDestination(icon=ft.Icons.STORAGE_OUTLINED, selected_icon=ft.Icons.STORAGE, label="Bóveda"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS_OUTLINED, selected_icon=ft.Icons.SETTINGS, label="Ajustes"),
        ],
        on_change=cambiar_pestana,
        bgcolor=ft.Colors.with_opacity(0.02, ft.Colors.WHITE)
    )

    return ft.Row(
        [
            rail_navegacion, 
            ft.VerticalDivider(width=1, color=ft.Colors.BLUE_GREY_900), 
            area_contenido_principal
        ], 
        expand=True
    )