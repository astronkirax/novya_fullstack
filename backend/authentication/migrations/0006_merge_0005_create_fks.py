# backend/authentication/migrations/0006_merge_0005_create_fks.py
# Merge migration to unify two authentication heads and depend on ai_assistant migration.
# Generated manually to resolve conflicting migration heads:
# - authentication: 0005_create_fks
# - authentication: fix_coin_transaction_constraint
# and to ensure migration graph references an existing ai_assistant migration
# (0005_create_calendar_table) so Django can validate the graph.

from django.db import migrations


class Migration(migrations.Migration):
    """
    This merge migration unites two migration heads in the `authentication` app.
    It intentionally contains no operations; its job is to declare dependencies so
    Django's migration graph has a single leaf node and the migrations can run
    in a consistent order on deploy.
    """

    dependencies = [
        # One of the conflicting heads from authentication
        ('authentication', '0005_create_fks'),

        # The other conflicting head — use the exact filename you have.
        # In your repo this file is named `fix_coin_transaction_constraint.py`,
        # and Django will reference it by its migration name (module name without .py).
        ('authentication', 'fix_coin_transaction_constraint'),

        # Ensure we depend on an existing ai_assistant migration so the graph is valid.
        # Your repo shows an ai_assistant migration named 0005_create_calendar_table.
        ('ai_assistant', '0005_create_calendar_table'),
    ]

    operations = [
        # No operations needed — this merge simply unifies the two heads.
    ]
