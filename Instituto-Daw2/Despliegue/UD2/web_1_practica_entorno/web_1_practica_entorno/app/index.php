<?php
require __DIR__ . '/config.php';

responder(200, <<<TXT
Práctica HTTP: estado y sesiones
================================
GET  /login.php    Formulario de acceso (para el navegador)
POST /login.php    Inicia sesión. Campos: usuario, password
GET  /perfil.php   Página privada: solo con sesión iniciada
GET  /logout.php   Cierra la sesión

Usuarios de prueba: ana / 1234   ·   luis / abcd
TXT);
