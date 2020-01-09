from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import *


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_manager',)}),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(PersonData)
admin.site.register(Proposal)
admin.site.register(ProposalStatus)
admin.site.register(Term)
admin.site.register(HistoricProposalStatus)
admin.site.register(Thesis)
admin.site.register(ThesisStatus)
admin.site.register(HistoricThesisStatus)
admin.site.register(Defence)
admin.site.register(Jury)
admin.site.register(PersonType)
