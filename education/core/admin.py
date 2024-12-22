from django.contrib import admin
from .models import Profile, Course, Enrollment, Event, Review, TeacherApplication, Post, Webinar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone_number', 'user_type')
    search_fields = ('user__username', 'full_name', 'email', 'phone_number')
    list_filter = ('user_type',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    search_fields = ('title',)
    list_filter = ('price',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'course')
    search_fields = ('profile__full_name', 'course__title')
    list_filter = ('course',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date')
    search_fields = ('title',)
    list_filter = ('date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('profile', 'course', 'rating', 'text')
    search_fields = ('profile__full_name', 'course__title', 'text')
    list_filter = ('rating', 'course')


@admin.register(TeacherApplication)
class TeacherApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    search_fields = ('title', 'author__full_name')
    list_filter = ('date',)


@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)
