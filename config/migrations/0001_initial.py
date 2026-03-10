# Migration to adopt existing generalData tables into config app.
# Uses SeparateDatabaseAndState: tables already exist (wgeneraldata_*), we only update migration state.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Social',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('facebook', models.URLField(blank=True, help_text='facebook page', null=True)),
                        ('instagram', models.URLField(blank=True, help_text='instagram', null=True)),
                        ('tiktok', models.URLField(blank=True, help_text='tiktok', null=True)),
                        ('youtube', models.URLField(blank=True, help_text='youtube channel', null=True)),
                    ],
                    options={'db_table': 'wgeneraldata_social'},
                ),
                migrations.CreateModel(
                    name='GeneralSettings',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('site_name', models.CharField(default='MultiSane', help_text='Brand name shown in titles, alt texts and meta tags (e.g., MultiSane)', max_length=100, verbose_name='Site Name')),
                        ('site_url', models.URLField(blank=True, help_text='Full canonical URL of the site (e.g., https://limpiezapozossepticos.com)', null=True, verbose_name='Site URL')),
                        ('address', models.TextField(blank=True, help_text='Business address', max_length=255, null=True, verbose_name='Address')),
                        ('lat', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                        ('lon', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                        ('tel', models.CharField(blank=True, help_text='Phone number (e.g., 3215779)', max_length=12, null=True, verbose_name='Phone')),
                        ('cel', models.CharField(blank=True, help_text='WhatsApp number (e.g., 76644033)', max_length=12, null=True, verbose_name='WhatsApp / Celular 1')),
                        ('mjeGlobo', models.CharField(blank=True, help_text='Leave blank to hide WhatsApp bubble', max_length=128, null=True, verbose_name='WhatsApp Bubble Message')),
                        ('cel2', models.CharField(blank=True, help_text='Secondary phone number', max_length=12, null=True, verbose_name='Celular 2')),
                        ('email', models.EmailField(blank=True, help_text='Contact email (e.g., contacto@tudominio.com)', max_length=255, null=True, verbose_name='Email Address')),
                        ('icon', models.FileField(blank=True, help_text='Website icon/logo (SVG, PNG, JPG)', null=True, upload_to='icons/', verbose_name='Icon')),
                        ('phone_prefix', models.CharField(default='591', help_text='Country phone prefix (e.g., 591)', max_length=5, verbose_name='Phone Prefix')),
                        ('theme', models.CharField(choices=[('serprolim', 'SerProLim (Amarillo/Verde)'), ('multisane', 'MultiSane (Emerald Green)'), ('limpio', 'Limpio (Compatible)'), ('limpio-ya', 'Limpio Ya (Logo Colors)')], default='multisane', help_text='Select the color palette for the site', max_length=50, verbose_name='Theme / Palette')),
                    ],
                    options={'db_table': 'wgeneraldata_generalsettings', 'verbose_name': 'General Settings', 'verbose_name_plural': 'General Settings'},
                ),
                migrations.CreateModel(
                    name='CountrySettings',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('country_code', models.SlugField(help_text='Unique code for the country (e.g., ar, py, bo)', max_length=5, unique=True, verbose_name='Country Code')),
                        ('name', models.CharField(help_text='Name of the country (e.g., Argentina)', max_length=100, verbose_name='Country Name')),
                        ('site_name', models.CharField(blank=True, default='MultiSane', help_text='Brand name for this country (overrides General Settings)', max_length=100, verbose_name='Site Name')),
                        ('site_url', models.URLField(blank=True, help_text='Full canonical URL for this country (e.g., https://limpiezapozossepticos.com)', null=True, verbose_name='Site URL')),
                        ('phone_prefix', models.CharField(default='591', help_text='Country phone prefix (e.g., 54)', max_length=5, verbose_name='Phone Prefix')),
                        ('address', models.TextField(blank=True, help_text='Business address for this country', max_length=255, null=True, verbose_name='Address')),
                        ('lat', models.FloatField(blank=True, null=True, verbose_name='Latitude')),
                        ('lon', models.FloatField(blank=True, null=True, verbose_name='Longitude')),
                        ('tel', models.CharField(blank=True, help_text='Phone number for this country', max_length=20, null=True, verbose_name='Phone')),
                        ('cel', models.CharField(blank=True, help_text='WhatsApp number for this country', max_length=20, null=True, verbose_name='WhatsApp / Celular 1')),
                        ('mjeGlobo', models.CharField(blank=True, help_text='Leave blank to hide WhatsApp bubble', max_length=128, null=True, verbose_name='WhatsApp Bubble Message')),
                        ('cel2', models.CharField(blank=True, help_text='Secondary phone number', max_length=20, null=True, verbose_name='Celular 2')),
                        ('email', models.EmailField(blank=True, help_text='Contact email for this country', max_length=255, null=True, verbose_name='Email Address')),
                        ('icon', models.FileField(blank=True, help_text='Website icon/logo for this country (SVG, PNG, JPG)', null=True, upload_to='icons/', verbose_name='Icon')),
                        ('theme', models.CharField(choices=[('serprolim', 'SerProLim (Amarillo/Verde)'), ('multisane', 'MultiSane (Emerald Green)'), ('limpio', 'Limpio (Compatible)'), ('limpio-ya', 'Limpio Ya (Logo Colors)')], default='multisane', help_text='Select the color palette for this country', max_length=50, verbose_name='Theme / Palette')),
                        ('facebook', models.URLField(blank=True, help_text='facebook page', null=True)),
                        ('instagram', models.URLField(blank=True, help_text='instagram', null=True)),
                        ('tiktok', models.URLField(blank=True, help_text='tiktok', null=True)),
                        ('youtube', models.URLField(blank=True, help_text='youtube channel', null=True)),
                    ],
                    options={'db_table': 'wgeneraldata_countrysettings', 'verbose_name': 'Country Settings', 'verbose_name_plural': 'Country Settings'},
                ),
            ],
            database_operations=[],  # Tables already exist from generalData
        ),
    ]
