from .utils import credentials
from sqlalchemy import create_engine

def get_engine():
    db = credentials.get_credentials('db')
    return create_engine(f"mysql+pymysql://{db['user']}:{db['pass']}@localhost:3306/Pictures")

def get_images(min_date, max_date, tags):
    with get_engine().begin() as conn:
        query = f"SELECT p.id, p.path, p.date, t.tag, t.confidence FROM pictures as p LEFT JOIN tags as t ON p.id = t.picture_id WHERE tag IN ({str(tags).replace('[','').replace(']', '')})"
        if min_date:
            query += f' AND date > "{min_date}"'
        
        if max_date:
            query += f' AND date < "{max_date}"'

        data = conn.execute(query)

        grouped_data = {}
        for item in data:
            print(item)
            key = item[:3]
            subkey = item[3]
            value = item[4]
            
            if key in grouped_data:
                grouped_data[key].append((subkey, value))
            else:
                grouped_data[key] = [(subkey, value)]

        result = []
        for key, values in grouped_data.items():
            formatted_datetime = key[2].strftime("%Y-%m-%d %H:%M:%S")
            category_list = [{subkey: value} for subkey, value in values]
            result.append((key[0], key[1], formatted_datetime, category_list))

        return result

def save_image(image_id, path, date, tags):
    with get_engine().begin() as conn:
        conn.execute(f"INSERT INTO pictures VALUES('{image_id}', '{path}', '{date}')")

        for tag in tags:
            conn.execute(f"INSERT INTO tags VALUES ('{tag['tag']}', '{image_id}', '{tag['confidence']}', '{date}')")

def get_image(image_id):
    with get_engine().begin() as conn:
        query = f"SELECT p.id, p.path, p.date, t.tag, t.confidence FROM pictures as p LEFT JOIN tags as t ON p.id = t.picture_id WHERE p.id = '{image_id}'"

        data = conn.execute(query)

        result = {}
        result['id'] = None
        result['date'] = None
        result['tags'] = []

        for item in data:
            if not result['id']:
                result['id'] = item[0]
                result['path'] = item[1]
                result['date'] = item[2].strftime("%Y-%m-%d %H:%M:%S")
            
            if item[3] is not None:
                result['tags'].append({item[3]: item[4]})

        return result

    