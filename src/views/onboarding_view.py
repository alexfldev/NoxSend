import flet as ft

def get_onboarding_view(page: ft.Page, al_completar_tutorial):
    # Estado actual del carrusel
    paso_actual = [0]

    # Contenido de las diapositivas
    diapositivas = [
        {
            "icon": ft.Icons.LOCK_OUTLINE,
            "title": "Bienvenido a NoxSend",
            "desc": "El estándar definitivo para el envío de archivos confidenciales. Protege tu información antes de que toque internet."
        },
        {
            "icon": ft.Icons.VISIBILITY_OFF_OUTLINED,
            "title": "Arquitectura Zero-Knowledge",
            "desc": "Ciframos tus archivos localmente con AES-256-GCM. Nosotros no tenemos tu llave. Nadie, ni siquiera el servidor, puede ver lo que envías."
        },
        {
            "icon": ft.Icons.GAVEL,
            "title": "Protocolo G.A.N.",
            "desc": "Geo-Acuse Notarial. Restringe quién y dónde pueden abrir tus archivos, y obtén un recibo criptográfico con validez de auditoría."
        }
    ]

    # --- 1. ANIMACIONES DE TRANSICIÓN ---
    def crear_vista_diapositiva(indice):
        data = diapositivas[indice]
        return ft.Column([
            ft.Icon(data["icon"], size=120, color=ft.Colors.BLUE_400),
            ft.Container(height=20),
            ft.Text(data["title"], size=36, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Container(height=15),
            ft.Text(data["desc"], size=18, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER, width=550)
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
        key=str(indice)) 

    contenido_animado = ft.AnimatedSwitcher(
        content=crear_vista_diapositiva(0), 
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=400, 
        switch_in_curve=ft.AnimationCurve.EASE_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
    )

    # --- 2. INDICADORES DINÁMICOS ---
    indicadores = ft.Row(alignment=ft.MainAxisAlignment.CENTER, spacing=8)
    
    def actualizar_indicadores():
        indicadores.controls.clear()
        for i in range(len(diapositivas)):
            is_active = i == paso_actual[0]
            indicadores.controls.append(
                ft.Container(
                    width=30 if is_active else 10,
                    height=10,
                    border_radius=5,
                    bgcolor=ft.Colors.BLUE_400 if is_active else ft.Colors.GREY_800,
                    animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT)
                )
            )

    actualizar_indicadores()

    # --- 3. BOTONES Y LÓGICA DE NAVEGACIÓN ---
    boton_siguiente = ft.ElevatedButton("SIGUIENTE", width=250, height=55, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
    
    # === SOLUCIÓN A LA PANTALLA DE ERROR ===
    # En las nuevas versiones de Flet, los TextButton usan "style=ft.ButtonStyle(color=...)"
    boton_atras = ft.TextButton("Atrás", style=ft.ButtonStyle(color=ft.Colors.GREY_400), visible=False)
    boton_saltar = ft.TextButton("Saltar tutorial", style=ft.ButtonStyle(color=ft.Colors.GREY_600))

    def actualizar_ui():
        contenido_animado.content = crear_vista_diapositiva(paso_actual[0])
        actualizar_indicadores()
        
        if paso_actual[0] == len(diapositivas) - 1:
            boton_siguiente.text = "COMENZAR AHORA"
            boton_siguiente.bgcolor = ft.Colors.GREEN_600
            boton_siguiente.icon = ft.Icons.ROCKET_LAUNCH 
        else:
            boton_siguiente.text = "SIGUIENTE"
            boton_siguiente.bgcolor = ft.Colors.BLUE_700
            boton_siguiente.icon = None

        boton_atras.visible = paso_actual[0] > 0
        page.update()

    def avanzar(e):
        if paso_actual[0] < len(diapositivas) - 1:
            paso_actual[0] += 1
            actualizar_ui()
        else:
            al_completar_tutorial()

    def retroceder(e):
        if paso_actual[0] > 0:
            paso_actual[0] -= 1
            actualizar_ui()

    boton_siguiente.on_click = avanzar
    boton_atras.on_click = retroceder
    boton_saltar.on_click = lambda e: al_completar_tutorial()

    # --- 4. RENDERIZADO FINAL ---
    return ft.Container(
        content=ft.Column([
            ft.Container(height=60), 
            contenido_animado,       
            ft.Container(height=60), 
            indicadores,             
            ft.Container(height=40),
            ft.Row([boton_siguiente], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=10),
            ft.Row([boton_atras, boton_saltar], alignment=ft.MainAxisAlignment.CENTER, spacing=40)
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        alignment=ft.alignment.center
    )