from django.db import models
from django.core.validators import RegexValidator

from .base_model import BaseModel  # import محلی از داخل فولدر models


class School(BaseModel):
    GENDER_CHOICES = [
        ('M', 'پسرانه'),
        ('F', 'دخترانه'),
    ]
    
    LEVEL_CHOICES = [
        ('PRIMARY', 'ابتدایی (۱ تا ۶)'),
        ('MIDDLE', 'متوسطه اول (۷ تا ۹)'),
        ('HIGH', 'متوسطه دوم (۱۰ تا ۱۲)'),
    ]

    name = models.CharField(max_length=200, verbose_name="نام مدرسه")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="جنسیت")
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name="مقطع تحصیلی")
    address = models.TextField(blank=True, null=True, verbose_name="آدرس مدرسه")
    education_manager = models.CharField(max_length=100, blank=True, null=True, verbose_name="نام مسئول آموزش")
    manager_phone = models.CharField(
        max_length=11,
        blank=True, null=True,
        validators=[RegexValidator(r'^09\d{9}$', 'شماره موبایل باید با ۰۹ شروع شود و ۱۱ رقم باشد.')],
        verbose_name="موبایل مسئول آموزش"
    )
    fabric_color_image = models.ImageField(
        upload_to='schools/fabric/', blank=True, null=True, verbose_name="عکس نمونه پارچه"
    )

    class Meta:
        verbose_name = "مدرسه"
        verbose_name_plural = "مدارس"
        unique_together = ['name', 'gender','level']
    def __str__(self):
        return f"{self.name} ({self.get_gender_display()} - {self.get_level_display()})"