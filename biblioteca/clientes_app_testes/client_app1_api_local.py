'''
Simulando código de aplicativo cliente utilizando API interna
'''
import requests

BASE_URL = "http://localhost:8000"

def cadastrar_autor(nome, data_nasc):
    url = f"{BASE_URL}/autores/"
    dados = {
        "nome": nome,
        "data_nascimento": data_nasc
    }
    
    response = requests.post(url, json=dados)
    
    if response.status_code == 201:
        print(f"Autor {nome} cadastrado com sucesso!")
        return response.json()
    else:
        print(f"Erro ao cadastrar: {response.status_code}")
        print(response.json())

def listar_livros():
    url = f"{BASE_URL}/livros/"
    response = requests.get(url)
    
    if response.status_code == 200:
        livros = response.json()
        print(f"\n--- Lista de Livros (Total: {len(livros)}) ---")
        for livro in livros:
            print(f"ID: {livro['id']} | Título: {livro['titulo']}")
    else:
        print("Não foi possível obter a lista de livros.")

# Executando o "App"
if __name__ == "__main__":
    # 1. Tenta cadastrar um autor
    cadastrar_autor("Jhon Newton", "1960-02-22")
    # 2. Lista os livros
    listar_livros()
