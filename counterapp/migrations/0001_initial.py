# Generated by Django 4.2 on 2023-04-21 15:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.IntegerField()),
                ('order_no', models.CharField(max_length=255, null=True)),
                ('invoice_no', models.CharField(max_length=255, null=True)),
                ('issuing_officer', models.CharField(max_length=255, null=True)),
                ('issuing_officer_designation', models.CharField(max_length=255, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_by', models.CharField(max_length=255, null=True)),
                ('receiving_officer', models.CharField(max_length=255, null=True)),
                ('receiving_officer_designation', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('count', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.IntegerField()),
                ('order_no', models.CharField(max_length=255, null=True)),
                ('invoice_no', models.CharField(max_length=255, null=True)),
                ('issuing_officer', models.CharField(max_length=255, null=True)),
                ('issuing_officer_designation', models.CharField(max_length=255, null=True)),
                ('receiving_officer', models.CharField(max_length=255, null=True)),
                ('receiving_officer_designation', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voucher_no', models.IntegerField()),
                ('order_no', models.CharField(max_length=255, null=True)),
                ('invoice_no', models.CharField(max_length=255, null=True)),
                ('requisitioning_officer', models.CharField(max_length=255, null=True)),
                ('requisitioning_officer_designation', models.CharField(max_length=255, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('approved_by', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User'), ('issuing', 'IssuingOfficer'), ('recieving', 'RecievingOfficer'), ('requisitioning', 'RequisitioningOfficer')], max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequisitionItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_no', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quantity_required', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counterapp.item')),
                ('requisition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisition_items', to='counterapp.requisition')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReceiptItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_no', models.IntegerField()),
                ('description', models.TextField()),
                ('quantity', models.IntegerField()),
                ('value', models.CharField(max_length=255)),
                ('remarks', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counterapp.item')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receipt_items', to='counterapp.receipt')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='IssueItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_no', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('quantity_issued', models.IntegerField()),
                ('remarks', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_items', to='counterapp.issue')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='counterapp.item')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
