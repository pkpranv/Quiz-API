from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
                email=self.normalize_email(email)
                )
        user.set_password(password)
        user.name = name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """creates and saves a new superuser with given details"""
        user = self.create_user(email,"super user", password)
        user.role = 'admin'
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255,default='username')
    active = models.BooleanField(default=True)
    role = models.CharField(max_length=255, default='normal user')
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin()

    def is_admin(self):
        return self.role == 'admin'

class Answer(models.Model):
    answer = models.CharField(max_length=25)

    def __str__(self):
        return self.answer

class Question(models.Model):
    question = models.TextField()
    choices = models.ManyToManyField(Answer, related_name='choice_set')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    def __str__(self):
        return self.question

class UserExamDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def number_of_correct_answer(self):
        return UserAnswer.objects.filter(user_exam_id = self.id, is_correct=True).count()

    def __str__(self):
        return self.user.name

class UserAnswer(models.Model):
    user_exam = models.ForeignKey(UserExamDetail, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=True)

    def __str__(self):
        return self.user_exam.user.name