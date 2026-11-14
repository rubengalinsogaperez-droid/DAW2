<?php
require __DIR__ . '/config.php';

if (!hay_sesion()) {
    responder(200, 'No había ninguna sesión abierta');
}

$usuario = $_SESSION['usuario'];
cerrar_sesion();
responder(200, "Sesión de $usuario cerrada");
