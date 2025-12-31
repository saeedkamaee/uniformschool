# core/models/academic_year.py
from django.db import models
from django.core.exceptions import ValidationError

from .base_model import BaseModel


class AcademicYear(BaseModel):
    year = models.CharField(
        max_length=9,
        unique=True,
        verbose_name="سال تحصیلی",
        help_text="مثال: ۱۴۰۳-۱۴۰۴"
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name="سال پیش‌فرض",
        help_text="فقط یک سال می‌تواند پیش‌فرض باشد"
    )
    start_date = models.DateField(verbose_name="تاریخ شروع")
    end_date = models.DateField(verbose_name="تاریخ پایان")

    class Meta:
        verbose_name = "سال تحصیلی"
        verbose_name_plural = "سال‌های تحصیلی"
        ordering = ['-year']

    def clean(self):
        super().clean()
        if self.is_default:
            # فقط یک سال پیش‌فرض داشته باشیم
            if AcademicYear.objects.filter(is_default=True).exclude(pk=self.pk).exists():
                raise ValidationError("فقط یک سال تحصیلی می‌تواند پیش‌فرض باشد.")

    def __str__(self):
        return self.year