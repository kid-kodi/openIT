from app import db
from flask import render_template, flash, redirect, url_for, request
from .forms import InterviewForm, OrderForm, EquipmentForm
from flask_login import current_user, login_required
from app.models import Interview, Order, Equipment, Category, Label, Service
from datetime import datetime
from . import bp
import csv
import io
import flask_excel as excel


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    interviews = Interview.query.all()
    orders = Order.query.all()
    equipments = Equipment.query.all()
    return render_template('home/dashboard.html', interviews=interviews
                           , orders=orders
                           , equipments=equipments)


#routes equipment
@bp.route('/equipment')
@login_required
def equipment():
    list = Equipment.query.all()
    return render_template('home/equipment/equipment.html', list=list)


@bp.route('/equipment/add', methods=['GET', 'POST'])
@login_required
def add_equipment():
    form = EquipmentForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.label.choices = [(c.id, c.name) for c in Label.query.all()]
    form.service.choices = [(c.id, c.name) for c in Service.query.all()]
    if form.validate_on_submit():
        equipment = Equipment(category_id=form.category.data,
                              label_id=form.label.data,
                              service_id=form.service.data,
                              model=form.model.data,
                              serial=form.serial.data,
                              name=form.name.data,
                              arrived_at=form.arrived_at.data,
                              created_by=current_user.id,
                              description=form.description.data)
        db.session.add(equipment)
        db.session.commit()
        flash('données enregistrées')
        return redirect(url_for('home.equipment'))
    return render_template('home/equipment/add_equipment.html', form=form)


@bp.route('/equipment/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_equipment( id ):
    equipment = Equipment.query.get_or_404(id)
    form = EquipmentForm(obj=equipment)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    form.label.choices = [(c.id, c.name) for c in Label.query.all()]
    form.service.choices = [(c.id, c.name) for c in Service.query.all()]
    if form.validate_on_submit():
        equipment.category_id = form.category.data
        equipment.label_id = form.label.data
        equipment.service_id = form.service.data
        equipment.model = form.model.data
        equipment.serial = form.serial.data
        equipment.name = form.name.data
        equipment.arrived_at = form.arrived_at.data
        equipment.description = form.description.data
        db.session.commit()
        flash('données modifiées')
        return redirect(url_for('home.equipment'))
    form.category.data = equipment.category_id
    form.label.data = equipment.label_id
    form.service.data = equipment.service_id
    form.model.data = equipment.model
    form.serial.data = equipment.serial
    form.name.data = equipment.name
    form.arrived_at.data = equipment.arrived_at
    form.description.data = equipment.description
    return render_template('home/equipment/add_equipment.html', form=form)


@bp.route('/equipment/detail/<int:id>')
@login_required
def detail_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    return render_template('home/equipment/detail_equipment.html', equipment=equipment)


@bp.route("/equipment/import", methods=['GET', 'POST'])
@login_required
def import_equipment():
    if request.method == 'POST':

        def equipment_init_func(row):
            c = Equipment()
            c.category_id = row['category_id']
            c.label_id = row['label_id']
            c.service_id = row['service_id']
            c.model = row['model']
            c.serial = row['serial']
            c.name = row['name']
            c.arrived_at = row['arrived_at']
            c.description = row['description']
            c.created_at = datetime.utcnow()
            c.created_by = current_user.id
            return c

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Equipment],
            initializers=[equipment_init_func])
        return redirect(url_for('home.equipment'), code=302)
    return render_template('home/equipment/import.html', equipment=equipment)


@bp.route("/equipment/export", methods=['GET'])
@login_required
def export_equipment():
    list = Equipment.query.all()
    column_names = ['category_id', 'label_id', 'service_id', 'model', 'serial', 'name', 'arrived_at', 'description']
    return excel.make_response_from_query_sets(list, column_names, "xls", file_name="equipment_data")


@bp.route("/equipment/download", methods=['GET'])
@login_required
def download_equipment():
    return excel.make_response_from_array([['category_id', 'label_id', 'service_id', 'model', 'serial', 'name',
                                            'arrived_at', 'description']], "xls", file_name="equipment_samples")


#routes interview
@bp.route('/interview')
@login_required
def interview():
    list = Interview.query.all()
    return render_template('home/interview/interview.html', list=list)


@bp.route('/interview/add', methods=['GET', 'POST'])
@login_required
def add_interview():
    form = InterviewForm()
    form.service.choices = [(c.id, c.name) for c in Service.query.all()]
    form.equipment.choices = [(c.id, c.name) for c in Equipment.query.all()]
    if form.validate_on_submit():
        interview = Interview(requester=form.requester.data,
                              equipment_id=form.equipment.data,
                              service_id=form.service.data,
                              reasons=form.reasons.data,
                              interviewer=form.interviewer.data,
                              actions=form.actions.data,
                              request_date=form.request_date.data,
                              request_time=form.request_time.data,
                              start_date=form.start_date.data,
                              end_date=form.end_date.data)
        db.session.add(interview)
        db.session.commit()
        flash('données enregistrées')
        return redirect(url_for('home.interview'))
    return render_template('home/interview/add_interview.html', form=form)


@bp.route('/interview/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_interview( id ):
    interview = Interview.query.get_or_404(id)
    form = InterviewForm(obj=interview)
    form.service.choices = [(c.id, c.name) for c in Service.query.all()]
    form.equipment.choices = [(c.id, c.name) for c in Equipment.query.all()]
    if form.validate_on_submit():
        interview.requester = form.requester.data
        interview.service_id = form.service.data
        interview.equipment_id = form.equipment.data
        interview.reasons = form.reasons.data
        interview.interviewer = form.interviewer.data
        interview.request_date = form.request_date.data
        interview.request_time = form.request_date.data
        interview.actions = form.actions.data
        interview.start_date = form.start_date.data
        interview.end_date = form.end_date.data
        interview.status = form.status.data
        db.session.commit()
        flash('données modifiées')
        return redirect(url_for('home.interview'))
    form.requester.data = interview.requester
    form.equipment.data = interview.equipment_id
    form.service.data = interview.service_id
    form.reasons.data = interview.reasons
    form.interviewer.data = interview.interviewer
    form.actions.data = interview.actions
    form.request_date.data = interview.request_date
    form.request_time.data = interview.request_time
    form.end_date.data = interview.end_date
    form.start_date.data = interview.start_date
    form.status.data = interview.status
    return render_template('home/interview/add_interview.html', form=form)


@bp.route('/interview/detail/<int:id>')
@login_required
def detail_interview(id):
    interview = Interview.query.get_or_404(id)
    return render_template('home/interview/detail_interview.html', interview=interview)


#routes order
@bp.route('/order')
@login_required
def order():
    list = Order.query.all()
    return render_template('home/order/order.html', list=list)


@bp.route('/order/add', methods=['GET', 'POST'])
@login_required
def add_order():
    form = OrderForm()
    if form.validate_on_submit():
        order = Order(requester=form.requester.data,
                              service=form.service.data,
                              description=form.description.data,
                              orderer=form.orderer.data,
                              actions=form.actions.data,
                              date=form.date.data)
        db.session.add(order)
        db.session.commit()
        flash('données enregistrées')
        return redirect(url_for('home.order'))
    return render_template('home/order/add_order.html', form=form)


@bp.route('/order/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_order( id ):
    order = Order.query.get_or_404(id)
    form = OrderForm(obj=order)
    if form.validate_on_submit():
        order.requester = form.requester.data
        order.service = form.service.data
        order.description = form.description.data
        order.orderer = form.orderer.data
        order.actions = form.actions.data
        order.date = form.date.data
        db.session.commit()
        flash('données modifiées')
        return redirect(url_for('home.order'))
    form.requester.data = order.requester
    form.service.data = order.service
    form.description.data = order.description
    form.orderer.data = order.orderer
    form.actions.data = order.actions
    form.date.data = order.date
    return render_template('home/order/add_order.html', form=form)


@bp.route('/order/detail/<int:id>')
@login_required
def detail_order(id):
    order = Order.query.get_or_404(id)
    return render_template('home/order/detail_order.html', order=order)


@bp.route("/import", methods=['GET', 'POST'])
@login_required
def doimport():
    if request.method == 'POST':

        def category_init_func(row):
            c = Category()
            c.id = row['id']
            c.name = row['name']
            c.description = row['description']
            return c

        request.save_book_to_database(
            field_name='file', session=db.session,
            tables=[Category],
            initializers=[category_init_func])
        return redirect(url_for('.handson_table'), code=302)
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xls, xlsx, ods please)</h1>
    <form action="" method=post enctype=multipart/form-data><p>
    <input type=file name=file><input type=submit value=Upload>
    </form>
    '''


@bp.route("/export", methods=['GET'])
@login_required
def doexport():
    return excel.make_response_from_tables(db.session, [Category], "xls")


@bp.route("/handson_view", methods=['GET'])
@login_required
def handson_table():
    return excel.make_response_from_tables(
        db.session, [Category], 'home/handsontable.html')
