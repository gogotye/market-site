from django import template


register = template.Library()

@register.inclusion_tag('tags/cards.html', name='cards')
def cards_func(query):
    return {'products': query}


@register.inclusion_tag('tags/categories.html', name='head_categories')
def categories_func(query):
    return {'categories': query}


@register.inclusion_tag('tags/sort-bars.html', name='sort_bars')
def sort_bars(request):
    sort_categories = [('Популярности', 'popularity'),
                     ('Цене', 'price'), ('Отзывам', 'reviews'),
                     ('Новизне', 'newest')]
    return {'sort_category': sort_categories, 'request': request}


@register.inclusion_tag('tags/pagination.html', name='pagination')
def paginate(page_obj, request, paginator):
    return {'page_obj': page_obj, 'request': request, 'paginator': paginator}


@register.inclusion_tag('tags/private-office-menu.html', name='private_office_menu')
def menu_office(item):
    lst = [('Личный кабинет', 'private_office:office'), ('Профиль', 'private_office:profile'), ('История заказов', 'private_office:history')]
    return {'active_cat': item, 'menu': lst}


@register.inclusion_tag('tags/cart_for_auth_user.html', name='auth_user_cart')
def cart_for_auth(items):
    return {'basket': items}


@register.inclusion_tag('tags/cart_for_not_auth_user.html', name='not_auth_user_cart')
def cart_for_not_auth(items):
    return {'basket': items}


@register.inclusion_tag('tags/ordering-menu.html', name='ordering_menu')
def ordering_menu(pointer):
    lst = [('Шаг 1. Параметры пользователя', 'order:step_1'), ('Шаг 2. Способ доставки',  'order:step_2'),
           ('Шаг 3. Способ оплаты',  'order:step_3'), ('Шаг 4. Подтверждение заказа',  'order:step_4')]
    return {'menu_pointer': pointer, 'menu_items': lst}