# Adopt StandardPage from base app. Table base_standardpage already exists.
from django.db import migrations, models
import django.db.models.deletion
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


def migrate_content_type(apps, schema_editor):
    """Update wagtailcore_page to use home.standardpage instead of base.standardpage."""
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Page = apps.get_model('wagtailcore', 'Page')

    old_ct = ContentType.objects.filter(app_label='base', model='standardpage').first()
    new_ct = ContentType.objects.filter(app_label='home', model='standardpage').first()

    if old_ct and new_ct:
        Page.objects.filter(content_type=old_ct).update(content_type=new_ct)
        old_ct.delete()


def reverse_migrate(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Page = apps.get_model('wagtailcore', 'Page')

    old_ct = ContentType.objects.filter(app_label='base', model='standardpage').first()
    new_ct = ContentType.objects.filter(app_label='home', model='standardpage').first()

    if old_ct and new_ct:
        Page.objects.filter(content_type=new_ct).update(content_type=old_ct)


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_landingpage_search_description'),
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='StandardPage',
                    fields=[
                        ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                        ('introduction', models.TextField(blank=True, help_text='Text to describe the page')),
                        ('body', wagtail.fields.StreamField([('heading_block', wagtail.blocks.StructBlock([('heading_text', wagtail.blocks.CharBlock(form_classname='title', required=True)), ('size', wagtail.blocks.ChoiceBlock(blank=True, choices=[('', 'Select a header size'), ('h2', 'H2'), ('h3', 'H3'), ('h4', 'H4')], required=False))])), ('paragraph_block', wagtail.blocks.RichTextBlock(icon='fa-paragraph', template='blocks/paragraph_block.html')), ('image_block', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.blocks.CharBlock(required=False)), ('attribution', wagtail.blocks.CharBlock(required=False))])), ('block_quote', wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock()), ('attribute_name', wagtail.blocks.CharBlock(blank=True, label='e.g. Mary Berry', required=False))])), ('embed_block', wagtail.embeds.blocks.EmbedBlock(help_text='Insert an embed URL e.g https://www.youtube.com/embed/SGJFWirQ3ks', icon='fa-s15', template='blocks/embed_block.html'))], blank=True, use_json_field=True, verbose_name='Page body')),
                    ],
                    options={'db_table': 'base_standardpage'},
                    bases=('wagtailcore.page',),
                ),
            ],
            database_operations=[],
        ),
        migrations.RunPython(migrate_content_type, reverse_migrate),
    ]
