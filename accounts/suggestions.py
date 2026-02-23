def generate_suggestions(student_user):
    """Generate smart suggestions based on student performance"""
    from analytics_app.models import Mark, Attendance
    from django.db.models import Avg

    suggestions = []

    # Get student's marks
    all_marks = Mark.objects.filter(student=student_user)
    overall_avg = all_marks.aggregate(Avg('marks_obtained'))['marks_obtained__avg'] or 0

    # Get student's attendance
    total_attendance = Attendance.objects.filter(student=student_user).count()
    present_days = Attendance.objects.filter(student=student_user, is_present=True).count()
    attendance_percentage = (present_days / total_attendance * 100) if total_attendance > 0 else 0

    # SUGGESTION 1: Attendance Warning
    if attendance_percentage < 75:
        suggestions.append({
            'type': 'warning',
            'emoji': '⚠️',
            'title': 'Improve Your Attendance',
            'message': f'Your attendance is {attendance_percentage:.1f}%. Attendance below 75% may affect your overall performance. Try to attend all classes regularly.',
            'priority': 'high'
        })
    elif attendance_percentage < 85:
        suggestions.append({
            'type': 'info',
            'emoji': '📌',
            'title': 'Attendance Could Be Better',
            'message': f'Your attendance is {attendance_percentage:.1f}%. Aim to increase it to 90% or above for better performance.',
            'priority': 'medium'
        })

    # SUGGESTION 2: Performance Level
    if overall_avg < 50:
        suggestions.append({
            'type': 'danger',
            'emoji': '🚨',
            'title': 'Critical: Focus on Your Studies',
            'message': f'Your current average is {overall_avg:.1f}%. This is below passing. Please speak with your teachers and focus on improving immediately.',
            'priority': 'high'
        })
    elif overall_avg < 60:
        suggestions.append({
            'type': 'warning',
            'emoji': '⚠️',
            'title': 'Focus on Your Studies',
            'message': f'Your current average is {overall_avg:.1f}%. Consider dedicating more time to your subjects and seeking help from your teachers.',
            'priority': 'high'
        })
    elif overall_avg < 75:
        suggestions.append({
            'type': 'info',
            'emoji': '📌',
            'title': 'Aim for Better Grades',
            'message': f'Your average is {overall_avg:.1f}%. With a bit more effort, you can push this higher. Focus on weak subjects.',
            'priority': 'medium'
        })
    elif overall_avg >= 80:
        suggestions.append({
            'type': 'success',
            'emoji': '✅',
            'title': 'Keep Up the Good Work!',
            'message': f'Your overall performance ({overall_avg:.1f}%) is excellent! Consistency is key to continued success.',
            'priority': 'low'
        })

    # SUGGESTION 3: Subject-specific
    if all_marks.exists():
        from django.db.models import Avg as AvgFunc
        subject_performance = all_marks.values('subject__name').annotate(avg=AvgFunc('marks_obtained')).order_by('avg')

        if subject_performance.exists():
            worst_subject = subject_performance.first()
            if worst_subject['avg'] < 60:
                suggestions.append({
                    'type': 'warning',
                    'emoji': '📚',
                    'title': f'Focus on {worst_subject["subject__name"]}',
                    'message': f'Your average in {worst_subject["subject__name"]} is {worst_subject["avg"]:.1f}%. This needs improvement. Allocate more study time to this subject.',
                    'priority': 'high'
                })
            elif worst_subject['avg'] < 75:
                suggestions.append({
                    'type': 'info',
                    'emoji': '📚',
                    'title': f'Improve {worst_subject["subject__name"]}',
                    'message': f'Your average in {worst_subject["subject__name"]} is {worst_subject["avg"]:.1f}%. Try to improve it through practice and revision.',
                    'priority': 'medium'
                })

    # SUGGESTION 4: Positive reinforcement
    if overall_avg >= 80 and attendance_percentage >= 90:
        suggestions.append({
            'type': 'success',
            'emoji': '🎯',
            'title': 'You\'re on Track!',
            'message': 'Excellent work! Both your grades and attendance are strong. Continue this momentum and you\'ll achieve great results.',
            'priority': 'low'
        })

    # SUGGESTION 5: General advice
    suggestions.append({
        'type': 'info',
        'emoji': '🌱',
        'title': 'General Tips for Success',
        'message': 'Review weak areas regularly, practice consistently, and don\'t hesitate to ask teachers for clarification. Regular effort compounds to excellent results!',
        'priority': 'low'
    })

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    suggestions.sort(key=lambda x: priority_order.get(x['priority'], 3))

    return suggestions