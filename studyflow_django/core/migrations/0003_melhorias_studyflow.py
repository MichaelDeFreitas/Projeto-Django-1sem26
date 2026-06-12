# Generated manually for StudyFlow improvements

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_categoria_anotacao_categoria_perfil_sessaoestudo'),
    ]

    operations = [
        migrations.AddField(
            model_name='anotacao',
            name='atualizada_em',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddConstraint(
            model_name='categoria',
            constraint=models.UniqueConstraint(fields=('usuario', 'nome'), name='categoria_unica_por_usuario'),
        ),
    ]
