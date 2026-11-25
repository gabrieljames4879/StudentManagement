import csv
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from .models import Student
from .forms import StudentForm

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student record added successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please check your input (duplicate ID/email or grade outside 0-100).')
    else:
        form = StudentForm()

    query = request.GET.get('q', '').strip()
    selected_course = request.GET.get('course', '').strip()
    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )
    if selected_course:
        students = students.filter(course=selected_course)

    course_stats = Student.objects.values('course').annotate(
        total=Count('id'),
        avg_grade=Avg('grade')
    ).order_by('course')

    labels = [item['course'] for item in course_stats]
    counts = [item['total'] for item in course_stats]
    avg_grades = [round(float(item['avg_grade'] or 0), 2) for item in course_stats]

    total_count = Student.objects.count()
    overall_avg = Student.objects.aggregate(Avg('grade'))['grade__avg']
    passing_count = Student.objects.filter(grade__gte=75).count()
    honor_count = Student.objects.filter(grade__gte=90).count()
    passing_rate = round((passing_count / total_count) * 100, 1) if total_count else 0

    # Course breakdown percentages for Donut chart
    course_breakdown = []
    for item in course_stats:
        pct = round((item['total'] / total_count) * 100, 1) if total_count else 0
        course_breakdown.append({
            'course': item['course'],
            'total': item['total'],
            'pct': pct
        })

    top_students = Student.objects.order_by('-grade')[:5]

    context = {
        'form': form,
        'students': students,
        'top_students': top_students,
        'query': query,
        'selected_course': selected_course,
        'course_choices': [c[0] for c in Student.COURSE_CHOICES],
        'total_students': total_count,
        'overall_avg': round(float(overall_avg), 2) if overall_avg else 0,
        'passing_rate': passing_rate,
        'honor_count': honor_count,
        'course_breakdown': course_breakdown,
        'labels_json': json.dumps(labels),
        'counts_json': json.dumps(counts),
        'avg_grades_json': json.dumps(avg_grades),
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f'Updated record for {student.name}.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid input. Please check the fields.')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit_student.html', {'form': form, 'student': student})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student record deleted.')
    return redirect('dashboard')

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_analytics_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Full Name', 'Email', 'Course', 'Grade (%)', 'Status'])
    for s in Student.objects.all():
        status = 'Passed' if s.grade >= 75 else 'Below 75'
        writer.writerow([s.student_id, s.name, s.email, s.course, s.grade, status])
    return response
