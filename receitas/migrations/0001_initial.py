# Generated by Django 4.0 on 2022-01-05 00:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receitas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.FloatField(verbose_name='Valor')),
                ('dataRecebimento', models.DateField(verbose_name='Data recebimento')),
                ('dataRecebimentoEsperado', models.DateField(verbose_name='Data esperada para recebimento')),
                ('descricao', models.CharField(max_length=500, verbose_name='Descrição')),
                ('tipoReceita', models.CharField(choices=[('SA', 'Salário'), ('PS', 'Presente'), ('PM', 'Prêmio'), ('OU', 'Outros')], max_length=50, verbose_name='Tipo')),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.contas')),
            ],
        ),
    ]
