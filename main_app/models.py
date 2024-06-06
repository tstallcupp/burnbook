from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

TEMPLATES = (
  ('P', 'Personal'),
  ('T', 'Travel'),
  ('H', 'Wellness'),
  ('W', 'Work'),
)

# Create your models here.
class Journal(models.Model):
  name = models.CharField(max_length=50)
  template = models.CharField(
	max_length=1,
	choices=TEMPLATES,
	default=TEMPLATES[0][0]
)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"journal.id: {self.id}, user {self.user.id}: {self.user},  name: '{self.name}', template: {self.get_template_display()}"
    
  def get_absolute_url(self):
    return reverse('journals_index')
