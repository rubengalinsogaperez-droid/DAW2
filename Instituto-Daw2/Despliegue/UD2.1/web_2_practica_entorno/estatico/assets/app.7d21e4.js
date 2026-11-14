// CSR: el HTML de los productos se construye AQUÍ, en el navegador,
// después de descargar este fichero y pedir los datos a la API.
fetch("/api/productos")
  .then((r) => r.json())
  .then((productos) => {
    const filas = productos.map((p) => `<li>${p.nombre}: ${p.precio} €</li>`).join("");
    document.getElementById("app").innerHTML = `<h1>Productos</h1><ul>${filas}</ul>`;
  });
