# uniforms/models/sizes/maghnaeh_size.py
from django.db import models
from core.models import BaseModel


class MaghnaehSize(BaseModel):
    MAGHNAEH_SIZES = [
        ('1', 'سایز ۱'),
        ('2', 'سایز ۲'),
        ('3', 'سایز ۳'),
        ('4', 'سایز ۴'),
        ('5', 'سایز ۵'),
        ('90', '۹۰'),
        ('100', '۱۰۰'),
    ]

    size = models.CharField(max_length=10, choices=MAGHNAEH_SIZES, unique=True, verbose_name="سایز مقنعه")

    class Meta:
        verbose_name = "سایز مقنعه"
        verbose_name_plural = "سایزهای مقنعه"

    def __str__(self):
        return self.get_size_display()