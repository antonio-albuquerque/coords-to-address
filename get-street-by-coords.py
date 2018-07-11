import requests

# Os nomes de ruas e CPFs são obtidos via Nominatim, um sistema de busca para OSM
# Veja mais em https://nominatim.openstreetmap.org/ 

path_in = 'input/'
path_out = 'output/'
base_url = 'http://nominatim.openstreetmap.org/reverse.php?format=json&'
out_filename = path_out + 'enderecos' + '.csv'
in_filename = path_in + 'coordenadas.txt'
header_csv = 'PAIS' + ';' + 'UF' + ';' + 'CIDADE' + ';' + 'RUA' + ';' + 'CEP'


with open(out_filename, 'w') as output:
    output.write(header_csv)

with open(in_filename) as coordenadas:
    for par_coord in coordenadas:
        latitude = par_coord.split(',')[0]
        longitude = par_coord.split(',')[1]

        path = base_url + 'lat=' + latitude + '&lon=' + longitude
        resposta = requests.get(path)

        if 'country' in resposta.json()['address']:
            pais = resposta.json()['address']['country']

        if 'state' in resposta.json()['address']:
            estado = resposta.json()['address']['state']

        if 'city' in resposta.json()['address']:
            cidade = resposta.json()['address']['city']

        
        if 'road' in resposta.json()['address']:
            rua = resposta.json()['address']['road']
        else:
            rua = 'Rua não encontrada'
        if 'postcode' in resposta.json()['address']:
            cep = resposta.json()['address']['postcode']
        else:
            cep = 'CEP não encontrado'

        line_write = pais + ';' + estado + ';' + cidade + ';' + rua + ';' + cep

        with open(out_filename, 'a') as output:
            output.write('\n' + line_write)
            
