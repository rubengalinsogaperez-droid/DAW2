<?php
// Configuración común de la sesión.
date_default_timezone_set('Europe/Madrid');

// El estado de cada sesión se guarda en el SERVIDOR, en ficheros dentro del directorio temporal
// (/tmp en el contenedor Docker).
ini_set('session.save_path', sys_get_temp_dir());
ini_set('session.use_strict_mode', '1');   // no acepta IDs de sesión inventados o caducados

session_set_cookie_params([
    'lifetime' => 0,        // cookie de sesión: se borra al cerrar el navegador
    'path'     => '/',
    'httponly' => true,     // JavaScript no puede leerla (protege frente a XSS)
    'samesite' => 'Lax',    // no se envía en peticiones iniciadas por otros sitios (protege frente a CSRF)
    // 'secure' => true,    // solo por HTTPS: lo activaremos en la UD3
]);

const USUARIOS = [
    'ana'  => '1234',
    'luis' => 'abcd',
];

// Responde en texto plano con el código de estado indicado y termina.
function responder(int $codigo, string $mensaje): void
{
    http_response_code($codigo);
    header('Content-Type: text/plain; charset=utf-8');
    echo $mensaje . "\n";
    exit;
}

// Devuelve true si el cliente trae una cookie de sesión válida con un usuario autenticado.
function hay_sesion(): bool
{
    if (!isset($_COOKIE[session_name()])) {
        return false;                       // el cliente no ha enviado cookie de sesión
    }
    // Abrimos la sesión con el ID que trae la cookie, sin que PHP envíe cookies nuevas por su cuenta:
    // aquí solo queremos LEER el estado guardado en el servidor.
    session_id($_COOKIE[session_name()]);
    session_start(['use_cookies' => 0]);
    if (empty($_SESSION['usuario'])) {      // ID inventado, caducado o de una sesión ya cerrada
        cerrar_sesion();                    // el servidor pide al cliente que borre esa cookie
        return false;
    }
    return true;
}

function cerrar_sesion(): void
{
    $_SESSION = [];
    setcookie(session_name(), '', ['expires' => time() - 3600, 'path' => '/']);
    session_destroy();
}
