from math import ceil

from Utils.View_BVZ import view_BVZ
from Utils.UniqueID import string_to_ID


def calculate_BVZ(dbase, request_form, menu, current_user):

    # --------------------------------------------------------------------------------------
    if "button-accept-settings" in request_form:  # Выбор продукта и проекта
        dbase.del_records('warehouse')
        request_form['user_email'] = current_user.get_user_email()
        request_form['selected'] = True
        request_form['lead_ID'] = dbase.get_record('lead', ('company', request_form['client']))['id']
        del request_form['button-accept-settings']
        dbase.add_record('warehouse', request_form)
        return view_BVZ(menu, request_form, accept_index=1)

    #  ----------------Выбор температуры склада---------------------------------------------------------------------
    if "button-accept-temperature" in request_form:
        del request_form['button-accept-temperature']
        record = dbase.get_last_record('warehouse')
        lead_ID = dbase.get_record('lead', ('company', record['client']))['id']

        dbase.update_record_by_id('warehouse', record['id'], {'temperature': request_form['temperature'],
                                                              'lead_ID': lead_ID})

        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])
        return view_BVZ(menu, last_data, accept_index=2)

    #  ----------------------Ввод размеров и вывод площадей---------------------------------------------------------
    if "button-accept-dimension" in request_form:
        dimension = dict(list(request_form.items())[:-1])
        dimension['area'] = int(dimension['width']) * int(dimension['length'])
        dimension['volume'] = int(dimension['width']) * int(dimension['length']) * float(dimension['height'])
        dbase.update_record_by_id('warehouse', dbase.get_last_record("warehouse")['id'], dimension)
        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])
        return view_BVZ(menu, last_data, accept_index=3)

    #  ----------------------Ввод и вывод основных стоимостей--------------------------------------------------------
    if "button-accept-pricing" in request_form:
        price = dict(list(request_form.items())[:-1])
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], price)
        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        pw = last_data["price_warehouse"]
        pc = last_data["price_customs"] = pw * 1 / 100
        pV = last_data["price_VAT"] = pw * 20 / 100

        last_data["cost_price"] = pw + pc + pV
        last_data["price_square_meters"] = round(last_data["cost_price"] / last_data['area'], 2)
        last_data["price_cubic_meters"] = round(last_data["cost_price"] / last_data['volume'], 2)
        last_data["price_project"] = last_data["cost_price"] + last_data["price_delivery"] + last_data["price_building"]
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)
        return view_BVZ(menu, last_data, accept_index=4)

    # ------ Ввод и вывод дополнительных стоимостей ------------------------------------------------------------------
    if "button-accept-cost" in request_form:
        advance_price = dict(list(request_form.items())[:-1])
        for key in advance_price:
            if advance_price[key] == '':
                advance_price[key] = 0
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], advance_price)
        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        if last_data['price_sq_met_found'] != '':
            wf = last_data['width'] + 1
            lf = last_data['length'] + 1
            last_data['dimension_found'] = f"Ш: {wf}m | Д: {lf}m"
            area_found = last_data['area_found'] = wf * lf
            last_data['price_foundation'] = last_data["price_sq_met_found"] * area_found
            dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)

        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)
        return view_BVZ(menu, last_data, accept_index=5)

    #  -------------------Ввод и вывод финальных расчетов---------------------------------------------
    if "button-accept-percent" in request_form:
        lst = list(dict(dbase.get_last_record("warehouse")).items())[1::]
        last_data = dict(lst)

        percent_w = int(request_form["percent_w"]) if request_form["percent_w"] != '' else 0  # Процент моржи склада
        percent_f = int(request_form["percent_f"]) if request_form["percent_f"] != '' else 0  # Процент моржи фундамента
        percent_o = int(request_form["percent_o"]) if request_form["percent_o"] != '' else 0  # Процент моржи опций
        exch_rate_from = int(request_form['exchange_rates_from'])  # Курс поставщика
        exch_rate_to = int(request_form['exchange_rates_TO'])  # Курс клиента

        cost_w_sq_m_EU = last_data["price_square_meters"]  # Себестоимость 1 кв.м. склада ЕВРО
        cost_project_EU = last_data["price_project"]  # Себестоимость проекта ЕВРО
        area_w = last_data["area"]  # Площадь склада

        cost_f_EU = last_data["price_foundation"]  # Себестоимость фундамента ЕВРО
        cost_f_sq_m_EU = last_data["price_sq_met_found"]  # Себестоимость метра фундамента ЕВРО
        area_f = last_data["area_found"]  # Площадь фундамента

        price_w_sq_m_EU = round((cost_w_sq_m_EU * percent_w / 100) + cost_w_sq_m_EU, 2)  # Цена 1м.кв. сырая ЕВРО
        price_w_sq_m_EU = round(price_w_sq_m_EU * exch_rate_to / exch_rate_from, 2)  # Преобразованная 1м ЕВРО
        price_w_EU = price_w_sq_m_EU * area_w + last_data["price_delivery"] + last_data["price_building"]
        price_sell_w_sq_m_EU = round(price_w_EU / area_w, 2)
        price_sell_warehouse_EU = round(price_sell_w_sq_m_EU * area_w, 2)  # Цена склада финал ЕВРО
        profit_warehouse_EU = price_sell_warehouse_EU - cost_project_EU  # Моржа на складе в ЕВРО

        price_sell_w_sq_m_UA = ceil(price_sell_w_sq_m_EU * exch_rate_from)  # Цена 1м склада финал ГРН
        price_sell_warehouse_UA = price_sell_w_sq_m_UA * area_w  # Цена склада финал ГРН
        profit_warehouse_UA = price_sell_warehouse_UA - (cost_project_EU * exch_rate_from)  # Моржа склад финал ГРН

        price_f_sq_m_EU = (cost_f_sq_m_EU * percent_f / 100) + cost_f_sq_m_EU  # Цена 1м пол ЕВРО
        price_sell_f_sq_m_EU = ceil(price_f_sq_m_EU * exch_rate_to / exch_rate_from)  # Цена 1м финал пол ЕВРО
        price_sell_f_sq_m_UA = price_sell_f_sq_m_EU * exch_rate_from  # Цена 1м финал пол ГРН
        price_sell_f_UA = price_sell_f_sq_m_UA * area_f  # Цена пол финал ГРН
        profit_f_UA = price_sell_f_UA - (cost_f_EU * exch_rate_from)

        # ---------- Добавляем в словарь данные -------------------------------------------------------------
        last_data["percent_w"] = int(percent_w)  # Добавляем в словарь Процент склада
        last_data["percent_f"] = int(percent_f)  # Добавляем в словарь Процент фундамента
        last_data["percent_o"] = int(percent_o)  # Добавляем в словарь Процент освещения + стеллажи

        last_data["exchange_rates_from"] = exch_rate_from  # Добавляем в словарь Курс поставщика
        last_data["exchange_rates_TO"] = exch_rate_to  # Добавляем в словарь Курс клиента

        last_data["price_selling_EU"] = price_sell_warehouse_EU
        last_data["profit_EU"] = round(profit_warehouse_EU, 2)
        last_data["cost_square_meters_EU"] = price_sell_w_sq_m_EU
        last_data["cost_cubic_meters_EU"] = round(price_sell_warehouse_EU / last_data["volume"], 2)

        last_data["price_selling_UA"] = price_sell_warehouse_UA
        last_data["profit_UA"] = round(profit_warehouse_UA, 2)
        last_data["cost_square_meters_UA"] = price_sell_w_sq_m_UA
        last_data["cost_cubic_meters_UA"] = round(last_data["price_selling_UA"] / last_data["volume"], 2)

        last_data["cost_foundation"] = price_sell_f_UA
        last_data["cost_sq_met_found"] = price_sell_f_sq_m_UA

        last_data["profit_percent"] = round(last_data["profit_EU"] / last_data["price_selling_EU"] * 100, 2)
        profit_o = (last_data["price_light"] + last_data["price_rack"]) * last_data["percent_o"] / 100
        last_data["cost_option"] = (last_data["price_light"] + last_data["price_rack"] + profit_o) * int(
            last_data["exchange_rates_TO"])
        profit_o_UA = profit_o * int(last_data["exchange_rates_TO"])

        final_price_UA = price_sell_warehouse_UA + price_sell_f_UA + last_data["cost_option"]
        last_data['final_cost_sq_m_pr'] = round(final_price_UA / area_w)
        last_data['final_price_UA'] = last_data['final_cost_sq_m_pr'] * area_w
        last_data['final_profit_UA'] = round(profit_warehouse_UA + profit_f_UA + profit_o_UA, 2)
        last_data['final_profit_percent'] = round(last_data['final_profit_UA'] / last_data['final_price_UA'] * 100,
                                                  2)

        string = string_to_ID(last_data['user_email'] + last_data['client'] +
                              last_data['project'] + str(last_data['final_price_UA']) +
                              str(last_data['final_profit_UA']) + str(last_data['final_profit_percent']))
        user_id = current_user.get_id()
        lead_id = dbase.get_record('lead', ('company', dbase.get_last_record('warehouse')['client']),
                                   ('user_email', current_user.get_user_email()))['id']
        last_data['unique_ID'] = str(user_id) + '_' + str(lead_id) + '_' + string
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)

        return view_BVZ(menu, last_data, accept_index=6)

    #  -------Сохраняем полученный результат в постоянную БД-----------------------------------------------
    if "button-save-pricing" in request_form:
        dbase.update_record_by_id('warehouse', dbase.get_last_record("warehouse")['id'],
                                  {'comments': request_form['input-field-comment-calc']})

        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        if dbase.check_records('my_warehouse'):
            if dbase.get_last_record('warehouse')['id'] != dbase.get_last_record("my_warehouse")['id']:
                dbase.save_warehouse()
            else:
                dbase.update_record_by_id("my_warehouse", dbase.get_last_record("my_warehouse")['id'], last_data)
        else:
            dbase.save_warehouse()

        # if dbase.check_records('my_warehouse'):
        #     unique_ID = dbase.get_last_record('warehouse')['unique_ID']
        #     if unique_ID == dbase.get_record('my_warehouse', ('unique_ID', unique_ID)):
        #         dbase.update_record_by_id
        #     else:
        #         dbase.update_record_by_id("my_warehouse", dbase.get_last_record("my_warehouse")['id'], last_data)
        # else:
        #     dbase.save_warehouse()

        return view_BVZ(menu, last_data, accept_index=7)

    #  ---------Начинаем новый расчет для данного проекта-------------------------------------------------
    if "button-update-pricing" in request_form:
        request_form = {
            'user_email': current_user.get_user_email(),
            'client': dbase.get_last_record('warehouse')['client'],
            'project': dbase.get_last_record('warehouse')['project'],
            'selected': dbase.get_last_record('warehouse')['selected'],
            'product': dbase.get_last_record('warehouse')['product'],
        }
        dbase.del_records('warehouse', dbase.get_last_record('warehouse')['id'])
        dbase.add_record('warehouse', request_form)

        return view_BVZ(menu, accept_index=1)

    if "button-raw-accept" in list(request_form.values()):
        try:
            del request_form['button_raw']
            del request_form['id']
            warehouse_data = request_form
            print(warehouse_data)
        except:
            return view_BVZ(menu, accept_index=0)

        dbase.del_records('warehouse')
        dbase.add_record('warehouse', warehouse_data)

        return view_BVZ(menu, warehouse_data, accept_index=7)
