from django.db import migrations


# noinspection PyPep8Naming
def populate_proposal_statuses(apps, schema_editor):
    ProposalStatus = apps.get_model('web', 'ProposalStatus')
    ProposalStatus(name='Por evaluar').save()
    ProposalStatus(name='Diferida').save()
    ProposalStatus(name='Aprobada').save()
    ProposalStatus(name='Rechazada').save()


# noinspection PyPep8Naming
def populate_thesis_statuses(apps, schema_editor):
    ThesisStatus = apps.get_model('web', 'ThesisStatus')
    ThesisStatus(name='Por entregar').save()
    ThesisStatus(name='Entregado y pendiente por defender').save()
    ThesisStatus(name='Diferido').save()
    ThesisStatus(name='Aprobado').save()
    ThesisStatus(name='Rechazado').save()
    ThesisStatus(name='Aprobado con solicitud de correcciones').save()


class Migration(migrations.Migration):
    dependencies = [
        ('web', '0006_auto_20200105_1839'),
    ]

    operations = [
        migrations.RunPython(populate_proposal_statuses),
        migrations.RunPython(populate_thesis_statuses),
    ]
