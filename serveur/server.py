import tkinter as tk
import socket
import threading

# Liste des clients connectés
clients_connectes = []

# Fonction pour gérer les messages d'un client
def gerer_client(client_socket, client_address):
    def recevoir_messages():
        while True:
            message = client_socket.recv(1024)
            if not message:
                # Si le client se déconnecte
                zone_messages.config(state=tk.NORMAL)
                zone_messages.insert(tk.END, f"Client {client_address} déconnecté.\n")
                zone_messages.config(state=tk.DISABLED)
                clients_connectes.remove(client_socket)
                break
            # Afficher le message reçu du client
            zone_messages.config(state=tk.NORMAL)
            zone_messages.insert(tk.END, f"Client {client_address}: {message.decode()}\n")
            zone_messages.config(state=tk.DISABLED)

            # Envoyer le message à tous les autres clients
            for client in clients_connectes:
                if client != client_socket:
                    client.sendall(message)

    # Thread pour gérer la réception des messages
    thread_reception = threading.Thread(target=recevoir_messages)
    thread_reception.start()

# Fonction pour envoyer un message à tous les clients
def envoyer_message():
    message = entree_message.get()
    if message:
        zone_messages.config(state=tk.NORMAL)
        zone_messages.insert(tk.END, f"Vous (Serveur): {message}\n")
        zone_messages.config(state=tk.DISABLED)
        entree_message.delete(0, tk.END)

        # Envoyer le message à tous les clients connectés
        for client_socket in clients_connectes:
            client_socket.sendall(message.encode())

# Fonction pour accepter les connexions des clients
def attendre_connexions():
    while True:
        client_socket, client_address = server_socket.accept()
        clients_connectes.append(client_socket)
        zone_messages.config(state=tk.NORMAL)
        zone_messages.insert(tk.END, f"Nouveau client connecté: {client_address}\n")
        zone_messages.config(state=tk.DISABLED)

        # Lancer un thread pour gérer ce client
        gerer_client(client_socket, client_address)

# Configuration du serveur
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 63000))
server_socket.listen(5)

# Création de l'interface serveur
fenetre = tk.Tk()
fenetre.title("Chat Serveur")

# Zone de messages
zone_messages = tk.Text(fenetre, height=20, width=50)
zone_messages.pack(pady=10)
zone_messages.config(state=tk.DISABLED)

# Zone d'entrée de message
entree_message = tk.Entry(fenetre, width=40)
entree_message.pack(side=tk.LEFT, padx=10)

# Bouton pour envoyer un message
bouton_envoyer = tk.Button(fenetre, text="Envoyer", command=envoyer_message)
bouton_envoyer.pack(side=tk.LEFT)

# Thread pour accepter les connexions des clients
thread_connexions = threading.Thread(target=attendre_connexions, daemon=True)
thread_connexions.start()

# Lancer la boucle principale tkinter
fenetre.mainloop()

# Fermer le socket serveur lors de la fermeture de l'application
server_socket.close()
