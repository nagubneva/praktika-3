def save_table(table, filename): #на вход принимает таблицу, название файла
    with open(filename + '.txt', 'w') as f: #открывает файл на запись
        for name in table['columns_names']: #печатает таблицу kak функция print_table
            print('{:<20}'.format(name), sep='', end='', file=f)
        print(file=f)
        for row in table['rows']:
            for el in row:
                print('{:<20}'.format(el), sep='', end='', file=f)
            print(file=f)