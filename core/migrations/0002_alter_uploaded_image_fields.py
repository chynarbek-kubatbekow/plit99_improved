from django.db import migrations, models

import core.media_utils


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryitem',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=core.media_utils.gallery_image_upload_to,
                verbose_name='Фото',
            ),
        ),
        migrations.AlterField(
            model_name='news',
            name='cover_image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=core.media_utils.news_cover_upload_to,
                verbose_name='Обложка',
            ),
        ),
    ]
