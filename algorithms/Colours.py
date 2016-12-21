import requests
import json

def from_colour_lovers(palette):
    return ['#'+i for i in palette]

def get_palettes(num_palettes=20, page=0):
    request=requests.get('http://www.colourlovers.com/api/palettes/top', params={'format':'json', 'numResults':str(num_palettes), 'resultOffset':str(page)})
    loaded=json.loads(request.text)
    return [[palette['title'], from_colour_lovers(palette['colors'])] for palette in loaded]

def get_static_palettes(num_palettes=20):
    with open('algorithms/static_palettes.txt', 'r') as read_file:
        prev_static_palettes = json.load(read_file)
    static_palettes=[]
    for i in prev_static_palettes:
        static_palettes.append([i[0], from_colour_lovers(i[1])])

    if num_palettes>=100: return static_palettes
    else: return static_palettes[:num_palettes]

def get_palettes_safe(num_palettes=20, page=0):
    try:
        palettes = get_palettes(num_palettes, page)
    except:
        palettes = get_static_palettes(num_palettes)
    return palettes
