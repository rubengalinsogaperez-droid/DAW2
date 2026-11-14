// Servidor de aplicaciones de la práctica 2.2 (Node.js, sin dependencias).
// Genera contenido DINÁMICO: cada respuesta se calcula al recibir la petición.
const http = require("http");
const os = require("os");

const VERSION = process.env.APP_VERSION || "dev"; // viene de la imagen (ver Dockerfile)
const MENSAJE = "Hola desde la tienda";
const CORS_ORIGIN = process.env.CORS_ORIGIN || "";

let visitas = 0; // estado en MEMORIA de esta instancia (no se comparte)

const productos = [
  { id: 1, nombre: "Teclado mecánico", precio: 59.9 },
  { id: 2, nombre: "Ratón inalámbrico", precio: 24.5 },
  { id: 3, nombre: "Monitor 27 pulgadas", precio: 219.0 },
];

function json(res, codigo, datos) {
  res.writeHead(codigo, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(datos, null, 2) + "\n");
}

const servidor = http.createServer((req, res) => {
  const url = new URL(req.url, "http://localhost");

  // CORS: solo si se ha configurado un origen permitido
  if (CORS_ORIGIN) {
    res.setHeader("Access-Control-Allow-Origin", CORS_ORIGIN);
    if (req.method === "OPTIONS") {
      res.writeHead(204, {
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE",
        "Access-Control-Allow-Headers": "Content-Type",
      });
      return res.end();
    }
  }

  switch (url.pathname) {
    case "/health":
      return json(res, 200, { estado: "ok" });

    case "/api/info":
      visitas++;
      return json(res, 200, {
        servidor: os.hostname(),
        version: VERSION,
        mensaje: MENSAJE,
        hora: new Date().toISOString(),
        visitas_en_esta_instancia: visitas,
      });

    case "/api/productos":
      return json(res, 200, productos);

    case "/api/ssr": {
      // HTML renderizado en el SERVIDOR: llega ya completo al navegador
      const filas = productos.map((p) => `      <li>${p.nombre}: ${p.precio} €</li>`).join("\n");
      res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
      return res.end(`<!doctype html>
<html lang="es">
  <head><meta charset="utf-8"><title>Tienda (SSR)</title></head>
  <body>
    <h1>Productos</h1>
    <ul>
${filas}
    </ul>
    <p>Generado por ${os.hostname()} a las ${new Date().toLocaleTimeString("es-ES")}</p>
  </body>
</html>
`);
    }

    case "/api/lento": {
      // Tarda N segundos en responder (sin bloquear al resto de peticiones)
      const s = Number(url.searchParams.get("s") || 5);
      return setTimeout(() => json(res, 200, { servidor: os.hostname(), espera_s: s }), s * 1000);
    }

    case "/api/calcular": {
      // Cálculo pesado: BLOQUEA el único hilo de Node mientras dura
      const inicio = Date.now();
      while (Date.now() - inicio < 2000) {}
      return json(res, 200, { servidor: os.hostname(), calculo_ms: Date.now() - inicio });
    }

    default:
      return json(res, 404, { error: "Ruta no encontrada" });
  }
});

servidor.listen(3000, () => console.log(`miapp ${VERSION} escuchando en ${os.hostname()}:3000`));

// Al hacer "docker compose stop" llega SIGTERM: deja de aceptar peticiones,
// termina las que tenga en curso y sale (sin esto, Docker espera 10 s y lo mata).
process.on("SIGTERM", () => servidor.close(() => process.exit(0)));
