from django.db import models


class University(models.Model):
    name = models.CharField(max_length=300)
    website = models.URLField()
    description = models.TextField()

    class Meta:
        verbose_name = "University"
        verbose_name_plural = "Universities"

    def __str__(self):
        return self.name


class College(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    link = models.URLField()
    college_description = models.TextField()

    def __str__(self):
        return self.name


class Department(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    department_description = models.TextField()

    def __str__(self):
        return self.name
