from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse

from core.models import Course, Post, Event, Review, TeacherApplication, Profile, Enrollment, Webinar


def index(request):
    top_5_courses = Course.objects.order_by('-pk')[:5]
    top_5_posts = Post.objects.order_by('-date')[:5]
    top_5_events = Event.objects.order_by('-date')[:5]
    top_5_reviews = Review.objects.order_by('-rating')[:5]

    if request.user.is_authenticated:
        try:
            profile = request.user.profile  # Get the user's profile
            enrolled_courses = profile.profile.all().values_list('course_id',
                                                                 flat=True)  # get all courses id where user is enrolled
            courses = Course.objects.exclude(pk__in=enrolled_courses)  # exclude courses where user is enrolled
        except Profile.DoesNotExist:
            # Handle the case where the user doesn't have a profile (unlikely but possible)
            courses = Course.objects.none()  # return empty queryset
    else:
        courses = Course.objects.none()

    context = {
        'title': 'Главная',
        'top_5_courses': top_5_courses,
        'top_5_posts': top_5_posts,
        'top_5_events': top_5_events,
        'top_5_reviews': top_5_reviews,
        'courses': courses,
    }
    return render(request, 'index.html', context=context)


def about(request):
    top_5_reviews = Review.objects.order_by('-rating')[:5]
    context = {
        'title': 'О нас',
        'top_5_reviews': top_5_reviews,
    }
    return render(request, 'about.html', context=context)


def courses(request):
    courses = Course.objects.all().order_by('title')
    top_5_events = Event.objects.order_by('-date')[:5]
    context = {
        'title': 'Курсы',
        'courses': courses,
        'top_5_events': top_5_events,
    }
    return render(request, 'courses.html', context=context)


@login_required
def course(request, course_id):
    course = Course.objects.get(pk=course_id)
    user_profile = request.user.profile

    try:
        enrollment = Enrollment.objects.get(profile=user_profile, course=course)
    except Enrollment.DoesNotExist:
        # return render(request, 'courses.html', context=context)
        return HttpResponseForbidden("You are not enrolled in this course.")

    webinars = Webinar.objects.filter(course=course)
    context = {
        'title': course.title,
        'course': course,
        'webinars': webinars,
    }
    return render(request, 'course_details.html', context=context)


def events(request):
    events = Event.objects.all().order_by('-date')
    context = {
        'title': 'События',
        'events': events,
    }
    return render(request, 'events.html', context=context)


def teacher_application(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        experience = request.POST.get('experience')

        if name and email and experience:
            application = TeacherApplication(name=name, email=email, experience=experience)
            application.save()
            return redirect(reverse('index'))
        else:
            return HttpResponse("Please fill in all fields.")
    return render(request, 'teacher_application_form.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Проверка на существующего пользователя
        if User.objects.filter(username=username).exists():
            return render(request, 'registration.html', {
                'error': 'Пользователь с таким именем уже существует.'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'registration.html', {
                'error': 'Пользователь с таким email уже зарегистрирован.'
            })

        # Создаем пользователя
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        # Аутентификация и вход
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))

        return render(request, 'registration.html', {
            'error': 'Что-то пошло не так. Попробуйте снова.'
        })

    return render(request, 'registration.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


def add_to_course(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        course = Course.objects.get(pk=course_id)
        profile = Profile.objects.get(user=request.user)
        Enrollment.objects.create(course=course, profile=profile)
        return redirect(reverse("index"))
    return render(request, 'add_to_course.html')


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    enroll_courses = Enrollment.objects.filter(profile=profile)
    context = {
        'profile': profile,
        'enroll_courses': enroll_courses
    }
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        profile.full_name = full_name
        profile.email = email
        profile.phone_number = phone_number
        profile.save()
    return render(request, 'profile.html', context=context)
