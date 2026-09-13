from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from accounts.models import Teacher, Student, User
from courses.models import Course
from attendance.models import Attendance

@login_required
def dashboard_redirect(request):
    role = request.user.role
    if role == 'ADMIN':
        total_students = Student.objects.count()
        total_teachers = Teacher.objects.count()
        total_courses = Course.objects.count()

        total_attendance_records = Attendance.objects.count()
        present_count = Attendance.objects.filter(status='PRESENT').count()
        if total_attendance_records > 0:
            attendance_percentage = round((present_count / total_attendance_records) * 100, 2)
        else:
            attendance_percentage = 0

        recent_students = Student.objects.select_related('user').order_by('-id')[:5]

        return render(request, 'dashboard_admin.html', {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'attendance_percentage': attendance_percentage,
            'recent_students': recent_students,
        })
    elif role == 'TEACHER':
        teacher = Teacher.objects.get(user=request.user)
        courses = teacher.courses.all()
        return render(request, 'dashboard_teacher.html', {'courses': courses})
    elif role == 'STUDENT':
        student = Student.objects.get(user=request.user)
        enrollments = student.enrollments.select_related('course')
        attendance_records = student.attendance_records.select_related('course').order_by('-date')
        marks_records = student.marks.select_related('course')
        return render(request, 'dashboard_student.html', {
            'enrollments': enrollments,
            'attendance_records': attendance_records,
            'marks_records': marks_records,
        })
    return redirect('login')