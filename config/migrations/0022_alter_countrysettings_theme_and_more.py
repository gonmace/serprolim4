from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0021_delete_social_generalsettings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrysettings',
            name='theme',
            field=models.CharField(choices=[('serprolim', 'SerProLim (Amarillo/Verde)'), ('multisane', 'MultiSane (Emerald Green)'), ('limpio', 'Limpio (Compatible)'), ('limpio-ya', 'Limpio Ya (Logo Colors)')], default='multisane', help_text='Select the color palette for this country', max_length=50, verbose_name='Theme / Palette'),
        ),
        # La tabla ya existe con nombre custom (wgeneralData_countrysettings).
        # Usamos SeparateDatabaseAndState para actualizar el estado sin tocar la DB.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterModelTable(
                    name='countrysettings',
                    table='wgeneraldata_countrysettings',
                ),
            ],
            database_operations=[],
        ),
    ]
