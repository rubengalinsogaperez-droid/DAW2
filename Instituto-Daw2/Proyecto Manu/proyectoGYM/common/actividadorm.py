from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from django.db.models import CharField, F
from django.db.models.functions import Cast
from django.utils import timezone

from billing.models import Cliente, Cobro, Factura

#nota mental, los ejercicios de manu pueden acabar con tu cordua un domigo por la noche, cojerlos con mucho mas tiempo...

def get_clientes_all():
    return Cliente.objects.all()


def get_factura_first_3():
    return Factura.objects.all()[:3]
    #tres primeras filas [:3]


def get_factura_0():
    return Factura.objects.filter(total=0)



def get_cliente_not_0612():
    return Cliente.objects.exclude(nif__startswith="74")


def get_cliente_dni_apellido():
    return Cliente.objects.filter(
        nif="92436593F",
        apellidos__icontains="Pérez",
    )


def get_cli_id_lt_2_num_fact_des():
    return Factura.objects.filter(pk__lt=2).order_by("-numero")
    #lt least than gt grater than

def get_cli_id_gt_2():
    return Cliente.objects.filter(pk__gt=2)


def get_fact_des_nom_des():
    return Factura.objects.filter(concepto__icontains="PHP").order_by("numero")


def get_fact_not_1():
    return Factura.objects.exclude(numero__endswith="1")


def get_cobro_python_id2():
    return (
        Cobro.objects.annotate(id_como_texto=Cast("pk", output_field=CharField()))
        .filter(
            factura__concepto__icontains="python",
            id_como_texto__endswith="2",
        )
        .order_by("pk")
        .first()
    )
#este necesito que me lo preguntar.profesor


def get_cobro_fact6_not_manu():
    return Cobro.objects.filter(
        factura__numero__icontains="06",
    ).exclude(factura__cliente__nombre__icontains="Manu")


def get_fact_gt_5():
    return Factura.objects.filter(total__gte=5)


def get_cobro_5_10():
    return Cobro.objects.filter(importe__range=(5, 10))


def create_cliente():
    cliente, _ = Cliente.objects.get_or_create(
        nif="12345678Z",
        defaults={
            "nombre": "Nuevo",
            "apellidos": "apellido1 apellido2",
            "email": "nuevo.12345678z@example.com",
        },
    )
    return cliente


def create_factura():
    cliente = create_cliente()
    return Factura.objects.create(
        cliente=cliente,
        numero=f"ORM-{uuid4().hex[:12].upper()}",
        concepto="Factura creada para la actividad ORM",
        fecha=timezone.localdate() - timedelta(days=1),
        total=Decimal("100.00"),
    )


def update_last_factura():
    factura = Factura.objects.order_by("-pk").first()
    if factura is None:
        return None

    factura.concepto += " (última)"
    factura.save(update_fields=["concepto"])
    return factura
    #preguntar.profesor


def update_cobro_fact2_x2():
    return Cobro.objects.filter(factura__numero__endswith="2").update(
        importe=F("importe") * 2,
    )


def update_cobro_fact1_cligonz_div2():
    return Cobro.objects.filter(
        factura__numero__endswith="1",
        factura__cliente__apellidos__icontains="González",
    ).update(importe=F("importe") * Decimal("0.5"))


def delete_cobro_fact_lt_1():
    return Cobro.objects.filter(factura__total__lt=1).delete()


def delete_cobro_cli_pablo():
    return Cobro.objects.filter(
        factura__cliente__nombre__icontains="Pablo",
    ).delete()