from django.contrib import admin

from testing.models import Test, TestResult, User, Question, UserAnswer

# Register your models here.

admin.site.register(Test)
admin.site.register(TestResult)
admin.site.register(User)
admin.site.register(Question)
admin.site.register(UserAnswer)