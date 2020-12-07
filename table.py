from copy import deepcopy


def create_table(columns_names, rows, types=None): 
    #Функция, которая возвращает словарь, содержащий название столбцов, список типов, строчки (внутреннее представление таблицы). Принимает на вход назване столбцов, список строчек, список типов (опционально).
    if not types:
        types = [str] * len(columns_names)
    table = {
        'columns_names': columns_names,
        'types': types,
        'rows': rows,
    }
    update_types(table) #Обновление типов (рассмотреть update_types)
    return table


def update_types(table): #Функция принимает таблицу. Эту таблицу для каждого типа для соответстующего столбца преобразует то, что лежит в каждой ячейке в новый тип, который берется из списка типов. 
    for col_i, t in zip(range(len(table['rows'][0])), table['types']):
        for row_i in range(len(table['rows'])):
            table['rows'][row_i][col_i] = t(table['rows'][row_i][col_i])


def print_table(table): #Принимает на вход таблицу, печатает ее в консоль.
    for name in table['columns_names']:
        print('{:<20}'.format(name), sep='', end='')
    print()
    for row in table['rows']:
        for el in row:
            print('{:<20}'.format(el), sep='', end='')
        print()


def get_rows_by_number(table, start, stop=None, copy_table=False):#Функция принимает таблицу и начало среза, конец среза опционально, также копирировать ли таблицу (опционально)
    if not stop: #Если не указан стоп, то стоп = кол-во строк 
        stop = len(table['rows'])
    if not 0 <= start < stop <= len(table['rows']): #Ошибка, если стоп не больше старта. Или если стоп и старт вне диапазаона таблицы. 
        raise ValueError('Неверно указаны start и [stop]')
    if copy_table: #Если таблицу копировать, то берем в качестве новых строчек глубокую копию старых
        #Если не копировать, то сохраняем ссылку на старые строчки. От таблицы берем срез.
        rows = deepcopy(table['rows'][start:stop]) 
    else:
        rows = table['rows'][start:stop]
    return create_table(table['columns_names'], rows, table['types']) #Создаем функцией create_table новую таблицу, передавая в нее имена старой таблицы новый список строк и список типов старой таблицы.


def get_rows_by_index(table, *values, copy_table=False): #Принимает на вход таблицу, последовательность значений и копировать ли таблицу (опционально), возвращает ее
    rows = [] #Создаем новый список строк
    for value in values:
        for row in table['rows']:
            if value == row[0]: #если значение в какой-то строчке совпадает со значением в нулевом столбике, то закидываем эту строчку в новый список строк
                if copy_table:
                    rows.append(deepcopy(row))
                else:
                    rows.append(row)
    if not len(rows): #Если в последовательности значений нет соответствующих значений в нулевом столбце, то новый список строк будет пустым. Это приводит к ошибке 
        raise ValueError('Пустая таблица не может быть создана, так как ни одного значения val1, ..., valN нет в первом столбце таблицы')
    return create_table(table['columns_names'], rows, table['types']) #Создаем функцией create_table новую таблицу, передавая в нее имена старой таблицы новый список строк и список типов старой таблицы.



def get_column_types(table, by_number=True): #Принимает таблицу и способ наименования столбцов (опционально)
    if not type(by_number) is bool:  #Если by_number не типа bool, то ошибка
        raise TypeError('Аргумент by_number должен быть типа str')
    if by_number:  #Если наименования столбцов по индексам, то ключи словаря типов - числа
        keys = range(len(table['columns_names']))
    else:  #Если наименования стобцов по названиям,  то ключи словаря типов - это список имен столбцов
        keys = table['columns_names']
    return {key: value for key, value in zip(keys, table['types'])}  #Создаем словарь из ключей, определенных выше, а значений из списка типов и возвращаем его 


def set_column_types(table, types_dict, by_number=True): #На вход принимает таблицу и словарь типов и способ наименования столбцов (опционально)
    if not type(by_number) is bool: #Здесь проверка на тип bool 
        raise TypeError('Аргумент by_number должен быть типа str')
    for key, value in types_dict.items():  #Интерируемся по словарю типов
        if value not in {str, int, bool, float}:  #Ошибка, если в словаре типов значение не из допустимого списка
            raise TypeError('Значения types_dict должны быть в виде str, int, bool или float')
        if by_number:  #Если способ наименования слобцов индексы, то проверяем, что индекс столбца находится в диапазоне таблицы и запоминаем ее
            if not 0 <= key <= len(table['types']): 
                raise ValueError('Ключ словаря не является индексом столбца')
            i = key
        else: #Если способ наименования столбцов это названия столбцов, то проверяем, находится ли название в списке названий. Если нет - ошибка, если да - запоминаем индекс столбца. 
            if key not in table['columns_names']: 
                raise ValueError('Ключ словаря не найден в списке имен столбцов')
            i = table['columns_names'].index(key)
        table['types'][i] = value #По соответствующему индексу столбца в список типов записываем новый тип
    update_types(table) #Обновляем типы


def get_values(table, column=0): #Принимает таблицу и названия или индекс столбца
    if type(column) is int: #Если столбец задан индексом, проверяем находится ли он в диапазоне таблицы и запоминаем его индекс
        if not 0 <= column <= len(table['rows'][0]):
            raise ValueError('Столбца с таким индексом не существует в таблице')
        col_i = column
    elif type(column) is str: #Если столбец задан названием, то проверяем находится ли оно в списке названий и столбцов, запоминаем его индекс
        if column not in table['columns_names']:
            raise ValueError('Столбца с таким именем не существует в таблице')
        col_i = table['columns_names'].index(column)
    else: #Если столбец задан не числом, не названием, то ошибка
        raise TypeError('Аргумент column должен быть типа int или str')

    values = []
    for row_i in range(len(table['rows'])): #Из таблицы в список values добавляем элементы столбца по его индексу и возвращаем этот список values
        values.append(table['rows'][row_i][col_i])
    return values


def get_value(table, column=0): #get_value работает как get_values, только для таблицы с одной строкой
    return get_values(table, column)[0]


def set_values(table, values, column=0): #Принимает таблицу и список значений и столбец
    if len(values) != len(table['rows']): #Ошибка, если кол-во значений не совпадает с кол-вом строк
        raise ValueError('Количество значений в списке values не соответствует количеству строчек таблицы')
    if type(column) is int: #Проверка на корректность column также как в get_values
        if not 0 <= column <= len(table['rows'][0]):
            raise ValueError('Столбца с таким индексом не существует в таблице')
        col_i = column
    elif type(column) is str:
        if column not in table['columns_names']:
            raise ValueError('Столбца с таким именем не существует в таблице')
        col_i = table['columns_names'].index(column)
    else:
        raise TypeError('Аргумент column должен быть типа int или str')
    for row_i, el in zip(range(len(table['rows'])), values):
        table['rows'][row_i][col_i] = el #В столбец по индексу записываются новые элементы из списка значений 
    update_types(table) #Обновляем типы


def set_value(table, value, column=0): #Работает также как set_values,только принимает не список значений, а одно значение и работает только с нулевой строкой
    if type(column) is int:
        if not 0 <= column <= len(table['rows'][0]):
            raise ValueError('Столбца с таким индексом не существует в таблице')
        col_i = column
    elif type(column) is str:
        if column not in table['columns_names']:
            raise ValueError('Столбца с таким именем не существует в таблице')
        col_i = table['columns_names'].index(column)
    else:
        raise TypeError('Аргумент column должен быть типа int или str')
    table['rows'][0][col_i] = value
    update_types(table)
    