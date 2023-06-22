import json

def get_credentials(name):
    with open('credentials.json', 'rb') as file:
        data = json.load(file)

        if name.lower() not in data.keys():
            raise Exception(f'Credentials name "{name}" not found in credentials.')
        
        return data[name]
