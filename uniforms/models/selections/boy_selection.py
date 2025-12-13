# uniforms/models/selections/boy_selection.py
from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel, Student
from ..sizes.shirt_size import ShirtSize
from ..sizes.pants_size import PantsSize
from ..prices.shirt_price import AgreedShirtPrice
from ..prices.pants_price import AgreedPantsPrice


class StudentSelectionBoy(BaseModel):
    student = models.OneToOneField(
        'core.Student',
        on_delete=models.PROTECT,
        limit_choices_to={'class_room__school__gender': 'M'},
        related_name='boy_selection',
        verbose_name="دانش‌آموز"
    )
    shirt_size = models.ForeignKey(
        ShirtSize,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='boy_selections',
        verbose_name="سایز پیراهن انتخابی"
    )
    pants_size = models.ForeignKey(
        PantsSize,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name='boy_selections',
        verbose_name="سایز شلوار انتخابی"
    )

    class Meta:
        verbose_name = "انتخاب سایز پسرانه"
        verbose_name_plural = "انتخاب‌های سایز پسرانه"

    def clean(self):
        super().clean()
        school = self.student.class_room.school if self.student else None
        if not school:
            return

        # چک کردن وجود قیمت توافقی برای سایز انتخابی
        if self.shirt_size:
            if not AgreedShirtPrice.objects.filter(school=school, size=self.shirt_size).exists():
                raise ValidationError(f"برای سایز پیراهن {self.shirt_size} در مدرسه {school.name} قیمت توافقی تعریف نشده است.")
        if self.pants_size:
            if not AgreedPantsPrice.objects.filter(school=school, size=self.pants_size).exists():
                raise ValidationError(f"برای سایز شلوار {self.pants_size} در مدرسه {school.name} قیمت توافقی تعریف نشده است.")

    @property
    def shirt_price(self):
        if not self.shirt_size or not self.student:
            return None
        try:
            return AgreedShirtPrice.objects.get(
                school=self.student.class_room.school,
                size=self.shirt_size
            )
        except AgreedShirtPrice.DoesNotExist:
            return None

    @property
    def pants_price(self):
        if not self.pants_size or not self.student:
            return None
        try:
            return AgreedPantsPrice.objects.get(
                school=self.student.class_room.school,
                size=self.pants_size
            )
        except AgreedPantsPrice.DoesNotExist:
            return None

    @property
    def total_agreed_amount(self):
        total = 0
        if self.shirt_price:
            total += self.shirt_price.agreed_amount
        if self.pants_price:
            total += self.pants_price.agreed_amount
        return total

    @property
    def total_advance_amount(self):
        total = 0
        if self.shirt_price:
            total += self.shirt_price.advance_amount
        if self.pants_price:
            total += self.pants_price.advance_amount
        return total

    @property
    def total_final_amount(self):
        return self.total_agreed_amount - self.total_advance_amount

    def __str__(self):
        return f"انتخاب سایز پسرانه - {self.student}"