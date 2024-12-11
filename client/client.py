import tkinter as tk
import socket
import threading

def recevoir_messages():
    while True:
        try:
            message = client_socket.recv(1024)
            if message:
                zone_messages.config(state=tk.NORMAL)  # Permet d'ajouter du texte
                zone_messages.insert(tk.END, f"Serveur: {message.decode()}\n")
                zone_messages.config(state=tk.DISABLED)  # Rendre la zone non modifiable
        except Exception as e:
            print(f"Erreur de réception : {e}")
            break

def envoyer_message():
    message = entree_message.get()
    if message:
        zone_messages.config(state=tk.NORMAL)  # Permet d'ajouter du texte
        zone_messages.insert(tk.END, f"Vous: {message}\n")
        zone_messages.config(state=tk.DISABLED)  # Rendre la zone non modifiable
        client_socket.sendall(message.encode())
        entree_message.delete(0, tk.END)

# Créer le client TCP/IP et se connecter au serveur
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('172.16.15.45', 63000)
client_socket.connect(server_address)

# Créer la fenêtre tkinter
fenetre = tk.Tk()
fenetre.title("Chat Client")

# Zone de messages en mode lecture seule
zone_messages = tk.Text(fenetre, height=20, width=50, state=tk.DISABLED)
zone_messages.pack(pady=10)

# Zone d'entrée de message
entree_message = tk.Entry(fenetre, width=40)
entree_message.pack(side=tk.LEFT, padx=10)

# Bouton pour envoyer un message
bouton_envoyer = tk.Button(fenetre, text="Envoyer", command=envoyer_message)
bouton_envoyer.pack(side=tk.LEFT)

# Démarrer un thread pour recevoir les messages
thread_reception = threading.Thread(target=recevoir_messages, daemon=True)
thread_reception.start()

# Démarrer la boucle principale de tkinter
fenetre.mainloop()

# Fermer la connexion après la fermeture de la fenêtre
client_socket.close()
