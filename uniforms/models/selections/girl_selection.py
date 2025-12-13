# uniforms/models/selections/girl_selection.py
from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel, Student
from ..sizes.mantoo_size import MantooSize
from ..sizes.maghnaeh_size import MaghnaehSize
from ..prices.mantoo_price import AgreedMantooPrice
from ..prices.maghnaeh_price import AgreedMaghnaehPrice


class StudentSelectionGirl(BaseModel):
    student = models.OneToOneField(
        'core.Student',
        on_delete=models.PROTECT,
        limit_choices_to={'class_room__school__gender': 'F'},
        related_name='girl_selection',
        verbose_name="دانش‌آموز"
    )
    mantoo_size = models.ForeignKey(
        MantooSize,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='girl_selections',
        verbose_name="سایز مانتو انتخابی"
    )
    maghnaeh_size = models.ForeignKey(
        MaghnaehSize,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='girl_selections',
        verbose_name="سایز مقنعه انتخابی"
    )

    class Meta:
        verbose_name = "انتخاب سایز دخترانه"
        verbose_name_plural = "انتخاب‌های سایز دخترانه"

    def clean(self):
        super().clean()
        school = self.student.class_room.school if self.student else None
        if not school:
            return

        if self.mantoo_size:
            if not AgreedMantooPrice.objects.filter(school=school, size=self.mantoo_size).exists():
                raise ValidationError(f"برای سایز مانتو {self.mantoo_size} در مدرسه {school.name} قیمت توافقی تعریف نشده است.")
        if self.maghnaeh_size:
            if not AgreedMaghnaehPrice.objects.filter(school=school, size=self.maghnaeh_size).exists():
                raise ValidationError(f"برای سایز مقنعه {self.maghnaeh_size} در مدرسه {school.name} قیمت توافقی تعریف نشده است.")

    @property
    def mantoo_price(self):
        if not self.mantoo_size or not self.student:
            return None
        try:
            return AgreedMantooPrice.objects.get(
                school=self.student.class_room.school,
                size=self.mantoo_size
            )
        except AgreedMantooPrice.DoesNotExist:
            return None

    @property
    def maghnaeh_price(self):
        if not self.maghnaeh_size or not self.student:
            return None
        try:
            return AgreedMaghnaehPrice.objects.get(
                school=self.student.class_room.school,
                size=self.maghnaeh_size
            )
        except AgreedMaghnaehPrice.DoesNotExist:
            return None

    @property
    def total_agreed_amount(self):
        total = 0
        if self.mantoo_price:
            total += self.mantoo_price.agreed_amount
        if self.maghnaeh_price:
            total += self.maghnaeh_price.agreed_amount
        return total

    @property
    def total_advance_amount(self):
        total = 0
        if self.mantoo_price:
            total += self.mantoo_price.advance_amount
        if self.maghnaeh_price:
            total += self.maghnaeh_price.advance_amount
        return total

    @property
    def total_final_amount(self):
        return self.total_agreed_amount - self.total_advance_amount

    def __str__(self):
        return f"انتخاب سایز دخترانه - {self.student}"