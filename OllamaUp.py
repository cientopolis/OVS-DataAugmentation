#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import time

def start_ollama_server(port=8080):
    try:
        command = ["ollama", "run","llama3.1", "8080"]
        
        # Ejecuta el comando en segundo plano
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"Starting Ollama server on port {port}...")
        
        # Permite que el servidor se inicie
        time.sleep(5)
        
        # Comprobación simple de si el servidor está corriendo
        if process.poll() is None:
            print("Ollama server is running.")
            return process
        else:
            print("Failed to start Ollama server.")
            print("Error:", process.stderr.read())
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

