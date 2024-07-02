from django.db.models import Sum

from .choices import StatusChoices


def update_appointment_status(appointment):
    total_profit = appointment.profits.aggregate(total=Sum("amount"))["total"] or 0
    if total_profit > 0:
        if appointment.price == total_profit:
            appointment.status = StatusChoices.FULLY_PAID
        else:
            appointment.status = StatusChoices.PARTIALLY_PAID
    return appointment


def update_doctor_balance_on_profit(profit):
    doctor = profit.appointment.doctor
    doctor.balance += (profit.amount * profit.appointment.service.kpi_percent) / 100
    doctor.save()  # Сохранение изменений в объекте доктора
    return profit


def update_doctor_balance_on_salary(salary):
    doctor = salary.doctor
    doctor.balance -= salary.amount
    doctor.save()  # Сохранение изменений в объекте доктора
    return salary
