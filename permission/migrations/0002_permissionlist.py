# Generated by Django 3.1.1 on 2021-03-20 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('can_create_test_case', '可以创建测试用例'), ('can_edit_test_case', '可以编辑测试用例')),
            },
        ),
    ]