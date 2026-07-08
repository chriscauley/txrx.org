-- Aligns the legacy (Django 1.9-era) txrx schema with what the fresh
-- Django 5.2 migrations produce, so the migration set can be recorded
-- with `migrate --fake` afterwards. Verified against live data:
-- object_pk <= 3 chars, no NULL m2m user_ids, priorities are digits,
-- extra_data is all valid JSON.
BEGIN;

-- django.contrib.auth widened group names (80 -> 150) in 2.x
ALTER TABLE auth_group ALTER COLUMN name TYPE varchar(150);

-- django-contrib-comments 2.x
ALTER TABLE django_comments ALTER COLUMN object_pk TYPE varchar(64);
ALTER TABLE django_comments ALTER COLUMN user_email TYPE varchar(254);

-- django-mailer 2.x
ALTER TABLE mailer_dontsendentry ALTER COLUMN id TYPE bigint;
ALTER TABLE mailer_message ALTER COLUMN id TYPE bigint;
ALTER TABLE mailer_message ALTER COLUMN priority TYPE smallint USING priority::smallint;
ALTER TABLE mailer_message ADD COLUMN retry_count integer NOT NULL DEFAULT 0;
ALTER TABLE mailer_messagelog ALTER COLUMN id TYPE bigint;
DROP INDEX IF EXISTS mailer_messagelog_priority_3b3412e66f6b86fc_like; -- varchar_pattern_ops, invalid for smallint
ALTER TABLE mailer_messagelog ALTER COLUMN priority TYPE smallint USING priority::smallint;
ALTER TABLE mailer_messagelog ALTER COLUMN message_data DROP NOT NULL;

-- columns whose model fields were removed years ago; keep the data but
-- stop NOT NULL from breaking inserts
ALTER TABLE membership_product ALTER COLUMN "order" DROP NOT NULL;

-- python-social-auth 0.2 -> social-auth-app-django 5.x
ALTER TABLE social_auth_association ALTER COLUMN id TYPE bigint;
ALTER TABLE social_auth_code ALTER COLUMN id TYPE bigint;
ALTER TABLE social_auth_code ADD COLUMN "timestamp" timestamptz NOT NULL DEFAULT now();
ALTER TABLE social_auth_nonce ALTER COLUMN id TYPE bigint;
ALTER TABLE social_auth_usersocialauth ALTER COLUMN id TYPE bigint;
ALTER TABLE social_auth_usersocialauth ALTER COLUMN extra_data TYPE jsonb USING extra_data::jsonb;
ALTER TABLE social_auth_usersocialauth ADD COLUMN created timestamptz NOT NULL DEFAULT now();
ALTER TABLE social_auth_usersocialauth ADD COLUMN modified timestamptz NOT NULL DEFAULT now();

-- legacy nullable m2m columns (data has no NULLs)
ALTER TABLE user_user_groups ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE user_user_user_permissions ALTER COLUMN user_id SET NOT NULL;

-- start the migration record fresh; `migrate --fake` rewrites it for 5.2
TRUNCATE django_migrations;

COMMIT;
