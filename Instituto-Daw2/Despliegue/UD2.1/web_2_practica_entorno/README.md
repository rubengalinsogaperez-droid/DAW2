# Entorno de la práctica 2.2 — Servidores web y de aplicaciones

## Con Docker (opción recomendada)

```bash
docker compose up -d --build
docker compose ps
```

| Servicio | URL | Qué es |
|----------|-----|--------|
| web | http://localhost:8080 | Nginx: sirve lo estático y reenvía `/api/` a los backends |
| app1, app2 | (sin puerto publicado) | Dos instancias de la misma aplicación Node.js (`miapp`) |
| otro-origen | http://localhost:9090 | Otra web que intenta llamar a la API (CORS) |

Contenido de la carpeta:

- `docker-compose.yml`: los cuatro servicios.
- `.env`: la versión de la imagen (`VERSION`) y el origen permitido por CORS (`CORS_ORIGIN`).
- `nginx/default.conf`: configuración de Nginx (balanceo, compresión, caché, proxy inverso).
- `estatico/`: ficheros que sirve Nginx tal cual.
- `app/`: el servidor de aplicaciones (`server.js`) y su `Dockerfile`.
- `otro-origen/`: la página de la otra web.

Para pararlo todo: `docker compose down`

> **Si cambias `nginx/default.conf`:** comprueba la sintaxis con `docker compose exec web nginx -t`
> y aplícalo sin parar el servidor con `docker compose exec web nginx -s reload`.

> **Si la API responde `502` justo después de arrancar o de parar/arrancar un backend:** espera unos
> 10 segundos. Nginx deja "en cuarentena" durante 10 s el backend que ha fallado (`fail_timeout=10s`).

## Sin Docker (plan B, parcial)

Necesitas Node.js 18 o superior. Desde la carpeta `app`:

```bash
APP_VERSION=1.0.0 node server.js
```

La aplicación queda en `http://localhost:3000` (sin Nginx delante). Con esto puedes hacer las partes 1
(cambiando `localhost:8080/api/...` por `localhost:3000/api/...`) y 4 (con `CORS_ORIGIN=http://localhost:9090`
delante del comando). Las partes 2, 3 y 5 necesitan Nginx y Docker: hazlas con un compañero.
