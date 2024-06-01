from django.db import models


class University(models.Model):
    name = models.CharField(max_length=300)
    website = models.URLField()

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class FacultyTRaining(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    link = models.URLField()

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty_training = models.ForeignKey(FacultyTRaining, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
