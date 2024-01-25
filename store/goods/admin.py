from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.html import format_html
from .models import Product, CategoryProduct, ProductShopRelations, Specifications, Tags, ProductImages
from .forms import FormProductAdmin
from django.core.cache import cache


class AdminProductShopRelationsInline(admin.TabularInline):
    model = Product.shops.through


class CategoryProductInline(admin.TabularInline):
    extra = 1
    model = Product


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    """Модель для интеграции Profile в админ-панель сайта"""

    inlines = [AdminProductShopRelationsInline]
    list_display = ['pk', 'title', 'desc_short', 'purchase_count', 'product_seen', 'is_active', 'show_image']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {'slug': ('title', )}
    form = FormProductAdmin

    def show_image(self, obj: Product):
        if obj.title_picture:
            return format_html(f'<img src={obj.title_picture.url} width="50" height="50">')
    show_image.short_description = 'Фотография'

    def desc_short(self, obj: Product, max_words=7):
        """
        Функция для вывода укороченного описания продукта, если число слов превышает заданное значение max_words

        :param obj: Инстанс класса Product
        :param max_words: Максимальное количество слов
        :return: Строка с описанием
        :rtype: str
        """
        return obj.description if len(obj.description.split()) <= max_words else truncatewords(obj.description, max_words) + "..."
    desc_short.short_description = 'Описание'

    def save_model(self, request, obj, form, change):
        key = f'product_details_{obj.slug}'
        if change and cache.get(key):
            cache.delete(key)

        images = {'images': request.FILES.getlist('pictures'),
                  'title_picture': request.FILES.get('title_pic')}
        obj.save()

        if images.get('title_picture'):
            obj.title_picture = images['title_picture']
            obj.save()
        if images.get('images'):
            for img in images.get('images'):
                ProductImages.objects.create(product=obj, image=img)


@admin.register(CategoryProduct)
class AdminCategoryProduct(admin.ModelAdmin):
    """Модель для интеграции CategoryProduct в админ-панель сайта"""

    inlines = [CategoryProductInline]
    list_display = ['pk', 'title', 'slug', 'show_image']
    list_display_links = ['pk', 'title']
    prepopulated_fields = {'slug': ('title', )}

    def show_image(self, obj: CategoryProduct):
        if obj.image:
            return format_html(f'<img src={obj.image.url} width="50" height="50">')
    show_image.short_description = 'Фотография'


@admin.register(ProductShopRelations)
class AdminProductShopRelations(admin.ModelAdmin):
    """Модель для интеграции Customer в админ-панель сайта"""

    list_display = ['pk']


@admin.register(Specifications)
class AdminSpecifications(admin.ModelAdmin):
    """Модель для интеграции Specifications в админ-панель сайта"""

    list_display = ['pk']


@admin.register(Tags)
class AdminTags(admin.ModelAdmin):
    """Модель для интеграции Tags в админ-панель сайта"""

    list_display = ['pk']


@admin.register(ProductImages)
class AdminProductImages(admin.ModelAdmin):
    """Модель для интеграции ProductImages в админ-панель сайта"""

    list_display = ['pk']

