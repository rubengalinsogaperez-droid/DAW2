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

### CAMBIO:
Añade una ruta nueva, junto con una plantilla y un enlace en la barra de navegación, para la búsqueda de clientes por nombre o por DNI.

### CAMBIO:
Borrado de cliente
