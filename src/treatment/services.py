from django.db.models import Sum

from .choices import StatusChoices


def update_appointment_status(appointment):
    total_profit = appointment.profits.aggregate(total=Sum("amount"))["total"] or 0
    if appointment.price == total_profit:
        appointment.status = StatusChoices.PAID
    return appointment


def update_doctor_balance_on_profit(profit):
    profit.appointment.doctor.balance += (
        profit.amount * profit.appointment.service.kpi_percent
    ) / 100
    return profit


def update_doctor_balance_on_salary(salary):
    salary.doctor.balance -= salary.amount
    return salary
