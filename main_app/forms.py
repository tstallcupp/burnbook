from django.forms import ModelForm
from .models import Journal, Entry


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = ['name', 'template']

class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['date', 'title', 'body', 'mood_tracker', 'notes']
        
