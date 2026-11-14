import django.db.models.deletion
from django.db import migrations, models


def copy_exercise_links(apps, schema_editor):
    Rutina = apps.get_model('core', 'Rutina')
    EjercicioRutina = apps.get_model('core', 'EjercicioRutina')

    EjercicioRutina.objects.bulk_create(
        EjercicioRutina(
            rutina_id=rutina.pk,
            ejercicio_id=rutina.ejercicio_id,
        )
        for rutina in Rutina.objects.all().iterator()
    )


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EjercicioRutina',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID',
                )),
                ('ejercicio', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='rutinas_asociadas',
                    to='core.ejercicio',
                )),
                ('rutina', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='ejercicios_rutina',
                    to='core.rutina',
                )),
            ],
        ),
        migrations.RunPython(copy_exercise_links, migrations.RunPython.noop),
        migrations.RenameField(
            model_name='rutina',
            old_name='serie',
            new_name='series',
        ),
        migrations.RenameField(
            model_name='rutina',
            old_name='reps',
            new_name='repeticiones',
        ),
        migrations.RemoveField(
            model_name='rutina',
            name='ejercicio',
        ),
    ]
