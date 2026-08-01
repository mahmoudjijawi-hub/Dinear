from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='image_url',
            new_name='image',
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.CharField(max_length=500, verbose_name='مسار الصورة'),
        ),
    ]
