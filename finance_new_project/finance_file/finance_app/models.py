from django.db import models
from datetime import date, timedelta
from decimal import Decimal


class Member(models.Model):
    loan_id = models.CharField(unique=True, max_length=50)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    loan_disbursement_amount = models.IntegerField()
    interest_amount = models.IntegerField()
    loan_date = models.DateField(auto_now_add=True)
    address = models.TextField()
    paid_amount = models.IntegerField(default=0)
    today_date = models.DateField(auto_now=True)
    end_date = models.DateField(null=True, blank=True)
    skipped_days = models.IntegerField(default=0)
    total_invoice_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_days = models.IntegerField(default=0)
    total_days = models.IntegerField(default=100)
    daily_interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.10')  # 10% daily interest rate
    )

    @property
    def paid_days(self):
        """Calculate the number of paid days dynamically from Payment records."""
        return Payment.objects.filter(member=self, is_paid=True).count()

    @property
    def unpaid_days(self):
        """Calculate the number of unpaid days dynamically."""
        return self.total_days - self.paid_days

    @property
    def recovery_amount(self):
        """Dynamically calculate the recovery amount based on paid amount and paid days."""
        # Formula: recovery_amount = paid_amount * paid_days (you can adjust this formula as needed)
        return self.paid_amount * self.paid_days

    @property
    def balance_amount(self):
        """Dynamically calculate the remaining balance based on total_invoice_amount and recovery_amount."""
        return self.total_invoice_amount - self.recovery_amount

    def end_date(self):
       
        """Calculate the end date ynamically based on the total days and paid days."""
        return self.loan_date + timedelta(days=self.total_days)


    def save(self, *args, **kwargs):
      
        try:
        # Convert loan_disbursement_amount to a float and skipped_days to an integer
            loan_disbursement_amount = float(self.loan_disbursement_amount)
            interest_amount = float(self.interest_amount)
            skipped_days = int(self.skipped_days) if self.skipped_days is not None else 0

        # Convert daily_interest_rate to a float
            daily_interest_rate = float(self.daily_interest_rate)

        # Calculate additional interest based on skipped days
            additional_interest = skipped_days * daily_interest_rate * loan_disbursement_amount

        # Calculate total invoice amount
            self.total_invoice_amount = loan_disbursement_amount + interest_amount + additional_interest
        except ValueError as e:
            print(f"Error calculating additional interest: {e}")
            self.total_invoice_amount = 0  # Default to 0 if calculation fails

        super().save(*args, **kwargs)
    @property
    def duration_in_days(self):
        """Calculate the total number of days from today to the end date."""
        return (self.end_date - date.today()).days

    def update_paid_unpaid_days(self):
        """Update the unpaid days based on paid days."""
        self.save()  # Save after the dynamic calculation of paid/unpaid days

    def __str__(self):
        return f"Loan ID: {self.loan_id}, Paid: {self.paid_days} days, Unpaid: {self.unpaid_days} days"


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    paid_date = models.DateField()
    is_paid = models.BooleanField(default=False)
    today_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        """Ensure today_date is always the current date when saving."""
        self.today_date = date.today()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.member.name} on {self.paid_date} (Paid: {self.is_paid})"


class Admin(models.Model):
    admin_name = models.CharField(max_length=100, default="s")
    admin_mobile = models.CharField(max_length=10, unique=True)
    admin_password = models.CharField(max_length=128)
    admin_code = models.CharField(max_length=50, default="cFJwQYwnuQINZt13oKZUl")

    def __str__(self):
        return f"Admin: {self.admin_name} (Mobile: {self.admin_mobile})"
