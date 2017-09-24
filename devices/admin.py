from django.contrib import admin
from devices import models

# Register your models here.
admin.site.register(models.Device)
admin.site.register(models.ActionInput)
admin.site.register(models.ActionOutput)
admin.site.register(models.ConfigTask)
admin.site.register(models.Task)
admin.site.register(models.Monitor)
