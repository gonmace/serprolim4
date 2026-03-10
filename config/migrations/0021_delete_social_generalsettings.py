from django.db import migrations


class Migration(migrations.Migration):
    """
    Elimina GeneralSettings y Social del estado de migraciones y de la DB.
    Las tablas tienen nombres custom (wgeneralData_*) de la epoca de la app 'wgeneraldata'.
    """

    dependencies = [
        ('config', '0020_alter_social_table'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(name='Social'),
                migrations.DeleteModel(name='GeneralSettings'),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='DROP TABLE IF EXISTS "wgeneralData_social";',
                    reverse_sql='',
                ),
                migrations.RunSQL(
                    sql='DROP TABLE IF EXISTS "wgeneralData_generalsettings";',
                    reverse_sql='',
                ),
            ],
        ),
    ]
