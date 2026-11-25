from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    COURSE_CHOICES = [
        ('Computer Science', 'Computer Science'),
        ('Business Admin', 'Business Admin'),
        ('Engineering', 'Engineering'),
        ('Graphic Design', 'Graphic Design'),
    ]

    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    course = models.CharField(max_length=50, choices=COURSE_CHOICES)
    grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_id} - {self.name}"
