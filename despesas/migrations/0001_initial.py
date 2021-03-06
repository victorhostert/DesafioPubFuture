# Generated by Django 4.0.1 on 2022-01-16 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Despesas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=15)),
                ('dataPagamento', models.DateField(verbose_name='Data pagamento')),
                ('dataPagamentoEsperado', models.DateField(blank=True, null=True, verbose_name='Data pagamento esperado')),
                ('tipoDespesa', models.CharField(choices=[('', '--------'), ('AL', 'Alimentação'), ('ED', 'Educação'), ('LA', 'Lazer'), ('MO', 'Moradia'), ('RO', 'Roupa'), ('SA', 'Saúde'), ('TR', 'Transporte'), ('OU', 'Outros')], max_length=2, verbose_name='Tipo')),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contas.contas')),
            ],
        ),
    ]
