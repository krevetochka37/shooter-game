import socket
import os
import datetime
import json

def create_directory():
    current_time = datetime.datetime.now()
    folder_name = current_time.strftime("%d-%m-%Y %H-%M-%S")
    os.makedirs(folder_name)
    return folder_name

def save_tree(tree_data, folder_name, tree_number):
    filename = os.path.join(folder_name, f"{tree_number}.json")
    with open(filename, 'w') as f:
        return json.dump(tree_data, f)