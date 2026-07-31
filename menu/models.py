from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """قسم المنيو (مقبلات، أطباق رئيسية، إلخ)"""
    name = models.CharField(max_length=100, verbose_name='الاسم')
    slug = models.SlugField(unique=True, verbose_name='المعرّف')
    order = models.PositiveIntegerField(default=0, verbose_name='الترتيب')

    class Meta:
        verbose_name = 'قسم'
        verbose_name_plural = 'الأقسام'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """منتج/طبق في المنيو"""
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='products', verbose_name='القسم',
    )
    name = models.CharField(max_length=150, verbose_name='الاسم')
    description = models.TextField(blank=True, verbose_name='الوصف')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='السعر')
    image_url = models.URLField(max_length=500, verbose_name='رابط الصورة')
    is_available = models.BooleanField(default=True, verbose_name='متوفر')
    order = models.PositiveIntegerField(default=0, verbose_name='الترتيب')

    class Meta:
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Order(models.Model):
    """طلب من العميل"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'قيد الانتظار'
        PREPARING = 'preparing', 'قيد التحضير'
        READY = 'ready', 'جاهز'
        DELIVERED = 'delivered', 'تم التسليم'
        CANCELLED = 'cancelled', 'ملغي'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='الحالة',
    )
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المجموع')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث')

    class Meta:
        verbose_name = 'طلب'
        verbose_name_plural = 'الطلبات'
        ordering = ['-created_at']

    def __str__(self):
        return f'طلب #{self.pk}'


class OrderItem(models.Model):
    """عنصر داخل الطلب"""
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='items', verbose_name='الطلب',
    )
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        null=True, verbose_name='المنتج',
    )
    product_name = models.CharField(max_length=150, verbose_name='اسم المنتج')
    quantity = models.PositiveIntegerField(verbose_name='الكمية')
    unit_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='سعر الوحدة')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المجموع الفرعي')

    class Meta:
        verbose_name = 'عنصر طلب'
        verbose_name_plural = 'عناصر الطلب'

    def __str__(self):
        return f'{self.product_name} x{self.quantity}'
