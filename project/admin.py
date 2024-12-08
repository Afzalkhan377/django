from django.contrib import admin

from .models import LiftProfile,LiftRecord, LiftPost, Comment

# Register your models here.
admin.site.register(LiftProfile)
admin.site.register(LiftRecord)
admin.site.register(LiftPost)
admin.site.register(Comment)

