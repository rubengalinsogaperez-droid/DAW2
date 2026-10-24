# Ejercicio práctico de Flask para RA2

## Enunciado

Modifica la aplicación base de facturación para practicar los criterios del resultado de aprendizaje RA2.

La aplicación debe permitir:

1. Registrar clientes con nombre, NIF y email
2. Validar que el NIF tenga ocho cifras y una letra final
3. Guardar facturas asociadas a un cliente
4. Registrar cobros parciales o totales
5. Calcular el estado de cada factura
6. Mostrar solo las facturas pendientes
7. Mostrar una página con un resumen de los criterios RA2

Se debe usar Flask para servir la aplicación y Jinja para mostrar los datos en HTML.

## CAMBIOS 

### CAMBIO:
Añade el nombre del autor en la plantilla de la ruta raíz.

### CAMBIO: 
Añade tres clientes nuevos en la carga inicial y reinicia los datos (última opción de menú).

### CAMBIO:
Añade una nueva constante para el límite de 3000 euros, que dispara la obligación de declarar anualmente facturas que superen ese límite.

### PREGUNTA:
¿Para qué sirve la función "next"?

### CAMBIO:
En la ruta raíz, muestra también el DNI del cliente asociado a cada factura.

## CAMBIO:
Añade estas validaciones de negocio, en la creación de un cliente:
que el id del cliente sea positivo
que el email tenga formato correcto

## CAMBIO:
Crea una función reutilizable para buscar cliente por id: obtener_cliente_por_id(cliente_id)

### CAMBIO
no permitir cobrar más del importe pendiente
no permitir facturas con fecha futura
no permitir cobros con importe cero


### CAMBIO:
Añade detalle de cliente con resumen: número de facturas, total facturado, total pendiente
Añade detalle de factura, con su estado.
Añade detalle de cobro.


@app.route("/clientes/<int:cliente_id>")
def cliente_detalle(cliente_id):
    cliente = next((c for c in clientes if c["id"] == cliente_id), None)

    if cliente is None:
        return render_template(
            "clientes.html",
            clientes=clientes,
            error="Cliente no encontrado",
        )

    return render_template("cliente_detalle.html", cliente=cliente)

{% extends 'base.html' %}

{% block title %}Detalle del cliente{% endblock %}

{% block content %}
  <h1>Detalle del cliente</h1>

  <ul>
    <li><strong>Id:</strong> {{ cliente.id }}</li>
    <li><strong>Nombre:</strong> {{ cliente.nombre }}</li>
    <li><strong>NIF:</strong> {{ cliente.nif }}</li>
    <li><strong>Email:</strong> {{ cliente.email }}</li>
  </ul>

  <a href="{{ url_for('clientes_view') }}">Volver al listado</a>
{% endblock %}

<tbody>
  {% for cliente in clientes %}
    <tr>
      <td>{{ cliente.id }}</td>
      <td>{{ cliente.nombre }}</td>
      <td>{{ cliente.nif }}</td>
      <td>{{ cliente.email }}</td>
      <td>
        <a href="{{ url_for('cliente_detalle', cliente_id=cliente.id) }}">Ver detalle</a>
      </td>
    </tr>
  {% endfor %}
</tbody>

### CAMBIO:
Añade una ruta nueva, junto con una plantilla y un enlace en la barra de navegación, para la búsqueda de clientes por nombre o por DNI.

### CAMBIO:
Borrado de cliente

@app.route("/clientes/<int:cliente_id>/borrar", methods=["POST"])
def borrar_cliente(cliente_id):
    cliente = next((c for c in clientes if c["id"] == cliente_id), None)

    if cliente is None:
        return redirect(url_for("clientes_view"))

    if any(f["cliente_id"] == cliente_id for f in facturas):
        return render_template(
            "clientes.html",
            clientes=clientes,
            error="No se puede borrar un cliente con facturas asociadas",
        )

    clientes[:] = [c for c in clientes if c["id"] != cliente_id]
    return redirect(url_for("clientes_view"))



{% extends 'base.html' %}

{% block title %}Gestión de clientes{% endblock %}

{% block content %}
  <h1>Clientes</h1>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  <form method="post">
    <label for="id">Id</label>
    <input id="id" name="id" type="number" required>

    <label for="nombre">Nombre</label>
    <input id="nombre" name="nombre" required>

    <label for="nif">NIF/CIF</label>
    <input id="nif" name="nif" required>

    <label for="email">Email</label>
    <input id="email" name="email" type="email" required>

    <button type="submit">Guardar cliente</button>
  </form>

  <h2>Listado</h2>
  <table>
    <thead>
      <tr>
        <th>Id</th>
        <th>Nombre</th>
        <th>NIF/CIF</th>
        <th>Email</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      {% for cliente in clientes %}
        <tr>
          <td>{{ cliente.id }}</td>
          <td>{{ cliente.nombre }}</td>
          <td>{{ cliente.nif }}</td>
          <td>{{ cliente.email }}</td>
          <td>
            <form
              method="post"
              action="{{ url_for('borrar_cliente', cliente_id=cliente.id) }}"
              onsubmit="return confirm('¿Seguro que quieres borrar este cliente?');"
            >
              <button type="submit">Borrar</button>
            </form>
          </td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
{% endblock %}
