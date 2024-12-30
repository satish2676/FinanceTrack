from django.shortcuts import render,redirect
from .models import Member,Admin
from django.shortcuts import render, get_object_or_404, redirect
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
        loan_disbursement_amount = request.POST.get('loan_disbursement_amount')
        interest_amount = request.POST.get('interest_amount')  # Adjust if needed  # 2% of loan_disberment_amount for intrest calculation
        total_invoice_amount = request.POST.get('total_invoice_amount')
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
            loan_disbursement_amount = loan_disbursement_amount,
            address = address,
            interest_amount=interest_amount,
            total_invoice_amount=total_invoice_amount,
            loan_date =  loan_date,
            paid_amount = paid_amount

           
        )
        messages.success(request, 'Member registered successfully.')
        return render(request, 'register.html') 
    else:
        return render(request, 'register.html')


def view_members(request):
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')  # Get loan_id from the form

        if not loan_id:  # If loan_id is empty
            messages.error(request, "Customer ID is required.")
            return render(request, 'view_members.html')

        # Check if loan_id exists in the database (optional but recommended)
        if Member.objects.filter(loan_id=loan_id).exists():
            return redirect('member_details', loan_id=loan_id)  # Redirect with loan_id
        else:
            messages.error(request, "No member found with the provided Customer ID.")
            return render(request, 'view_members.html')

    return render(request, 'view_members.html')




from datetime import timedelta

from datetime import timedelta

from datetime import timedelta
from django.contrib import messages
from .models import Member, Payment

def member_details(request, loan_id=None):
    if request.method == "POST":
        loan_id = request.POST.get('loan_id')

        if not loan_id:
            messages.error(request, "Please enter Loan Id.")
            return render(request, 'view_members.html')

        try:
            # Fetch member details using loan_id
            member = get_object_or_404(Member, loan_id=loan_id)
            
            loan_date = member.loan_date

            # Add 100 days to the loan date to get the end date
            end_date = loan_date + timedelta(days=100)

            # Generate a 100-day schedule starting from the next day after loan_date
            schedules = [
                {
                    "day": f"Day {i}",
                    "disbursement_date": (loan_date + timedelta(days=i)).strftime('%Y-%m-%d'),
                    "paid_status": "Unpaid"  # Default status
                }
                for i in range(1, 101)

            ]

            # Count the number of paid days
            paid_days_count = Payment.objects.filter(member=member, is_paid=True).count()

            # Calculate unpaid days dynamically (if total_days is available or calculate it)
            unpaid_days_count = 100 - paid_days_count  # Assuming total_days is 100 based on your calculation logic

            # Fetch payments and get the dates that are marked as paid
            payments = Payment.objects.filter(member=member, is_paid=True)
            paid_dates = {payment.paid_date.strftime('%Y-%m-%d') for payment in payments}

            if unpaid_days_count > 0:
        # Add skipped days after 100 days
                for i in range(101, 101 + unpaid_days_count):
                    disbursement_date = loan_date + timedelta(days=i)
                    schedules.append({
                    "day": f"Day {i}",
                    "disbursement_date": disbursement_date.strftime('%Y-%m-%d'),
                    "paid_status": "Unpaid"  # Initially, all skipped days are unpaid
                })

            # Update schedules with paid status based on the paid dates
            for schedule in schedules:
                if schedule["disbursement_date"] in paid_dates:
                    schedule["paid_status"] = "Paid"

            # Render the member details with schedules and the unpaid days count
            return render(request, 'member_details.html', {
                'member': member,
                'schedules': schedules,
                'paid_days_count': paid_days_count,
                'unpaid_days_count': unpaid_days_count
            })

        except Member.DoesNotExist:
            messages.error(request, "No member found with the given Loan ID.")
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "No member found with the given Loan ID.")

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
    headers = ['Customer iD', 'Date', 'Member Name', 'Mobile Number', 'Total Invoice Amount', 'Collect Amount']
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
                member.loan_disbursement_amount,
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


from openpyxl import Workbook
def export_all_members_excel(request):
    # Create a new workbook and get the active worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = "All Members"

    # Write the header row
    headers = ['Customer ID', 'Name', 'Address', 'Mobile No', 'Total Invoice Amount']
    ws.append(headers)

    # Fetch all members and write data rows
    members = Member.objects.all()
    for member in members:
        ws.append([
            member.loan_id,
            member.name,
            member.address,
            member.mobile,
            member.total_invoice_amount
        ])

    # Prepare the response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="all_members.xlsx"'

    # Save the workbook to the response
    wb.save(response)
    return response


def add_payment(self, amount_paid):
    """
    Add a payment to the total amount paid and save the changes.
    """
    self.recovery_amount += amount_paid
    self.save()



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
    member = None

    if request.method == 'POST':
        try:
            member = get_object_or_404(Member, id=member_id)

            # Parse the disbursement_date to a datetime object
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

            # Update the member's paid and unpaid days dynamically
            paid_days = Payment.objects.filter(member=member, is_paid=True).count()
            member.update_paid_unpaid_days(paid_days)

            messages.success(request, "Payment marked as paid successfully.")

        except Member.DoesNotExist:
            messages.error(request, "Member not found.")
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "Payment marked as paid successfully.")

        # Ensure that the member object exists before redirecting
        if member:
            # Redirect to the member_details view using the correct loan_id
            return redirect('member_details', loan_id=member.loan_id)

    return redirect('member_details', loan_id=member.loan_id) if member else redirect('member_details')


def all_members(request):
    members = Member.objects.all()
    return render (request,'all_members.html',{'members': members})
    
 
