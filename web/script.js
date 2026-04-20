/* =========================================
   SISTEMA DE TRADUCCIÓN (ESPAÑOL / INGLÉS)
========================================= */

// 1. Aquí guardamos todos los textos de la web. 
// Cada frase tiene un ID (ej: "hero-title") que luego buscaremos en el HTML.
const translations = {
    en: {
        "nav-about": "Why NoxSend?", "nav-how": "How to use", "nav-decrypt": "Receive File", "nav-btn-app": "Try App",
        "hero-title": "Send files without <br>leaving a trace.", 
        "hero-sub": "Share photos, videos, and documents with the certainty that your files are shielded. Thanks to our source-encryption technology, you maintain total control.",
        "hero-btn": "Download for Desktop", 
        "breach-title": "No centralized cloud is 100% secure.",
        "breach-sub": "Millions of accounts and private files have been exposed because servers held the users' 'keys'.",
        "breach-conclusion": "Are you going to trust them with your most sensitive documents?",
        "eco-title": "How does it work?", "eco-sub": "It's so simple it doesn't even feel like security tech.",
        "card-send-label": "If you are sending", "card-send-title": "Use our App", 
        "card-send-desc": "Download our desktop application. It takes care of cleaning and locking your files before they even leave your computer.",
        "card-send-list": "<li>✔ Wipes hidden info (GPS, author...)</li><li>✔ Locks file with a unique 'key'</li><li>✔ You decide when it's deleted</li>",
        "card-send-btn": "Download App", "card-receive-label": "If you are receiving", "card-receive-title": "Use this Web", 
        "card-receive-desc": "No need to install anything. Just open the link you were sent and NoxSend will open the file directly on your screen.",
        "card-receive-list": "<li>✔ No installs or sign-ups</li><li>✔ Files open securely in browser</li><li>✔ Self-destructs after download</li>",
        "card-receive-btn": "Go to Receiving Panel", "about-title": "Uncompromising Privacy. <br>We are your 'blind spot.'",
        "about-p1": "Most cloud services keep copies of what you send. We don't.", 
        "about-p2": "NoxSend was created to keep your private documents private. By using local processing, your file's trail is erased before anyone else can see it.",
        "about-quote": "If we can't see your data, no one can steal it from us.", "decrypt-title": "Recover File", "decrypt-sub": "Enter the code you were given to open the package.",
        "label-id": "File ID", "label-key": "Secret Code (#)", "input-id": "Paste link or ID here", "input-key": "Opening key",
        "decrypt-btn": "Decrypt & Download", "privacy-note": "Privacy Note: Decryption happens entirely in your browser.",
        "footer-text": "© 2026 NOXSEND - Made in Spain 🇪🇸 for a world without spies."
    },
    es: {
        "nav-about": "¿Por qué NoxSend?", "nav-how": "Cómo se usa", "nav-decrypt": "Recibir archivo", "nav-btn-app": "Probar App",
        "hero-title": "Envía archivos sin <br>dejar ni rastro.", 
        "hero-sub": "Comparte fotos, vídeos y documentos con la certeza de que tus archivos están blindados. Gracias a nuestra tecnología, tú mantienes el control total.",
        "hero-btn": "Descargar para ordenador", 
        "breach-title": "Ninguna nube centralizada es 100% segura.",
        "breach-sub": "Millones de cuentas y archivos privados han sido expuestos porque los servidores guardaban las 'llaves' de los usuarios.",
        "breach-conclusion": "¿Vas a confiarles tus documentos más sensibles?",
        "eco-title": "¿Cómo funciona?", "eco-sub": "Es tan sencillo que no parece tecnología de seguridad.",
        "card-send-label": "Si tú envías", "card-send-title": "Usa nuestra App", 
        "card-send-desc": "Bájate nuestra aplicación para ordenador. Ella se encarga de limpiar y cerrar con llave tus archivos antes de que salgan de casa.",
        "card-send-list": "<li>✔ Borra datos ocultos (GPS, autor...)</li><li>✔ Cierra el archivo con una 'llave'</li><li>✔ Tú decides cuándo se borra</li>",
        "card-send-btn": "Descargar App", "card-receive-label": "Si tú recibes", "card-receive-title": "Usa esta Web", 
        "card-receive-desc": "No tienes que instalar nada. Solo abre el enlace y NoxSend abrirá el archivo directamente en tu pantalla.",
        "card-receive-list": "<li>✔ Sin instalaciones ni registros</li><li>✔ Apertura segura en el navegador</li><li>✔ Se autodestruye al terminar</li>",
        "card-receive-btn": "Ir al panel de recepción", "about-title": "Privacidad sin compromisos. <br>Somos tu 'punto ciego'.",
        "about-p1": "La mayoría de los servicios en la nube conservan copias de lo que envías. Nosotros no.", 
        "about-p2": "NoxSend nació para que tus documentos sigan siendo privados. El rastro de tu archivo se borra antes de que nadie pueda verlo.",
        "about-quote": "Si nosotros no podemos ver tus datos, nadie puede robárnoslos.", "decrypt-title": "Recuperar Archivo", "decrypt-sub": "Escribe el código que te han pasado para abrir el paquete.",
        "label-id": "ID del archivo", "label-key": "Código Secreto (#)", "input-id": "Pega aquí el enlace o ID", "input-key": "Llave de apertura",
        "decrypt-btn": "Abrir y Descargar", "privacy-note": "Nota: Todo ocurre en tu equipo. Nosotros nunca vemos la llave.",
        "footer-text": "© 2026 NOXSEND - Hecho en España 🇪🇸 para un mundo sin espías."
    }
};

// 2. Miramos el idioma del navegador del usuario. Si es español, lo ponemos en 'es', si no, por defecto en 'en' (inglés).
let currentLang = navigator.language.startsWith('es') ? 'es' : 'en';

// 3. Función que recorre el diccionario y cambia los textos en la pantalla
function updateTexts() {
    // Cogemos el bloque de textos del idioma actual (español o inglés)
    const langData = translations[currentLang];
    
    // Recorremos todos los IDs que tenemos guardados
    for (let id in langData) {
        const elementoWeb = document.getElementById(id); // Buscamos la etiqueta en el HTML
        
        // Si el elemento existe en el HTML, le cambiamos el texto
        if (elementoWeb) {
            // Si es un input (como la caja de poner contraseñas), cambiamos el texto "fantasma" (placeholder)
            if (elementoWeb.tagName === 'INPUT') {
                elementoWeb.placeholder = langData[id];
            } else {
                // Si es texto normal, metemos el texto directamente
                elementoWeb.innerHTML = langData[id];
            }
        }
    }
}

// 4. Función que se dispara cuando le damos al botón "ES / EN" en la web
function toggleLanguage() {
    // Cambia la variable: si está en 'en' pasa a 'es', y viceversa
    currentLang = currentLang === 'en' ? 'es' : 'en';
    // Llamamos a la función de arriba para aplicar los cambios
    updateTexts();
}

// 5. Arrancamos los textos correctos nada más cargar la página web
updateTexts();