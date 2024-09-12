#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import requests
import json
from OllamaUp import start_ollama_server

# df = pd.read_csv('sample.csv', dialect='excel', keep_default_na=False, dtype=str)

name_colum = ['Elemento grande y fuerte']
#df = pd.read_csv('pruebas_de_jugueteA.csv', dialect='excel', keep_default_na=False, dtype=str, encoding='utf-8', delimiter=',', names = name_colum, header=None)
# funciona


df = pd.read_csv('pb_inmobiliario.csv', dialect='excel', keep_default_na=False, dtype=str, encoding='utf-8', delimiter=',', names=name_colum, header=None)


def interact_with_ollama(model_name, prompt):

    headers = {
        "Content-Type": "application/json",
        "Accept-Language": "es"
    }

    data = {
        "model": model_name,
        "prompt": prompt
    }

    try:
        OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"
        
        response = requests.post( OLLAMA_API_URL, headers=headers, json=data, stream=False)
        
        if response.status_code != 200:
            raise Exception(f"Error en la solicitud. Código de estado: {response.status_code}")
        
        final_response = ""  # Variable para almacenar la respuesta final

        for line in response.iter_lines():
            if line:
                try:
                    json_line = json.loads(line.decode('utf-8'))
                    
                    # Imprime el contenido relevante del JSON
                    if 'response' in json_line:
                        print(json_line['response'], end='')
                        final_response += json_line['response']  # Acumula la respuesta

                    if json_line.get('done'):
                        break  # Termina cuando el modelo indica que ha terminado
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar JSON: {e}")

        # Devuelve la respuesta completa al final
        return final_response

    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        raise Exception(f"Error en la solicitud HTTP: {e}")

def main():
    
    columna_elemento = df['Elemento grande y fuerte']

    elementos = []
    for texto in columna_elemento:
        elementos.append(texto)
    
    prompt = "A continuación te proporciono descripciones inmobiliarias detalladas. Necesito que generes variaciones textuales de cada una de las descripciones. Las variaciones deben transmitir la misma información pero con diferentes palabras y estructuras. \n" + "\n".join(elementos)

    model_name = "llama3.1"
     
    server_process = start_ollama_server();
    
    # Mantener el script en ejecución para que el servidor siga funcionando
    if server_process:
        try:
            print("Press Ctrl+C to stop the server.")    
            interact_with_ollama(model_name, prompt)
            server_process.wait()            
        except KeyboardInterrupt:
            print("\nStopping Ollama server...")
            server_process.terminate()
            server_process.wait()
            print("Server stopped.")

      
    
if __name__ == "__main__":
    main()
