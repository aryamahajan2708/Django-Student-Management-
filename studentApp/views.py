from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
import math
import datetime
from django.db.models import Sum
from .models import Student, Fee 

# Apne courses aur unki total fees yahan set karein
COURSE_FEES = {
    'Basic Computer Course':4000,
    'Web Development':16000,
    'Web Designing':10000,
    'Digital Marketing':15000,
    'Graphic Designing':8000,
    'Tally with GST':5000,
    'Advanced Excel':6000,
    'Programming in Python':10000,
    'Java Programming':14000,
    'Full Stack Development':20000,
    'Data Entry & Typing':2000,
    'Artificial Intelligence (AI)':20000
}

def home(request):
    return render(request, 'home.html')

# def dashboard(request):
#     total_students = Person.objects.count()
#     return render(request, 'dashboard.html', {'total_students': total_students})

def dashboard(request):
    students = Person.objects.all()
    total_students = students.count()
    
    # Calculate total collected and pending fees from Person model
    total_collected = 0
    total_assigned = 0
    
    for student in students:
        paid = student.paid_installments * 2000
        # Ensure paid does not exceed total_fees (e.g., for ₹2500 or ₹4500 courses)
        if paid > student.total_fees:
            paid = student.total_fees
        total_collected += paid
        total_assigned += student.total_fees

    pending_fees = total_assigned - total_collected

    context = {
        'total_students': total_students,
        'total_collected': total_collected,
        'pending_fees': pending_fees,
    }
    return render(request, 'dashboard.html', context)

def add(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        course = request.POST.get('course')
        mobile = request.POST.get('mobile')
        age = request.POST.get('age')
        email = request.POST.get('email')

        # Course ke hisab se total fees nikalna (agar list me nahi hai to default 10000)
        fees = COURSE_FEES.get(course, 10000)

        Person.objects.create(
            first_name=fname,
            last_name=lname,
            age=age,
            course=course,
            mobile=mobile,
            email=email,
            total_fees=fees,
            paid_installments=0
        )
        return redirect('add')
    return render(request, 'add.html')

def view(request):
    per = Person.objects.all()
    return render(request, 'view.html', {'persons': per})

def confirm_person(request):
    if request.method == 'POST':
        first_name = request.POST.get('fName')
        last_name = request.POST.get('lName')
        P = Person.objects.filter(first_name__iexact=first_name, last_name__iexact=last_name)
        
        if P.count() == 1:
            p = P.first()
            return redirect('update_person', id=p.id)
        elif P.count() > 1:
            return render(request, 'confirm.html', {'error': 'Multiple students found. Please use a unique student ID.'})
        else:
            return render(request, 'confirm.html', {'error': 'Student not found! Please check the name.'})
    return render(request, 'confirm.html')

def update_person(request, id):
    persons = get_object_or_404(Person, id=id)
    if request.method == 'POST':
        persons.first_name = request.POST.get('fName')
        persons.last_name = request.POST.get('lName')
        persons.age = request.POST.get('age')
        persons.mobile = request.POST.get('mobile')
        persons.email = request.POST.get('email')
        persons.course = request.POST.get('course')
        persons.total_fees = COURSE_FEES.get(persons.course, 10000)
        persons.save()
        return redirect('add')
    return render(request, 'update.html', {'persons': persons})

def delete_person(request, id):
    person = get_object_or_404(Person, id=id)
    person.delete()
    return redirect('view')

# --- COLLECT FEES VIEW ---
def collectfees(request):
    students = Person.objects.all()
    selected_student = None
    installments_list = []

    # Jab kisi student ke naam par click hoga (GET request se id aayegi)
    student_id = request.GET.get('student_id')
    if student_id:
        selected_student = get_object_or_404(Person, id=student_id)
        
        # Agar purane student ki fees 0 hai to course ke hisab se update karein
        if selected_student.total_fees == 0:
            selected_student.total_fees = COURSE_FEES.get(selected_student.course, 10000)
            selected_student.save()

        # 2000 ke hisab se total installments calculate karna
        total_inst = math.ceil(selected_student.total_fees / 2000)
        for i in range(1, total_inst + 1):
            installments_list.append({
                'number': i,
                'amount': 2000,
                'is_paid': i <= selected_student.paid_installments
            })

    # Jab Save & Generate Receipt button par click hoga
    if request.method == 'POST':
        s_id = request.POST.get('student_id')
        student = get_object_or_404(Person, id=s_id)
        
        # Kitne checkboxes tick kiye gaye hain unhe count karna
        checked_installments = request.POST.getlist('installment_check')
        new_paid_count = len(checked_installments)
        
        # Nayi pay ki gayi installments nikalna receipt ke liye
        newly_paid = new_paid_count - student.paid_installments
        if newly_paid < 0:
            newly_paid = 0
            
        student.paid_installments = new_paid_count
        student.save()
        
        # Receipt page par bhejne ke liye data session mein save karna
        request.session['receipt_data'] = {
            'student_id': student.id,
            'name': f"{student.first_name} {student.last_name}",
            'course': student.course,
            'mobile': student.mobile,
            'email': student.email,
            'total_fees': student.total_fees,
            'paid_now': newly_paid * 2000,
            'total_paid': student.paid_installments * 2000,
            'remaining_fees': student.total_fees - (student.paid_installments * 2000),
            'date': datetime.date.today().strftime("%d-%m-%Y"),
            'receipt_no': f"REC-{student.id}-{student.paid_installments}"
        }
        return redirect('recipt')

    return render(request, 'collectfees.html', {
        'students': students,
        'selected_student': selected_student,
        'installments_list': installments_list
    })

# --- RECEIPT VIEW ---
def recipt(request):
    receipt_data = request.session.get('receipt_data', None)
    return render(request, 'recipt.html', {'receipt': receipt_data})




