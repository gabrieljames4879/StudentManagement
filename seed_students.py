from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from students.models import Student

class Command(BaseCommand):
    help = 'Seeds sample student records and demo admin account (admin / admin12345)'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@school.edu', 'admin12345')
            self.stdout.write(self.style.SUCCESS('Created demo admin user: admin / admin12345'))

        sample_data = [
            ('2026-0001', 'Maria Clara Santos', 'maria.santos@school.edu', 'Computer Science', 94.50),
            ('2026-0002', 'Juan Dela Cruz', 'juan.delacruz@school.edu', 'Computer Science', 88.25),
            ('2026-0003', 'Angela Reyes', 'angela.reyes@school.edu', 'Computer Science', 91.00),
            ('2026-0004', 'Carlos Mendoza', 'carlos.mendoza@school.edu', 'Engineering', 84.75),
            ('2026-0005', 'Sofia Bautista', 'sofia.bautista@school.edu', 'Engineering', 89.50),
            ('2026-0006', 'Miguel Torres', 'miguel.torres@school.edu', 'Engineering', 73.00),
            ('2026-0007', 'Camille Ramos', 'camille.ramos@school.edu', 'Business Admin', 90.20),
            ('2026-0008', 'Rafael Navarro', 'rafael.navarro@school.edu', 'Business Admin', 82.40),
            ('2026-0009', 'Bea Alonzo', 'bea.alonzo@school.edu', 'Graphic Design', 95.00),
            ('2026-0010', 'Marco Villanueva', 'marco.villanueva@school.edu', 'Graphic Design', 87.80),
            ('2026-0011', 'Elena Flores', 'elena.flores@school.edu', 'Graphic Design', 92.15),
            ('2026-0012', 'Daniel Castro', 'daniel.castro@school.edu', 'Computer Science', 79.50),
        ]

        created_count = 0
        for sid, name, email, course, grade in sample_data:
            _, created = Student.objects.get_or_create(
                student_id=sid,
                defaults={'name': name, 'email': email, 'course': course, 'grade': grade}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} new sample student records!'))
