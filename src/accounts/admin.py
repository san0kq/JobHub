from django.contrib import admin

from accounts.models import (
    EmailConfirmationCode,
    Client,
    Freelancer,
    User
)

admin.site.register(EmailConfirmationCode)
admin.site.register(Client)
admin.site.register(Freelancer)
admin.site.register(User)
