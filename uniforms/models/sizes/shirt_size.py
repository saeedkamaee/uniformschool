# uniforms/models/sizes/shirt_size.py
from django.db import models
from core.models import BaseModel


class ShirtSize(BaseModel):
    SHIRT_SIZES = [
        ('S', 'اسمال'),
        ('M', 'مدیوم'),
        ('L', 'لارج'),
        ('XL', 'اکسترا لارج'),
        ('2XL', '۲ اکسترا لارج'),
        ('3XL', '۳ اکسترا لارج'),
        ('4XL', '۴ اکسترا لارج'),
        ('5XL', '۵ اکسترا لارج'),
        ('6XL', '۶ اکسترا لارج'),
    ]

    size = models.CharField(max_length=10, choices=SHIRT_SIZES, unique=True, verbose_name="سایز پیراهن")

    class Meta:
        verbose_name = "سایز پیراهن"
        verbose_name_plural = "سایزهای پیراهن"

    def __str__(self):
        return self.get_size_display()