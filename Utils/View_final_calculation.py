
title_table = [
    {"name": 'width', "title": 'Ширина'},
    {"name": 'length', "title": 'Длинна'},
    {"name": 'height', "title": 'Высота'},
    {"name": 'area', "title": 'Площадь'},
    {"name": 'price_selling_UA', "title": 'Цена склада'},
    {"name": 'cost_square_meters_UA', "title": 'Цена 1 [m²]'},
    {"name": 'price_delivery', "title": 'Цена доставки'},
    {"name": 'price_building', "title": 'Цена монтажа'},
    {"name": 'price_foundation', "title": 'Цена фундамента'},
    {"name": 'cost_sq_met_found', "title": 'Цена 1 [m²]'},
    {"name": 'cost_option', "title": 'Цена опций'},
    {"name": 'profit_UA', "title": 'Моржа'},
    {"name": 'final_price_UA', "title": 'Цена проекта'},
    {"name": 'final_cost_sq_m_pr', "title": 'Цена 1 [m²]'},
    {"name": 'final_profit_UA', "title": 'Доход'},
]

mask_value_project_in_table = {
    "id": False,
    "width": False,
    "length": False,
    "height": False,
    "area": False,
    "price_selling_UA": False,
    "cost_square_meters_UA": False,
    "price_delivery": False,
    "price_building": False,
    "price_foundation": False,
    "cost_sq_met_found": False,
    "cost_option": False,
    "profit_UA": False,
    "final_price_UA": False,
    "final_cost_sq_m_pr": False,
    "final_profit_UA": False
}


def view_table_warehouse(dbase, current_user, current_lead):
    result = []
    if dbase.check_records('my_warehouse'):
        current_records = dbase.get_info_records('my_warehouse',
                                                 current_user.get_user_email(),
                                                 ('client', current_lead['company']))
        for record in current_records:
            result.append({key: record[key] for key in mask_value_project_in_table})

    return title_table, result
