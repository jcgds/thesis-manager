from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(PersonData)
admin.site.register(Proposal)
admin.site.register(ProposalStatus)
admin.site.register(Term)
admin.site.register(HistoricProposalStatus)
