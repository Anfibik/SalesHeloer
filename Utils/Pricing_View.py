from flask import render_template


def pricing_view(menu, choose_project, update_dict=None, accept_index=None):
    accepts = ['none'] * 6
    if accept_index is not None:
        for i in range(accept_index):
            accepts[i] = "block"
    accept_1, accept_2, accept_3, accept_4, accept_5, accept_6 = accepts

    m_dict = {'width': False, 'length': False, 'height': False, 'area': False, 'volume': False,
              'price_Protan': False, 'price_square_meters': False, 'price_cubic_meters': False,
              'price_cost': False, "price_customs": False, 'price_VAT': False,
              'cost_price': False, 'profit': False, 'selling_price': False,
              'price_delivery': False, 'price_warehouse': False, 'price_building': False,
              'price_foundation': False, 'price_light': False, 'price_rack': False}
    if update_dict is not None:
        for key, vol in update_dict.items():
            m_dict[key] = vol

    set_title_table_dimension = [
        {"name": 'width', "title": 'ширина', "placeholder": 'метры', "current_vol": m_dict['width']},
        {"name": 'length', "title": 'длинна', "placeholder": 'метры', "current_vol": m_dict['length']},
        {"name": 'height', "title": 'высота', "placeholder": 'метры', "current_vol": m_dict['height']}
    ]

    set_title_table_pricing = [
        {"name": 'price_warehouse', "title": 'склад', "placeholder": 'евро', "current_vol": m_dict['price_warehouse']},
        {"name": 'price_delivery', "title": 'доставка', "placeholder": 'евро', "current_vol": m_dict['price_delivery']},
        {"name": 'price_building', "title": 'монтаж', "placeholder": 'евро', "current_vol": m_dict['price_building']},
    ]
    set_title_table_second_pricing = [
        {"name": 'price_foundation', "title": 'фундамент', "placeholder": 'евро',
         "current_vol": m_dict['price_foundation']},
        {"name": 'price_light', "title": 'освещение', "placeholder": 'евро', "current_vol": m_dict['price_light']},
        {"name": 'price_rack', "title": 'стеллажи', "placeholder": 'евро', "current_vol": m_dict['price_rack']}
    ]
    get_title_table_dimension = [
        {"result": f"W: {m_dict['width']}m | L: {m_dict['length']}m | H: {m_dict['height']}m", "title": 'Размеры: '},
        {"result": f"{m_dict['area']} m²", "title": 'Площадь: '},
        {"result": f"{m_dict['volume']} m³", "title": 'Объем: '},
    ]
    get_title_table_pricing = [
        {"name": 'price_Protan', "title": 'Цена Protan: ', "result": f"{m_dict['price_warehouse']} euro"},
        {"name": 'price_delivery', "title": 'Цена Доставка: ', "result": f"{m_dict['price_delivery']} euro"},
        {"name": 'price_building', "title": 'Цена Монтаж: ', "result": f"{m_dict['price_building']} euro"},

        {"name": 'price_square_meters', "title": 'Цена за 1 [m²]: ', "result": f"{m_dict['price_square_meters']} euro"},
        {"name": 'price_cubic_meters', "title": 'Цена за 1 [m³]: ', "result": f"{m_dict['price_cubic_meters']} euro"},
    ]
    get_title_table_cost = [
        {"name": 'price_cost', "title": 'Себестоимость: ', "result": f"{m_dict['price_cost']} euro"},
        {"name": 'price_customs', "title": 'Таможня: ', "result": f"{m_dict['price_customs']} euro"},
        {"name": 'price_VAT', "title": 'НДС: ', "result": f"{m_dict['price_VAT']} euro"},
    ]

    get_title_table_total_coast = [
        {"name": 'cost_price', "title": 'Себестоимость: ', "result": f"{m_dict['cost_price']} euro"},
        {"name": 'profit', "title": 'Маржинальность: ', "result": f"{m_dict['profit']} euro"},
        {"name": 'selling_price', "title": 'Цена продажи: ', "result": f"{m_dict['selling_price']} euro"},
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
