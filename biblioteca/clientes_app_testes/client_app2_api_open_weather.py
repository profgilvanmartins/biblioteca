'''
Simulando código de aplicativo cliente utilizando API externa (open weather)
'''
import requests

BASE_URL = "http://localhost:8000"

# Fazendo uma solicitação GET para uma API pública 
# de previsão do tempo (https://openweathermap.org/) através de uma função criada
# chamada de get_temperatura que recebe como parâmetro o nome da cidade
# Substitua o conteúdo da variável api_key pela chave gerada na plataforma (faça o cadastro gratuito)

def get_temperatura(city):
  api_key = "sua chave gerada na plataforma openweather"
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
  
  response = requests.get(url)
  if response.status_code == 200:
      data = response.json()
      temperatura = data['main']['temp']
      return temperatura - 273.15 # Converte Kelvin para Celsius
  else:
      return None


# Exemplo de uso
if __name__ == "__main__":
    cidade = "Salvador, BR" 
    temperatura = get_temperatura(cidade)
    if temperatura:
        print(f"A temperatura em {cidade} é de {temperatura:.2f} graus Celsius.")
    else:
        print("Não foi possível obter a temperatura.")

 