from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'amount', 'photo']

class UpdateMemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'email', 'amount', 'photo']
