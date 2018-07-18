import requests


# Os nomes de ruas e CPFs são obtidos via Nominatim, um sistema de busca para OSM
# Veja mais em https://nominatim.openstreetmap.org/ 

path_in = 'input/'
path_out = 'output/'
base_url = 'http://nominatim.openstreetmap.org/reverse.php?format=json&'
base_url_overspeed = 'http://nominatim.openstreetmap.org/api/0.6/way/'
out_filename = path_out + 'enderecos' + '.csv'
in_filename = path_in + 'coordenadas.txt'
header_csv = 'PAIS' + ';' + 'UF' + ';' + 'CIDADE' + ';' + 'RUA' + ';' + 'CEP' + ';' + 'LOCAL' + ';' + 'CONSOLIDADO'


with open(out_filename, 'w') as output:
    output.write(header_csv)
    
with open(in_filename) as f:
    numero_linhas = sum(1 for _ in f)

i = 0
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
        
        if 'building' in resposta.json()['address']:
            local = resposta.json()['address']['building']
        else:
            local = 'Local não especificado'

        if 'display_name' in resposta.json():
            consolidado = resposta.json()['display_name']
        else:
            consolidado = 'Não encontrado'
        
        i = i + 1

        print(format(((i / numero_linhas) * 100), '.4f'), '%')
        

        line_write = pais + ';' + estado + ';' + cidade + ';' + rua + ';' + cep + ';' + local + ';' + consolidado

        with open(out_filename, 'a') as output:
            output.write('\n' + line_write)
            
