from django import forms

# from pilotCore.models import Profile

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = {
#             'external_id',
#             'name',
#         }
#         widgets = {
#             'name': forms.TextInput,
#         }

class BroadcastForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    broadcast_text = forms.CharField(widget=forms.Textarea)
