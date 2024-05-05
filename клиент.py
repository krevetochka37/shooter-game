import socket
import struct
import json


# Устанавливаем хост и порт для соединения
host = '127.0.0.1'
port = 12345

# Создаем сокет и устанавливаем соединение с сервером
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

# Основной цикл программы для взаимодействия с сервером
while True:
    command = input("Введите команду (create_directory, append_numbers or q): ")
    s.send(command.encode())

    # Обработка команды 'create_directory' и 'q'
    if command == 'create_directory':
        print(s.recv(2048).decode())

    elif command == 'append_numbers':
        user_input = input("введите числа для бинарного дерева: ")
        s.send(user_input.encode())
        print(s.recv(2048).decode())


    elif command == 'q':
        break

s.close()
