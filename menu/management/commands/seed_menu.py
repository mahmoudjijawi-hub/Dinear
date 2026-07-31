from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from menu.models import Category, Product


# بيانات المنيو الأولية
MENU_DATA = [
    {
        'name': 'مقبلات',
        'slug': 'appetizers',
        'order': 1,
        'products': [
            {'name': 'حمص بزيت زيتون', 'price': '4.50', 'image': 'https://images.unsplash.com/photo-1626200480038-6352d6a09f04?w=400&h=300&fit=crop'},
            {'name': 'متبل باذنجان', 'price': '4.00', 'image': 'https://images.unsplash.com/photo-1609501676915-b1754437fbab?w=400&h=300&fit=crop'},
            {'name': 'سمبوسك جبنة', 'price': '5.00', 'image': 'https://images.unsplash.com/photo-1601050690597-df0568fa7098?w=400&h=300&fit=crop'},
        ],
    },
    {
        'name': 'سلطات',
        'slug': 'salads',
        'order': 2,
        'products': [
            {'name': 'تبولة', 'price': '5.50', 'image': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop'},
            {'name': 'فتوش', 'price': '5.50', 'image': 'https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop'},
        ],
    },
    {
        'name': 'أطباق رئيسية',
        'slug': 'main-dishes',
        'order': 3,
        'products': [
            {'name': 'مشاوي مشكلة', 'price': '14.00', 'image': 'https://images.unsplash.com/photo-1529042410759-befb1204bda8?w=400&h=300&fit=crop'},
            {'name': 'كبسة دجاج', 'price': '12.00', 'image': 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?w=400&h=300&fit=crop'},
            {'name': 'كباب حلبي', 'price': '13.50', 'image': 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400&h=300&fit=crop'},
        ],
    },
    {
        'name': 'مشروبات',
        'slug': 'drinks',
        'order': 4,
        'products': [
            {'name': 'عصير ليمون بالنعناع', 'price': '3.50', 'image': 'https://images.unsplash.com/photo-1621263764928-df1444c5e859?w=400&h=300&fit=crop'},
            {'name': 'شاي بالنعناع', 'price': '2.50', 'image': 'https://images.unsplash.com/photo-1556675593-ef703c1ce2b3?w=400&h=300&fit=crop'},
            {'name': 'عيران', 'price': '2.00', 'image': 'https://images.unsplash.com/photo-1622483767028-3f66fbf34efa?w=400&h=300&fit=crop'},
        ],
    },
    {
        'name': 'حلويات',
        'slug': 'desserts',
        'order': 5,
        'products': [
            {'name': 'تيراميسو كلاسيك', 'price': '5.50', 'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop'},
            {'name': 'بقلاوة بالفستق', 'price': '4.00', 'image': 'https://images.unsplash.com/photo-1598110757814-bcd6591dca56?w=400&h=300&fit=crop'},
            {'name': 'كنافة نابلسية', 'price': '6.00', 'image': 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400&h=300&fit=crop'},
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
                        'image_url': prod_data['image'],
                        'order': i,
                    },
                )

        # إنشاء مستخدم مدير
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@dinear.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('تم إنشاء مستخدم المدير: admin / admin123'))
        else:
            self.stdout.write('مستخدم المدير موجود مسبقاً')

        self.stdout.write(self.style.SUCCESS('تمت تعبئة البيانات بنجاح!'))
