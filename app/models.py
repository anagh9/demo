from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def get_total_income(self):
        total_credit = self.incomeexpense_set.filter(
            type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        total_debit = self.incomeexpense_set.filter(type='expense').aggregate(
            models.Sum('amount'))['amount__sum'] or 0
        return total_credit - total_debit
    
    @property
    def get_total_credit(self):
        total_credit = self.incomeexpense_set.filter(
            type='income').aggregate(models.Sum('amount'))['amount__sum'] or 0
        return total_credit

    @property
    def get_total_debit(self):
        total_debit = self.incomeexpense_set.filter(type='expense').aggregate(
            models.Sum('amount'))['amount__sum'] or 0
        return total_debit

    def __str__(self):
        return self.name


class IncomeExpense(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField()
    date = models.DateField()
    category = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=255, choices=TYPE_CHOICES)

    def __str__(self):
        return self.category

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

