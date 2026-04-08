import json

from pathlib import Path



import requests



API_URL = "http://127.0.0.1:8004/characters/"

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "data" / "characters.json"





def load_characters():

    with open(DATA_FILE, "r", encoding="utf-8") as file:

        return json.load(file)





def get_existing_characters():

    response = requests.get(API_URL)

    response.raise_for_status()

    return response.json()





def seed_characters():

    characters = load_characters()

    existing_characters = get_existing_characters()



    existing_by_name = {character["name"]: character for character in existing_characters}



    for character in characters:

        existing_character = existing_by_name.get(character["name"])



        if existing_character:

            character_id = existing_character["id"]

            update_url = f"{API_URL}{character_id}"



            response = requests.put(update_url, json=character)



            if response.status_code == 200:

                print(f"Updated: {character['name']}")

            else:

                print(f"Failed to update {character['name']}")

                print(response.text)

        else:

            response = requests.post(API_URL, json=character)



            if response.status_code == 201:

                print(f"Added: {character['name']}")

            else:

                print(f"Failed to add {character['name']}")

                print(response.text)





if __name__ == "__main__":

    seed_characters()