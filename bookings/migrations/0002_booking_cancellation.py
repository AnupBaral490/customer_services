# Generated migration for booking cancellation feature

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='booking',
            name='cancelled_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='cancellation_reason',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='refund_status',
            field=models.CharField(
                choices=[
                    ('full_refund', 'Full Refund'),
                    ('fifty_percent', '50% Refund'),
                    ('no_refund', 'No Refund (Fee Retained)'),
                    ('refunded', 'Refunded'),
                    ('pending', 'Pending'),
                    ('not_applicable', 'Not Applicable'),
                ],
                default='not_applicable',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='booking',
            name='refund_amount',
            field=models.CharField(blank=True, help_text='Refund amount or percentage', max_length=100),
        ),
        migrations.AddField(
            model_name='booking',
            name='cancellation_requested_by',
            field=models.CharField(
                blank=True,
                choices=[('customer', 'Customer'), ('admin', 'Admin')],
                max_length=100,
            ),
        ),
        migrations.AddField(
            model_name='booking',
            name='reminder_sent',
            field=models.BooleanField(default=False, help_text='Whether cancellation policy reminder was sent'),
        ),
    ]
