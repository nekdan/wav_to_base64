import base64
import os
import sqlite3

path = "D:\\Instrumentation-2\\01-1. Скрипка.wav"
mypath = "C:\\Program Files (x86)\\Инструментоведение\\sound"


def insert_instruments(records):
    try:
        sqlite_connection = sqlite3.connect('D:\\Instrum-v2\\app.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        '''
        cursor.execute("SELECT Name FROM Instuments")
        instruments_in_bd = cursor.fetchall()
        print(instruments_in_bd[0])
        print((records[0],))
        if instruments_in_bd[0] == (records[0],):
            print('Такой инструмент есть в базе')
        '''

        sqlite_insert_query = """INSERT INTO Instuments
                                 (Id, Name, CategoryId)
                                 VALUES (NULL, ?, 1);"""

        # cursor.execute("INSERT INTO Instuments VALUES(NULL, ?, 1)", (records[2],))
        for instrument in records:
            cursor.execute(sqlite_insert_query, (instrument,))
        # .executemany(sqlite_insert_query, (records,))
        # cursor.executemany("INSERT INTO Instuments VALUES(NULL, ?, 1)", (records,))
        sqlite_connection.commit()
        print("Записи успешно вставлены в таблицу sqlitedb_developers", cursor.rowcount)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def search_folder(search_path, name_folder):
    with os.scandir(search_path) as scan:
        list_folder = [file.name for file in scan if file.is_dir()]
    for folder in list_folder:
        name_folder.append(folder.split('. ')[1])
    return name_folder


def search_subfolder(search_path, name_subfolder, count_subfolder):
    with os.scandir(search_path) as scan:
        subdir = [file.name for file in scan if file.is_dir()]
        # count_subfolder += 1
        # print(count_subfolder)
        if subdir:
            # print(subdir)
            count_subfolder += 1
            # print(count_subfolder)
            if count_subfolder < 2:
                print(subdir)  # список папок (инструментов)
                print(search_path)  # путь к основной папке
            else:
                print(subdir)  # список подпапок ( вложенные инструменты)
                print(search_path)  # путь к инструменту
        for file in subdir:
            if os.path.isdir(search_path + '\\' + file):
                # print(file)
                search_subfolder(search_path + '\\' + file, name_subfolder, count_subfolder)
    # print(subdir)

    for folder in subdir:
        name_subfolder.append(folder.split('. ')[1])
    # print(name_subfolder)
    '''
    list_subfolder = os.listdir(search_path)
    for subfolder in list_subfolder:
        name_subfolder.append(subfolder.split('. ')[1])
        # print(name_subfolder)
        if os.path.isfile(search_path + '\\' + subfolder):
            print(subfolder)
        else:
            search_subfolder(search_path + '\\' + subfolder, name_subfolder)
            #print(search_path + '\\' + subfolder)
    return subfolder
    '''


def search_audio(search_path, keyword):
    for file in os.listdir(search_path):
        if os.path.isfile(search_path + '\\' + file):
            if keyword in file:
                print(file, '==>', search_path + '\\' + file)
        else:
            search_audio(search_path + '\\' + file, keyword)


# Pass the audio data to an encoding function.
def encode_audio(path_audio):
    """
    with open(path_audio, 'rb') as f:
        for line in f:
            data_line = f.readline()
            #print(data_line)
            encoded = base64.b64encode(data_line)
            #print(encoded)
        with open('dasa.txt', 'wb') as fi:  # открытие в режиме записи
            fi.write(encoded)
    """

    with open(path_audio, "rb") as file:
        data = file.read()
    encoded = base64.b64encode(data)
    with open('xyz.txt', 'wb') as f:  # открытие в режиме записи
        f.write(encoded)  # запись в файл


if __name__ == "__main__":
    list_folder = search_folder(os.path.abspath(mypath), [])
    search_subfolder(os.path.abspath(mypath), [], 0)
    # name_folder = ['Jaroslav', 'Timofei', 'Nikita']
    # insert_instruments(list_folder)
    # search_audio(os.path.abspath(mypath), '')  # jpg формат поиска # '.' все файлы '123'
    # encode_audio(path)
    print(path)
    print(mypath)
