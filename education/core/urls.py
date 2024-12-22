from django.urls import path
from core.views import (
    index,
    about,
    courses,
    events,
    teacher_application,
    course,
    register,
    logout_view,
    login_view,
    add_to_course,
    profile
)

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('courses/', courses, name='course_all'),
    # single course
    path('courses/<int:course_id>/', course, name='course'),
    path('events/', events, name='events_all'),
    # single event
    path('teacher_application/', teacher_application, name='teacher_application'),
    path('accounts/login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('accounts/logout/', logout_view, name='logout'),
    path('add_to_course/', add_to_course, name='add_to_course'),
    path('profile/', profile, name='profile'),

]
