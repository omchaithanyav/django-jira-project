from django.contrib import admin

# Register your models here.
from .models import Project, Sprint, Label, Issue, UserProject, Watcher, Comment

admin.site.register(Project)
admin.site.register(Sprint)
admin.site.register(Label)
admin.site.register(Issue)
admin.site.register(UserProject)
admin.site.register(Watcher)
admin.site.register(Comment)
