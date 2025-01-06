from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .forms import RegisterForm, LoginForm, TaskForm
from .models import User, Task
from . import db  # از نمونه‌ی تعریف‌شده در __init__.py استفاده می‌کنیم
from flask import request


routes = Blueprint('routes', __name__)


@routes.route('/')
def index():
    if current_user.is_authenticated:
        # اگر کاربر لاگین کرده است، او را به داشبورد هدایت کنید
        return redirect(url_for('routes.dashboard'))
    return render_template('index.html')  # صفحه اصلی برای کاربران غیرفعال


# ثبت‌نام کاربر جدید
@routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)


# ورود کاربر
@routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('routes.dashboard'))
        flash('Login unsuccessful. Check username and/or password', 'danger')
    return render_template('login.html', form=form)


# داشبورد کاربر پس از ورود
@routes.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)


# ایجاد Task جدید
@routes.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('routes.dashboard'))
    return render_template('create_task.html', form=form)


# ویرایش Task
@routes.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You are not authorized to edit this task!', 'danger')
        return redirect(url_for('routes.dashboard'))

    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    form.title.data = task.title
    return render_template('edit_task.html', form=form)


@routes.route('/delete_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You are not authorized to delete this task!', 'danger')
        return redirect(url_for('routes.dashboard'))

    if request.method == 'POST':
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('delete_task.html', task=task)


# خروج کاربر
@routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.index'))
