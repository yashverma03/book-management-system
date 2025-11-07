import utils.models.enum_field
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE TYPE users_user_role_enum AS ENUM ('admin', 'manager');",
            reverse_sql="DROP TYPE IF EXISTS users_user_role_enum CASCADE;"
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255, null=False)),
                ('name', models.CharField(max_length=255)),
                ('role', utils.models.enum_field.EnumField(default='manager', enum_type='users_user_role_enum')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'users',
                'indexes': [models.Index(fields=['role'], name='users_role_0ace22_idx')],
            },
        ),
    ]
