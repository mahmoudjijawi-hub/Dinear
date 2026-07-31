from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from menu.models import Category, Product


# بيانات المنيو — كل صورة فريدة ومحلية باسم الطبق
MENU_DATA = [
    {
        'name': 'مقبلات',
        'slug': 'appetizers',
        'order': 1,
        'products': [
            {'name': 'حمص بزيت زيتون', 'price': '4.50', 'image': 'images/products/hummus.jpg'},
            {'name': 'متبل باذنجان', 'price': '4.00', 'image': 'images/products/mutabal.jpg'},
            {'name': 'سمبوسك جبنة', 'price': '5.00', 'image': 'images/products/samosa.jpg'},
        ],
    },
    {
        'name': 'سلطات',
        'slug': 'salads',
        'order': 2,
        'products': [
            {'name': 'تبولة', 'price': '5.50', 'image': 'images/products/tabbouleh.jpg'},
            {'name': 'فتوش', 'price': '5.50', 'image': 'images/products/fattoush.jpg'},
        ],
    },
    {
        'name': 'أطباق رئيسية',
        'slug': 'main-dishes',
        'order': 3,
        'products': [
            {'name': 'مشاوي مشكلة', 'price': '14.00', 'image': 'images/products/mixed-grill.jpg'},
            {'name': 'كبسة دجاج', 'price': '12.00', 'image': 'images/products/kabsa.jpg'},
            {'name': 'كباب حلبي', 'price': '13.50', 'image': 'images/products/kebab.jpg'},
        ],
    },
    {
        'name': 'مشروبات',
        'slug': 'drinks',
        'order': 4,
        'products': [
            {'name': 'عصير ليمون بالنعناع', 'price': '3.50', 'image': 'images/products/lemonade.jpg'},
            {'name': 'شاي بالنعناع', 'price': '2.50', 'image': 'images/products/mint-tea.jpg'},
            {'name': 'عيران', 'price': '2.00', 'image': 'images/products/ayran.jpg'},
        ],
    },
    {
        'name': 'حلويات',
        'slug': 'desserts',
        'order': 5,
        'products': [
            {'name': 'تيراميسو كلاسيك', 'price': '5.50', 'image': 'images/products/tiramisu.jpg'},
            {'name': 'بقلاوة بالفستق', 'price': '4.00', 'image': 'images/products/baklava.jpg'},
            {'name': 'كنافة نابلسية', 'price': '6.00', 'image': 'images/products/kunafa.jpg'},
        ],
    },
]


class Command(BaseCommand):
    help = 'تعبئة قاعدة البيانات ببيانات المنيو الأولية ومستخدم المدير'

    def handle(self, *args, **options):
        self.stdout.write('جاري تعبئة البيانات...')

        for cat_data in MENU_DATA:
            category, created = Category.objects.update_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name'], 'order': cat_data['order']},
            )
            action = 'تم إنشاء' if created else 'تم تحديث'
            self.stdout.write(f'  {action} قسم: {category.name}')

            for i, prod_data in enumerate(cat_data['products']):
                Product.objects.update_or_create(
                    category=category,
                    name=prod_data['name'],
                    defaults={
                        'price': Decimal(prod_data['price']),
                        'image': prod_data['image'],
                        'order': i,
                    },
                )

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@dinear.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('تم إنشاء مستخدم المدير: admin / admin123'))
        else:
            self.stdout.write('مستخدم المدير موجود مسبقاً')

        self.stdout.write(self.style.SUCCESS('تمت تعبئة البيانات بنجاح!'))
