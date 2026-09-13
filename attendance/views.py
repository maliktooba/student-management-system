from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course
from .models import Attendance

@login_required
def mark_attendance(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Security check: teacher can only mark attendance for their own course
    if request.user.role != 'TEACHER' or course.teacher.user != request.user:
        return redirect('dashboard')

    enrollments = course.enrollments.select_related('student__user')

    if request.method == 'POST':
        date = request.POST.get('date')
        for enrollment in enrollments:
            status = request.POST.get(f'status_{enrollment.student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=enrollment.student,
                    course=course,
                    date=date,
                    defaults={'status': status}
                )
        messages.success(request, 'Attendance saved successfully.')
        return redirect('mark_attendance', course_id=course.id)

    return render(request, 'attendance/mark_attendance.html', {
        'course': course,
        'enrollments': enrollments,
        'status_choices': Attendance.Status.choices,
    })