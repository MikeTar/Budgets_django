# Generated by Django 3.1.4 on 2020-12-24 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Budgets', '0007_auto_20201224_1029'),
    ]

    operations = [
        migrations.AddField(
            model_name='ppo_budget',
            name='budgetname',
            field=models.TextField(blank=True, max_length=254, null=True, verbose_name='Наименование бюджета'),
        ),
    ]
