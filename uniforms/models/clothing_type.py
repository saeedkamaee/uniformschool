# uniforms/models/clothing_type.py
from django.db import models

from core.models import BaseModel


class ClothingType(BaseModel):
    GENDER_CHOICES = [
        ('M', 'پسرانه'),
        ('F', 'دخترانه'),
    ]
    TYPE_CHOICES = [
        ('SHIRT', 'پیراهن'),
        ('PANTS', 'شلوار'),
        ('MANTOO', 'مانتو'),
        ('MAGHNAEH', 'مقنعه'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت لباس")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="نوع لباس")

    class Meta:
        unique_together = ['gender', 'type']
        verbose_name = "نوع لباس"
        verbose_name_plural = "انواع لباس"

    def __str__(self):
        return f"{self.get_gender_display()} - {self.get_type_display()}"