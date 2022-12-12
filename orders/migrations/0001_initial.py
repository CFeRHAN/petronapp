# Generated by Django 4.1.1 on 2022-11-20 13:11

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('producer', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_manager', '0001_initial'),
        ('freight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('payment_date', models.DateField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('rejection_reasons', models.TextField(blank=True)),
                ('bill_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_bill', to='file_manager.attachment')),
                ('receipt_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payment_receipt', to='file_manager.attachment')),
            ],
        ),
        migrations.CreateModel(
            name='PaperWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_date', models.DateField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('rejection_reasons', models.TextField(blank=True)),
                ('bill_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='file_manager.attachment')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_type', models.CharField(choices=[('0', 'FCA'), ('1', 'CPT')], max_length=1, null=True)),
                ('ordering_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.CharField(max_length=200)),
                ('weight', models.FloatField()),
                ('vehicle_type', models.CharField(max_length=200)),
                ('loading_location', models.CharField(max_length=200)),
                ('destination', models.CharField(max_length=200)),
                ('second_destination', models.CharField(blank=True, max_length=200)),
                ('loading_date', models.DateTimeField()),
                ('border_passage', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True)),
                ('orderer_completion_date', models.DateTimeField(blank=True, null=True)),
                ('freight_completion_date', models.DateTimeField(blank=True, null=True)),
                ('order_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderer_order_number', to='orders.paperwork')),
                ('orderer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderer', to=settings.AUTH_USER_MODEL)),
                ('producer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='petro_seller_co', to='producer.producer')),
                ('proforma', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proforma', to='file_manager.attachment')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(null=True)),
                ('orderer_acception', models.BooleanField(default=False)),
                ('freight_acception', models.BooleanField(default=False)),
                ('prepayment_percentage', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)])),
                ('bijak', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bijak', to='orders.paperwork')),
                ('deal_draft', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prescript', to='orders.paperwork')),
                ('demurrage', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='demurrage_price', to='orders.payment')),
                ('drivers_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='drivers_info', to='orders.paperwork')),
                ('final_payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='final_payment', to='orders.payment')),
                ('freight', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='freight.freight')),
                ('inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inventory_price', to='orders.payment')),
                ('invoice_packing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='invoice_packing', to='orders.paperwork')),
                ('lading_bill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='lading_bill', to='orders.paperwork')),
                ('load_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='load_info', to='orders.paperwork')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('order_number', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='order_number', to='orders.paperwork')),
                ('prepayment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='prepayment_receipt', to='orders.payment')),
                ('second_destination_cost', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='second_destination_cost', to='orders.payment')),
            ],
        ),
    ]
