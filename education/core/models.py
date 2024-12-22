
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Модель для профилей пользователей
class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('student', _('Студент')),
        ('teacher', _('Преподаватель')),
    ]
    full_name = models.CharField(max_length=255, verbose_name=_("Полное имя"))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_("Пользователь"))
    email = models.EmailField(verbose_name=_("Электронная почта"))
    phone_number = models.CharField(max_length=20, verbose_name=_("Номер телефона"))
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student', verbose_name=_("Тип пользователя"))

    class Meta:
        verbose_name = _("Профиль")
        verbose_name_plural = _("Профили")

    def __str__(self):
        return f"{self.user.username} ({self.user_type})"


# Модель курсов
class Course(models.Model):
    image = models.ImageField(upload_to='courses/', verbose_name=_("Изображение"))
    title = models.CharField(max_length=255, verbose_name=_("Название курса"))
    description = models.TextField(verbose_name=_("Описание курса"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Стоимость курса"))

    class Meta:
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")

    def __str__(self):
        return self.title


# Модель записи на курс
class Enrollment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile', verbose_name=_("Профиль"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name=_("Курс"))

    class Meta:
        verbose_name = _("Запись на курс")
        verbose_name_plural = _("Записи на курсы")

    def __str__(self):
        return f"{self.profile.full_name} - {self.course.title}"


# Модель событий
class Event(models.Model):
    image = models.ImageField(upload_to='events/', verbose_name=_("Изображение"))
    date = models.DateField(verbose_name=_("Дата события"))
    title = models.CharField(max_length=255, verbose_name=_("Название события"))
    description = models.TextField(verbose_name=_("Описание события"))

    class Meta:
        verbose_name = _("Событие")
        verbose_name_plural = _("События")

    def __str__(self):
        return self.title


# Модель отзывов
class Review(models.Model):
    profile = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL, related_name='reviews',
                                verbose_name=_("Профиль"))
    course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Курс"))
    rating = models.PositiveSmallIntegerField(verbose_name=_("Оценка"))
    text = models.TextField(verbose_name=_("Текст отзыва"))

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self):
        return f"{self.profile or _('Аноним')} - {self.rating}/5"


# Модель анкеты преподавателей
class TeacherApplication(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Имя"))
    email = models.EmailField(verbose_name=_("Электронная почта"))
    experience = models.TextField(verbose_name=_("Опыт работы"))

    class Meta:
        verbose_name = _("Анкета преподавателя")
        verbose_name_plural = _("Анкеты преподавателей")

    def __str__(self):
        return self.name


# Модель постов
class Post(models.Model):
    image = models.ImageField(upload_to='posts/', verbose_name=_("Изображение"))
    date = models.DateField(auto_now_add=True, verbose_name=_("Дата публикации"))
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts', verbose_name=_("Автор"))
    title = models.CharField(max_length=255, verbose_name=_("Заголовок"))
    text = models.TextField(verbose_name=_("Текст поста"))

    class Meta:
        verbose_name = _("Пост")
        verbose_name_plural = _("Посты")

    def __str__(self):
        return self.title


# Модель вебинаров
class Webinar(models.Model):
    video_link = models.URLField(verbose_name=_("Ссылка на видео"))
    title = models.CharField(max_length=255, verbose_name=_("Название вебинара"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание вебинара"))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='webinars', verbose_name=_("Курс"))

    class Meta:
        verbose_name = _("Вебинар")
        verbose_name_plural = _("Вебинары")

    def __str__(self):
        return self.title


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
