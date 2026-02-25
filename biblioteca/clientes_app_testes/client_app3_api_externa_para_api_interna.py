'''
Simulando código de aplicativo cliente utilizando API interna e externa
'''
import requests

BASE_URL = "http://localhost:8000"

#Utilizaremos a API do open library (https://openlibrary.org) para alimentar nossa API local

def localizar_autor_na_lista(lista_de_autores, nome_buscado):
    '''
    busca na lista_de_autores pelo nome do autor (nome_buscado)
    '''
    for autor in lista_de_autores:
        if autor['nome'] == nome_buscado:
            return autor
    return None

def buscar_livros_api_externa_adicionar_api_interna(tema):
    print(f"--- Iniciando processamento para o tema: {tema} ---")
    
    # 1. Busca 5 livros na Open Library
    url_externa = f"https://openlibrary.org/search.json?q={tema}&limit=5"
    try:
        res_ext = requests.get(url_externa).json()
    except Exception as e:
        print(f"Erro ao acessar API externa: {e}")
        return

    livros_externos = res_ext.get('docs', [])

    for item in livros_externos:
        titulo = item.get('title')
        
        # 2. Verifica se o livro já existe na API LOCAL (GET)
        # Filtramos pelo título para evitar duplicatas
        res_local = requests.get(f"{BASE_URL}/livros/?search={titulo}")
        if res_local.status_code == 200 and any(l['titulo'] == titulo
            for l in res_local.json()):
                print(f"O livro '{titulo}' já consta na API local. Pulando...")
                continue

        # 3. Identifica e cadastra os autores primeiro
        # Precisamos dos IDs dos autores para o ManyToMany do Livro
        lista_nomes_autores = item.get('author_name', [])
        ids_autores_locais = []

        for nome in lista_nomes_autores:
            # Verifica se autor já existe, se não, cadastra
            res_aut = requests.get(f"{BASE_URL}/autores/?search={nome}").json()
            
            # Tenta achar o autor pelo nome exato na lista retornada
            autor_existente = localizar_autor_na_lista(res_aut, nome)
            
            if autor_existente:
                ids_autores_locais.append(autor_existente['id'])
            else:
                # POST para criar novo autor
                novo_aut = requests.post(f"{BASE_URL}/autores/", json={"nome": nome}).json()
                ids_autores_locais.append(novo_aut['id'])

        # 4. Monta o JSON para o POST do Livro
        json_livro = {
            "titulo": titulo,
            "autores": ids_autores_locais, # Passamos a lista de IDs
            "resumo": f"Importado da Open Library. Edição: {item.get('edition_count')}",
            "data_pub": "2000-01-01" # Simplificado, por enquanto [VER EXERCÍCIO].
        }

        # 5. Faz o POST na API local
        res_post = requests.post(f"{BASE_URL}/livros/", json=json_livro)
        
        if res_post.status_code == 201:
            print(f"Sucesso: '{titulo}' adicionado!")
        else:
            print(f"Erro ao adicionar '{titulo}': {res_post.text}")

if __name__ == "__main__":
    buscar_livros_api_externa_adicionar_api_interna("django")