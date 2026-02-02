# uniforms/admin.py
from django.contrib import admin
from .models import ClothingType, ClothingSize, AgreedPrice


@admin.register(ClothingType)
class ClothingTypeAdmin(admin.ModelAdmin):
    list_display = ['get_gender_display', 'get_type_display']
    list_filter = ['gender']
    search_fields = ['type']


@admin.register(ClothingSize)
class ClothingSizeAdmin(admin.ModelAdmin):
    list_display = ['size', 'clothing_type']
    list_filter = ['clothing_type__gender', 'clothing_type__type']
    search_fields = ['size', 'clothing_type__type']
    raw_id_fields = ['clothing_type']  # برای انتخاب سریع نوع لباس


@admin.register(AgreedPrice)
class AgreedPriceAdmin(admin.ModelAdmin):
    list_display = ['academic_year', 'school', 'clothing_size', 'agreed_amount', 'advance_amount']
    list_filter = ['academic_year', 'school', 'clothing_size__clothing_type__gender']
    search_fields = ['school__name', 'clothing_size__size']
    raw_id_fields = ['academic_year', 'school', 'clothing_size']