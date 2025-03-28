# Generated by Django 5.1.4 on 2025-01-16 00:18

import django_summernote.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_alter_post_category_alter_post_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Defaults to filename, if left blank', max_length=255, null=True)),
                ('file', models.FileField(upload_to=django_summernote.utils.uploaded_filepath)),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Anexo do post',
                'verbose_name_plural': 'Anexos dos posts',
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='data/posts/%Y/%m/', verbose_name='Imagem de Capa'),
        ),
    ]
