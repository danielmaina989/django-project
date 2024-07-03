from django.contrib import admin
from .models import Choice, Question

# Register your models here.

# class QuestionAdmin(admin.ModelAdmin):
#     fields = ["pub_date", "question_text"]
# admin.site.register(Question, QuestionAdmin)


# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3

# make the display tabular instead of inline

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

# split the form up into fields

class QuestionAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None, {"fields": ["question_text"]}),
    #     ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    # ]
        # ...
        #   inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date","was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]
    


admin.site.register(Question, QuestionAdmin)
# Adding multiple choices


