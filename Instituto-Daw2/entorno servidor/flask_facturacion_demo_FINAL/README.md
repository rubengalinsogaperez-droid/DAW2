# Demo Flask de facturación

Ejemplo pequeño basado en el cuaderno de Python para mostrar la lógica de clientes, facturas y cobros con Flask y Jinja.

## Requisitos

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar

```bash
flask --app app run --debug
```

## Ruta principal

- `/`: resumen del ejemplo y relación con los criterios RA2
- `/clientes`: alta de clientes
- `/facturas`: creación de facturas
- `/cobros`: registro de cobros
- `/reset`: reinicia los datos de demostración
