import csv
import os

folder_path = 'data/'


def new_csv_from_net(file_txt, file_csv):
    with open(file_txt, 'r') as file:
        lines = file.readlines()

    new_lines = [' '.join(line.split()) + '\n' for line in lines]

    with open(file_txt, 'w') as new_file:
        new_file.writelines(new_lines)

    with open(file_txt, 'r') as file:
        lines = file.readlines()

    data = [list(map(float, line.strip().split())) for line in lines]

    with open(file_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)

    print(f'Plik CSV został utworzony: {file_csv}')


def loop_for_convert():
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            input_path = os.path.join(folder_path, filename)
            output_csv_name = f"{os.path.splitext(filename)[0]}.csv"
            output_path = os.path.join(folder_path, output_csv_name)
            new_csv_from_net(input_path, output_path)


def load_from_csv(file_csv):
    data_array = []

    with open(os.path.join(folder_path, file_csv), 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            row = list(map(float, row))
            data_array.append(row)

    return data_array
