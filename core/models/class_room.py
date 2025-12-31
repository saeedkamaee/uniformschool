# core/models/class_room.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from .base_model import BaseModel


class ClassRoom(BaseModel):
    school = models.ForeignKey('School', on_delete=models.PROTECT, related_name='classes', verbose_name="مدرسه")  # string notation برای جلوگیری از circular import
    grade = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name="پایه تحصیلی"
    )
    section = models.CharField(max_length=10, blank=True, null=True, verbose_name="شعبه (مثلاً الف، ب)")

    class Meta:
        unique_together = ['school', 'grade', 'section']
        verbose_name = "کلاس"
        verbose_name_plural = "کلاس‌ها"
        ordering = ['grade']

    def clean(self):
        # جلوگیری از تناقض مقطع و پایه
        if self.school.level == 'PRIMARY' and self.grade > 6:
            raise ValidationError("مدرسه ابتدایی نمی‌تواند پایه بالاتر از ششم داشته باشد.")
        if self.school.level == 'MIDDLE' and (self.grade < 7 or self.grade > 9):
            raise ValidationError("متوسطه اول فقط پایه‌های ۷، ۸ و ۹ را شامل می‌شود.")
        if self.school.level == 'HIGH' and self.grade < 10:
            raise ValidationError("متوسطه دوم فقط پایه‌های ۱۰، ۱۱ و ۱۲ را شامل می‌شود.")

    def __str__(self):
        return f"{self.school.name} - پایه {self.grade} {self.section or ''}".strip()