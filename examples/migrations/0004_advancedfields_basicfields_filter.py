# Generated by Django 2.1.4 on 2018-12-10 18:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('examples', '0003_pageload'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('regex_field', models.CharField(max_length=256)),
                ('choice_field', models.CharField(max_length=8, null=True)),
                ('multiplechoice_field', models.CharField(max_length=8, null=True)),
                ('filepath_field', models.FilePathField(null=True)),
                ('file_field', models.FileField(blank=True, null=True, upload_to='examples/')),
                ('image_field', models.ImageField(blank=True, null=True, upload_to='examples/')),
                ('hidden_field', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='BasicFields',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boolean_field', models.BooleanField(null=True)),
                ('nullboolean_field', models.NullBooleanField()),
                ('char_field', models.CharField(max_length=32, null=True)),
                ('email_field', models.EmailField(max_length=254, null=True)),
                ('slug_field', models.SlugField(null=True)),
                ('url_field', models.URLField(null=True)),
                ('uuid_field', models.UUIDField(null=True)),
                ('ipaddress_field', models.GenericIPAddressField(null=True)),
                ('integer_field', models.IntegerField(null=True)),
                ('float_field', models.IntegerField(null=True)),
                ('decimal_field', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('datetime_field', models.DateTimeField(null=True)),
                ('date_field', models.DateField(null=True)),
                ('time_field', models.TimeField(null=True)),
                ('duration_field', models.DurationField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_field', models.CharField(help_text='Char field', max_length=20, verbose_name='Char field')),
                ('datetime_field', models.DateTimeField(help_text='Datetime field', verbose_name='Datetime field')),
                ('int_field', models.IntegerField(help_text='Integer field', verbose_name='Integer field')),
                ('int_choice_field', models.IntegerField(choices=[(0, 'Choice 1'), (1, 'Choice 2'), (2, 'Choice 3'), (3, 'Choice 4')], help_text='Integer field with choices', verbose_name='Integer field with choices')),
                ('bool_field', models.BooleanField(help_text='Boolean field', verbose_name='Boolean field')),
            ],
        ),
    ]
