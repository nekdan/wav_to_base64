import base64
import os
import sqlite3

#path = "D:\\Instrumentation-2\\01-1. Скрипка.wav"
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


def search_image(search_path, name_image):
    with os.scandir(search_path) as scan:
        list_folder = [file.name for file in scan if file.is_dir()]
    for folder in list_folder:
        name_image.append(folder.split('. ')[1])
    return name_image


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


def search_audio(search_path, keyword, count_subfolder):

    '''
    for file in os.listdir(search_path):
        if os.path.isfile(search_path + '\\' + file):
            if keyword in file:
                #print(file, '==>', search_path + '\\' + file)
                #print(file)
                name = file.partition(' ')[2]
                #print(name)
        else:
            search_audio(search_path + '\\' + file, keyword)
    '''
    count_track = 0
    count_subfolder += 1

    try:
        sqlite_connection = sqlite3.connect('D:\\Instrum-v2\\app.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        for file in os.listdir(search_path):
            if os.path.isdir(search_path + '\\' + file):
                if keyword in file:
                    print('ЭТО ПОДПАПКА - ', file)
            if os.path.isfile(search_path + '\\' + file):
                if keyword in file:
                    # print(file, '==>', search_path + '\\' + file)
                    # print(file)
                    name = file.partition(' ')[2]
                    # print(name)
                    name_without_extension = name.split('.')[0]
                    number = file.split(' ')[0]
                    instrument = search_path.rpartition('\\')[-1]
                    instrument_name = instrument.partition(' ')[2]
                    print(instrument_name)
                    print('-----------СЧЁТЧИК--', count_subfolder)
                    # если это папка с треками
                    if count_subfolder < 3:
                        cursor.execute("SELECT Id FROM Instuments WHERE Name = ?", (instrument_name,))
                        instrument_id = cursor.fetchone()
                        print(instrument_id)
                        if '.' not in number:
                            # записываем категорию для входящих в неё треков
                            name_category = name
                            # заполняем таблицу Sounds категориями треков
                            cursor.execute("SELECT Id FROM Instuments WHERE Name = ?", (instrument_name,))
                            instrument_id = cursor.fetchone()
                            # print(instrument_id)
                            sqlite_insert_query = """INSERT INTO Sounds
                                                             (Id, Name, SubinstumentId, InstumentId, SubinstrumentId)
                                                             VALUES (NULL, ?, NULL, ?, NULL);"""
                            cursor.execute(sqlite_insert_query, (name, instrument_id[0]))
                        elif '-' in number:
                            # определяем треки в категории
                            # name_without_extension = name.split('.')[0]
                            print(name_without_extension, 'Это трек в категории:', name_category)
                            cursor.execute("SELECT Id FROM Sounds WHERE Name = ? AND InstumentId = ?",
                                           (name_category, instrument_id[0]))
                            sound_id = cursor.fetchone()
                            print(sound_id[0], 'это id sound')
                            print(instrument_id[0], '- это id instrument')
                            sqlite_insert_query = """INSERT INTO Subsounds
                                                        (Id, Name, SoundId) 
                                                        VALUES (NULL, ?, ?);"""
                            cursor.execute(sqlite_insert_query, (name_without_extension, sound_id[0]))
                            path = search_path + '\\' + file
                            audio_base64 = encode_audio(path)
                            # print(audio_base64)
                            cursor.execute("SELECT Id FROM Subsounds WHERE Name = ? AND SoundId = ? ORDER BY Id DESC",
                                           (name_without_extension, sound_id[0]))
                            subsound_id = cursor.fetchone()
                            # Проверить с обратной сортировкой, что он добавляет файл, потом считывает, а не добавляет сразу
                            if subsound_id:
                                print(subsound_id[0], 'это id subsound')
                                # print('Кортеж с треком -- ', (name, audio_base64, subsound_id[0]))
                                # Добавляем треки с описанием в категориях
                                sqlite_insert_query = """INSERT INTO SoundsDatas
                                                        (Id, Description, SoundBase64, SoundId, SubsoundId) 
                                                        VALUES (NULL, ?, ?, NULL, ?);"""
                                # Разобраться почему вставляет base64 в другом формате -------------------------
                                cursor.execute(sqlite_insert_query, (name, audio_base64, subsound_id[0]))
                        else:
                            # записываем самостоятельные треки в Sounds
                            print('самостоятельный трек', name_without_extension, 'id =', instrument_id)
                            sqlite_insert_query = """INSERT INTO Sounds
                                                        (Id, Name, SubinstumentId, InstumentId, SubinstrumentId)
                                                        VALUES (NULL, ?, NULL, ?, NULL);"""
                            cursor.execute(sqlite_insert_query, (name_without_extension, instrument_id[0]))
                            path = search_path + '\\' + file
                            audio_base64 = encode_audio(path)
                            cursor.execute("SELECT Id FROM Sounds WHERE Name = ? AND InstumentId = ?",
                                           (name_without_extension, instrument_id[0]))
                            sound_id = cursor.fetchone()
                            #print('sound_id =', sound_id)
                            # условие для отладки
                            # if sound_id[0] == 125:
                            # добавляем самостоятельный трек в базу
                            sqlite_insert_query = """INSERT INTO SoundsDatas 
                                                    (Id, Description, SoundBase64, SoundId, SubsoundId)
                                                    VALUES (NULL, ?, ?, ?, NULL);"""
                            cursor.execute(sqlite_insert_query, (name, audio_base64, sound_id[0]))
                    # если это подпапка, сохраняем логику как в папке
                    else:
                        cursor.execute("SELECT Id FROM Subinstuments WHERE Name = ?", (instrument_name,))
                        subinstrument_id = cursor.fetchone()
                        print(subinstrument_id)
                        print(instrument_name, 'Инструмент')
                        print(file)
                        if '.' not in number:
                            # записываем категорию для входящих в неё треков
                            name_category = name
                            # заполняем таблицу Sounds категориями треков
                            sqlite_insert_query = """INSERT INTO Sounds
                                                             (Id, Name, SubinstumentId, InstumentId, SubinstrumentId)
                                                             VALUES (NULL, ?, ?, NULL, NULL);"""
                            cursor.execute(sqlite_insert_query, (name, subinstrument_id[0]))
                        elif '-' in number:
                            # определяем треки в категории
                            # name_without_extension = name.split('.')[0]
                            print(name_without_extension, 'Это трек в категории:', name_category)
                            cursor.execute("SELECT Id FROM Sounds WHERE Name = ? AND SubinstumentId = ?",
                                           (name_category, subinstrument_id[0]))
                            sound_id = cursor.fetchone()
                            print(sound_id[0], 'это id sound')
                            print(subinstrument_id[0], '- это id instrument')
                            sqlite_insert_query = """INSERT INTO Subsounds
                                                        (Id, Name, SoundId) 
                                                        VALUES (NULL, ?, ?);"""
                            cursor.execute(sqlite_insert_query, (name_without_extension, sound_id[0]))
                            path = search_path + '\\' + file
                            audio_base64 = encode_audio(path)
                            # print(audio_base64)
                            cursor.execute("SELECT Id FROM Subsounds WHERE Name = ? AND SoundId = ? ORDER BY Id DESC",
                                           (name_without_extension, sound_id[0]))
                            subsound_id = cursor.fetchone()
                            # Проверить с обратной сортировкой, что он добавляет файл, потом считывает, а не добавляет сразу
                            if subsound_id:
                                print(subsound_id[0], 'это id subsound')
                                # print('Кортеж с треком -- ', (name, audio_base64, subsound_id[0]))
                                sqlite_insert_query = """INSERT INTO SoundsDatas
                                                        (Id, Description, SoundBase64, SoundId, SubsoundId) 
                                                        VALUES (NULL, ?, ?, NULL, ?);"""
                                # Разобраться почему вставляет base64 в другом формате -------------------------
                                cursor.execute(sqlite_insert_query, (name, audio_base64, subsound_id[0]))
                        else:
                            # записываем самостоятельные треки в Sounds
                            print('самостоятельный трек', name_without_extension, 'subindtrument id =', subinstrument_id)
                            sqlite_insert_query = """INSERT INTO Sounds
                                                        (Id, Name, SubinstumentId, InstumentId, SubinstrumentId)
                                                        VALUES (NULL, ?, ?, NULL, NULL);"""
                            cursor.execute(sqlite_insert_query, (name_without_extension, subinstrument_id[0]))
                            path = search_path + '\\' + file
                            audio_base64 = encode_audio(path)
                            cursor.execute("SELECT Id FROM Sounds WHERE Name = ? AND SubinstumentId = ?",
                                           (name_without_extension, subinstrument_id[0]))
                            sound_id = cursor.fetchone()
                            #print('sound_id =', sound_id)
                            # условие для отладки
                            # if sound_id[0] == 125:
                            # добавляем трек в базу
                            sqlite_insert_query = """INSERT INTO SoundsDatas
                                                    (Id, Description, SoundBase64, SoundId, SubsoundId)
                                                    VALUES (NULL, ?, ?, ?, NULL);"""
                            cursor.execute(sqlite_insert_query, (name, audio_base64, sound_id[0]))

                    if file.endswith('.wav'):
                        # заполняем треками
                        count_track += 1
                        #print(name, ' - это трек')
                        instrument = search_path.rpartition('\\')[-1]
                        instrument_name = instrument.partition(' ')[2]
                        #print(file)
                        #number = file.split('. ')[0]
                        #if '-' in number:
                            #print(file, '- входит в категорию')
                        #else:
                            #print(file, '- самостоятельный')

            else:
                if count_subfolder > 1:
                    print("ЭТО ПОДПАПКА ------------------------------------------------------", file)
                    print('это счётчик подпапок -', count_subfolder)
                    print(search_path)
                    instrument = search_path.rpartition('\\')[-1]
                    instrument_name = instrument.partition(' ')[2]
                    name = file.partition(' ')[2]
                    name_without_extension = name.split('.')[0]
                    print(instrument_name)
                    cursor.execute("SELECT Id FROM Instuments WHERE Name = ?",
                                   (instrument_name,))
                    instrument_id = cursor.fetchone()
                    print(instrument_id, 'instrument ID')
                    sqlite_insert_query_subinstruments = """INSERT INTO Subinstuments
                                                            (Id, Name, InstumentId) 
                                                                VALUES (NULL, ?, ?);"""
                    # тест записи в бд
                    # cursor.execute(sqlite_insert_query_subinstruments)
                    cursor.execute(sqlite_insert_query_subinstruments, (name_without_extension, instrument_id[0]))
                    sqlite_connection.commit()
                    print("Записи успешно вставлены в таблицу sqlitedb_developers", cursor.rowcount)
                    #sqlite_connection.commit()
                    #cursor.close()
                    #print((name_without_extension, instrument_id[0]))

                    #sqlite_insert_query = """INSERT INTO SoundsDatas
                                                #(Id, Description, SoundBase64, SoundId, SubsoundId)
                                                #VALUES (NULL, ?, ?, ?, NULL);"""
                    # cursor.execute(sqlite_insert_query, (name, audio_base64, sound_id[0]))

                search_audio(search_path + '\\' + file, keyword, count_subfolder)
        print(count_track)

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
        #for instrument in records:
        #    cursor.execute(sqlite_insert_query, (instrument,))
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


def insert_images(records):
    try:
        sqlite_connection = sqlite3.connect('D:\\Instrum-v2\\app.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_query = """INSERT INTO NoteImages
                                 (Id, NoteBase64, Name, SoundId, SubsoundId)
                                 VALUES (NULL, ?, ?, NULL, NULL);"""

        #cursor.execute(sqlite_insert_query, (records[2],))
        for image in records:
            cursor.execute(sqlite_insert_query, (image,))
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
    #with open('xyz.txt', 'wb') as f:  # открытие в режиме записи
    #    f.write(encoded)  # запись в файл
    #print(encoded)
    return encoded


if __name__ == "__main__":
    # list_folder = search_folder(os.path.abspath(mypath), [])
    # search_subfolder(os.path.abspath(mypath), [], 0)
    # name_folder = ['Jaroslav', 'Timofei', 'Nikita']
    # insert_instruments(list_folder)
    search_audio(os.path.abspath(mypath), '', 0)  # jpg формат поиска # '.' все файлы '123'
    # encode_audio(path)
    print(mypath)
