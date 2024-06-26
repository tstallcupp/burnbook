from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Journal
from .forms import JournalForm, EntryForm

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def home(request):
    return render(request, 'home.html')


def journals_index(request):
  journals = Journal.objects.filter(user=request.user)
  user = request.user
  return render(request, 'journals/index.html', { 'journals': journals, 'user': user })


@login_required
def journals_create(request):
  error_message = ''
  journal_form = JournalForm(request.POST)
  user = request.user.id
  if journal_form.is_valid():
    new_journal = journal_form.save(commit=False)
    new_journal.user_id = user
    new_journal.save()
    return redirect(journals_index)
  else:
    error_message = "Invalid journal creation - try again"
  return render(request, 'journals/journal_form.html', { 
    'journal_form': journal_form,
    'error_message': error_message
  })

@login_required
def journals_detail(request, journal_id):
  journal = Journal.objects.get(id=journal_id)
  if journal.has_no_entries():
    return render(request, 'journals/detail.html', {
    'journal': journal,
  })
  elif journal.has_entries():
    entries = journal.entry_set.all()
    return render(request, 'journals/detail.html', {
    'journal': journal,
    'entries': entries,
  })


@login_required
def add_entry(request, journal_id):
  error_message = ''
  entry_form = EntryForm(request.POST)
  journal = journal_id
  if entry_form.is_valid():
    new_entry = entry_form.save(commit=False)
    new_entry.journal_id = journal
    new_entry.save()
    return redirect('detail', journal_id=journal_id)
  else:
    error_message = "Invalid entry creation - try again"
  return render(request, 'journals/entry_form.html', { 
    'entry_form': entry_form,
    'error_message': error_message
  })
