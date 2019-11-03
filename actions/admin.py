from django.contrib import admin
from .models import Action


class ActionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'verb', 'target', 'created',)
    list_filter = ('created',)
    search_fields = ('user', 'verb',)

admin.site.register(Action, ActionsAdmin)
