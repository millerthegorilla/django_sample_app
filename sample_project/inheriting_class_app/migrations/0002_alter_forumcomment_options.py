# Generated by Django 3.2.9 on 2021-11-10 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inheriting_class_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='forumcomment',
            options={'permissions': [('approve_comment', 'Approve Comment')]},
        ),
    ]
