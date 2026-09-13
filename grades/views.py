from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course
from .models import Marks

@login_required
def enter_marks(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Security check: teacher can only enter marks for their own course
    if request.user.role != 'TEACHER' or course.teacher.user != request.user:
        return redirect('dashboard')

    enrollments = course.enrollments.select_related('student__user')
    exam_types = Marks.ExamType.choices

    if request.method == 'POST':
        exam_type = request.POST.get('exam_type')
        total_marks = request.POST.get('total_marks')

        for enrollment in enrollments:
            obtained = request.POST.get(f'marks_{enrollment.student.id}')
            if obtained:  # skip blanks instead of saving empty rows
                Marks.objects.update_or_create(
                    student=enrollment.student,
                    course=course,
                    exam_type=exam_type,
                    defaults={
                        'marks_obtained': obtained,
                        'total_marks': total_marks,
                    }
                )
        messages.success(request, 'Marks saved successfully.')
        return redirect('enter_marks', course_id=course.id)

    return render(request, 'grades/enter_marks.html', {
        'course': course,
        'enrollments': enrollments,
        'exam_types': exam_types,
    })