/* =========================================
   SISTEMA DE TRADUCCIÓN (ESPAÑOL / INGLÉS)
========================================= */

const translations = {
    en: {
        "nav-about": "Why NoxSend?", "nav-how": "How it works", "nav-decrypt": "Receive File", "nav-btn-app": "Try App",
        "hero-title": "Send files without <br>leaving a trace.", 
        "hero-sub": "Share photos, videos, or sensitive docs with complete peace of mind. Everything is encrypted on your PC before hitting the internet. You have total control, we know nothing.",
        "breach-title": "Centralized clouds are not 100% reliable.",
        "breach-sub": "Giant servers get breached every day because they hold the keys to the files. If their systems fail, your data is exposed.",
        "breach-conclusion": "Are you seriously going to trust them with your most private information?",
        "eco-title": "How does it work?", "eco-sub": "Advanced security, zero hassle.",
        "card-send-label": "If you are sending", "card-send-title": "Use the PC App", 
        "card-send-desc": "Download our app. Select the file and the system encrypts it with a unique key before it even touches the internet.",
        "card-send-list": "<li>✔ Wipes hidden info (GPS, author...)</li><li>✔ Military-grade encryption</li><li>✔ You set the expiration date</li>",
        "card-receive-label": "If you are receiving", "card-receive-title": "Directly on the Web", 
        "card-receive-desc": "No installations. Open the link, enter the secret key, and download the file securely.",
        "card-receive-list": "<li>✔ No sign-ups required</li><li>✔ Decrypts right in your browser</li><li>✔ Self-destructs instantly</li>",
        "card-receive-btn": "Go unlock file", 
        "about-title": "Real privacy. <br>Your data isn't our business.",
        "about-p1": "Most clouds keep copies of everything you upload. We don't do that.", 
        "about-p2": "NoxSend was born out of the need to regain control over our privacy. Here, you are the sole owner of your information. You send it, they download it, and it's gone forever.",
        "about-quote": "If we don't have your key, it's mathematically impossible for anyone to access your data.", 
        "decrypt-title": "Unlock File", "decrypt-sub": "Paste the ID and the secret key shared with you via a secure channel.",
        "label-id": "FILE ID", "label-key": "SECRET KEY (#)", "input-id": "Paste ID here", "input-key": "Your opening key",
        "decrypt-btn": "Unlock & Download", "privacy-note": "Note: The whole process happens on your computer. We never see or store this key.",
        "footer-text": "© 2026 NOXSEND - Made in Spain 🇪🇸 to improve your security."
    },
    es: {
        "nav-about": "¿Por qué NoxSend?", "nav-how": "Cómo funciona", "nav-decrypt": "Recibir Archivo", "nav-btn-app": "Probar App",
        "hero-title": "Envía archivos sin <br>dejar rastro.", 
        "hero-sub": "Comparte fotos, vídeos o documentos sensibles con total tranquilidad. Todo se encripta en tu PC antes de salir a internet. Tú tienes el control, nosotros no sabemos nada.",
        "breach-title": "Las nubes centralizadas no son 100% fiables.",
        "breach-sub": "Todos los días se vulneran servidores gigantes porque guardan las llaves de los archivos. Si sus sistemas fallan, tus datos quedan expuestos.",
        "breach-conclusion": "¿En serio vas a confiarles tu información más privada?",
        "eco-title": "¿Cómo funciona?", "eco-sub": "Seguridad avanzada, sin complicaciones.",
        "card-send-label": "Si vas a enviar", "card-send-title": "Usa la App de PC", 
        "card-send-desc": "Descarga nuestra aplicación. Selecciona el archivo y el sistema lo encriptará con una llave única antes de que toque internet.",
        "card-send-list": "<li>✔ Limpia datos ocultos (GPS, autor...)</li><li>✔ Cifrado de grado alto</li><li>✔ Tú decides cuándo caduca</li>",
        "card-receive-label": "Si vas a recibir", "card-receive-title": "Directo en la Web", 
        "card-receive-desc": "Cero instalaciones. Abres el enlace que te pasen, introduces la llave secreta y descargas el archivo de forma segura.",
        "card-receive-list": "<li>✔ Sin necesidad de registrarte</li><li>✔ Desencriptado en tu propio navegador</li><li>✔ Se autodestruye al instante</li>",
        "card-receive-btn": "Ir a desbloquear archivo", "about-title": "Privacidad real.<br>Nuestro negocio no son tus datos.",
        "about-p1": "La mayoría de las nubes guardan copias de todo lo que subes. Nosotros no lo hacemos.", 
        "about-p2": "NoxSend nació de la necesidad de recuperar el control sobre nuestra privacidad. Aquí tú eres el único dueño de tu información. La envías, la descargan y se borra para siempre.",
        "about-quote": "Si nosotros no tenemos tu llave, es matemáticamente imposible que accedan a tus datos.", "decrypt-title": "Desbloquear Archivo", "decrypt-sub": "Pega el ID y la llave secreta que te han compartido por un canal seguro.",
        "label-id": "ID DEL ARCHIVO", "label-key": "LLAVE SECRETA (#)", "input-id": "Pega aquí el ID", "input-key": "Tu llave de apertura",
        "decrypt-btn": "Abrir y Descargar", "privacy-note": "Nota: Todo el proceso se hace en tu ordenador. Nosotros ni vemos ni guardamos esta llave.",
        "footer-text": "© 2026 NOXSEND - Hecho en España 🇪🇸 para mejorar tu seguridad."
    }
};

let currentLang = navigator.language.startsWith('es') ? 'es' : 'en';

function updateTexts() {
    const langData = translations[currentLang];
    for (let id in langData) {
        const elementoWeb = document.getElementById(id); 
        if (elementoWeb) {
            if (elementoWeb.tagName === 'INPUT') {
                elementoWeb.placeholder = langData[id];
            } else {
                elementoWeb.innerHTML = langData[id];
            }
        }
    }
}

function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'es' : 'en';
    updateTexts();
}

document.addEventListener('DOMContentLoaded', updateTexts);

/* ============================================================
   LÓGICA DE RECEPCIÓN Y DESTRUCCIÓN 100% GARANTIZADA
============================================================ */

const SUPABASE_URL = "https://bgoidqslfkiedrwrlftm.supabase.co"; 
const SUPABASE_KEY = "sb_publishable_t606hk-jApr5gyOB0wfylA_ZTQz91wI";

async function descargarYDesencriptar() {
    const idInput = document.getElementById('input-id'); 
    const keyInput = document.getElementById('input-key');
    const statusMsg = document.getElementById('decrypt-sub'); 
    const btnDecrypt = document.getElementById('decrypt-btn');

    if (!idInput || !keyInput || !statusMsg) return;

    if (!idInput.value || !keyInput.value) {
        alert(currentLang === 'es' ? "Faltan datos por rellenar." : "Missing data.");
        return;
    }

    if (btnDecrypt) {
        btnDecrypt.disabled = true;
        btnDecrypt.style.opacity = "0.5";
        btnDecrypt.innerText = currentLang === 'es' ? "Procesando..." : "Processing...";
    }

    statusMsg.innerText = currentLang === 'es' ? "Buscando en la base de datos..." : "Searching database...";
    statusMsg.style.color = "#38bdf8"; 
    
    try {
        const headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': `Bearer ${SUPABASE_KEY}`,
            'Content-Type': 'application/json'
        };

        const dbUrl = `${SUPABASE_URL}/rest/v1/archivos_seguros?id=eq.${idInput.value}`;

        // 1. COMPROBAR QUE EXISTE (Bypass de caché)
        const dbResponse = await fetch(dbUrl, { method: 'GET', headers: headers, cache: 'no-store' });
        const dbData = await dbResponse.json();

        if (!dbData || dbData.length === 0) {
            throw new Error(currentLang === 'es' ? "❌ Error: Este archivo no existe. O te han pasado mal el ID o ya se ha autodestruido." : "❌ Error: File not found or already destroyed.");
        }

        statusMsg.innerText = currentLang === 'es' ? "Archivo localizado. Ejecutando protocolo de autodestrucción..." : "File located. Initiating self-destruct protocol...";

        // 2. ORDEN DE BORRADO (DELETE) A LA BASE DE DATOS
        const deleteResponse = await fetch(dbUrl, { method: 'DELETE', headers: headers });

        if (!deleteResponse.ok) {
            const errorDetails = await deleteResponse.text();
            alert(`⚠️ ALERTA DE SEGURIDAD ⚠️\n\nSupabase ha bloqueado la orden de autodestrucción.\n\nVe a Supabase -> Table Editor -> tabla 'archivos_seguros' -> clic en RLS -> 'Disable RLS'.`);
            throw new Error("Descarga bloqueada por fallo en la autodestrucción.");
        }

        statusMsg.innerText = currentLang === 'es' ? "Rastro borrado. Descargando tu archivo..." : "Traces wiped. Downloading your file...";

        // 3. COMO SE HA BORRADO CORRECTAMENTE, AHORA SÍ ENTREGAMOS EL ARCHIVO
        const fileUrl = `${SUPABASE_URL}/storage/v1/object/public/archivos-cifrados/${idInput.value}`;
        const fileResponse = await fetch(fileUrl, { cache: 'no-store' });
        
        if (!fileResponse.ok) {
            throw new Error("El archivo no se pudo recuperar del servidor de almacenamiento.");
        }
        
        const encryptedData = await fileResponse.arrayBuffer();

        const decryptedBlob = new Blob([encryptedData], { type: "application/octet-stream" });
        const url = window.URL.createObjectURL(decryptedBlob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `noxsend_recibido_${idInput.value.substring(0,5)}.nox`;
        document.body.appendChild(a);
        a.click();
        
        window.URL.revokeObjectURL(url);
        
        statusMsg.innerText = currentLang === 'es' ? "✅ ¡Descargado! El archivo ya no existe en la nube." : "✅ Downloaded! File is wiped from the cloud.";
        statusMsg.style.color = "#4ade80"; 

    } catch (error) {
        console.error("Error:", error);
        statusMsg.innerText = error.message;
        statusMsg.style.color = "#f87171"; 
    } finally {
        if (btnDecrypt) {
            btnDecrypt.disabled = false;
            btnDecrypt.style.opacity = "1";
            btnDecrypt.innerText = currentLang === 'es' ? "Abrir y Descargar" : "Unlock & Download";
        }
    }
}