from django import forms
from .models import DirectMessage


class DirectMessageForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DirectMessageForm, self).__init__(*args, **kwargs)
        self.fields['direct_message'].label = ""

    class Meta:
        model = DirectMessage
        fields = ['direct_message']
