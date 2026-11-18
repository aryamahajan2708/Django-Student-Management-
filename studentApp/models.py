from django.db import models

class Person(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField()
    mobile = models.CharField(max_length=10)
    email = models.EmailField()
    course = models.CharField(max_length=200)
    
    # Naye fields fees track karne ke liye
    total_fees = models.IntegerField(default=10000) 
    paid_installments = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    name = models.CharField(max_length=100)
    # Add your other student fields here

    def __str__(self):
        return self.name

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def pending_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"{self.student.name} - Paid: {self.paid_amount} / {self.total_amount}"