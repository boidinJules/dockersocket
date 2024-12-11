import tkinter as tk
import socket
import threading

# Fonction pour gérer les clients
def gerer_client(client_socket, client_address):
    def recevoir_messages():
        while True:
            message = client_socket.recv(1024)
            if not message:
                zone_messages.config(state=tk.NORMAL)  # Autoriser l'édition pour ajouter le message
                zone_messages.insert(tk.END, f"Client : déconnecté.\n")
                zone_messages.config(state=tk.DISABLED)  # Désactiver l'édition après l'ajout
                break
            zone_messages.config(state=tk.NORMAL)  # Autoriser l'édition pour ajouter le message
            zone_messages.insert(tk.END, f"Client : {message.decode()}\n")
            zone_messages.config(state=tk.DISABLED)  # Désactiver l'édition après l'ajout
        client_socket.close()

    # Thread pour gérer la réception des messages du client
    thread_reception = threading.Thread(target=recevoir_messages)
    thread_reception.start()

def envoyer_message():
    message = entree_message.get()
    for client_socket in clients_connectes:
        client_socket.sendall(message.encode())
    zone_messages.config(state=tk.NORMAL)  # Autoriser l'édition pour ajouter le message
    zone_messages.insert(tk.END, f"Vous (serveur): {message}\n")
    zone_messages.config(state=tk.DISABLED)  # Désactiver l'édition après l'ajout
    entree_message.delete(0, tk.END)

def attendre_connexions():
    while True:
        client_socket, client_address = server_socket.accept()
        clients_connectes.append(client_socket)
        zone_messages.config(state=tk.NORMAL)  # Autoriser l'édition pour ajouter le message
        zone_messages.insert(tk.END, f"Nouveau client connecté: {client_address}\n")
        zone_messages.config(state=tk.DISABLED)  # Désactiver l'édition après l'ajout
        gerer_client(client_socket, client_address)

# Configuration du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 63000))
server_socket.listen(5)
clients_connectes = []

# Création de l'interface serveur
fenetre = tk.Tk()
fenetre.title("Chat Serveur")

# Zone de messages
zone_messages = tk.Text(fenetre, height=20, width=50)
zone_messages.pack(pady=10)
zone_messages.config(state=tk.DISABLED)  # Initialement en mode lecture seule

# Zone d'entrée de message
entree_message = tk.Entry(fenetre, width=40)
entree_message.pack(side=tk.LEFT, padx=10)

# Bouton pour envoyer un message
bouton_envoyer = tk.Button(fenetre, text="Envoyer", command=envoyer_message)
bouton_envoyer.pack(side=tk.LEFT)

# Thread pour accepter les connexions des clients
thread_connexions = threading.Thread(target=attendre_connexions, daemon=True)
thread_connexions.start()

# Lancement de la boucle principale tkinter
fenetre.mainloop()

# Fermer le socket serveur lors de la fermeture de l'application
server_socket.close()
