import os
import csv
import base64
import json


def new_row_format(bio='bio', img1='img1', img2='img2', img3='img3', img4='img4', img5='img5'):
    return {"bio": bio, "img1": img1, "img2": img2, "img3": img3, "img4": img4, "img5": img5}

def write_bio(new_row = {"bio": "bio", "img1": "img1", "img2": "img2", "img3": "img3",  "img4": "img4", "img5": "img5"}):
    # Define the file path for the CSV
    file_path = "bio.csv"

    # Define the headers and a sample row to add
    headers = ["id", "bio", "img1", "img2", "img3",  "img4", "img5"]

    # Ensure the CSV file exists or create it with headers
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()  # Write headers if creating a new file
        print(f"File '{file_path}' created with headers.")

    # Load the existing data (if any) and append the new row
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)  # Load existing rows into memory
        row_count = len(data)

    # Append the new row
    data.append({**new_row, "id": row_count + 1})

    # Save the updated data back to the CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write headers first
        writer.writerows(data)  # Write all rows (including the new one)

    print(f"Row added to '{file_path}': {new_row}")
    return {**new_row, "id": row_count + 1}


def write_img(obj, name, idx):
    json_obj = json.loads(obj)
    # File name to save the image
    file_name = f"./client/vue-project/public/img/{name}_{idx}.png"

    # Decode the Base64 string to bytes
    image_data = base64.b64decode(json_obj['image'])

    # Write the image bytes to a file
    with open(file_name, "wb") as image_file:
        image_file.write(image_data)

    print(f"Image saved as {file_name}")
    return f'./img/{name}_{idx}.png'


def write_chat(new_row = {"id": 0, "isUser": True, "msg": "msg", "time": "time"}):
    # Define the file path for the CSV
    file_path = "chat.csv"

    # Define the headers and a sample row to add
    headers = ["id", "isUser", "msg", "time"]

    # Ensure the CSV file exists or create it with headers
    if not os.path.exists(file_path):
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()  # Write headers if creating a new file
        print(f"File '{file_path}' created with headers.")

    # Load the existing data (if any) and append the new row
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = list(reader)  # Load existing rows into memory

    # Append the new row
    data.append(new_row)

    # Save the updated data back to the CSV file
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Write headers first
        writer.writerows(data)  # Write all rows (including the new one)

    print(f"Row added to '{file_path}': {new_row}")

