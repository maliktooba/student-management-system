from django.db import models
from accounts.models import Student
from courses.models import Course

class Marks(models.Model):
    class ExamType(models.TextChoices):
        QUIZ = 'QUIZ', 'Quiz'
        MIDTERM = 'MIDTERM', 'Midterm'
        FINAL = 'FINAL', 'Final'
        ASSIGNMENT = 'ASSIGNMENT', 'Assignment'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='marks')
    exam_type = models.CharField(max_length=15, choices=ExamType.choices)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    date_recorded = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course', 'exam_type')
        verbose_name_plural = "Marks"

    def __str__(self):
        return f"{self.student} - {self.course} - {self.exam_type}: {self.marks_obtained}/{self.total_marks}"

    @property
    def percentage(self):
        if self.total_marks:
            return round((self.marks_obtained / self.total_marks) * 100, 2)
        return 0