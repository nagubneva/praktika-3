import csv


def save_table(table, filename): #принимает на вход таблицу названия файла, куда ее записать
    with open(filename + '.csv', 'w', newline='') as f: #открывает файл по названию
        file_writer = csv.writer(f, delimiter=';') #из модуля csv берем функцию writer, разделитель(;)
        file_writer.writerow(table['columns_names']) #пишем в файл имена столбцов 
        for row in table['rows']: #пишем в файл все строчки из таблицы
            file_writer.writerow(row)


def load_table(filename): #принимает на вход название файла
    from .table import create_table #из модуля table берем create_ table
    with open(filename + '.csv', 'r', newline='') as f: #открываем файл на чтение
        file_reader = csv.reader(f, delimiter=';') #из модуля берем reader разделитель (;)
        rows = []
        for row in file_reader: #в список новых строк добавляем строки, прочитанные из файла
            rows.append(row)
        return create_table(rows[0], rows[1:]) #возвращаем новую таблицу, нулевая строчка - список названий столбцов, остальные - список строк