from packaging.version import parse as parse_version

from wagtail import __version__ as WAGTAIL_VERSION
from wagtail import hooks

if parse_version(WAGTAIL_VERSION) <= parse_version('2.15'):
    raise Exception('wagtailextraicons 2 requires Wagtail > 2.15')

icons = [
    'cta-with-button.svg', '2-col-paragraph.svg', 'testimonial.svg', 'multiple-items.svg',
    'person.svg', 'hidden.svg', 'map.svg', 'person-solo.svg', '2-col-lg.svg', '4-col.svg',
    'banner.svg', '2-col-video.svg', 'checkboxes.svg', '2-col-with-links.svg', 'paragraphs.svg',
    'three-items.svg', 'number.svg', 'radio.svg', 'paragraph.svg', 'tabs.svg', 'small-list.svg',
    'email.svg', 'people.svg', 'button.svg', 'image.svg', 'basic-field.svg', 'table.svg',
    'sign-up.svg', '2-col-right-small.svg', 'notice.svg', 'cta-inverted.svg', 'checkbox.svg',
    'map-and-content.svg', 'large-list.svg', 'dropdown.svg', '3-col-links.svg', 'money.svg',
    'text-box.svg', 'video.svg', 'map-pin.svg', '4-col-heading.svg', 'useful-links.svg',
    '3-col.svg', 'quote.svg', 'logos.svg', 'heading-icon.svg', 'image-gallery.svg', 'date.svg',
    'block-quote.svg', 'multi-select.svg', '2-col.svg', '2-col-heading-text.svg', 'cards.svg',
    'url.svg', 'cta.svg', 'facebook.svg', 'dribbble.svg'
]


@hooks.register('register_icons')
def register_icons(_icons):
    for icon in icons:
        _icons.append("extraicons/{}".format(icon))
    return _icons
