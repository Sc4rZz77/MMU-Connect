# Generated by Django 5.2 on 2025-05-12 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_author_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='faculty',
            field=models.CharField(choices=[('FCI', 'Faculty of Computing'), ('FCA', 'Faculty of IDK'), ('FCM', 'Faculty of Creative Multimedia'), ('FOM', 'Faculty of Management'), ('FAC', 'Faculty of Applied Comm')], default='FCI', max_length=5),
        ),
    ]
