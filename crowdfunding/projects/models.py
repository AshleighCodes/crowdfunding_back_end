from django.db import models
from django.contrib.auth import get_user_model

# Create your models here - ORIGINAL.
# class Project(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     goal = models.IntegerField()
#     image = models.URLField()
#     is_open = models.BooleanField()
#     date_created = models.DateTimeField(auto_now_add=True)
#     owner = models.ForeignKey(
#         get_user_model(),
#         on_delete=models.CASCADE,
#         related_name='owned_projects'
#         )

# class Pledge(models.Model):
#     amount = models.IntegerField()
#     comment = models.CharField(max_length=200)
#     anonymous = models.BooleanField()
#     project = models.ForeignKey(
#         'Project',
#         on_delete=models.CASCADE,
#         related_name='pledges'
#         )
#     supporter = models.ForeignKey(
#         get_user_model(),
#         on_delete=models.CASCADE,
#         related_name='pledges'
#         )

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )

    def check_goal_reached(self):
        total_pledged = sum(pledge.amount for pledge in self.pledges.all())
        if total_pledged >= self.goal:
            self.is_open = False
            self.save()

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='pledges'
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.check_goal_reached()