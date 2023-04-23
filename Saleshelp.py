import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, g, abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from Utils.UserLogin import UserLogin

from Utils.FDataBase import FDataBase
from Utils.NumConvert import number_to_words
from Utils.form import LoginForm, RegistrationForm
from Utils.Pricing_View import pricing_view

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
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для работы в приложении"
login_manager.login_message_category = "success"


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


@login_manager.user_loader
def load_user(user_id):
    dbase = FDataBase(get_db())
    return UserLogin().fromDB(user_id, dbase)


menu = [
    {"url": '/', "name": 'Главная'},
    {"url": '/leads', "name": 'Мои лиды'},
    {"url": '/pricing', "name": 'Расчет стоимостей'},
    {"url": '/morzh', "name": 'Личные финансы'},
    {"url": '/about', "name": 'О программе'}
]


# --------------------Login----------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    dbase = FDataBase(get_db())

    if current_user.is_authenticated:
        return redirect(url_for('leads'))

    form = LoginForm()
    if form.validate_on_submit():
        # здесь можно добавить логику для проверки введенных данных
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['psw'], form.password.data):
            user_login = UserLogin().create(user)
            rm = True if form.remember_user.data else False

            login_user(user_login, remember=rm)
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
    dbase = FDataBase(get_db())

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
    {"name": 'company', "type": 'text', "placeholder": 'Компания'},
    {"name": 'name', "type": 'text', "placeholder": 'ФИО'},
    {"name": 'phone', "type": 'tel', "placeholder": 'Телефон'},
    {"name": 'mail', "type": 'email', "placeholder": 'Почта'},
    {"name": 'project', "type": 'text', "placeholder": 'Проект'},
]


@app.route('/leads', methods=["POST", "GET"])
@login_required
def leads():
    dbase = FDataBase(get_db())

    # Добавление лидов в базу данных
    if request.method == "POST":
        checkbox_value = request.form.getlist('check-lead')
        button_delete = request.form.get('button-delete-lead')
        button_add = request.form.get('button-add-lead')

        if checkbox_value and button_delete:
            print(f"Выполняем процедуру {button_delete} для строк с id: {checkbox_value}")
            res = dbase.del_records('lead', checkbox_value)
        else:
            print(f"Выполняем процедуру {button_add}")
            res = dbase.set_new_lead(request.form.get('company'), request.form.get('name'), request.form.get('phone'),
                                     request.form.get('mail'), request.form.get('project'),
                                     current_user.get_user_email())
            if not res:
                flash('Ошибка добавления лида', category='error')
            else:
                flash('Лид добавлен успешно', category='success')
            # else:
            #     flash('Ошибка добавления лида', category='error')

    # Чтение лидов из базы данных
    get_new_lead = dbase.get_info_records('lead', current_user.get_user_email())
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
    dbase = FDataBase(get_db())

    current_lead = dbase.get_lead(alias)
    if not current_lead:
        abort(404)

    return render_template('lead.html', menu=menu, title=current_lead, current_lead=current_lead)


# -----PRICING форма расчетов----------------------------------------------------->
@app.route('/pricing', methods=["POST", "GET"])
@login_required
def pricing():
    dbase = FDataBase(get_db())
    choose_project = [{"project": row['project'], "lead": row['company']}
                      for row in dbase.get_info_records('lead', current_user.get_user_email())]

    if request.method == 'POST':

        if "button-accept-settings" in request.form:
            settings = dict(list(request.form.items())[1:-1])
            dbase.add_record('warehouse', settings)

            return pricing_view(menu, choose_project, settings, accept_index=1)

        if "button-accept-dimension" in request.form:
            dimension = dict(list(request.form.items())[:-1])
            dimension['area'] = int(dimension['width']) * int(dimension['length'])
            dimension['volume'] = int(dimension['width']) * int(dimension['length']) * int(dimension['height'])
            dbase.update_record_by_id('warehouse', dbase.get_last_record("warehouse")['id'], dimension)

            return pricing_view(menu, choose_project, dimension, accept_index=2)

        if "button-accept-pricing" in request.form:
            price = dict(list(request.form.items())[:-1])
            dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], price)
            last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])
            last_data["price_square_meters"] = round(last_data['price_warehouse'] / last_data['area'], 2)
            last_data["price_cubic_meters"] = round(last_data['price_warehouse'] / last_data['volume'], 2)

            return pricing_view(menu, choose_project, last_data, accept_index=3)

        if "button-accept-cost" in request.form:
            advance_price = dict(list(request.form.items())[:-1])
            dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], advance_price)
            last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])
            pw = last_data["price_warehouse"]
            pc = last_data["price_customs"] = pw * 1 / 100
            pV = last_data["price_VAT"] = pw * 20 / 100
            last_data["price_square_meters"] = round(pw / last_data['area'], 2)
            last_data["price_cubic_meters"] = round(pw / last_data['volume'], 2)
            return pricing_view(menu, choose_project, last_data, accept_index=4)

        if "button-accept-percent" in request.form:
            cost_percent = request.form["percent_input"]
            print(cost_percent)

            # price_Protan = dbase.get_last_warehouse()['price_warehouse']
            # percent = request.form['percent_input']
            # price_customs = price_Protan * 1 / 100
            # price_VAT = price_Protan * 20 / 100
            #
            # cost_price = price_customs + price_VAT + price_Protan
            # profit = cost_price * int(percent) / 100
            # selling_price = cost_price + profit
            #
            # get_title_table_total_coast[0]['result'] = '{:,.2f}'.format(cost_price).replace(',', " ")
            # get_title_table_total_coast[1]['result'] = '{:,.2f}'.format(profit).replace(',', " ")
            # get_title_table_total_coast[2]['result'] = '{:,.2f}'.format(selling_price).replace(',', " ")

        if "button-save-pricing" in request.form:
            accept_1 = 'block'
            accept_2 = 'block'
            accept_3 = 'block'
            accept_4 = 'block'
            accept_5 = 'block'
            # dbase.save_warehouse()
            # value_warehouse = list(dict(dbase.get_last_warehouse()).values())[1::]

        if "button-update-pricing" in request.form:
            #
            pass

    return pricing_view(menu, choose_project, )


# <-------------------------------------------------------------------------------->
@app.route('/morzh', methods=["POST", "GET"])
@login_required
def morzh():
    result = None
    if request.method == 'POST':
        result = {key: vol for key, vol in request.form.items()}

    return render_template('morzh.html', title='My MONEY', menu=menu, result=result)


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
