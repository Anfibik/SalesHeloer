from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, g, abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from Utils.UserLogin import UserLogin

from Utils.FDataBase import FDataBase
from Utils.NumConvert import number_to_words
from Utils.form import LoginForm, RegistrationForm
import sqlite3
import os

# Конфигурация
DATABASE = '/tmp/SH_site.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
USERNAME = 'admin'
PASSWORD = '123'

# Инициализируем приложение
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'SH_site.db')))

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, dbase)


# ------------Создаем базу данных----------------------------
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно было установлено"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


menu = [
    {"url": '/', "name": 'Home'},
    {"url": '/leads', "name": 'Leads list'},
    {"url": '/pricing', "name": 'Cost Calculation'},
    {"url": '/morzh', "name": 'My Money'},
    {"url": '/about', "name": 'About'}
]


# --------------------Login----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # здесь можно добавить логику для проверки введенных данных
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['psw'], form.password.data):
            user_login = UserLogin().create(user)
            login_user(user_login)
            return redirect(url_for('leads'))
        flash("Неверная пара логин/пароль", "error")

    return render_template('login.html', title='Login', form=form, menu=menu)


# -----------------LOGOUT------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --------------------Registration----------------------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session.pop('_flashes', None)
        # здесь можно добавить логику для создания нового пользователя
        hash = generate_password_hash(form.password.data)
        res = dbase.add_user(form.username.data, form.email.data, hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    else:
        flash("Неверно заполнены поля", "error")

    return render_template('register.html', title='Register', form=form, menu=menu)


# --------------Домашняя страница--------------------------------------
@app.route('/')
def main_space():
    return render_template('base.html', title='My site', menu=menu)


# --------------Экран добавления лидов--------------------------------------
title_table_leads = [
    {"name": 'company', "placeholder": 'Компания'},
    {"name": 'name', "placeholder": 'ФИО'},
    {"name": 'job_title', "placeholder": 'Должность'},
    {"name": 'phone', "placeholder": 'Телефон'},
    {"name": 'mail', "placeholder": 'Почта'},
    {"name": 'project', "placeholder": 'Проект'},
    {"name": 'price', "placeholder": 'Цена продажи'},
    {"name": 'profit', "placeholder": 'Моржа'},
    {"name": 'status', "placeholder": 'Статус'},
]


@app.route('/leads', methods=["POST", "GET"])
@login_required
def leads():
    print("!!")
    # Добавление лидов в базу данных
    if request.method == "POST":
        checkbox_value = request.form.getlist('check-lead')
        button_delete = request.form.get('button-delete-lead')
        button_add = request.form.get('button-add-lead')

        print(checkbox_value, button_delete, button_add)

        if checkbox_value and button_delete:
            print(f"Выполняем процедуру {button_delete} для строк с id: {checkbox_value}")
            res = dbase.del_lead(checkbox_value)
        else:
            print(f"Выполняем процедуру {button_add}")
            # if all([vol['name'] for vol in title_table_leads]):
            res = dbase.set_new_lead(request.form.get('company'), request.form.get('name'),
                                     request.form.get('job_title'),
                                     request.form.get('phone'), request.form.get('mail'), request.form.get('project'),
                                     request.form.get('price'), request.form.get('profit'), request.form.get('status'))
            if not res:
                flash('Ошибка добавления лида', category='error')
            else:
                flash('Лид добавлен успешно', category='success')
            # else:
            #     flash('Ошибка добавления лида', category='error')

    # Чтение лидов из базы данных
    get_new_lead = dbase.get_info_lead()
    get_new_lead = [[row[column_name] for column_name in row.keys()] for row in get_new_lead]

    return render_template('leads.html',
                           title='My LEADS',
                           menu=menu,
                           title_table_leads=title_table_leads,
                           get_new_lead=get_new_lead,
                           current_user=current_user.get_user_name(),
                           )


# ---Экран информации о лиде----------------------------------
@app.route("/lead/<alias>")
def show_info_lead(alias):
    current_lead = dbase.get_lead(alias)
    if not current_lead:
        abort(404)

    return render_template('lead.html', menu=menu, title=current_lead, current_lead=current_lead)


# -------------------------------------------------------------
@app.route('/pricing')
@login_required
def pricing():
    return render_template('pricing.html', title='My PRICING', menu=menu)


@app.route('/morzh')
@login_required
def morzh():
    return render_template('morzh.html', title='My MONEY', menu=menu)


@app.route('/about')
def about():
    return render_template('about.html', title='ABOUT', menu=menu)


# -----------------Модальное окно----------------------------------------
@app.route('/convert_num', methods=['POST'])
def multiply_by_10():
    data = request.json
    input_value = data['input']
    output_value = number_to_words(int(input_value))
    return jsonify({'result': output_value})


if __name__ == "__main__":
    app.run(debug=True)
