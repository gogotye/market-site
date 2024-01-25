import os
from django.core.exceptions import ValidationError
from django.db.models import Min, QuerySet


class GetUploadPath:
    """
    Данный класс содержит в себе функции для построения гибкого пути для разных моделей
    """
    @staticmethod
    def get_upload_path_for_category_image(inst, filename):
        """
        :param inst: Инстанс класса CategoryProduct
        :param filename: Имя передаваемого файла
        :return: Путь до filename в папке media в корне проекта
        :rtype: path(bytes)
        """
        return os.path.join('category_image', inst.slug, filename)

    @staticmethod
    def get_upload_path_for_user_avatar(inst, filename):
        """
        :param inst: Инстанс класса Profile
        :param filename: Имя передаваемого файла
        :return: Путь до filename в папке media в корне проекта
        :rtype: path(bytes)
        """
        return os.path.join('user_avatar', inst.email, filename)

    @staticmethod
    def get_upload_path_for_title_product_image(inst, filename):
        """
        :param inst: Инстанс класса Product
        :param filename: Имя передаваемого файла
        :return: Путь до filename в папке media в корне проекта
        :rtype: path(bytes)
        """
        return os.path.join('product_images', str(inst.pk), inst.slug, 'title_image', filename)

    @staticmethod
    def get_upload_path_for_product_images(inst, filename):
        """
        :param inst: Инстанс класса ProductImage
        :param filename: Имя передаваемого файла
        :return: Путь до filename в папке media в корне проекта
        :rtype: path(bytes)
        """
        return os.path.join('product_images', str(inst.product.pk), inst.product.slug, 'images', filename)


def validate_image(image):
    """
    Функция для валидации размера передаваемого изображения,
     выбрасывает исключение, если file_size_mb превышает megabyte_limit

    :param image: Изображение
    """
    file_size_mb = image.size / 1024 ** 2
    megabyte_limit = 2
    if file_size_mb > megabyte_limit:
        raise ValidationError("Максимальный размер файла {}MB".format(megabyte_limit))


def get_active_categories(context):
    """Функция для выбора активных категорий товаров"""
    from goods.models import CategoryProduct

    active_categories = CategoryProduct.objects.filter(cat_products__is_active=True).distinct()
    context.update({'active_categories': active_categories})


def change_sort_order(request):
    if not request.session.get('sorted'):
        request.session['sorted'] = 'acs'
        return

    if request.session['sorted'] == 'acs':
        request.session['sorted'] = 'decs'
    else:
        request.session['sorted'] = 'acs'


def sort_by(queryset, request, key):
    if request.GET.get('change_order'):
        change_sort_order(request=request)

    order = request.session['sorted']
    if key == 'popularity':
        queryset = queryset.order_by('purchase_count') if order == 'acs' else queryset.order_by('-purchase_count')
    elif key == 'price':
        queryset = queryset.order_by('avg_price') if order == 'acs' else queryset.order_by('-avg_price')
    elif key == 'reviews':
        queryset = queryset.order_by('product_seen') if order == 'acs' else queryset.order_by('-product_seen')
    elif key == 'newest':
        queryset = queryset.order_by('date') if order == 'acs' else queryset.order_by('-date')

    return queryset


def total_sum_and_quantity_update_context(context, request, queryset_for_cart_table=None):
    from cart.service import CartService

    cart_service = CartService(request=request)

    context.update(
        {
            'quantity_of_goods': cart_service.get_quantity_of_products_in_cart(request=request, queryset=queryset_for_cart_table),
            'sum': cart_service.get_total_sum(request=request, queryset=queryset_for_cart_table),
        }
    )
    get_active_categories(context=context)


def get_product_shop_with_min_price(request):
    from goods.models import ProductShopRelations

    p_id = request.POST.get('product_id')
    lowest_price_product = ProductShopRelations.objects.filter(
        product__pk=p_id,
        price=ProductShopRelations.objects.filter(product__pk=p_id).aggregate(min_price=Min('price'))['min_price']
    ).select_related('product').first()

    return lowest_price_product


def round_total_sum(list_of_products: QuerySet, field: str) -> None:
    """Округляет переданное поле field до 2 знаков после запятой"""

    for i in list_of_products:
        if hasattr(i, field) and getattr(i, field) is not None:
            val = getattr(i, field)
            setattr(i, field, round(float(val), 2))
