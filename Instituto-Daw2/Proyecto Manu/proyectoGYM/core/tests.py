from datetime import date
from io import BytesIO
from tempfile import TemporaryDirectory

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from PIL import Image

from .models import (
    Ejercicio,
    EjercicioRutina,
    Entrenamiento,
    Rutina,
    SerieEjercicioRutina,
    Usuario,
    UsuarioRutina,
)


class CoreDetailViewTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nickname='detalle',
            objetivo='ganar fuerza',
        )
        self.ejercicio = Ejercicio.objects.create(
            nombre='sentadilla',
            descripcion='Ejercicio de piernas',
            objetivo='fuerza',
        )
        self.rutina = Rutina.objects.create(nombre='piernas')
        EjercicioRutina.objects.create(
            rutina=self.rutina,
            ejercicio=self.ejercicio,
        )
        self.entrenamiento = Entrenamiento.objects.create(
            usuario=self.usuario,
            rutina=self.rutina,
            fecha=date(2026, 1, 15),
            notas='Primera sesión',
        )

    def test_detail_views_render_the_requested_objects(self):
        details = [
            ('usuario_detail', self.usuario.pk, 'detalle'),
            ('ejercicio_detail', self.ejercicio.pk, 'Ejercicio de piernas'),
            ('rutina_detail', self.rutina.pk, 'sentadilla'),
            ('entrenamiento_detail', self.entrenamiento.pk, 'Primera sesión'),
        ]

        for route_name, pk, expected_text in details:
            response = self.client.get(reverse(route_name, kwargs={'pk': pk}))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, expected_text)
            if route_name == 'usuario_detail':
                self.assertNotContains(response, 'Eliminar usuario')
            elif route_name == 'ejercicio_detail':
                self.assertNotContains(response, 'Eliminar ejercicio')
            elif route_name == 'rutina_detail':
                self.assertNotContains(response, 'Eliminar rutina')


class UsuarioCreateViewTests(TestCase):
    def test_create_form_renders_cancel_link_to_usuario_list(self):
        response = self.client.get(reverse('usuario_create'))

        self.assertEqual(response.status_code, 200)
        # UD4.2.c: En creación se muestra su título y no se ofrece borrado.
        self.assertEqual(response.context['titulo_creacion'], 'Crear usuario')
        self.assertIsNone(response.context['titulo_actualizacion'])
        self.assertIsNone(response.context['url_borrado'])
        self.assertContains(response, '<h2>Crear usuario</h2>', html=True)
        self.assertEqual(response.context['entity_name'], 'usuario')
        self.assertEqual(response.context['list_url_name'], 'usuario_list')
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, 'name="foto_perfil"')
        self.assertContains(response, 'href="/core/usuarios/"')
        self.assertNotContains(response, 'Eliminar usuario')

    def test_create_user_uploads_and_displays_profile_photo(self):
        image_buffer = BytesIO()
        Image.new('RGB', (1, 1), color='blue').save(image_buffer, format='PNG')
        image_file = SimpleUploadedFile(
            'perfil.png',
            image_buffer.getvalue(),
            content_type='image/png',
        )

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse('usuario_create'),
                    {
                        'nickname': 'con_foto',
                        'objetivo': 'salud',
                        'foto_perfil': image_file,
                    },
                )

                self.assertRedirects(response, reverse('usuario_list'))
                usuario = Usuario.objects.get(pk='con_foto')
                self.assertTrue(usuario.foto_perfil.name.startswith('perfiles/'))
                self.assertTrue(
                    usuario.foto_perfil.storage.exists(usuario.foto_perfil.name)
                )

                detail_response = self.client.get(
                    reverse('usuario_detail', kwargs={'pk': usuario.pk})
                )
                self.assertContains(detail_response, usuario.foto_perfil.url)

    def test_existing_user_can_upload_photo_from_detail(self):
        usuario = Usuario.objects.create(pk='existente', objetivo='salud')
        image_buffer = BytesIO()
        Image.new('RGB', (1, 1), color='red').save(image_buffer, format='PNG')
        image_file = SimpleUploadedFile(
            'perfil.png',
            image_buffer.getvalue(),
            content_type='image/png',
        )

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                detail_url = reverse('usuario_detail', kwargs={'pk': usuario.pk})
                detail_response = self.client.get(detail_url)
                self.assertContains(
                    detail_response,
                    reverse('usuario_update', kwargs={'pk': usuario.pk}),
                )
                update_response = self.client.get(
                    reverse('usuario_update', kwargs={'pk': usuario.pk})
                )
                # UD4.2.c: En actualización se muestra el título y el enlace de borrado.
                self.assertEqual(
                    update_response.context['titulo_actualizacion'],
                    'Actualizar usuario',
                )
                self.assertIsNone(update_response.context['titulo_creacion'])
                self.assertEqual(
                    update_response.context['url_borrado'],
                    'usuario_delete',
                )
                self.assertContains(
                    update_response,
                    '<h2>Actualizar usuario</h2>',
                    html=True,
                )
                self.assertContains(
                    update_response,
                    reverse('usuario_delete', kwargs={'pk': usuario.pk}),
                )

                response = self.client.post(
                    reverse('usuario_update', kwargs={'pk': usuario.pk}),
                    {
                        'nickname': usuario.nickname,
                        'objetivo': usuario.objetivo,
                        'foto_perfil': image_file,
                    },
                )

                self.assertRedirects(response, detail_url)
                usuario.refresh_from_db()
                self.assertTrue(usuario.foto_perfil)
                self.assertContains(self.client.get(detail_url), usuario.foto_perfil.url)


class UsuarioDeleteViewTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(pk='borrar', objetivo='salud')
        self.delete_url = reverse(
            'usuario_delete',
            kwargs={'pk': self.usuario.pk},
        )

    def test_delete_view_confirms_and_deletes_unrelated_user(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_confirm_delete.html')
        # UD4.2.e: La vista aporta título y mensaje a la plantilla común.
        self.assertEqual(response.context['titulo'], 'Eliminar usuario')
        self.assertContains(
            response,
            f'<h2>Eliminar usuario: {self.usuario}</h2>',
            html=True,
        )
        self.assertEqual(
            response.context['mensaje_confirmación'],
            '¿Seguro que quieres eliminar este usuario? '
            'Esta acción no se puede deshacer.',
        )
        self.assertContains(response, '¿Seguro que quieres eliminar')

        response = self.client.post(self.delete_url)

        self.assertRedirects(response, reverse('usuario_list'))
        self.assertFalse(Usuario.objects.filter(pk=self.usuario.pk).exists())

    def test_delete_is_blocked_when_user_has_trainings(self):
        rutina = Rutina.objects.create(nombre='rutina_borrar')
        Entrenamiento.objects.create(
            usuario=self.usuario,
            rutina=rutina,
            fecha=date(2026, 1, 15),
        )

        response = self.client.post(self.delete_url, follow=True)

        self.assertRedirects(response, reverse('usuario_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {self.usuario}.',
        )
        self.assertEqual(
            list(response.context['messages'])[0].level_tag,
            'error',
        )
        self.assertTrue(Usuario.objects.filter(pk=self.usuario.pk).exists())

    def test_delete_is_blocked_when_user_has_assigned_routines(self):
        rutina = Rutina.objects.create(nombre='rutina_asignada')
        UsuarioRutina.objects.create(usuario=self.usuario, rutina=rutina)

        response = self.client.post(self.delete_url, follow=True)

        self.assertRedirects(response, reverse('usuario_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {self.usuario}.',
        )
        self.assertTrue(Usuario.objects.filter(pk=self.usuario.pk).exists())


class EjercicioCrudViewTests(TestCase):
    def setUp(self):
        self.ejercicio = Ejercicio.objects.create(
            nombre='press',
            descripcion='Press de banca',
            objetivo='fuerza',
        )

    def test_create_exercise(self):
        response = self.client.get(reverse('ejercicio_create'))
        self.assertEqual(response.status_code, 200)
        # UD4.2.c: La vista de creación entrega el título en el contexto.
        self.assertEqual(response.context['titulo_creacion'], 'Crear ejercicio')
        self.assertIsNone(response.context['titulo_actualizacion'])
        self.assertIsNone(response.context['url_borrado'])
        self.assertContains(response, '<h2>Crear ejercicio</h2>', html=True)
        self.assertContains(response, 'enctype="multipart/form-data"')
        self.assertContains(response, 'name="imagen"')
        self.assertContains(response, '>Crear</button>')
        self.assertNotContains(response, 'Eliminar ejercicio')

        response = self.client.post(
            reverse('ejercicio_create'),
            {
                'nombre': 'sentadilla',
                'descripcion': 'Sentadilla con barra',
                'objetivo': 'fuerza',
                'mayor_peso': '',
            },
        )

        self.assertRedirects(response, reverse('ejercicio_list'))
        self.assertTrue(Ejercicio.objects.filter(pk='sentadilla').exists())

    def test_update_exercise_redirects_to_detail(self):
        url = reverse('ejercicio_update', kwargs={'pk': self.ejercicio.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        # UD4.2.c: La vista de actualización entrega el título y URL de borrado.
        self.assertEqual(
            response.context['titulo_actualizacion'],
            'Actualizar ejercicio',
        )
        self.assertIsNone(response.context['titulo_creacion'])
        self.assertEqual(response.context['url_borrado'], 'ejercicio_delete')
        self.assertContains(response, '<h2>Actualizar ejercicio</h2>', html=True)
        self.assertContains(response, '>Actualizar</button>')
        self.assertContains(
            response,
            reverse('ejercicio_delete', kwargs={'pk': self.ejercicio.pk}),
        )

        response = self.client.post(
            url,
            {
                'nombre': self.ejercicio.nombre,
                'descripcion': 'Press de banca actualizado',
                'objetivo': 'fuerza',
                'mayor_peso': '',
            },
        )

        self.assertRedirects(
            response,
            reverse('ejercicio_detail', kwargs={'pk': self.ejercicio.pk}),
        )
        self.ejercicio.refresh_from_db()
        self.assertEqual(self.ejercicio.descripcion, 'Press de banca actualizado')

    def test_renaming_exercise_replaces_old_record_and_keeps_routine(self):
        rutina = Rutina.objects.create(nombre='empuje')
        ejercicio_rutina = EjercicioRutina.objects.create(
            rutina=rutina,
            ejercicio=self.ejercicio,
        )

        response = self.client.post(
            reverse('ejercicio_update', kwargs={'pk': self.ejercicio.pk}),
            {
                'nombre': 'press inclinado',
                'descripcion': 'Press de banca actualizado',
                'objetivo': 'fuerza',
                'mayor_peso': '',
            },
        )

        self.assertRedirects(
            response,
            reverse('ejercicio_detail', kwargs={'pk': 'press inclinado'}),
        )
        self.assertFalse(Ejercicio.objects.filter(pk='press').exists())
        ejercicio_nuevo = Ejercicio.objects.get(pk='press inclinado')
        self.assertEqual(ejercicio_nuevo.descripcion, 'Press de banca actualizado')
        ejercicio_rutina.refresh_from_db()
        self.assertEqual(ejercicio_rutina.ejercicio, ejercicio_nuevo)
        self.assertEqual(Ejercicio.objects.count(), 1)

    def test_delete_unassigned_exercise(self):
        url = reverse('ejercicio_delete', kwargs={'pk': self.ejercicio.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_confirm_delete.html')

        response = self.client.post(url)

        self.assertRedirects(response, reverse('ejercicio_list'))
        self.assertFalse(Ejercicio.objects.filter(pk=self.ejercicio.pk).exists())

    def test_delete_is_blocked_when_exercise_belongs_to_a_routine(self):
        rutina = Rutina.objects.create(nombre='piernas')
        EjercicioRutina.objects.create(
            rutina=rutina,
            ejercicio=self.ejercicio,
        )

        response = self.client.post(
            reverse('ejercicio_delete', kwargs={'pk': self.ejercicio.pk}),
            follow=True,
        )

        self.assertRedirects(response, reverse('ejercicio_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {self.ejercicio}.',
        )
        self.assertTrue(Ejercicio.objects.filter(pk=self.ejercicio.pk).exists())

    def test_exercise_photo_is_rendered_in_list_and_detail(self):
        image_buffer = BytesIO()
        Image.new('RGB', (1, 1), color='green').save(image_buffer, format='PNG')

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                self.ejercicio.imagen.save(
                    'ejercicio.png',
                    SimpleUploadedFile(
                        'ejercicio.png',
                        image_buffer.getvalue(),
                        content_type='image/png',
                    ),
                    save=True,
                )

                list_response = self.client.get(reverse('ejercicio_list'))
                detail_response = self.client.get(
                    reverse(
                        'ejercicio_detail',
                        kwargs={'pk': self.ejercicio.pk},
                    )
                )

                self.assertContains(list_response, self.ejercicio.imagen.url)
                self.assertContains(detail_response, self.ejercicio.imagen.url)


class RutinaCrudViewTests(TestCase):
    def setUp(self):
        self.rutina = Rutina.objects.create(nombre='rutina_test')

    def ejercicio_formset_data(self, total_forms, initial_forms):
        return {
            'ejercicios-TOTAL_FORMS': str(total_forms),
            'ejercicios-INITIAL_FORMS': str(initial_forms),
            'ejercicios-MIN_NUM_FORMS': '0',
            'ejercicios-MAX_NUM_FORMS': '1000',
        }

    def test_create_routine(self):
        response = self.client.get(reverse('rutina_create'))
        self.assertEqual(response.status_code, 200)
        # UD4.2.c: La rutina nueva usa el título de creación de la plantilla común.
        self.assertEqual(response.context['titulo_creacion'], 'Crear rutina')
        self.assertIsNone(response.context['titulo_actualizacion'])
        self.assertIsNone(response.context['url_borrado'])
        self.assertContains(response, '<h2>Crear rutina</h2>', html=True)
        self.assertEqual(response.context['entity_name'], 'rutina')
        self.assertNotContains(response, 'Eliminar rutina')

        response = self.client.post(
            reverse('rutina_create'),
            {'nombre': 'rutina_nueva'},
        )

        self.assertRedirects(response, reverse('rutina_list'))
        self.assertTrue(Rutina.objects.filter(pk='rutina_nueva').exists())

    def test_update_routine_redirects_to_detail(self):
        response = self.client.get(
            reverse('rutina_update', kwargs={'pk': self.rutina.pk})
        )
        self.assertEqual(response.status_code, 200)
        # UD4.2.c: La actualización conserva su formset dentro de la plantilla común.
        self.assertTemplateUsed(response, 'base_create_update.html')
        self.assertEqual(
            response.context['titulo_actualizacion'],
            'Actualizar rutina',
        )
        self.assertIsNone(response.context['titulo_creacion'])
        self.assertEqual(response.context['url_borrado'], 'rutina_delete')
        self.assertContains(response, '<h2>Actualizar rutina</h2>', html=True)
        self.assertContains(response, 'Ejercicios de la rutina')
        self.assertContains(response, 'Actualizar rutina y ejercicios')
        self.assertContains(
            response,
            reverse('rutina_delete', kwargs={'pk': self.rutina.pk}),
        )

        ejercicio = Ejercicio.objects.create(
            nombre='press_rutina',
            descripcion='Press de banca',
            objetivo='fuerza',
        )
        ejercicio_rutina = EjercicioRutina.objects.create(
            rutina=self.rutina,
            ejercicio=ejercicio,
        )
        usuario = Usuario.objects.create(pk='usuario_rutina_edit', objetivo='salud')
        Entrenamiento.objects.create(
            usuario=usuario,
            rutina=self.rutina,
            fecha=date(2026, 1, 15),
        )
        UsuarioRutina.objects.create(usuario=usuario, rutina=self.rutina)
        data = self.ejercicio_formset_data(total_forms=2, initial_forms=1)
        data.update({
            'nombre': 'rutina_modificada',
            'ejercicios-0-id': str(ejercicio_rutina.pk),
            'ejercicios-0-ejercicio': ejercicio.pk,
            'ejercicios-0-tiempo': '',
            'ejercicios-1-id': '',
            'ejercicios-1-ejercicio': '',
            'ejercicios-1-tiempo': '',
        })

        response = self.client.post(
            reverse('rutina_update', kwargs={'pk': self.rutina.pk}),
            data,
        )

        self.assertRedirects(
            response,
            reverse('rutina_detail', kwargs={'pk': 'rutina_modificada'}),
        )
        rutina_modificada = Rutina.objects.get(pk='rutina_modificada')
        self.assertFalse(Rutina.objects.filter(pk='rutina_test').exists())
        self.assertEqual(
            EjercicioRutina.objects.get(pk=ejercicio_rutina.pk).rutina,
            rutina_modificada,
        )
        self.assertEqual(
            Entrenamiento.objects.get(usuario=usuario).rutina,
            rutina_modificada,
        )
        self.assertEqual(
            UsuarioRutina.objects.get(usuario=usuario).rutina,
            rutina_modificada,
        )

    def test_update_routine_can_add_exercises(self):
        ejercicio = Ejercicio.objects.create(
            nombre='sentadilla_rutina',
            descripcion='Sentadilla con barra',
            objetivo='fuerza',
        )
        response = self.client.get(
            reverse('rutina_update', kwargs={'pk': self.rutina.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ejercicios-TOTAL_FORMS')

        data = self.ejercicio_formset_data(total_forms=1, initial_forms=0)
        data.update({
            'nombre': self.rutina.nombre,
            'ejercicios-0-id': '',
            'ejercicios-0-ejercicio': ejercicio.pk,
            'ejercicios-0-tiempo': '',
        })

        response = self.client.post(
            reverse('rutina_update', kwargs={'pk': self.rutina.pk}),
            data,
        )

        self.assertRedirects(
            response,
            reverse('rutina_detail', kwargs={'pk': self.rutina.pk}),
        )
        self.assertTrue(
            EjercicioRutina.objects.filter(
                rutina=self.rutina,
                ejercicio=ejercicio,
            ).exists()
        )

    def test_edit_exercise_repetitions_and_weight(self):
        ejercicio = Ejercicio.objects.create(
            nombre='peso_muerto',
            descripcion='Peso muerto',
            objetivo='fuerza',
        )
        ejercicio_rutina = EjercicioRutina.objects.create(
            rutina=self.rutina,
            ejercicio=ejercicio,
        )
        url = reverse(
            'rutina_series_update',
            kwargs={
                'pk': self.rutina.pk,
                'ejercicio_rutina_pk': ejercicio_rutina.pk,
            },
        )

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="series-0-repeticiones"')
        self.assertContains(response, 'name="series-0-peso"')
        self.assertContains(response, 'id="add-series"')
        self.assertContains(response, '__prefix__')
        self.assertContains(response, 'Quitar esta serie')

        response = self.client.post(
            url,
            {
                'series-TOTAL_FORMS': '2',
                'series-INITIAL_FORMS': '0',
                'series-MIN_NUM_FORMS': '0',
                'series-MAX_NUM_FORMS': '1000',
                'series-0-id': '',
                'series-0-repeticiones': '8',
                'series-0-peso': '40.00',
                'series-1-id': '',
                'series-1-repeticiones': '6',
                'series-1-peso': '45.00',
            },
        )

        self.assertRedirects(
            response,
            reverse('rutina_detail', kwargs={'pk': self.rutina.pk}),
        )
        series = list(
            SerieEjercicioRutina.objects.filter(
                ejercicio_rutina=ejercicio_rutina
            ).order_by('numero')
        )
        self.assertEqual(len(series), 2)
        self.assertEqual([serie.numero for serie in series], [1, 2])
        self.assertEqual(series[0].repeticiones, 8)
        self.assertEqual(series[0].peso, 40)

        response = self.client.post(
            url,
            {
                'series-TOTAL_FORMS': '3',
                'series-INITIAL_FORMS': '2',
                'series-MIN_NUM_FORMS': '0',
                'series-MAX_NUM_FORMS': '1000',
                'series-0-id': str(series[0].pk),
                'series-0-repeticiones': '10',
                'series-0-peso': '42.00',
                'series-1-id': str(series[1].pk),
                'series-1-repeticiones': '6',
                'series-1-peso': '45.00',
                'series-2-id': '',
                'series-2-repeticiones': '',
                'series-2-peso': '',
            },
        )

        self.assertRedirects(
            response,
            reverse('rutina_detail', kwargs={'pk': self.rutina.pk}),
        )
        series[0].refresh_from_db()
        self.assertEqual(series[0].repeticiones, 10)
        self.assertEqual(series[0].peso, 42)

        response = self.client.post(
            url,
            {
                'series-TOTAL_FORMS': '3',
                'series-INITIAL_FORMS': '2',
                'series-MIN_NUM_FORMS': '0',
                'series-MAX_NUM_FORMS': '1000',
                'series-0-id': str(series[0].pk),
                'series-0-repeticiones': '10',
                'series-0-peso': '42.00',
                'series-0-DELETE': 'on',
                'series-1-id': str(series[1].pk),
                'series-1-repeticiones': '6',
                'series-1-peso': '45.00',
                'series-2-id': '',
                'series-2-repeticiones': '',
                'series-2-peso': '',
            },
        )

        self.assertRedirects(
            response,
            reverse('rutina_detail', kwargs={'pk': self.rutina.pk}),
        )
        self.assertFalse(
            SerieEjercicioRutina.objects.filter(pk=series[0].pk).exists()
        )
        self.assertTrue(
            SerieEjercicioRutina.objects.filter(pk=series[1].pk).exists()
        )

    def test_delete_unassigned_routine(self):
        url = reverse('rutina_delete', kwargs={'pk': self.rutina.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base_confirm_delete.html')

        response = self.client.post(url)

        self.assertRedirects(response, reverse('rutina_list'))
        self.assertFalse(Rutina.objects.filter(pk=self.rutina.pk).exists())

    def test_delete_routine_with_related_records_shows_error(self):
        usuario = Usuario.objects.create(pk='usuario_rutina', objetivo='salud')
        usuario_rutina = UsuarioRutina.objects.create(
            usuario=usuario,
            rutina=self.rutina,
        )
        entrenamiento = Entrenamiento.objects.create(
            usuario=usuario,
            rutina=self.rutina,
            fecha=date(2026, 1, 15),
        )

        response = self.client.post(
            reverse('rutina_delete', kwargs={'pk': self.rutina.pk}),
            follow=True,
        )

        self.assertRedirects(response, reverse('rutina_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {self.rutina}.',
        )
        self.assertTrue(Rutina.objects.filter(pk=self.rutina.pk).exists())
        self.assertTrue(Usuario.objects.filter(pk=usuario.pk).exists())
        self.assertTrue(
            UsuarioRutina.objects.filter(pk=usuario_rutina.pk).exists()
        )
        entrenamiento.refresh_from_db()
        self.assertEqual(entrenamiento.rutina, self.rutina)

    def test_delete_assigned_routine_shows_error(self):
        usuario = Usuario.objects.create(pk='usuario_asignado', objetivo='salud')
        usuario_rutina = UsuarioRutina.objects.create(
            usuario=usuario,
            rutina=self.rutina,
        )

        response = self.client.post(
            reverse('rutina_delete', kwargs={'pk': self.rutina.pk}),
            follow=True,
        )

        self.assertRedirects(response, reverse('rutina_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'Existen dependencias para el objeto {self.rutina}.',
        )
        self.assertTrue(Rutina.objects.filter(pk=self.rutina.pk).exists())
        self.assertTrue(Usuario.objects.filter(pk=usuario.pk).exists())
        self.assertTrue(
            UsuarioRutina.objects.filter(pk=usuario_rutina.pk).exists()
        )
