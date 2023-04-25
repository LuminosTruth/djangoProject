from django import template
from django.urls import resolve, reverse, Resolver404, NoReverseMatch
from menu.models import MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    current_url = context['request'].path
    menu_items = MenuItem.objects.filter(name=menu_name)

    def build_menu(menu_items, current_item=None):
        menu_html = '<ul>'
        for item in menu_items:
            active_class = ''
            if urlnamed_exists(item.url):
                if reverse(item.url) == current_url:
                    active_class = 'active'
            else:
                if item.url == current_url:
                    active_class = 'active'
            if current_item is None and item.parent is None:
                menu_html += f'<li class="{active_class}">'
            elif current_item is not None and item.parent == current_item:
                menu_html += f'<li class="{active_class}">'
            else:
                continue

            if urlnamed_exists(item.url):
                menu_url = reverse(item.url)
            else:
                menu_url = item.url
            menu_html += f'<a href="{menu_url}">{item.name}</a>'

            children = MenuItem.objects.filter(parent=item)
            if children.exists():
                menu_html += build_menu(children, item)
            menu_html += '</li>'
        menu_html += '</ul>'
        return menu_html

    # Строим дерево элементов меню
    menu_html = build_menu(menu_items)

    return menu_html


def urlnamed_exists(urlnamed):
    """Returns True for successful resolves()'s."""
    try:
        return bool(reverse(urlnamed))
    except NoReverseMatch:
        return False
