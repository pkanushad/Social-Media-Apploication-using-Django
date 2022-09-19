from django.contrib import admin
from blog_app.models import UserProfile,Blogs,Comments
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Blogs)
admin.site.register(Comments)
