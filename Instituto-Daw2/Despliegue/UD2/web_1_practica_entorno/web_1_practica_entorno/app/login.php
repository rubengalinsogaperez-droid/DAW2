<?php
require __DIR__ . '/config.php';

$metodo = $_SERVER['REQUEST_METHOD'];

if ($metodo === 'GET') {
    header('Content-Type: text/html; charset=utf-8');
    echo <<<HTML
    <!DOCTYPE html>
    <html lang="es">
    <head><meta charset="utf-8"><title>Login</title></head>
    <body>
      <h1>Iniciar sesión</h1>
      <form method="post" action="/login.php">
        <p><label>Usuario: <input name="usuario"></label></p>
        <p><label>Contraseña: <input name="password" type="password"></label></p>
        <p><button>Entrar</button></p>
      </form>
    </body>
    </html>
    HTML;
    exit;
}

if ($metodo !== 'POST') {
    header('Allow: GET, POST');
    responder(405, "Método $metodo no permitido en /login.php");
}

$usuario  = $_POST['usuario']  ?? '';
$password = $_POST['password'] ?? '';

if (!isset(USUARIOS[$usuario]) || USUARIOS[$usuario] !== $password) {
    responder(401, 'Usuario o contraseña incorrectos');
}

// Credenciales correctas: creamos la sesión y guardamos el estado EN EL SERVIDOR.
session_start();
if (isset($_COOKIE[session_name()])) {
    session_regenerate_id(true);    // si ya traía una cookie, se cambia el ID al autenticarse
}
$_SESSION['usuario'] = $usuario;
$_SESSION['visitas'] = 0;
$_SESSION['inicio']  = date('H:i:s');

// 303 See Other: "pide /perfil.php con GET". Así, recargar la página no reenvía el formulario.
header('Location: /perfil.php', true, 303);
responder(303, 'Login correcto. Redirigiendo a /perfil.php');
