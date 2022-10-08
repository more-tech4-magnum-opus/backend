from rest_framework.generics import get_object_or_404

from events.models import EventAttendance


def submit_attendance(token: str):
    attendance = get_object_or_404(EventAttendance, token=token)
    if not attendance.attended:
        attendance.attended = True
        attendance.save()

        attendance.event.attended += 1
        attendance.event.save()
