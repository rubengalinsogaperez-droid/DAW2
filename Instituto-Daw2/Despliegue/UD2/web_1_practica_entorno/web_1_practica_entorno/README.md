# Entorno de la práctica 2.1 — HTTP, cookies y sesiones

## Con Docker (opción recomendada)

```bash
docker compose up -d
docker compose ps
```

| Servicio | URL |
|----------|-----|
| httpbin  | http://localhost:8080 |
| sesiones | http://localhost:8000 |

Para pararlo todo: `docker compose down`

## Sin Docker (plan B)

**httpbin:** descarga el binario de tu sistema desde
https://github.com/mccutchen/go-httpbin/releases (por ejemplo `go-httpbin-windows-amd64.zip`),
descomprímelo y ejecuta:

```bash
./go-httpbin -port 8080
```

**sesiones:** necesitas PHP 8 instalado (por ejemplo, el que trae XAMPP). Desde esta carpeta:

```bash
php -S localhost:8000 -t app
```

En este caso el fichero de sesión no estará en `/tmp` del contenedor: la página `/perfil.php`
te dice la ruta exacta, y puedes abrirlo directamente con `cat` o con un editor
(en lugar de usar `docker compose exec`).

**Último recurso para las partes 1 a 4:** usa `https://httpbin.org` en lugar de `localhost:8080`.
Es un servicio público, a veces va lento o responde `503`, y muestra las cabeceras con un formato
ligeramente distinto.
