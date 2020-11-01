from django.contrib import admin

from .models import User, posts, follow, likes

# Register your models here.
admin.site.register(User)
admin.site.register(posts)
admin.site.register(follow)
admin.site.register(likes)
