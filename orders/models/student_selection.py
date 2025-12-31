# orders/models/student_selection.py
from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel, Student,AcademicYear
from uniforms.models import ClothingSize, AgreedPrice


class StudentSelection(BaseModel):
    academic_year = models.ForeignKey('core.AcademicYear', on_delete=models.PROTECT, verbose_name="سال تحصیلی")
    student = models.OneToOneField(
        'core.Student',
        on_delete=models.PROTECT,
        related_name='selection',
        verbose_name="دانش‌آموز"
    )
    clothing_size1 = models.ForeignKey(
        ClothingSize,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='selections_as_primary',
        verbose_name="سایز لباس اصلی (پیراهن/مانتو)"
    )
    clothing_size2 = models.ForeignKey(
        ClothingSize,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='selections_as_secondary',
        verbose_name="سایز لباس فرعی (شلوار/مقنعه)"
    )
    is_ready1 = models.BooleanField(default=False, verbose_name="لباس اصلی آماده؟")
    is_ready2 = models.BooleanField(default=False, verbose_name="لباس فرعی آماده؟")
    delivery_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تحویل")
    is_paid = models.BooleanField(default=False, verbose_name="تسویه کامل شده؟")

    class Meta:
        unique_together = ['academic_year', 'student']
        verbose_name = "انتخاب سایز دانش‌آموز"
        verbose_name_plural = "انتخاب‌های سایز دانش‌آموزان"

    def clean(self):
        super().clean()
        if not self.student:
            return

        school = self.student.class_room.school
        school_gender = school.gender

        # چک لباس اصلی (۱)
        if self.clothing_size1:
            ctype1 = self.clothing_size1.clothing_type
            if ctype1.gender != school_gender:
                raise ValidationError("جنسیت لباس اصلی با جنسیت مدرسه همخوانی ندارد.")
            if school_gender == 'M' and ctype1.type != 'SHIRT':
                raise ValidationError("لباس اصلی برای پسران باید پیراهن باشد.")
            if school_gender == 'F' and ctype1.type != 'MANTOO':
                raise ValidationError("لباس اصلی برای دختران باید مانتو باشد.")

            if not AgreedPrice.objects.filter(school=school, clothing_size=self.clothing_size1).exists():
                raise ValidationError(f"قیمت توافقی برای {self.clothing_size1} در مدرسه {school.name} تعریف نشده است.")

        # چک لباس فرعی (۲)
        if self.clothing_size2:
            ctype2 = self.clothing_size2.clothing_type
            if ctype2.gender != school_gender:
                raise ValidationError("جنسیت لباس فرعی با جنسیت مدرسه همخوانی ندارد.")
            if school_gender == 'M' and ctype2.type != 'PANTS':
                raise ValidationError("لباس فرعی برای پسران باید شلوار باشد.")
            if school_gender == 'F' and ctype2.type != 'MAGHNAEH':
                raise ValidationError("لباس فرعی برای دختران باید مقنعه باشد.")

            if not AgreedPrice.objects.filter(school=school, clothing_size=self.clothing_size2).exists():
                raise ValidationError(f"قیمت توافقی برای {self.clothing_size2} در مدرسه {school.name} تعریف نشده است.")

    @property
    def total_agreed_amount(self):
        total = 0
        school = self.student.class_room.school
        if self.clothing_size1:
            price = AgreedPrice.objects.filter(school=school, clothing_size=self.clothing_size1).first()
            if price:
                total += price.agreed_amount
        if self.clothing_size2:
            price = AgreedPrice.objects.filter(school=school, clothing_size=self.clothing_size2).first()
            if price:
                total += price.agreed_amount
        return total

    @property
    def total_advance_amount(self):
        total = 0
        school = self.student.class_room.school
        if self.clothing_size1:
            price = AgreedPrice.objects.filter(school=school, clothing_size=self.clothing_size1).first()
            if price:
                total += price.advance_amount
        if self.clothing_size2:
            price = AgreedPrice.objects.filter(school=school, clothing_size=self.clothing_size2).first()
            if price:
                total += price.advance_amount
        return total

    @property
    def total_remaining_amount(self):
        return self.total_agreed_amount - (self.student.payments.filter(status='COMPLETED').aggregate(
            models.Sum('amount'))['amount__sum'] or 0)

    def __str__(self):
        return f"انتخاب سایز - {self.student}"