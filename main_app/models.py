from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    REASON_CHOICES = [
        ('Lack of Knowledge', 'Bilgi Eksikliği'),
        ('Other Reasons', 'Diğer Sebepler')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    question_image = models.ImageField(upload_to='questions/')
    answer_image = models.ImageField(upload_to='answers/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    mistake_reason = models.CharField(max_length=20, choices=REASON_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"Soru {self.id} - {self.category.name if self.category else 'Kategori Yok'}"
