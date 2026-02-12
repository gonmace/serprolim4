from wagtail_modeladmin.options import ModelAdmin, modeladmin_register
from taggit.models import Tag


class TagAdmin(ModelAdmin):
    model = Tag
    menu_label = 'Tags'
    menu_icon = 'tag'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


modeladmin_register(TagAdmin)
