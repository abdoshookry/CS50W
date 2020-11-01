from django.contrib import admin
from .models import User
from .models import auction_listings, comments, bid, watchlists

# Register your models here.
admin.site.register(User)
admin.site.register(auction_listings)
admin.site.register(comments)
admin.site.register(bid)
admin.site.register(watchlists)