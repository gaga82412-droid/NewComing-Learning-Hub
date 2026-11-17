from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField(blank=True, default='')
    career = models.TextField(blank=True, default='')
    semester = models.IntegerField()

    def __str__(self):
        return self.name


class Resource(models.Model):
    title = models.CharField(max_length=200)

    link = models.URLField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='resources'
    )

    def __str__(self):
        return self.title