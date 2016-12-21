import requests
import json

def get_palettes(num_palettes=20, page=0):
    request=requests.get('http://www.colourlovers.com/api/palettes/top', params={'format':'json', 'numResults':str(num_palettes), 'resultOffset':str(page)})
    loaded=json.loads(request.text)
    return [[palette['title'], palette['colors']] for palette in loaded]

def get_static_palettes(num_palettes=20):
    with open('static_palettes.txt', 'r') as read_file:
        static_palettes = json.load(read_file)
    if num_palettes>=100: return static_palettes
    else: return static_palettes[:num_palettes]

def get_palettes_safe(num_palettes=20, page=0):
    try:
        palettes = get_palettes(num_palettes, page)
    except:
        palettes = get_static_palettes(num_palettes)
    return palettes
