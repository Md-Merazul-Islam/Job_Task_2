from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    account_no = models.IntegerField(unique=True, blank=True, null=True)
    profile_image = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.account_no:
            last_account_no = Profile.objects.order_by('account_no').last()
            self.account_no = last_account_no.account_no + 1 if last_account_no else 5000
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile : {self.account_no}'

    @property
    def is_staff(self):
        return self.user.is_staff
