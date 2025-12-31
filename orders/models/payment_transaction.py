# orders/models/payment_transaction.py
from django.db import models

from core.models import BaseModel, Student,AcademicYear


class PaymentTransaction(BaseModel):
    academic_year = models.ForeignKey('core.AcademicYear', on_delete=models.PROTECT, verbose_name="سال تحصیلی")
    TYPE_CHOICES = [
        ('ADVANCE', 'علی‌الحساب'),
        ('FINAL', 'تسویه نهایی'),
        ('EXTRA', 'پرداخت اضافی'),
        ('REFUND', 'استرداد'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'در انتظار'),
        ('COMPLETED', 'تکمیل شده'),
        ('FAILED', 'ناموفق'),
        ('CANCELLED', 'لغو شده'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name="دانش‌آموز"
    )
    payment_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='ADVANCE', verbose_name="نوع پرداخت")
    amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="مبلغ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name="وضعیت")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ پرداخت")
    reference_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="شماره پیگیری درگاه")
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات")

    class Meta:
        verbose_name = "تراکنش پرداخت"
        verbose_name_plural = "تراکنش‌های پرداخت"
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.get_payment_type_display()} {self.amount:,} تومان - {self.student}"