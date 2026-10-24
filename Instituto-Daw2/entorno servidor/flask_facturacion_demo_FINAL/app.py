import re

from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "demo-facturacion"

DINERO_CERO = Decimal("0.00")
LIMITE_TRES_MIL = Decimal("3000.00")

clientes = []
facturas = []
cobros = []


def convertir_a_dinero(valor):
    """Convierte un texto o un número en un importe Decimal positivo."""
    try:
        importe = Decimal(str(valor).replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("El importe debe ser numérico") from exc

    if importe <= DINERO_CERO:
        raise ValueError("El importe debe ser mayor que cero")

    return importe.quantize(Decimal("0.01"))


def nif_valido(nif):
    nif = str(nif).strip().upper()
    return len(nif) == 9 and nif[:8].isdigit() and nif[8].isalpha()


def calcular_total_cobrado(factura_id):
    total = DINERO_CERO
    for cobro in cobros:
        if cobro["factura_id"] == factura_id:
            total += cobro["importe"]
    return total


def resumen_factura(factura):
    cobrado = calcular_total_cobrado(factura["id"])
    pendiente = factura["total"] - cobrado

    if pendiente == DINERO_CERO:
        estado = "PAGADA"
    elif cobrado > DINERO_CERO:
        estado = "PARCIAL"
    else:
        estado = "PENDIENTE"

    return {
        "cobrado": cobrado,
        "pendiente": pendiente,
        "estado": estado,
    }

def busqueda_cliente(cliente_id):
    return next((c for c in clientes if c["id"] == cliente_id), None)

def busqueda_cliente_expandida(cliente_id):
    for cliente in clientes:
        if cliente["id"] == cliente_id:
            return cliente
    return None


def cargar_datos_demo():

    clientes = [{"id": 1, "nombre": "Ada Lovelace", "nif": "12345678A", "email": "ada@ejemplo.es",},
                {"id": 2, "nombre": "Alan Turing", "nif": "87654321B","email": "alan@ejemplo.es",},
                {"id": 3, "nombre": "Grace Hopper", "nif": "23456789C","email": "grace@ejemplo.es",},
                {"id": 4, "nombre": "Tim Berners-Lee", "nif": "34567890D","email": "tim@ejemplo.es",},
                {"id": 5, "nombre": "Linus Torvalds", "nif": "45678901E","email": "linus@ejemplo.es",},
                {"id": 6, "nombre": "Margaret Hamilton", "nif": "56789012F","email": "margaret@ejemplo.es",},
                ]

    facturas = [{"id": 101, "cliente_id": 1, "concepto": "Desarrollo de portal web y despliegue inicial", "fecha": date(2026, 9, 15), "total": Decimal("1250.00"),},
                {"id": 102, "cliente_id": 2, "concepto": "Mantenimiento mensual", "fecha": date(2026, 9, 18), "total": Decimal("300.00"),}]

    cobros = [{"id": 501, "factura_id": 101, "fecha": date(2026, 9, 20), "importe": Decimal("400.00"), },
                {"id": 502, "factura_id": 101, "fecha": date(2026, 9, 21), "importe": Decimal("850.00"),},]
    
    return clientes, facturas, cobros


clientes, facturas, cobros = cargar_datos_demo()


@app.route("/")
def index():
    facturas_con_resumen = []
    for factura in facturas:
        cliente = busqueda_cliente(factura["cliente_id"])
        cliente_nombre = cliente["nombre"]
        cliente_nif = cliente["nif"]

        facturas_con_resumen.append({
            'id': factura["id"],
            'cliente_id': factura["cliente_id"],
            'concepto': factura["concepto"],
            'fecha': factura["fecha"],
            'total': factura["total"],
            'resumen': resumen_factura(factura),
            'cliente_nombre': cliente_nombre,
            'nif_cliente': cliente_nif,
        })

    return render_template(
        "index.html",
        clientes=clientes,
        facturas=facturas_con_resumen,
        criterios=[
            "Se reconocen mecanismos de generación de páginas web a partir de plantillas",
            "Se identifican tecnologías principales asociadas",
            "Se utiliza HTML con etiquetas y contenido dinámico",
            "Se reconoce la sintaxis del lenguaje de programación",
            "Se usan sentencias condicionales y bucles",
            "Se usan variables y operadores",
            "Se aplican reglas de negocio y validaciones",
        ],
    )


@app.route("/clientes", methods=["GET", "POST"])
def clientes_view():
    if request.method == "POST":
        try:
            cliente_id = int(request.form["id"])
            nombre = request.form["nombre"].strip()
            nif = request.form["nif"].strip().upper()
            email = request.form["email"].strip().lower()

            if not cliente_id > 0:
                raise ValueError("El identificador del cliente debe ser un número positivo")
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                raise ValueError("El email debe tener el formato correcto")
            if not nombre:
                raise ValueError("El nombre es obligatorio")
            if not nif_valido(nif):
                raise ValueError("El NIF debe tener ocho cifras y una letra")
            if not email:
                raise ValueError("El email es obligatorio")
            if cliente_id in clientes:
                raise ValueError("Ya existe ese identificador")
            if any(c["nif"] == nif for c in clientes):
                raise ValueError("Ese NIF ya existe")
            if any(c["email"] == email for c in clientes):
                raise ValueError("Ese email ya existe")

            clientes.append({
                "id": cliente_id,
                "nombre": nombre,
                "nif": nif,
                "email": email,
            })
        except ValueError as error:
            return render_template(
                "clientes.html",
                clientes=clientes,
                error=str(error),
            )

    return render_template("clientes.html", clientes=clientes, error=None)

@app.route("/clientes/<int:cliente_id>")
def cliente_detalle(cliente_id):
    cliente = busqueda_cliente(cliente_id)
    
    # numero_facturas = 0
    # for factura in facturas:
    #     if factura["cliente_id"] == cliente_id:
    #         numero_facturas += 1
    # total_facturas = 0
    # total_pendiente = 0 # Se puede reutilizar resumen_factura
    # for factura in facturas:
    #     if factura["cliente_id"] == cliente_id:
    #         # numero_facturas += 1
    #         total_facturas += factura["total"]
    #         total_pendiente += factura["pendiente"]

    numero_facturas = sum(1 for factura in facturas if factura["cliente_id"] == cliente_id)
    total_facturas = sum(f["total"] for f in facturas if f["cliente_id"] == cliente_id)
    total_pendiente = sum(resumen_factura(f)["pendiente"] for f in facturas if f["cliente_id"] == cliente_id)

    if cliente is None:
        return render_template(
            "cliente_detalle.html",
            cliente_nombre=None,
            numero_facturas=numero_facturas,
            total_facturas=total_facturas,
            total_pendiente=total_pendiente,
            error="Cliente no encontrado",
        )
    else:
        return render_template(
            "cliente_detalle.html",
            cliente_nombre=cliente["nombre"],
            numero_facturas=numero_facturas,
            total_facturas=total_facturas,
            total_pendiente=total_pendiente,
            error=None,
        )

@app.route("/clientes_eliminar/<int:cliente_id>")
def cliente_eliminar(cliente_id):
    cliente = busqueda_cliente(cliente_id)
    if cliente:
        encontrado = False
        for factura in facturas:
            if factura["cliente_id"] == cliente_id:
                encontrado = True
                break
        if encontrado:
            return render_template("clientes.html", clientes=clientes, error="No se puede eliminar el cliente porque tiene facturas asociadas")
        else:
            clientes.remove(cliente)
            return render_template("clientes.html", clientes=clientes, error=None, message="Cliente eliminado correctamente")

        # ALTERNATIVA COMPACTADA
        # if any(f["cliente_id"] == cliente_id for f in facturas):
        #     return render_template("clientes.html", clientes=clientes, error="No se puede eliminar el cliente porque tiene facturas asociadas")
        # else:
        #     clientes.remove(cliente)
        #     return render_template("clientes.html", clientes=clientes, error=None, message="Cliente eliminado correctamente")
    else:
        return render_template("clientes.html", clientes=clientes, error="Cliente no encontrado")


@app.route("/clientes_buscar", methods=['POST', 'GET'])
def clientes_buscar_view():
    if request.method == 'POST':
        cliente_name = request.form['nombre']
        print(f"Buscando clientes con nombre: {cliente_name}")
        clientes_encontrados = []
        for cliente in clientes:
            if cliente_name.lower() in cliente['nombre'].lower():
                clientes_encontrados.append(cliente)
        return render_template("clientes_buscar.html", clientes=clientes_encontrados, error=None)

    return render_template("clientes_buscar.html", clientes=[], error=None)



@app.route("/facturas", methods=["GET", "POST"])
def facturas_view():
    if request.method == "POST":
        try:
            factura_id = int(request.form["id"])
            cliente_id = int(request.form["cliente_id"])
            concepto = request.form["concepto"].strip()
            fecha_texto = request.form["fecha"]
            total = request.form["total"]

            if any(f["id"] == factura_id for f in facturas):
                raise ValueError("La factura ya existe")
            if not any(c["id"] == cliente_id for c in clientes):
                raise ValueError("Debe seleccionar un cliente válido")
            if not concepto:
                raise ValueError("El concepto es obligatorio")
            # no permitir facturas con fecha futura
            if date.fromisoformat(fecha_texto) > date.today():
                raise ValueError("La fecha de la factura no puede ser futura")
            if convertir_a_dinero(total) < 0:
                raise ValueError("El total de la factura no puede ser negativo")

            factura = {
                "id": factura_id,
                "cliente_id": cliente_id,
                "concepto": concepto,
                "fecha": date.fromisoformat(fecha_texto),
                "total": convertir_a_dinero(total),
            }
            facturas.append(factura)
        except (ValueError, TypeError) as error:
            return render_template(
                "facturas.html",
                clientes=clientes,
                facturas=[
                    {**factura, "resumen": resumen_factura(factura)}
                    for factura in facturas
                ],
                error=str(error),
            )

    facturas_con_resumen = [
        {
            **factura,
            "resumen": resumen_factura(factura),
            "cliente_nombre": next((c["nombre"] for c in clientes if c["id"] == factura["cliente_id"]), ""),
        }
        for factura in facturas
    ]
    return render_template(
        "facturas.html",
        clientes=clientes,
        facturas=facturas_con_resumen,
        error=None,
    )

@app.route("/facturas/<int:factura_id>", methods=["GET"])
def factura_detalle(factura_id):
    factura = next((f for f in facturas if f["id"] == factura_id), None)
    try:
        if not factura:
            raise ValueError("Factura no encontrada")
        return render_template(
            "factura_detalle.html",
            factura=factura,
            estado_factura=resumen_factura(factura),
            cliente_nombre=next((c["nombre"] for c in clientes if c["id"] == factura["cliente_id"]), ""),
        )
    except ValueError as error:
        return render_template(
            "factura_detalle.html",
            factura=None,
            cliente_nombre="",
            error=str(error),
        )


@app.route("/cobros", methods=["GET", "POST"])
def cobros_view():
    if request.method == "POST":
        try:
            cobro_id = int(request.form["id"])
            factura_id = int(request.form["factura_id"])
            fecha_texto = request.form["fecha"]
            importe = request.form["importe"]

            if cobro_id in cobros:
                raise ValueError("Ese cobro ya existe")
            if not any(f["id"] == factura_id for f in facturas):
                raise ValueError("La factura indicada no existe")

            importe_validado = convertir_a_dinero(importe)
            pendiente = next(f["total"] for f in facturas if f["id"] == factura_id) - calcular_total_cobrado(factura_id)
            if importe_validado > pendiente:
                raise ValueError(f"El cobro supera el pendiente de {pendiente:.2f} €")
            # no permitir cobros con importe cero
            if importe_validado <= 0:
                raise ValueError("El importe del cobro no puede ser cero o negativo")

            cobros.append({
                "id": cobro_id,
                "factura_id": factura_id,
                "fecha": date.fromisoformat(fecha_texto),
                "importe": importe_validado,
            })
        except (ValueError, TypeError) as error:
            return render_template(
                "cobros.html",
                facturas=[
                    {**factura, "resumen": resumen_factura(factura)}
                    for factura in facturas
                ],
                cobros=list(cobros.values()),
                error=str(error),
            )

    return render_template(
        "cobros.html",
        facturas=[
            {**factura, "resumen": resumen_factura(factura)}
            for factura in facturas
        ],
        cobros=cobros,
        error=None,
    )

@app.route("/cobro_detalle/<int:cobro_id>")
def cobro_detalle_view(cobro_id):
    cobro = next((c for c in cobros if c["id"] == cobro_id), None)
    if not cobro:
        return render_template("cobro_detalle.html", 
                               cobro=None, 
                               error="No se encontró el cobro")
    return render_template("cobro_detalle.html", 
                           cobro=cobro, 
                           error=None)

@app.route("/ra2")
def ra2_evaluacion():
    criterios = [
        {
            "id": "a",
            "texto": "Se reconocen mecanismos de generación de páginas web a partir de plantillas con Flask y Jinja2",
        },
        {
            "id": "b",
            "texto": "Se identifican las principales tecnologías asociadas al desarrollo web en servidor",
        },
        {
            "id": "c",
            "texto": "Se utiliza HTML con etiquetas y contenido dinámico para renderizar datos de la aplicación",
        },
        {
            "id": "d",
            "texto": "Se reconoce la sintaxis del lenguaje de programación y la separación entre lógica y vista",
        },
        {
            "id": "e",
            "texto": "Se usan sentencias condicionales, bucles y estructuras de control para resolver el flujo de la aplicación",
        },
        {
            "id": "f",
            "texto": "Se utilizan variables, operadores y funciones para modificar el comportamiento de la aplicación",
        },
        {
            "id": "g",
            "texto": "Se usan tipos y colecciones para guardar clientes, facturas y cobros y evitar duplicados",
        },
        {
            "id": "h",
            "texto": "Se identifican los ámbitos de uso de las variables y las restricciones del dominio de negocio",
        },
    ]

    ejemplos = [
        "@app.route('/clientes')",
        "if request.method == 'POST':",
        "for factura in facturas.values():",
        "pendiente = factura['total'] - calcular_total_cobrado(factura['id'])",
        "clientes[cliente_id] = {'id': cliente_id, 'nombre': nombre, 'nif': nif, 'email': email}",
    ]

    return render_template("ra2_evaluacion.html", criterios=criterios, ejemplos=ejemplos)


@app.route("/reset")
def reset_demo():
    global clientes, facturas, cobros
    clientes, facturas, cobros = cargar_datos_demo()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
