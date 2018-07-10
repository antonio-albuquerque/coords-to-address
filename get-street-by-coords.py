import requests


# Os nomes de ruas e CPFs são obtidos via Nominatim, um sistema de busca para OSM
# Veja mais em https://nominatim.openstreetmap.org/ 

base_url = 'http://nominatim.openstreetmap.org/reverse.php?format=json&'

print('RUA',';', 'CEP')
with open('coordenadas.txt') as coordenadas:
    for par_coord in coordenadas:
        latitude = par_coord.split(',')[0]
        longitude = par_coord.split(',')[1]

        path = base_url + 'lat=' + latitude + '&lon=' + longitude
        resposta = requests.get(path)
        
        if 'road' in resposta.json()['address']:
            rua = resposta.json()['address']['road']
        else:
            rua = 'Rua não encontrada'
        if 'postcode' in resposta.json()['address']:
            cep = resposta.json()['address']['postcode']
        else:
            cep = 'CEP não encontrado'
        print(rua, ';', cep)
