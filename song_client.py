import socket
import pyaudio
import wave
import sys

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
clientsocket.connect(("192.168.42.239", 5554)) #connect to the server

p = pyaudio.PyAudio()

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                frames_per_buffer=CHUNK)
while True:
    res = clientsocket.recv(1024).decode() #receive song list from server
    print(res)
    print("\n")

    x = input("Enter song name : ")
    clientsocket.send(x.encode()) #send song name to server
    ch = int(clientsocket.recv(1024).decode()) #receive present or not response from server 
    if ch == 0:
        print("Enter the song name as displayed in the playlist")
        continue
    if ch == 1:
        print("\nCurrently Playing : ", x, " ")
        data = "1"
        
        while data != "":
            try:
                data = clientsocket.recv(1024)
                stream.write(data)
            
            except KeyboardInterrupt:
                print("Streaming Paused...") 
                stream.stop_stream() #pause playback
                response = input("Press \nR to Resume  \nE to Exit : ")
                if response.upper() == "R":
                    print("Resuming Song...")
                    print("\nCurrently Playing : ", x, " ")
                    stream.start_stream() #resume playback
                    continue
                if response.upper() == "E":
                    print("Stream Terminated by the user...")
                    stream.close() #terminate playback
                    p.terminate()
                    continue

stream.stop_stream()
stream.close()
p.terminate()