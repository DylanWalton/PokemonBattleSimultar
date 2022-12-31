from tkinter import *
import customtkinter
from PIL import Image
import socket
import threading
from random import randint
import c_pokemon
import c_dresseur

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

assetsLoc = "..\\PokemonBattleSimulator\\Assets\\"
dataLoc = "..\\PokemonBattleSimulator\\Data\\"
pokImagesLoc = "..\\PokemonBattleSimulator\\PokemonData\\Images\\"
pokMetaLoc = "..\\PokemonBattleSimulator\\PokemonData\\Meta\\"

window = customtkinter.CTk()
window.geometry("700x500")
window.title("Pokemon Battle Simulator")
icon = PhotoImage(file=f"{assetsLoc}icon3.png")
window.iconphoto(True, icon)
window.resizable(False, False)

tabView = customtkinter.CTkTabview(master=window, width=window._current_width-20, height=window._current_height-15)
tabView.pack(padx=1, pady=1)
tab_Game = tabView.add("Game")
tab_Settings = tabView.add("Settings")

m_masterGameTab = tab_Game
m_masterSettingsTab = tab_Settings
                                                                            
#region MainTab
#region Images 
background = customtkinter.CTkImage(light_image=Image.open(f"{assetsLoc}MainBackground.png"),
                                    size=(450,170))
bg = customtkinter.CTkButton(master=m_masterGameTab, 
                             text="",
                             image=background,
                             width=500,
                             height=200,
                             fg_color="#222222",
                             hover=False)
bg.place(relx=.5, rely=.4, anchor=CENTER)
#endregion

#region Commands(Functions)
def play() :
    #load()

    try :
        client_connect(str(ip), int(port))
        receive_Process.start()
    except ValueError as v :
        errorPopUp("Double check the IP and Port")
        #loadFailed()
    except ConnectionRefusedError as c :
        if c.winerror != 1 :
            errorPopUp("The attempted server is likely down")
            #loadFailed()
    except OSError as e:
        if e.winerror != 1 :
            errorPopUp("Double check the IP and Port")
            #loadFailed()

def settings() :
    tabView.set("Settings")

def quit() :
    #try :
    #    client.send(f"!left:{username}".encode(FORMAT))
    #    client.close()
    #except :
    #    exit()
    exit()
#endregion

#region Labels
label_Title = customtkinter.CTkLabel(master=m_masterGameTab, 
                                     text="Pokemon Battle Simulator", 
                                     text_color="white", 
                                     font=("Roboto", 24))
label_Title.place(relx=.5, rely=.1, anchor=CENTER)
#endregion

#region Buttons
m_height = 34
m_width = 174
m_fontSize = 17

button_Play = customtkinter.CTkButton(master=m_masterGameTab, 
                                      text="Play",
                                      command=play,
                                      width=m_width,
                                      height=m_height,
                                      font=(None, m_fontSize))

button_Settings = customtkinter.CTkButton(master=m_masterGameTab, 
                                         text="Settings",
                                         command=settings,
                                         width=m_width,
                                         height=m_height,
                                         font=(None, m_fontSize))

button_Quit = customtkinter.CTkButton(master=m_masterGameTab, 
                                      text="Quit",
                                      command=quit,
                                      width=m_width,
                                      height=m_height,
                                      font=(None, m_fontSize))

button_Play.place(relx=.5, rely=.65, anchor=CENTER)
button_Settings.place(relx=.5, rely=.74, anchor=CENTER)
button_Quit.place(relx=.5, rely=.83, anchor=CENTER)
#endregion
#endregion

#region SettingsTab

shouldSavePresets = False
savePresetsToggleValue = 0
ip, port = "", 0
username = ""
with open(f"{dataLoc}username.txt", "r") as file :
    username = file.read()

with open(f"{dataLoc}presets.txt", "r") as file :
    m_savePresets = file.readlines()
for i, ligne in enumerate(m_savePresets) :
    m_savePresets[i] = m_savePresets[i][:-1]
for i, ligne in enumerate(m_savePresets) :
    m_savePresets[i] = m_savePresets[i].split(",")
displaySavePresets = []
for i in range(len(m_savePresets)) :
    displaySavePresets.append(m_savePresets[i][0])

#region Commands(Functions)
def set_username() :
    global username

    if len(entry_Username.get()) <= 20 :
        username = entry_Username.get()
        with open (f"{dataLoc}username.txt", "w") as file :
            file.write(username)
        print(entry_Username.get())
    else :
        entry_Username.delete(0, len(entry_Username.get()))
        entry_Username.configure(placeholder_text="Limit Exceeded!", placeholder_text_color="red")

def set_PortIP() :
    global ip, port, m_savePresets

    ip = entry_IP.get()
    port = entry_Port.get()

    if shouldSavePresets and (ip != "" and port != "") :
        m_name = entry_ServerName.get()
        data = [m_name, ip, port]
        with open(f"{dataLoc}presets.txt", "a") as file :
            file.write(m_name+","+ip+","+port+"\n")
        m_savePresets.append(data)
        displaySavePresets.append(data[0])
        optionMenu_LoadPresets.configure(values=displaySavePresets)

def save_Presets() :
    global savePresetsToggleValue, shouldSavePresets

    if savePresetsToggleValue == 1 :
        radioButton_SavePresets.deselect()
        savePresetsToggleValue = 0
        shouldSavePresets = False
        entry_ServerName.place(relx=.1, rely=4, anchor=W)
    else : 
        radioButton_SavePresets.select()
        savePresetsToggleValue = 1
        shouldSavePresets = True
        entry_ServerName.place(relx=.1, rely=.86, anchor=W)
    
def activatePreset(value) :
    global ip, port
    
    i = 0
    while displaySavePresets[i] != value :
        i+=1
    if i != 0 :
        entry_IP.delete(0, len(entry_IP.get()))
        entry_Port.delete(0, len(entry_Port.get()))
        entry_IP.insert(0, m_savePresets[i][1])
        entry_Port.insert(0, m_savePresets[i][2])
        entry_IP.configure(text_color="#42f58a")
        entry_Port.configure(text_color="#42f58a")
        ip, port = m_savePresets[i][1], m_savePresets[i][2]
    else :
        entry_IP.delete(0, len(entry_IP.get()))
        entry_Port.delete(0, len(entry_Port.get()))
        entry_IP.configure(placeholder_text="Enter the server IP address (i.e 127.0.0.1)", placeholder_text_color="grey")
        entry_Port.configure(placeholder_text="Enter the server port to connect to (i.e 1234)", placeholder_text_color="grey")
        ip, port = "", 0

def set_ServerName(name : str) :
    print(name)
#endregion

# Username Stuff
label_Username = customtkinter.CTkLabel(master=m_masterSettingsTab,
                                        text="Username",
                                        text_color="white",
                                        font=(None, 21))
label_Username.place(relx=.1, rely=.05, anchor=W)
entry_Username = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                        placeholder_text="Enter your username, 20 characters at the maximum",
                                        width=330)
if username != "" :
    entry_Username.configure(placeholder_text=username)                                        
entry_Username.place(relx=.1, rely=.13, anchor=W)
button_Username = customtkinter.CTkButton(master=m_masterSettingsTab,
                                          text="Set username",
                                          width=50,
                                          height=30,
                                          font=(None, 14),
                                          command=set_username)
button_Username.place(relx=.1, rely=.22, anchor=W)                

# IP and Port Stuff
label_Port = customtkinter.CTkLabel(master=m_masterSettingsTab,
                                    text="Server Port",
                                    font=(None, 21))
label_Port.place(relx=.1, rely=.4, anchor=W)
entry_Port = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                    placeholder_text="Enter the server port to connect to (i.e 1234)",
                                    width=330)
entry_Port.place(relx=.1, rely=.48, anchor=W)

label_IP = customtkinter.CTkLabel(master=m_masterSettingsTab,
                                    text="Server IP Address",
                                    font=(None, 21))
label_IP.place(relx=.1, rely=.59, anchor=W)
entry_IP = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                    placeholder_text="Enter the server IP address (i.e 127.0.0.1)",
                                    width=330)
entry_IP.place(relx=.1, rely=.67, anchor=W)
button_setPortIP = customtkinter.CTkButton(master=m_masterSettingsTab,
                                           text="Set IP and Port",
                                           width=90,
                                           height=30,
                                           font=(None, 14),
                                           command=set_PortIP)
button_setPortIP.place(relx=.1, rely=.76, anchor=W)
entry_ServerName = customtkinter.CTkEntry(master=m_masterSettingsTab,
                                          placeholder_text="Server Name",
                                          width=240)
# Save Presets Stuff
radioButton_SavePresets = customtkinter.CTkRadioButton(master=m_masterSettingsTab,
                                                       text="Save Presets",
                                                       font=(None, 14), 
                                                       value=savePresetsToggleValue,
                                                       command=save_Presets)
radioButton_SavePresets.place(relx=.3, rely=.76, anchor=W)

optionMenu_LoadPresets = customtkinter.CTkOptionMenu(master=m_masterSettingsTab,
                                                     values=displaySavePresets,
                                                     command=activatePreset)                                                     
optionMenu_LoadPresets.place(relx=.3, rely=.4, anchor=W)
#endregion

#region LoadingFrame
#frame_LoadingFrame = customtkinter.CTkFrame(master=window,
#                                            width=window._current_width-20, 
#                                            height=window._current_height-20)
#progressBar_LoadingBar = customtkinter.CTkProgressBar(master=frame_LoadingFrame,
#                                                        width=300,
#                                                        height=15,
#                                                        progress_color="yellow",
#                                                        mode="indeterminate",
#                                                        indeterminate_speed=1)

#def load() :
#    tabView.place(relx=10)
#    frame_LoadingFrame.place(relx=.5, rely=.5, anchor=CENTER)   
#
#    label_Loading = customtkinter.CTkLabel(master=frame_LoadingFrame,
#                                        text="Loading",
#                                        text_color="white",
#                                        font=(None, 31))
#    label_Loading.place(relx=.5, rely=.4, anchor=CENTER)
#    progressBar_LoadingBar.place(relx=.5, rely=.5, anchor=CENTER)
#    progressBar_LoadingBar.start()

#def loadFailed() :
#    tabView.place(relx=.5, rely=.488, anchor=CENTER)
#    frame_LoadingFrame.place(relx=20)
#    progressBar_LoadingBar.stop()
#endregion

#region Error Notifier
label_ErrorNotifier = customtkinter.CTkLabel(master=window,
                                             text_color="red",
                                             font=(None, 17))

image_IgnoreError = customtkinter.CTkImage(light_image=Image.open(f"{assetsLoc}YellowDot.png"),
                                    size=(20,20))

def ignorePopUp() :
    label_ErrorNotifier.place(relx=.17, rely=5, anchor=S)
    button_IgnoreError.place(relx=.353, rely=5, anchor=S)

button_IgnoreError = customtkinter.CTkButton(master=window,
                                             image=image_IgnoreError,
                                             width=28,
                                             height=28,
                                             command=ignorePopUp,
                                             text="",
                                             fg_color="#1A1A1A")

def errorPopUp(error : str) :
    label_ErrorNotifier.configure(text=error)
    if len(error) < 31 :
        label_ErrorNotifier.place(relx=.17, rely=.99, anchor=S)
        button_IgnoreError.place(relx=.353, rely=.99, anchor=S)
    else :
        label_ErrorNotifier.place(relx=.2, rely=.99, anchor=S)
        button_IgnoreError.place(relx=.415, rely=.99, anchor=S)
#endregion

#region Client
client = None
connected = False
FORMAT = "utf-8"
players = []

def client_connect(ip : str, port : int) :
    global client
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))
    lobby()

def client_receive() :
    while True :
        try :
            message = client.recv(1024).decode(FORMAT)
            print(message)
            if message == "alias?" :
                client.send(username.encode(FORMAT))
            elif "!" in message :
                if "!players:" in message :
                    global players
                    client.send(" ".encode(FORMAT))
                    message = message.replace("!players:", "")
                    message = message.replace("[", "")
                    message = message.replace("]", "")
                    message = message.replace("b'", "")
                    message = message[:-1]
                    message = message.split(",")
                    players = message
                    i = 0
                    for player in players :
                        player = player.replace(" ", "")
                        player = player.replace("'", "")
                        players[i] = player
                        i += 1
                    players.remove(username)
                    displayPlayers()
                elif "!invite:" in message :
                    message = message.replace("!invite:", "")
                    message = message.split(",")
                    print(message)
                    if message[0] == username :
                        recvInvite(message[1])
                elif "!inviteaccepted:" in message :
                    message = message.replace("!inviteaccepted:", "")
                    #message = message.split(",")
                    print(message)
                    if message == chosenPlayer :
                        battle()
                elif "!left:" in message :
                    message = message.replace("!left:", "")
                    message = message.replace("b'", "")
                    message = message[:-1]
                    print(message)
                    print(players)
                    global poppedPlayer
                    poppedPlayer = players.index(message)
                    print(poppedPlayer)
                    players.remove(message)
                    print(players)
                    displayPlayers()
                elif "!ready:" in message :
                    global opponentIsReady
                    message = message.replace("!ready:", "")
                    message = message.replace("b'", "")
                    message = message.split(",")
                    print(message)
                    if message[1] == chosenPlayer :
                        goToBattle()
            else :
                print(message)
                textbox_Chat.insert("0.0", message+"\n\n")
        except :
            print("Error!")
            client.close()
            break

def client_send() :
    if entry_Chat.get() != "" :
        message = f"{username}  >>  {entry_Chat.get()}"
        client.send(message.encode(FORMAT))
        entry_Chat.delete(0, len(entry_Chat.get()))
#endregion

#region Lobby
frame_LobbyFrame = customtkinter.CTkFrame(master=window,
                                              width=window._current_width-20, 
                                              height=window._current_height-20)
entry_Chat = customtkinter.CTkEntry(master=frame_LobbyFrame, placeholder_text="Message everyone", width=593, height=30)
colours = ["red", "blue", "green", "yellow", "orange", "pink", "white", "purple"]
#colours[randint(0, len(colours)-1)]
textbox_Chat = customtkinter.CTkTextbox(master=frame_LobbyFrame, width=290, height=370, border_color="black", border_width=1, text_color="orange")
frame_Players = customtkinter.CTkFrame(master=frame_LobbyFrame, width=210, height=370, fg_color="#1A1A1A", border_color="black", border_width=1)

def lobby() :
    tabView.place(relx=10)
    frame_LobbyFrame.place(relx=.5, rely=.5, anchor=CENTER)

    label_ServerTitle = customtkinter.CTkLabel(master=frame_LobbyFrame,
                                               text=optionMenu_LoadPresets.get(),
                                               font=(None, 27),
                                               text_color="#229fe7")
    label_ServerTitle.place(relx=.42, rely=0.05, anchor=CENTER)

    label_Players = customtkinter.CTkLabel(master=frame_LobbyFrame, text="Players", font=(None, 20))
    label_Players.place(relx=.545, rely=.126, anchor=W)
    frame_Players.place(relx=.436, rely=.54, anchor=W)
    button_Battle = customtkinter.CTkButton(master=frame_LobbyFrame, text="Battle", font=(None, 18), fg_color="green", width=160, height=30, text_color="white", command=requestBattle)
    button_Battle.place(relx=.873, rely=.27, anchor=CENTER)
    button_Back = customtkinter.CTkButton(master=frame_LobbyFrame, text="Back", font=(None, 18), fg_color="#ef9c06", width=160, height=30, text_color="white", command=backToMain)
    button_Back.place(relx=.873, rely=.34, anchor=CENTER)
    button_QuitLobby = customtkinter.CTkButton(master=frame_LobbyFrame, text="Quit", font=(None, 18), fg_color="#af0400", width=160, height=30, text_color="white", command=quit)
    button_QuitLobby.place(relx=.873, rely=.41, anchor=CENTER)

    entry_Chat.place(relx=0, rely=.97, anchor=W)
    image_SendArrow = customtkinter.CTkImage(light_image=Image.open(f"{assetsLoc}SendArrow2.png"),
                                    size=(34,23))
    button_SendChat = customtkinter.CTkButton(master=frame_LobbyFrame, fg_color="#229fe7", image=image_SendArrow, width=85, height=30, text="", command=client_send)
    button_SendChat.place(relx=.875, rely=.97, anchor=W)

    label_Chat = customtkinter.CTkLabel(master=frame_LobbyFrame, text="Chat", font=(None, 20))
    label_Chat.place(relx=.18, rely=.126, anchor=W)
    textbox_Chat.place(relx=0, rely=.54, anchor=W)

playerLabels = []
chosenPlayer = None
optionMenu_Players = None
poppedPlayer = None

def displayPlayers() :
    global players, playerLabels, optionMenu_Players
    values = ["Players"]
    j = 0
    for label in playerLabels :
        label.destroy()
        playerLabels.pop(j)
        j += 1

    i = 0
    n = .04
    distanceBetweenButtons = .07

    for player in players :      
        values.append(player)
        playerLabels.append(None)
        playerLabels[i] = customtkinter.CTkLabel(master=frame_Players, text=player, width=180, height=25, font=(None, 17))
        #, corner_radius=0, fg_color="#121212"
        playerLabels[i].place(relx=.5, rely=n, anchor=CENTER)
        i += 1
        n += distanceBetweenButtons
    print(players)

    optionMenu_Players = customtkinter.CTkOptionMenu(master=frame_LobbyFrame, values=values, command=playerChosen, width=160)
    optionMenu_Players.place(relx=.873, rely=.19, anchor=CENTER)

def playerChosen(text) :
    global chosenPlayer
    chosenPlayer = text
    print(text)

inviteDenied = True
inviterName = None

def requestBattle() :
    # send invite to chosen player
    if inviteDenied :
        client.send(f"!invite:{chosenPlayer},{username}".encode(FORMAT))
        textbox_Chat.insert("0.0", f"Invite sent to {chosenPlayer}\n")
    elif optionMenu_Players.get() == inviterName :
        client.send(f"!inviteaccepted:{username}".encode(FORMAT))
        battle()

def backToMain() :
    global client
    client.close()
    frame_LobbyFrame.place(relx=10)
    tabView.place(relx=.5, rely=.488, anchor=CENTER)

def recvInvite(inviter : str) :
    global inviterName, inviteDenied
    for label in playerLabels :
        if label.cget("text") == inviter :
            label.configure(text=label.cget("text")+" wants to battle!", text_color="yellow")
            inviterName = inviter
            inviteDenied = False
            break
#endregion

#region Battle

#region Pokemon
with open(f"{pokMetaLoc}pokemonMetaData.txt", "r") as file :
    pokemon = file.readlines()
for i in range(len(pokemon)) :
    pokemon[i] = pokemon[i].replace("\n", "")
for i in range(len(pokemon)) :
    pokemon[i] = pokemon[i].split(",")

pikachu = c_pokemon.Pokemon(pokemon[0][0], int(pokemon[0][1]), int(pokemon[0][2]), int(pokemon[0][3]), int(pokemon[0][4]))
charizard = c_pokemon.Pokemon(pokemon[1][0], int(pokemon[1][1]), int(pokemon[1][2]), int(pokemon[1][3]), int(pokemon[1][4]))
lucario = c_pokemon.Pokemon(pokemon[2][0], int(pokemon[2][1]), int(pokemon[2][2]), int(pokemon[2][3]), int(pokemon[2][4]))
mewtwo = c_pokemon.Pokemon(pokemon[3][0], int(pokemon[3][1]), int(pokemon[3][2]), int(pokemon[3][3]), int(pokemon[3][4]))
suicune = c_pokemon.Pokemon(pokemon[4][0], int(pokemon[4][1]), int(pokemon[4][2]), int(pokemon[4][3]), int(pokemon[4][4]))
rayquaza = c_pokemon.Pokemon(pokemon[5][0], int(pokemon[5][1]), int(pokemon[5][2]), int(pokemon[5][3]), int(pokemon[5][4]))
#endregion

frame_PokemonChoice = customtkinter.CTkFrame(master=window, width=window._current_width-20, height=window._current_height-20)

image_Pikachu = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Pikachu.png"), size=(270,250))
image_Charizard = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Charizard.png"), size=(300,230))
image_Lucario = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Lucario.png"), size=(160, 280))
image_Mewtwo = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Mewtwo.png"), size=(250, 280))
image_Suicune = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Suicune.png"), size=(290, 260))
image_Rayquaza = customtkinter.CTkImage(Image.open(f"{pokImagesLoc}Rayquaza.png"), size=(250, 280))

button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, text="", image=image_Pikachu, width=430, height=400, fg_color="#222222", hover=False)
label_Name = customtkinter.CTkLabel(master=frame_PokemonChoice, text=pikachu.get_nom(), font=(None, 25))
label_Pv = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Pv : "+str(pikachu.get_pv()), font=(None, 23))
label_Attaque = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Attaque : "+str(pikachu.get_attaque()), font=(None, 23))
label_Defense = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Defense : "+str(pikachu.get_defense()), font=(None, 23))
label_Level = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Level : "+str(pikachu.get_niveau())+" / 100", font=(None, 23))

def battle() :
    global pokemon

    frame_LobbyFrame.place(relx=10)

    frame_PokemonChoice.place(relx=.5, rely=.5, anchor=CENTER)
    label_PokemonChoice = customtkinter.CTkLabel(master=frame_PokemonChoice, text="Choose a Pokemon", font=(None, 28))
    label_PokemonChoice.place(relx=.5, rely=.1, anchor=CENTER)

    optionMenu_Pokemon.place(relx=.5, rely=.18, anchor=CENTER)

    button_PokemonImage1.place(relx=.3, rely=.5, anchor=CENTER)
    label_Name.place(relx=.6, rely=.37, anchor=CENTER)
    label_Pv.place(relx=.6, rely=.44, anchor=CENTER)
    label_Attaque.place(relx=.6, rely=.51, anchor=CENTER)
    label_Defense.place(relx=.6, rely=.58, anchor=CENTER)
    label_Level.place(relx=.6, rely=.65, anchor=CENTER)

    button_Choose = customtkinter.CTkButton(master=frame_PokemonChoice, text="Play", font=(None, 23), height=30, width=100, command=waitForOpponent)
    button_Choose.place(relx=.5, rely=.9, anchor=CENTER)
    # choose your pokemon

chosenPokemon = pikachu

def choosePokemon(pokName) :
    # Display the appropriate pokemon info
    global button_PokemonImage1, chosenPokemon
    if pokName == "Pikachu" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=270, height=250, image=image_Pikachu, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.3, rely=.5, anchor=CENTER)
        label_Name.configure(text=pikachu.get_nom())
        label_Pv.configure(text="Pv : "+str(pikachu.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(pikachu.get_attaque()))
        label_Defense.configure(text="Defense : "+str(pikachu.get_defense()))
        label_Level.configure(text="Level : "+str(pikachu.get_niveau())+" / 100")
        chosenPokemon = pikachu
    elif pokName == "Charizard" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=300, height=230, image=image_Charizard, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.26, rely=.5, anchor=CENTER)
        label_Name.configure(text=charizard.get_nom())
        label_Pv.configure(text="Pv : "+str(charizard.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(charizard.get_attaque()))
        label_Defense.configure(text="Defense : "+str(charizard.get_defense()))
        label_Level.configure(text="Level : "+str(charizard.get_niveau())+" / 100")
        chosenPokemon = charizard
    elif pokName == "Lucario" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=150, height=280, image=image_Lucario, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.3, rely=.55, anchor=CENTER)
        label_Name.configure(text=lucario.get_nom())
        label_Pv.configure(text="Pv : "+str(lucario.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(lucario.get_attaque()))
        label_Defense.configure(text="Defense : "+str(lucario.get_defense()))
        label_Level.configure(text="Level : "+str(lucario.get_niveau())+" / 100")
        chosenPokemon = lucario
    elif pokName == "Mewtwo" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=260, height=280, image=image_Mewtwo, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.27, rely=.55, anchor=CENTER)
        label_Name.configure(text=mewtwo.get_nom())
        label_Pv.configure(text="Pv : "+str(mewtwo.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(mewtwo.get_attaque()))
        label_Defense.configure(text="Defense : "+str(mewtwo.get_defense()))
        label_Level.configure(text="Level : "+str(mewtwo.get_niveau())+" / 100")
        chosenPokemon = mewtwo
    elif pokName == "Suicune" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=290, height=260, image=image_Suicune, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.26, rely=.5, anchor=CENTER)
        label_Name.configure(text=suicune.get_nom())
        label_Pv.configure(text="Pv : "+str(suicune.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(suicune.get_attaque()))
        label_Defense.configure(text="Defense : "+str(suicune.get_defense()))
        label_Level.configure(text="Level : "+str(suicune.get_niveau())+" / 100")
        chosenPokemon = suicune
    elif pokName == "Rayquaza" :
        button_PokemonImage1.destroy()
        button_PokemonImage1 = customtkinter.CTkButton(master=frame_PokemonChoice, width=250, height=280, image=image_Rayquaza, text="", fg_color="#222222", hover=False)
        button_PokemonImage1.place(relx=.27, rely=.55, anchor=CENTER)
        label_Name.configure(text=rayquaza.get_nom())
        label_Pv.configure(text="Pv : "+str(rayquaza.get_pv()))
        label_Attaque.configure(text="Attaque : "+str(rayquaza.get_attaque()))
        label_Defense.configure(text="Defense : "+str(rayquaza.get_defense()))
        label_Level.configure(text="Level : "+str(rayquaza.get_niveau())+" / 100")
        chosenPokemon = rayquaza

#region Battle for real

frame_Battle = customtkinter.CTkFrame(master=window, width=window._current_width-20, height=window._current_height-20)

tamer = c_dresseur.Dresseur(username, chosenPokemon)

def goToBattle() :

    label_Loading.destroy()
    progressBar.destroy()

    button_MyPokemon = customtkinter.CTkButton(master=frame_Battle, image=button_PokemonImage1.cget("image"), width=button_PokemonImage1._current_width-20, height=button_PokemonImage1._current_height-20, text="", hover=False, fg_color="#222222")
    button_MyPokemon.place(relx=.26, rely=.6, anchor=CENTER)

    print(f"Your pokemon is {tamer.get_nom_pokemon()}")

label_Loading = customtkinter.CTkLabel(master=frame_Battle, text="Waiting for opponent", text_color="white", font=(None, 31))
progressBar = customtkinter.CTkProgressBar(master=frame_Battle, width=300, height=15, progress_color="yellow", mode="indeterminate", indeterminate_speed=1)

def waitForOpponent() :
    frame_PokemonChoice.place(relx=-10)
    frame_Battle.place(relx=.5, rely=.5, anchor=CENTER)
    label_Loading.place(relx=.5, rely=.4, anchor=CENTER)
    progressBar.place(relx=.5, rely=.5, anchor=CENTER)
    progressBar.start()
    client.send(f"!ready:{tamer.get_nom_pokemon()},{username}".encode(FORMAT))
#endregion

pokemonNames = []
for i in pokemon :
    pokemonNames.append(i[0])
optionMenu_Pokemon = customtkinter.CTkOptionMenu(master=frame_PokemonChoice, values=pokemonNames, command=choosePokemon)
#endregion


#region Threads
receive_Process = threading.Thread(target=client_receive)
receive_Process.daemon = True
#endregion

window.mainloop()
