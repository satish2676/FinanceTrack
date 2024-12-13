from django.shortcuts import render,redirect
from .models import Member,Admin

from datetime import date
from django.contrib import messages
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.utils.timezone import now
from django.db import models
#import openpyxl
from .models import  Payment
from django.contrib.auth.hashers import make_password

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Admin




def admin_register(request):
    if request.method == 'POST':
        admin_name = request.POST['admin_name']
        admin_mobile = request.POST['admin_mobile']
        admin_password = request.POST['admin_password']
          # Unique database name

        # Check if the admin already exists
        if Admin.objects.filter(admin_mobile=admin_mobile).exists():
            messages.error(request, 'Admin with this name already exists.')
            return redirect('login')    # Redirect back to registration page with error messag
        hashed_admin_password = make_password(admin_password)
        Admin.objects.create(admin_name=admin_name, admin_mobile=admin_mobile, admin_password=hashed_admin_password, )
        messages.success(request, 'Admin registered successfully.')
        return redirect('login')

    return render(request, 'register.html')





def admin_login(request):
    if request.method == 'POST':
        admin_mobile = request.POST.get('admin_mobile_login')
        admin_password = request.POST.get('admin_password')
        admin_code = request.POST.get('admin_code')

        try:
            admin = Admin.objects.get(admin_mobile=admin_mobile)
            # Check if the password is correct
            if check_password(admin_password, admin.admin_password) and admin_code == admin.admin_code:
                return redirect('index')  # Redirect to admin dashboard
            else:
                messages.error(request, 'Invalid credentials.')
                return render(request, 'login.html', {'messages': messages.get_messages(request)})

        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'login.html', {'messages': messages.get_messages(request)})

    return render(request, 'login.html', {'messages': messages.get_messages(request)})


def index(request):
    return render(request, 'index.html')  # Example index view


def register(request):
    if request.method == 'POST':
        loan_id = request.POST.get('loan_id')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        loan_disberment_amount = request.POST.get('loan_disberment_amount')
        address = request.POST.get('address')
        loan_date = request.POST.get('loan_date') 
        paid_amount = request.POST.get('paid_amount')
       
        if Member.objects.filter(loan_id=loan_id).exists():
            messages.success(request, 'Loan ID already exists.')
            return render(request, 'register.html')
        else:
            Member.objects.create(
            loan_id=loan_id,
            name = name,
            mobile = mobile,
            loan_disberment_amount = loan_disberment_amount,
            address = address,
            loan_date =  loan_date,
            paid_amount = paid_amount

           
        )
        messages.success(request, 'Member registered successfully.')
        return render(request, 'register.html') 
    else:
        return render(request, 'register.html')



def view_members(request):
    member = None
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')
        if Member.objects.filter(loan_id=loan_id).exists():
            details = Member.objects.get(loan_id=loan_id)
            return render(request, 'member_details.html')
    return render(request, 'view_members.html')




from datetime import timedelta

from datetime import timedelta

from datetime import timedelta
from django.contrib import messages
from .models import Member, Payment

def member_details(request):
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')

        if not loan_id:
            messages.error(request, "Please enter Loan Id.")
            return render(request, 'view_members.html')

        try:
            # Fetch member details
            member = Member.objects.get(loan_id=loan_id)
            loan_date = member.loan_date

            # Generate a 100-day schedule starting from the next day of the loan date
            schedules = [
                {
                    "day": f"Day {i}",
                    "disbursement_date": (loan_date + timedelta(days=i)).strftime('%Y-%m-%d'),  # Start from the next day
                    "paid_status": "Unpaid"  # Default status
                }
                for i in range(1, 101)
            ]

            # Fetch payments for the member
            payments = Payment.objects.filter(member=member, is_paid=True)
            paid_dates = {payment.paid_date.strftime('%Y-%m-%d') for payment in payments}

            # Update schedules with payment status
            for schedule in schedules:
                if schedule["disbursement_date"] in paid_dates:
                    schedule["paid_status"] = "Paid"

            # Render the member details with schedules
            return render(request, 'member_details.html', {
                'member': member,
                'schedules': schedules
            })

        except Member.DoesNotExist:
            messages.error(request, "No member found with the given Book No.")
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "An error occurred while processing the request.")

    return render(request, 'view_members.html')

from datetime import date
from django.utils.timezone import localdate

import openpyxl
from django.http import HttpResponse
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render
from django.utils.timezone import localdate
from .models import Member, Payment  # Replace with your actual models

def daily_collection(request):
    today = localdate()  # Get the current date dynamically in the server's time zone

    # Filter members whose loans started before today
    members = Member.objects.filter(loan_date__lt=today)  # Loans started before today
    members_with_paid_amount = members.filter(paid_amount__gt=0)

    # Calculate total paid amount
    total_paid_amount = members_with_paid_amount.aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0  

    # Fetch payments made today
    payments = Payment.objects.filter(paid_date=today).select_related('member')

    if request.method == 'POST':
        if 'export_to_excel' in request.POST:  # Handle Excel export
            return export_to_excel(members_with_paid_amount, today)

        # Handle payments
        for key, value in request.POST.items():
            if key.startswith("paid_") and value:  # Only process keys with 'paid_' prefix
                member_id = key.split("_")[1]  # Extract member ID
                try:
                    member = Member.objects.get(id=member_id)

                    # Create or update today's payment record
                    payment, created = Payment.objects.get_or_create(
                        member=member,
                        paid_date=today,
                        defaults={'is_paid': True}
                    )
                    if not created:
                        payment.is_paid = True
                        payment.save()

                    messages.success(request, f"Payment recorded for {member.mobile}.")
                except Member.DoesNotExist:
                    messages.error(request, f"Member with ID {member_id} not found.")
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")

        # Reload updated data after POST
        payments = Payment.objects.filter(paid_date=today).select_related('member')

    # Render initial data or reload after POST
    return render(request, 'daily_collection.html', {
        'collections': members,
        'total_paid_amount': total_paid_amount,
        'payments': payments,
        'today': today,  # Pass the current date to the template
    })


from django.http import HttpResponse
from django.utils.timezone import localdate
from .models import Member  # Adjust import to match your models

def export_daily_collection(request):
    # Get today's date
    today = localdate()

    # Fetch all members whose loan_date is before or on today, and their payment schedule starts today
    # Payment schedule starts from the next day of loan_date, and we include members whose payment is due within the next 100 days.
    start_date = today - timedelta(days=1)  # Members whose payment schedule starts today
    end_date = today + timedelta(days=100)  # Members whose payment is due within the next 100 days

    collections = Member.objects.filter(loan_date__lte=start_date)

    # Create a new workbook and add a worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Daily Collection'

    # Add headers
    headers = ['Book NO', 'Date', 'Member Name', 'Mobile Number', 'Loan Disbursement Amount', 'Amount Collected']
    ws.append(headers)

    # Add data rows for each member whose payment schedule includes today or the next 100 days
    for member in collections:
        # If the member's payment schedule includes today (loan_date + 1 day <= today <= loan_date + 100 days)
        if member.loan_date + timedelta(days=1) <= today <= member.loan_date + timedelta(days=100):
            row = [
                member.loan_id,
                today,
                member.name,
                member.mobile,
                member.loan_disberment_amount,
                member.paid_amount,  # Adjust if needed
            ]
            ws.append(row)

    # Create an HTTP response with an Excel file attachment
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = f'attachment; filename=Daily_Collection_{today}.xlsx'

    # Save the workbook to the response
    wb.save(response)
    return response



from django.db.models import Sum
from django.utils.timezone import now

def paid_status(request):
    today = now().date()

    # Get payments made today and related members who have paid
    payments = Payment.objects.filter(paid_date=today, is_paid=True).select_related('member')

    # Calculate total paid amount for members who made payments today
    total_paid_amount = payments.aggregate(Sum('member__paid_amount'))['member__paid_amount__sum'] or 0  

    # Get member details for today's date (if necessary)
    member_details = Member.objects.filter(today_date=today)

    return render(request, 'paid_status.html', {
        'payments': payments,
        'member_details': member_details,
        'total_paid_amount': total_paid_amount
    })

def mark_paid(request, member_id, disbursement_date):
    if request.method == 'POST':
        try:
            member = Member.objects.get(id=member_id)
            payment_date = datetime.strptime(disbursement_date, "%Y-%m-%d").date()

            # Update or create the payment record
            payment, created = Payment.objects.get_or_create(
                member=member,
                paid_date=payment_date,
                defaults={'is_paid': True}
            )
            if not created:
                payment.is_paid = True
                payment.save()

            messages.success(request, "Payment marked as paid.")
        except Member.DoesNotExist:
            messages.error(request, "Member not found.")
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "An error occurred while processing the payment.")

    return render(request,'member_details.html')  # Update with the correct view na






