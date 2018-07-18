import requests

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

# 
# Sample Usage
# 

# from time import sleep

# # A List of Items
# items = list(range(0, 57))
# l = len(items)




# Os nomes de ruas e CPFs são obtidos via Nominatim, um sistema de busca para OSM
# Veja mais em https://nominatim.openstreetmap.org/ 

path_in = 'input/'
path_out = 'output/'
base_url = 'http://nominatim.openstreetmap.org/reverse.php?format=json&'
base_url_overspeed = 'http://nominatim.openstreetmap.org/api/0.6/way/'
out_filename = path_out + 'enderecos' + '.csv'
in_filename = path_in + 'coordenadas.txt'
header_csv = 'ID' + ';' + 'PAIS' + ';' + 'UF' + ';' + 'CIDADE' + ';' + 'RUA' + ';' + 'CEP' + ';' + 'LOCAL' + ';' + 'CONSOLIDADO'


with open(out_filename, 'w') as output:
    output.write(header_csv)
    
with open(in_filename) as f:
    numero_linhas = sum(1 for _ in f)

i = 0
with open(in_filename) as coordenadas:
    for par_coord in coordenadas:
        id = par_coord.split(',')[0]
        latitude = par_coord.split(',')[1]
        longitude = par_coord.split(',')[2]

        path = base_url + 'lat=' + latitude + '&lon=' + longitude
        resposta = requests.get(path)

        if 'country' in resposta.json()['address']:
            pais = resposta.json()['address']['country']
        else:
            pais = 'País não reconhecido'

        if 'state' in resposta.json()['address']:
            estado = resposta.json()['address']['state']
        else:
            estado = 'Estado não reconhecido'

        if 'city' in resposta.json()['address']:
            cidade = resposta.json()['address']['city']
        else:
            'Cidade não reconhecida'

        
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
        printProgressBar(i + 1, numero_linhas, prefix = 'Progress:', suffix = 'Complete', length = 100)
        

        line_write = id + ';' + pais + ';' + estado + ';' + cidade + ';' + rua + ';' + cep + ';' + local + ';' + consolidado

        with open(out_filename, 'a') as output:
            output.write('\n' + line_write)
            
# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     sleep(0.1)
#     # Update Progress Bar
    # printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)