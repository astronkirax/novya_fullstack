# backend/authentication/migrations/0006_merge_0005_create_fks.py
from django.db import migrations

class Migration(migrations.Migration):
    # Ensure this merge references both authentication heads (your repo had two)
    # and depends on an existing ai_assistant migration (we point to 0005_create_calendar_table that exists).
    dependencies = [
        ('authentication', '0005_create_fks'),                 # one authentication head
        ('authentication', 'fix_coin_transaction_constraint'), # the other head (use the exact filename you have)
        ('ai_assistant', '0005_create_calendar_table'),        # must reference an existing ai_assistant migration
    ]

    operations = [
        # This merge migration does not need operations; it just unifies heads
    ]
