# Generated by Django 4.1.7 on 2023-03-30 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_article_user_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='cotent',
            new_name='content',
        ),
    ]