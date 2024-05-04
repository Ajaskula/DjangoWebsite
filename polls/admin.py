from django.contrib import admin
from .models import  SVGImage, Rectangle

class RectangleInline(admin.TabularInline):
    model = Rectangle
    extra = 1

class SVGImageAdmin(admin.ModelAdmin):
    inlines = [RectangleInline]

# admin.site.register(Question)
admin.site.register(SVGImage, SVGImageAdmin)
# admin.site.register(Editor)
