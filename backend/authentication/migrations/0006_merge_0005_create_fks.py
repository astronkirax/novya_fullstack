# backend/authentication/migrations/0006_merge_0005_create_fks.py
from django.db import migrations

class Migration(migrations.Migration):
    # This migration merges two heads:
    #  - ai_assistant.0005_create_fks
    #  - authentication.fix_coin_transaction_constraint
    dependencies = [
        ('authentication', 'fix_coin_transaction_constraint'),
        ('ai_assistant', '0005_create_fks'),
    ]

    operations = [
        # No operations - this is an empty merge migration to join the two heads.
    ]
