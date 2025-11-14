# backend/ai_assistant/migrations/0005_create_fks.py
from django.db import migrations

class Migration(migrations.Migration):
    # Some operations touch multiple tables; run outside transaction to avoid locking issues.
    atomic = False

    dependencies = [
        ('ai_assistant', '0004_fix_chat_history_fk_constraint'),
        ('authentication', '0002_add_registration_models'),  # <- depends on the migration that creates student_registration
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            DECLARE
                table_name TEXT;
                constraint_name TEXT;
                tables_to_fix TEXT[] := ARRAY[
                    'ai_study_plans',
                    'ai_generated_notes',
                    'manual_notes',
                    'ai_chat_history',
                    'ai_interaction_sessions',
                    'ai_favorites'
                ];
            BEGIN
                -- ensure referenced table exists before creating FKs
                IF to_regclass('student_registration') IS NULL THEN
                    RAISE NOTICE 'student_registration not found; skipping FK creation.';
                    RETURN;
                END IF;

                FOREACH table_name IN ARRAY tables_to_fix LOOP
                    IF to_regclass(table_name) IS NULL THEN
                        -- table doesn't exist in this DB; skip it
                        CONTINUE;
                    END IF;

                    constraint_name := table_name || '_student_id_fkey';

                    -- Drop the old constraint if it exists
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint
                        WHERE conname = constraint_name
                        AND conrelid = table_name::regclass
                    ) THEN
                        EXECUTE format('ALTER TABLE %I DROP CONSTRAINT %I', table_name, constraint_name);
                    END IF;

                    -- Add the correct FK (if not present)
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint
                        WHERE conname = constraint_name
                        AND conrelid = table_name::regclass
                    ) THEN
                        EXECUTE format(
                            'ALTER TABLE %I ADD CONSTRAINT %I FOREIGN KEY (student_id) REFERENCES student_registration(student_id) ON DELETE CASCADE',
                            table_name,
                            constraint_name
                        );
                    END IF;
                END LOOP;
            END $$;
            """,
            reverse_sql="""
            ALTER TABLE IF EXISTS ai_study_plans DROP CONSTRAINT IF EXISTS ai_study_plans_student_id_fkey;
            ALTER TABLE IF EXISTS ai_generated_notes DROP CONSTRAINT IF EXISTS ai_generated_notes_student_id_fkey;
            ALTER TABLE IF EXISTS manual_notes DROP CONSTRAINT IF EXISTS manual_notes_student_id_fkey;
            ALTER TABLE IF EXISTS ai_chat_history DROP CONSTRAINT IF EXISTS ai_chat_history_student_id_fkey;
            ALTER TABLE IF EXISTS ai_interaction_sessions DROP CONSTRAINT IF EXISTS ai_interaction_sessions_student_id_fkey;
            ALTER TABLE IF EXISTS ai_favorites DROP CONSTRAINT IF EXISTS ai_favorites_student_id_fkey;
            """
        ),
    ]
