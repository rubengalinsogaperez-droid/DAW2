<?php
require __DIR__ . '/config.php';

if (!hay_sesion()) {
    header('Location: /login.php', true, 302);
    responder(302, 'No has iniciado sesión. Redirigiendo a /login.php');
}

$_SESSION['visitas']++;

$usuario = $_SESSION['usuario'];
$visitas = $_SESSION['visitas'];
$inicio  = $_SESSION['inicio'];
$id      = session_id();
$fichero = session_save_path() . '/sess_' . $id;

responder(200, <<<TXT
Hola, $usuario.
Visitas a tu perfil en esta sesión: $visitas
Sesión iniciada a las $inicio.
Tu ID de sesión es: $id
El estado de esta sesión está guardado en el servidor, en el fichero: $fichero
TXT);
