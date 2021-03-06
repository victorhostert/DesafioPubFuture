# Generated by Django 4.0.1 on 2022-01-16 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=15)),
                ('tipoConta', models.CharField(choices=[('', '--------'), ('CA', 'Carteira'), ('CC', 'Conta Corrente'), ('PO', 'Poupança')], max_length=2, verbose_name='Tipo de Conta')),
                ('instituicaoFinanceira', models.CharField(max_length=255, verbose_name='Instituição Financeira')),
            ],
        ),
    ]
