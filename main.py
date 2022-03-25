import base64
import os

path = "D:\\Instrumentation-2\\01-1. Скрипка.wav"
mypath = "C:\\Program Files (x86)\\Инструментоведение\\sound"


def search_subfolder(search_path):
    print(os.listdir(search_path))


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
    search_subfolder(os.path.abspath(mypath))
    search_audio(os.path.abspath(mypath), '')  # jpg формат поиска # '.' все файлы '123'
    # encode_audio(path)
    print(path)
    print(mypath)
