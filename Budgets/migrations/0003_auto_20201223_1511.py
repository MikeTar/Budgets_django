# Generated by Django 3.1.4 on 2020-12-23 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Budgets', '0002_remove_budget_oktmocode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budget',
            options={'verbose_name': 'Бюджеты', 'verbose_name_plural': 'Справочник бюджетов'},
        ),
        migrations.AlterField(
            model_name='budget',
            name='budgettype',
            field=models.CharField(choices=[(None, 'Неопределённый'), ('00', 'Прочие бюджеты'), ('01', 'Федеральный бюджет'), ('02', 'Бюджет субъекта РФ'), ('03', 'Бюджеты внутригородских МО г. Москвы и г. Санкт-Петербурга'), ('04', 'Бюджет городского округа'), ('05', 'Бюджет муниципального района'), ('06', 'Бюджет Пенсионного фонда РФ'), ('07', 'Бюджет ФСС РФ'), ('08', 'Бюджет ФФОМС'), ('09', 'Бюджет ТФОМС'), ('10', 'Бюджет поселения'), ('11', 'Бюджет городского округа с внутригородским делением'), ('12', 'Бюджет внутригородского района городского округа'), ('13', 'Бюджет городского поселения'), ('14', 'Бюджет города федерального значения'), ('98', 'Распределяемый доход'), ('99', 'Доход организации (только для ПДИ)')], default='Неопределённый', max_length=2, verbose_name='Тип бюджета'),
        ),
    ]
