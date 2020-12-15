import socket
import pyaudio
import wave
import os


CHUNK = 1024 #number of frames in the buffer
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100 #number of samples collected per second.

p = pyaudio.PyAudio()

print("\nWaiting for Client to connect...")

# function to connect to the client
def client(conn, address):
    print("\nConnected to Client ", address, "")
    while True:

        song = os.listdir("./Songs") #song directory
        ss = "\n\t" "----PLAYLIST----" "\n"
        for i in range(len(song)): #fetch all songs from directory
            song[i] = song[i][:-4] #hide file extension
            ss = ss + "\t" + str(i+1) + " -> " + song[i] + "\n" #display all songs in directory
        conn.send(ss.encode())
        s = conn.recv(1024).decode() #receive selected song from client
        
        for i in song: #check for the presence of the song
            if s.lower() == i.lower(): #compare input from client and song name
                print("Song fetched at Server.. !")
                conn.send("1".encode()) # send 1 to client if found
                s = i
                break
        else:
            conn.send("0".encode()) # send 0 to client if not found
            continue
        
        s = "./Songs/"+s+".wav"
        print("Requested Song Located at :" + s) # display song directory
        wf = wave.open(s, 'rb')
        
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
        stream.start_stream()
        data = 1
        
        while data:
            data = wf.readframes(CHUNK)
            conn.send(data)

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind(("192.168.42.239", 5554))
serversocket.listen(10)

while True:
    conn, address = serversocket.accept()
    client (conn, address) #call client connection function 