import json
import urllib.request
import unicodedata

print("1. Baixando malha oficial de municípios do Rio de Janeiro...")
# URL corrigida apontando para o GeoJSON oficial dos municípios do RJ
url = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-33-mun.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
except Exception as e:
    print(f"Erro ao baixar os dados: {e}")
    exit(1)

# Definição estrita das regiões solicitadas
capital = ["Rio de Janeiro"]
grande_niteroi = [
    "Niterói", "São Gonçalo", "Itaboraí", "Maricá", 
    "Tanguá", "Rio Bonito", "Cachoeiras de Macacu"
]
baixada = [
    "Duque de Caxias", "Nova Iguaçu", "São João de Meriti", "Belford Roxo", 
    "Nilópolis", "Mesquita", "Queimados", "Japeri", "Paracambi", 
    "Seropédica", "Itaguaí", "Magé", "Guapimirim"
]

def normalize(s):
    return "".join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower().strip()

capital_norm = [normalize(n) for n in capital]
grande_niteroi_norm = [normalize(n) for n in grande_niteroi]
baixada_norm = [normalize(n) for n in baixada]

print("2. Classificando municípios por região...")
for feature in data['features']:
    # O arquivo geojs-33-mun usa 'name' em vez de 'description'
    name = feature['properties'].get('name', '')
    norm_name = normalize(name)
    
    if norm_name in capital_norm:
        reg = "Capital"
    elif norm_name in grande_niteroi_norm:
        reg = "Grande Niterói"
    elif norm_name in baixada_norm:
        reg = "Baixada Fluminense"
    else:
        reg = "Interior"
        
    # Injeta a propriedade da região no arquivo final
    feature['properties']['regiao_customizada'] = reg

output_file = "regioes_rj.geojson"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSucesso! O arquivo '{output_file}' foi gerado.")