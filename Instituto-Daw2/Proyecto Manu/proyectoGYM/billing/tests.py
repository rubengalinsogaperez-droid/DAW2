from django.test import TestCase
from django.urls import reverse
from .models import Cliente, Cobro, Factura


class ClienteCreateViewTests(TestCase):
    def test_create_cliente(self):
        url = reverse('cliente_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_create_update.html')

        response = self.client.post(url, {
            'nombre': 'Ada',
            'apellidos': 'Lovelace',
            'nif': 'TEST-123',
            'email': 'ada@example.com',
        })

        self.assertTrue(Cliente.objects.filter(nif='TEST-123').exists())
        cliente = Cliente.objects.get(nif='TEST-123')
        self.assertRedirects(
            response,
            reverse('cliente_update', kwargs={'pk': cliente.pk}),
        )

    def test_update_cliente(self):
        cliente = Cliente.objects.create(
            nombre='Ada',
            apellidos='Lovelace',
            nif='TEST-456',
            email='ada.update@example.com',
        )
        url = reverse('cliente_update', kwargs={'pk': cliente.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_create_update.html')

        response = self.client.post(url, {
            'nombre': 'Ada',
            'apellidos': 'Byron',
            'nif': 'TEST-456',
            'email': 'ada.update@example.com',
        })

        self.assertRedirects(
            response,
            reverse('cliente_update', kwargs={'pk': cliente.pk}),
        )
        cliente.refresh_from_db()
        self.assertEqual(cliente.apellidos, 'Byron')

    def test_delete_cliente(self):
        cliente = Cliente.objects.create(
            nombre='Ada',
            apellidos='Lovelace',
            nif='TEST-789',
            email='ada.delete@example.com',
        )
        url = reverse('cliente_delete', kwargs={'pk': cliente.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_confirm_delete.html')
        # UD4.2.e: La vista aporta el contexto de confirmación de borrado.
        self.assertEqual(response.context['titulo'], 'Eliminar cliente')
        self.assertContains(
            response,
            f'<h2>Eliminar cliente: {cliente}</h2>',
            html=True,
        )
        self.assertEqual(
            response.context['mensaje_confirmación'],
            '¿Seguro que quieres eliminar este cliente? '
            'Esta acción no se puede deshacer.',
        )

        response = self.client.post(url)
        self.assertRedirects(response, reverse('cliente_list'))
        self.assertFalse(Cliente.objects.filter(pk=cliente.pk).exists())

    def test_delete_cliente_with_facturas_shows_error(self):
        cliente = Cliente.objects.create(
            nombre='Ada',
            apellidos='Lovelace',
            nif='TEST-987',
            email='ada.factura@example.com',
        )
        Factura.objects.create(
            cliente=cliente,
            numero='FAC-987',
            concepto='Cuota mensual',
        )
        url = reverse('cliente_delete', kwargs={'pk': cliente.pk})

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('cliente_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {cliente}.',
        )
        self.assertTrue(Cliente.objects.filter(pk=cliente.pk).exists())


class ClienteListOrderingTests(TestCase):
    def test_ordering_parameter_uses_cliente_primary_key(self):
        primero = Cliente.objects.create(
            nombre='Primero',
            apellidos='Zeta',
            nif='ORDER-1',
            email='primero@example.com',
        )
        segundo = Cliente.objects.create(
            nombre='Segundo',
            apellidos='Alfa',
            nif='ORDER-2',
            email='segundo@example.com',
        )

        asc_response = self.client.get(
            reverse('cliente_list'),
            {'ordering': 'asc'},
        )
        desc_response = self.client.get(
            reverse('cliente_list'),
            {'ordering': 'desc'},
        )

        self.assertEqual(
            [cliente.pk for cliente in asc_response.context['object_list']],
            [primero.pk, segundo.pk],
        )
        self.assertEqual(
            [cliente.pk for cliente in desc_response.context['object_list']],
            [segundo.pk, primero.pk],
        )


class FacturaViewTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(
            nombre='Ada',
            apellidos='Lovelace',
            nif='FACT-CLIENT',
            email='ada.factura.test@example.com',
        )

    def test_create_factura(self):
        url = reverse('factura_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_create_update.html')
        self.assertContains(response, 'Crear factura')

        response = self.client.post(url, {
            'cliente': self.cliente.pk,
            'numero': 'FAC-CREATE',
            'concepto': 'Cuota mensual',
            'fecha': '2026-01-15',
            'total': '25.00',
        })

        factura = Factura.objects.get(numero='FAC-CREATE')
        self.assertRedirects(
            response,
            reverse('factura_update', kwargs={'pk': factura.pk}),
        )

    def test_update_factura(self):
        factura = Factura.objects.create(
            cliente=self.cliente,
            numero='FAC-UPDATE',
            concepto='Cuota mensual',
            total='25.00',
        )
        url = reverse('factura_update', kwargs={'pk': factura.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_create_update.html')
        self.assertContains(response, 'Actualizar factura')

        response = self.client.post(url, {
            'cliente': self.cliente.pk,
            'numero': 'FAC-UPDATE',
            'concepto': 'Cuota anual',
            'fecha': '2026-01-15',
            'total': '250.00',
        })

        self.assertRedirects(response, url)
        factura.refresh_from_db()
        self.assertEqual(factura.concepto, 'Cuota anual')

    def test_delete_factura(self):
        factura = Factura.objects.create(
            cliente=self.cliente,
            numero='FAC-DELETE',
            concepto='Cuota mensual',
        )
        url = reverse('factura_delete', kwargs={'pk': factura.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_confirm_delete.html')
        self.assertContains(response, str(factura))

        response = self.client.post(url)

        self.assertRedirects(response, reverse('factura_list'))
        self.assertFalse(Factura.objects.filter(pk=factura.pk).exists())

    def test_delete_factura_with_cobros_shows_error(self):
        factura = Factura.objects.create(
            cliente=self.cliente,
            numero='FAC-COBRO',
            concepto='Cuota mensual',
        )
        Cobro.objects.create(factura=factura, importe='10.00')
        url = reverse('factura_delete', kwargs={'pk': factura.pk})

        response = self.client.post(url, follow=True)

        self.assertRedirects(response, reverse('factura_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {factura}.',
        )
        self.assertTrue(Factura.objects.filter(pk=factura.pk).exists())


class CobroViewTests(TestCase):
    def setUp(self):
        cliente = Cliente.objects.create(
            nombre='Grace',
            apellidos='Hopper',
            nif='COBRO-CLIENT',
            email='grace.cobro.test@example.com',
        )
        self.factura = Factura.objects.create(
            cliente=cliente,
            numero='COBRO-FACTURA',
            concepto='Cuota mensual',
            total='50.00',
        )

    def test_create_cobro(self):
        url = reverse('cobro_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_create_update.html')
        self.assertContains(response, 'Crear cobro')

        response = self.client.post(url, {
            'factura': self.factura.pk,
            'fecha': '2026-01-15',
            'importe': '25.00',
        })

        cobro = Cobro.objects.get(factura=self.factura, importe='25.00')
        self.assertRedirects(
            response,
            reverse('cobro_update', kwargs={'pk': cobro.pk}),
        )

    def test_create_cobro_cannot_exceed_invoice_total(self):
        Cobro.objects.create(factura=self.factura, importe='30.00')

        response = self.client.post(reverse('cobro_create'), {
            'factura': self.factura.pk,
            'fecha': '2026-01-15',
            'importe': '25.00',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'La suma de los importes de los cobros no puede superar '
            'el importe de la factura.',
            response.context['form'].errors['importe'],
        )
        self.assertEqual(Cobro.objects.filter(factura=self.factura).count(), 1)

    def test_update_cobro(self):
        cobro = Cobro.objects.create(factura=self.factura, importe='25.00')
        Cobro.objects.create(factura=self.factura, importe='20.00')
        url = reverse('cobro_update', kwargs={'pk': cobro.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_create_update.html')
        self.assertContains(response, 'Actualizar cobro')

        response = self.client.post(url, {
            'factura': self.factura.pk,
            'fecha': '2026-01-15',
            'importe': '31.00',
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'La suma de los importes de los cobros no puede superar '
            'el importe de la factura.',
            response.context['form'].errors['importe'],
        )
        cobro.refresh_from_db()
        self.assertEqual(cobro.importe, 25)

    def test_update_cobro_does_not_count_its_old_amount_twice(self):
        cobro = Cobro.objects.create(factura=self.factura, importe='25.00')
        url = reverse('cobro_update', kwargs={'pk': cobro.pk})

        response = self.client.post(url, {
            'factura': self.factura.pk,
            'fecha': '2026-01-15',
            'importe': '30.00',
        })

        self.assertRedirects(response, url)
        cobro.refresh_from_db()
        self.assertEqual(cobro.importe, 30)

    def test_delete_cobro(self):
        cobro = Cobro.objects.create(factura=self.factura, importe='25.00')
        url = reverse('cobro_delete', kwargs={'pk': cobro.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_confirm_delete.html')
        self.assertContains(response, str(cobro))

        response = self.client.post(url)

        self.assertRedirects(response, reverse('cobro_list'))
        self.assertFalse(Cobro.objects.filter(pk=cobro.pk).exists())
