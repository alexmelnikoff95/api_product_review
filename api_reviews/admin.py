from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from api_reviews.models import Review, Category, Product, Specifications, Manufacturer, RatingStar, Rating


# class ProductAdminForm(forms.ModelForm):
#     """Форма с виджетом ckeditor"""
#     description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
#
#     class Meta:
#         model = Product
#         fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("name", "url")
    list_display_links = ("name",)


class ReviewInline(admin.TabularInline):
    """Отзывы о продукте"""
    model = Review
    extra = 1
    readonly_fields = ("name", "email")


class SpecificationsInline(admin.TabularInline):
    model = Specifications
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Продукты"""
    list_display = ("title", "category", "url", "published")
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [SpecificationsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("published",)
    actions = ["publish", "unpublish"]
    # form = ProductAdminForm
    readonly_fields = ("get_image",)
    fieldsets = (
        (None, {
            "fields": (("title",),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_image"))
        }),
        (None, {
            "fields": (("year", "country"),)
        }),
        ("Manufacturer", {
            "classes": ("collapse",),
            "fields": (("create_product", "category"),)
        }),
        (None, {
            "fields": (("price_in_dollar", "price_in_you_country"),)
        }),
        ("Options", {
            "fields": (("url", "published"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="110"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы к фильму"""
    list_display = ("name", "email", "parent", "product", "id")
    readonly_fields = ("name", "email")


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    """Производители"""
    list_display = ("name", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "product", "ip")


admin.site.register(RatingStar)
