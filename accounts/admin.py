from django.contrib import admin
from .models import Category, Claim,Item

# Register your models here.

class ClaimAdmin(admin.ModelAdmin):
    list_display= ['item', 'user', 'status', 'created_at']
    list_fliter = ['status']
    action = ['approve_claims', 'reject_claims']

    def approve_claims(self, request, queryset):
        queryset.update(status='approved')
        for claim in queryset:
            claim.item.status = 'claimed'
            claim.item.save()
        self.message_user(request, f"{queryset.count()} claims approved.")
    approve_claims.short_description = 'Approve selected claims'

    def reject_claims(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} claims rejected.")
    reject_claims.shory_description = 'Reject selected claims'


admin.site.register(Category)
admin.site.register(Claim)
admin.site.register(Item)