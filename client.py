import sys
import socket
import colorama
import threading

colorama.init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], 5050))
s.settimeout(0.8)

while True:
    while True:
        try:
            print(s.recv(16).decode("utf-8"), end="")
        except socket.timeout:
            break

    conn = input("->")

    s.send(bytes(conn, "utf-8"))

    if conn == "exit":
        break
