from datetime import datetime, timedelta
from flask import Blueprint, render_template, url_for, redirect, request, flash

from webapp.employee.form import EmployeeForm
from webapp.model import db, Event, Employee, Position_type, Schedule

blueprint = Blueprint('employee', __name__, url_prefix='/employees')


@blueprint.route('/', methods=['GET', 'POST'])
def employees():
    title = 'Пользователи'
    positions = [(p.id, p.position_name) for p in Position_type.query.all()]
    form = EmployeeForm(request.form)
    form.position_type.choices = positions
    employees_list = Employee.query.all()

    if form.validate_on_submit():
        print(1)
        first_name = form.first_name.data
        last_name = form.last_name.data
        slack_id = form.slack_id.data
        position_type = form.position_type.data
        start_date = form.start_date.data
        new_employee = Employee(first_name=first_name,
                                last_name=last_name,
                                slack_id=slack_id,
                                start_date=start_date,
                                position_type=position_type)
        schedule_to_insert = [new_employee]
        events = Event.query.filter(Event.positions.any(
            id=form.position_type.data)).all()

        for event in events:
            day_now = datetime.now().date()
            interval = timedelta(days=event.interval)
            delivery_date = start_date + interval

            if delivery_date < day_now:
                continue

            schedule_to_insert.append(Schedule(employee=new_employee,
                                               event_id=event.id,
                                               delivery_date=delivery_date))

        db.session.add_all(schedule_to_insert)
        db.session.commit()
        flash('Пользователь успешно добавлен.')
        return redirect(url_for('employee.employees'))

    return render_template('employee/employee.html',
                           title=title,
                           form=form,
                           employees_list=employees_list)


@blueprint.route('/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    title = 'Пользователь: {firstname} {lastname}'.format(
        firstname=employee.first_name, lastname=employee.last_name)
    form = EmployeeForm(obj=employee)
    form.position_type.choices = [
        (employee.position.id, employee.position.position_name)]
    schedule = Schedule.query.options(db.joinedload(Schedule.event)).filter_by(employee_id=employee_id).all()

    if form.validate_on_submit():
        form.populate_obj(employee)
        db.session.commit()
        flash('Пользователь {firstname} {lastname} успешно обновлен.'.format(
            firstname=employee.first_name, lastname=employee.last_name))
        return redirect(url_for('employee.employees'))

    return render_template('employee/edit_employee.html',
                           title=title,
                           employee=employee,
                           schedule=schedule,
                           form=form)


@blueprint.route('/delete_employee/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    return 'Пользователь успешно удален!'
