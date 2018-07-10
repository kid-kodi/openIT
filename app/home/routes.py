from app import db
from flask import render_template, flash, redirect, url_for
from .forms import InterviewForm, OrderForm, EquipmentForm
from flask_login import current_user, login_required
from app.models import Interview, Order, Equipment, Category, Label, Service
from datetime import datetime
from . import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('home/dashboard.html', title='Home', posts=posts)


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
    form.description.data = equipment.description
    return render_template('home/equipment/add_equipment.html', form=form)


@bp.route('/equipment/detail/<int:id>')
@login_required
def detail_equipment(id):
    equipment = Equipment.query.get_or_404(id)
    return render_template('home/equipment/detail_equipment.html', equipment=equipment)


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
                              description=form.description.data,
                              interviewer=form.interviewer.data,
                              actions=form.actions.data,
                              date=form.date.data)
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
        interview.equipment_id = form.equipment.data
        interview.description = form.description.data
        interview.interviewer = form.interviewer.data
        interview.actions = form.actions.data
        interview.date = form.date.data
        db.session.commit()
        flash('données modifiées')
        return redirect(url_for('interview'))
    form.requester.data = interview.requester
    form.equipment.data = interview.equipment
    form.description.data = interview.description
    form.interviewer.data = interview.interviewer
    form.actions.data = interview.actions
    form.date.data = interview.date
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