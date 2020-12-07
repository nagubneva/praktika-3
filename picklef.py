import pickle


def save_table(table, filename): #принимает таблицу, название файла
    with open(filename + '.pickle', 'wb') as f: #открывает  файл на запись в режиме двоичного кода
        pickle.dump(table, f) #из модуля pickle функцией dump записываем таблицу в файл


def load_table(filename): #принимает название файла
    with open(filename + '.pickle', 'rb') as f: #открывает файл на чтение в двоичном режиме
        return pickle.load(f) #возвращает содержимое файла (таблицу)