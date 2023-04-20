
from flask import render_template


def pricing_view(menu, choose_project, accept_index=None,
                 **kwargs):

    accepts = ['none'] * 6
    if accept_index is not None:
        for a in range(accept_index):
            accepts[a] = "block"
    accept_1, accept_2, accept_3, accept_4, accept_5, accept_6 = accepts

    set_title_table_dimension = [
        {"name": 'width', "title": 'ширина', "placeholder": 'метры', "current_vol": False},
        {"name": 'length', "title": 'длинна', "placeholder": 'метры', "current_vol": False},
        {"name": 'height', "title": 'высота', "placeholder": 'метры', "current_vol": False}
    ]

    set_title_table_pricing = [
        {"name": 'price_warehouse', "title": 'склад', "placeholder": 'евро', "current_vol": False},
        {"name": 'price_delivery', "title": 'доставка', "placeholder": 'евро', "current_vol": False},
        {"name": 'price_building', "title": 'монтаж', "placeholder": 'евро', "current_vol": False},
    ]
    set_title_table_second_pricing = [
        {"name": 'price_foundation', "title": 'фундамент', "placeholder": 'евро', "current_vol": False},
        {"name": 'price_light', "title": 'освещение', "placeholder": 'евро', "current_vol": False},
        {"name": 'price_option', "title": 'стеллажи', "placeholder": 'евро', "current_vol": False}
    ]
    get_title_table_pricing = [
        {"name": 'price_Protan', "title": 'Цена Protan: ', "result": f'{0} euro'},
        {"name": 'price_square_meters', "title": 'Цена за 1 [m²]: ', "result": f'{0} euro'},
        {"name": 'price_cubic_meters', "title": 'Цена за 1 [m³]: ', "result": f'{0} euro'},
    ]
    get_title_table_cost = [
        {"name": 'price_cost', "title": 'Себестоимость: ', "result": f'{0} euro'},
        {"name": 'price_customs', "title": 'Таможня: ', "result": f'{0} euro'},
        {"name": 'price_VAT', "title": 'НДС: ', "result": f'{0} euro'},
    ]
    get_title_table_dimension = [
        {"result": f"W: {kwargs['width']}m | L: {kwargs['length']}m | H: {kwargs['height']}m", "title": 'Размеры: '},
        {"result": f"{kwargs['area']} m²", "title": 'Площадь: '},
        {"result": f"{kwargs['volume']} m³", "title": 'Объем: '},
    ]
    get_title_table_total_coast = [
        {"name": 'cost_price', "title": 'Себестоимость: ', "result": f'{0} euro'},
        {"name": 'profit', "title": 'Маржинальность: ', "result": f'{0} euro'},
        {"name": 'selling_price', "title": 'Цена продажи: ', "result": f'{0} euro'},
    ]
    title_table = [
        {"name": 'width', "title": 'Ширина'},
        {"name": 'length', "title": 'Длинна'},
        {"name": 'height', "title": 'Высота'},
        {"name": 'area', "title": 'Площадь'},
        {"name": 'volume', "title": 'Объем'},
        {"name": 'price_warehouse', "title": 'Цена склада'},
        {"name": 'price_delivery', "title": 'Цена доставки'},
        {"name": 'price_building', "title": 'Цена монтажа'},
        {"name": 'price_foundation', "title": 'Цена фундамента'},
        {"name": 'price_light', "title": 'Цена света'},
        {"name": 'cost_price', "title": 'Моржа'},
        {"name": 'price_selling', "title": 'Цена продажи'},
        {"name": 'price_one_m_squad', "title": 'Цена 1 [m²]'},
    ]
    value_warehouse = []

    choose_product = [
        {"name": 'БВЗ', "product": 'Warehouse'},
        {"name": 'Стеллажи', "product": 'Racks'},
        {"name": 'Мусорные баки', "product": 'Trash-can'},
        {"name": 'Поддоны', "product": 'Pallets'},
        {"name": 'Пластиковая тара', "product": 'Plastic-container'},
        {"name": 'Техника', "product": 'Equipment'},
    ]

    return render_template('pricing.html',
                           title='My PRICING',
                           menu=menu,
                           accept_1=accept_1,
                           accept_2=accept_2,
                           accept_3=accept_3,
                           accept_4=accept_4,
                           accept_5=accept_5,
                           accept_6=accept_6,
                           set_title_table_dimension=set_title_table_dimension,
                           set_title_table_pricing=set_title_table_pricing,
                           set_title_table_second_pricing=set_title_table_second_pricing,
                           get_title_table_cost=get_title_table_cost,
                           get_title_table_dimension=get_title_table_dimension,
                           get_title_table_pricing=get_title_table_pricing,
                           get_title_table_total_coast=get_title_table_total_coast,
                           title_table=title_table,
                           value_warehouse=value_warehouse,
                           choose_project=choose_project,
                           choose_product=choose_product
                           )

