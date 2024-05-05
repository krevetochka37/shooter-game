import os
import datetime
import json
import socket
import struct

# Установка хоста и порта для соединения
host = '127.0.0.1'
port = 12345

# Создание сокета и привязка к хосту и порту
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1) #указывает на максимальное количество ожидающих соединений (В данном случае 1 указывает на то, что сервер будет принимать\
# только одно соединение за раз.)

# Принятие подключения
conn, addr = s.accept()

def create_directory():
    current_time = datetime.datetime.now()
    folder_name = current_time.strftime("%d-%m-%Y %H-%M-%S")
    os.makedirs(folder_name)
    return folder_name

def save_tree(tree_data, folder_name, tree_number):
    filename = os.path.join(folder_name, f"{tree_number}.json")
    with open(filename, 'w') as f:
        json.dump(tree_data, f)
    return json.dumps(tree_data)


def main():
    folder_name = create_directory()
    tree_number = 1
    tree_data = []
    current_path = os.getcwd()

    while True:
        try:
            command = conn.recv(2048).decode()  # Получаем команду от клиента
            conn.send("Команда обработана".encode()) 
        except ConnectionResetError:
            print("Соединение с клиентом разорвано.")
            break

        if command == 'create_directory':
            create_directory()

        elif command == 'append_numbers':
            while True:
                user_input = conn.recv(2048).decode()
                if user_input:
                    save_tree(user_input, folder_name, tree_number)
                    print(f"Дерево {tree_number} сохранено в {folder_name}")
                    tree_number += 1
                    break
                
        elif command == 'show_list':
            with open(os.path.join(current_path, 'files_info.json'), 'r', encoding='utf-8') as file:
                files_info = json.load(file)
                json_data = json.dumps(files_info, ensure_ascii=False)
                json_data_bytes = json_data.encode()  # Преобразуем JSON данные в байты
                json_data_length = len(json_data_bytes)

                # Отправляем длину JSON данных клиенту
                conn.send(struct.pack('I', json_data_length))

                # Отправляем JSON данные клиенту фрагментами
                sent = 0
                while sent < json_data_length:
                    remaining = json_data_length - sent
                    send_size = min(4096, remaining)
                    sent += conn.send(json_data_bytes[sent:sent + send_size])

        # Обработка команды 'q'
        elif command == 'q':
            break 

    conn.close()

if __name__ == "__main__":
    main()

