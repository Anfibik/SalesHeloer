from math import ceil

from Utils.View_BVZ import view_BVZ
from Utils.UniqueID import string_to_ID


def calculate_BVZ(dbase, request_form, menu, current_user, choose_project):
    if "button-accept-settings" in request_form:  # Выбор продукта, проекта, формата склада
        dbase.del_records('warehouse')
        settings = dict(list(request_form.items())[0:-1])
        for d in choose_project:
            for key, vol in d.items():
                if settings["project"] == vol:
                    settings["client"] = d["lead"]
        settings['user'] = current_user.get_user_email()

        settings['selected'] = True

        dbase.add_record('warehouse', settings)

        return view_BVZ(dbase, menu, current_user, settings, accept_index=1)

    if "button-accept-dimension" in request_form:  # Ввод размеров и вывод площадей
        dimension = dict(list(request_form.items())[:-1])
        dimension['area'] = int(dimension['width']) * int(dimension['length'])
        dimension['volume'] = int(dimension['width']) * int(dimension['length']) * float(dimension['height'])
        dbase.update_record_by_id('warehouse', dbase.get_last_record("warehouse")['id'], dimension)
        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        return view_BVZ(dbase, menu, current_user, last_data, accept_index=2)

    if "button-accept-pricing" in request_form:  # Ввод и вывод основных стоимостей
        price = dict(list(request_form.items())[:-1])
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], price)
        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        pw = last_data["price_warehouse"]
        pc = last_data["price_customs"] = pw * 1 / 100
        pV = last_data["price_VAT"] = pw * 20 / 100

        last_data["cost_price"] = pw + pc + pV
        last_data["price_square_meters"] = round(last_data["cost_price"] / last_data['area'], 2)
        last_data["price_cubic_meters"] = round(last_data["cost_price"] / last_data['volume'], 2)
        last_data["price_project"] = last_data["cost_price"] + last_data["price_delivery"] + last_data[
            "price_building"]

        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)

        return view_BVZ(dbase, menu, current_user, last_data, accept_index=3)

    # ------ Ввод и вывод дополнительных стоимостей ------------------------------------------------------------------
    if "button-accept-cost" in request_form:
        advance_price = dict(list(request_form.items())[:-1])
        for key in advance_price:
            if advance_price[key] == '':
                advance_price[key] = 0
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], advance_price)
        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        if last_data['price_foundation'] != '':
            wf = last_data['width'] + 1
            lf = last_data['length'] + 1
            last_data['dimension_found'] = f"Ш: {wf}m | Д: {lf}m"
            area_found = last_data['area_found'] = wf * lf
            last_data['price_sq_met_found'] = round(last_data["price_foundation"] / area_found, 2)
            dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)

        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)
        return view_BVZ(dbase, menu, current_user, last_data, accept_index=4)

    if "button-accept-percent" in request_form:  # Ввод и вывод финальных расчетов
        lst = list(dict(dbase.get_last_record("warehouse")).items())[1::]
        last_data = dict(lst)

        percent_w = request_form["percent_w"] if request_form["percent_w"] != '' else 0
        percent_f = request_form["percent_f"] if request_form["percent_f"] != '' else 0
        percent_o = request_form["percent_o"] if request_form["percent_o"] != '' else 0

        last_data["percent_w"] = int(percent_w)  # Процент склада
        last_data["percent_f"] = int(percent_f)  # Процент фундамента
        last_data["percent_o"] = int(percent_o)  # Процент освещения + стеллажи

        last_data["exchange_rates_from"] = request_form['exchange_rates_from']  # Курс поставщика
        last_data["exchange_rates_TO"] = request_form['exchange_rates_TO']  # Курс клиента

        profit = int(last_data["cost_price"]) * int(last_data["percent_w"]) / 100  # Заработок склад евро
        price_selling_EU = int(last_data["price_project"]) + profit  # Стоимость склада в евро для клиента
        cost_square_meters_EU = ceil(price_selling_EU / last_data["area"])  # Стоимость 1 кв.м.

        last_data["cost_square_meters_EU"] = cost_square_meters_EU
        last_data["price_selling_EU"] = cost_square_meters_EU * last_data["area"]
        last_data["cost_cubic_meters_EU"] = round(last_data["price_selling_EU"] / last_data["volume"], 2)
        last_data["profit_EU"] = last_data["price_selling_EU"] - last_data["price_project"]

        last_data["price_selling_UA"] = last_data["price_selling_EU"] * int(last_data["exchange_rates_TO"])
        last_data["profit_UA"] = last_data["price_selling_UA"] - int(last_data["price_project"]) * int(
            last_data["exchange_rates_from"])
        last_data["cost_square_meters_UA"] = last_data["price_selling_UA"] / int(last_data["area"])
        last_data["cost_cubic_meters_UA"] = last_data["price_selling_UA"] / last_data["volume"]

        last_data["profit_percent"] = last_data["profit_EU"] / last_data["price_selling_EU"] * 100

        profit_f = last_data["price_foundation"] * int(last_data["percent_f"]) / 100
        profit_o = (last_data["price_light"] + last_data["price_rack"]) * last_data["percent_o"] / 100

        last_data["cost_foundation"] = (last_data["price_foundation"] + profit_f) * int(
            last_data["exchange_rates_TO"])
        last_data["cost_option"] = (last_data["price_light"] + last_data["price_rack"] + profit_o) * int(
            last_data["exchange_rates_TO"])
        last_data["cost_sq_met_found"] = round(last_data["cost_foundation"] / last_data["area_found"], 2)

        profit_w_UA = last_data['profit_UA']
        profit_f_UA = profit_f * int(last_data["exchange_rates_TO"])
        profit_o_UA = profit_o * int(last_data["exchange_rates_TO"])

        last_data['final_price_UA'] = last_data["price_selling_UA"] + last_data["cost_foundation"] + last_data[
            "cost_option"]
        last_data['final_profit_UA'] = profit_w_UA + profit_f_UA + profit_o_UA
        last_data['final_profit_percent'] = round(last_data['final_profit_UA'] / last_data['final_price_UA'] * 100,
                                                  2)
        last_data['final_cost_sq_m_pr'] = last_data['final_price_UA'] / last_data['area']

        string = string_to_ID(last_data['user'] + last_data['client'] +
                              last_data['project'] + str(last_data['final_price_UA']) +
                              str(last_data['final_profit_UA']) + str(last_data['final_profit_percent']))
        user_id = current_user.get_id()
        lead_id = dbase.get_record('lead', ('company', dbase.get_last_record('warehouse')['client']),
                                   ('user_email', current_user.get_user_email()))['id']
        last_data['unique_ID'] = str(user_id) + '_' + str(lead_id) + '_' + string
        dbase.update_record_by_id("warehouse", dbase.get_last_record("warehouse")['id'], last_data)

        return view_BVZ(dbase, menu, current_user, last_data, accept_index=5)

    if "button-save-pricing" in request_form:

        last_data = dict(list(dict(dbase.get_last_record("warehouse")).items())[1::])

        if dbase.check_records('my_warehouse'):
            if dbase.get_last_record('warehouse')['id'] != dbase.get_last_record("my_warehouse")['id']:
                dbase.save_warehouse()
            else:
                dbase.update_record_by_id("my_warehouse", dbase.get_last_record("my_warehouse")['id'], last_data)

        return view_BVZ(menu, choose_project, last_data, accept_index=6)

    if "button-update-pricing" in request_form:
        dbase.del_records('warehouse', dbase.get_last_record('warehouse')['id'])

        return view_BVZ(dbase, menu, current_user, accept_index=0)
