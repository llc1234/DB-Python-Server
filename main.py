import os
import time
import socket
import colorama
import threading


class Server:
    def __init__(self):
        colorama.init()

        self.running = True

        self.IP = "127.0.0.1"
        self.PORT = 5050
        
        self.FilePath = "data"
        self.ServerName = "python db test"
        self.ServerUsername = "admin" # None
        self.ServerPassword = "None" # None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.StartUp()

    def GetIP(self):
        sp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sp.connect(("8.8.8.8", 80))
        self.IP = sp.getsockname()[0]

    def print_red(self, text, end="\n"):
        print(f"{colorama.Fore.RED}{text}{colorama.Fore.WHITE}", end=end)

    def print_blue(self, text, end="\n"):
        print(f"{colorama.Fore.BLUE}{text}{colorama.Fore.WHITE}", end=end)

    def print_light_blue(self, text, end="\n"):
        print(f"{colorama.Fore.LIGHTBLUE_EX}{text}{colorama.Fore.WHITE}", end=end)

    def print_green(self, text, end="\n"):
        print(f"{colorama.Fore.GREEN}{text}{colorama.Fore.WHITE}", end=end)

    def print_clear(self):
        print('\r' + ' ' * 30 + '\r', end='', flush=True)

    def print_input(self):
        print(f"{colorama.Fore.GREEN}{self.ServerName}>{colorama.Fore.WHITE}", end="", flush=True)
        # self.print_green(self.ServerName + ">", "")

    def OpenPort(self):
        self.GetIP()

        try:
            self.s.settimeout(2)
            self.s.bind((self.IP, self.PORT))
            self.s.listen()

            return True

        except:
            return False

    def StartUp(self):
        self.print_light_blue("\nStarting Server")
        print("")
        
        if self.OpenPort():
            self.print_light_blue(f"IP                  : {self.IP}")
            self.print_light_blue(f"PORT                : {self.PORT}")
            
            if self.ServerPassword != "None":
                self.print_light_blue(f"password protected  : true")

            print("")

            threading.Thread(target=self.StartServer).start()
            self.OpenTerminal()

    def command_dir(self, conn):
        extension = None

        try:
            for root, dirs, files in os.walk(self.FilePath):
                for file in files:
                    if extension is None or file.endswith(extension):
                        conn.send(bytes(os.path.join(root, file) + "\n", "utf-8"))
        except Exception as e:
            pass

    def command_search(self, conn, command):
        extension = None

        file_list = []

        f_command = ""

        for i in range(1, len(command)):
            f_command += command[i] + " "
        
        f_command = f_command[0:-1]

        try:
            for root, dirs, files in os.walk(self.FilePath):
                for file in files:
                    if extension is None or file.endswith(extension):
                        file_list.append(os.path.join(root, file).lower())
        except Exception as e:
            pass
        
        for pp in file_list:
            if not pp.find(f_command) == -1:
                st = f"{pp.replace(f_command, colorama.Fore.RED + pp[pp.find(f_command):pp.find(f_command)+len(f_command)] + colorama.Fore.WHITE)}"
                conn.send(bytes(st + "\n", "utf-8"))

    def command_help(self, conn):
        text = """
        - dir      "view all file in the folder"
        - search   "search for a name of char"
        - download <filename and path>
        - upload   <filename and path>
        """

        conn.send(bytes(text + "\n", "utf-8"))

    def ClientTerminal(self, conn, addr):
        run = True
        while self.running and run:
            try:
                comm = conn.recv(256).decode("utf-8").split(" ")
                command = [item for item in comm if item != '']

                self.print_clear()
                print(f"Client: {addr}, Command: {command}")
                self.print_input()

                if command[0] == "dir":
                    self.command_dir(conn)
                elif command[0] == "search":
                    self.command_search(conn, command)
                elif command[0] == "help":
                    self.command_help(conn)
                elif command[0] == "exit":
                    conn.close()

                    self.print_clear()
                    # print(f"Client Has Disconnected: {addr}")
                    self.print_red(f"Client Has Disconnected: {addr}", "\n")
                    self.print_input()

                    run = False

            except:
                run = False

    def ClientLogin(self, conn, addr):
        try:
            if self.ServerPassword != "None":
                conn.send(bytes(f"{self.ServerName}'s username ", "utf-8"))
                username = conn.recv(256).decode("utf-8")

                conn.send(bytes(f"{self.ServerName}'s password ", "utf-8"))
                password = conn.recv(256).decode("utf-8")

                if username == self.ServerUsername and password == self.ServerPassword:
                    conn.send(bytes("logged in successfully\n", "utf-8"))
                    self.ClientTerminal(conn, addr)
                else:
                    conn.send(bytes("logged in ERROR\n", "utf-8"))
            else:
                conn.send(bytes("logged in successfully\n", "utf-8"))
                self.ClientTerminal(conn, addr)
        
        except:
            conn.close()

    def StartServer(self):
        while self.running:
            try:
                conn, addr = self.s.accept()
                
                self.print_clear()
                self.print_red(f"New Client: {addr}", "\n")
                self.print_input()

                threading.Thread(target=lambda: self.ClientLogin(conn, addr)).start()

            except socket.timeout:
                pass

    def OpenTerminal(self):
        # self.print_green(self.ServerName + ">", "")

        while self.running:
            self.print_input()

            con = input().split(" ")
            command = [item for item in con if item != '']

            if command[0] == "exit":
                self.print_red(f"Terminating Server...\n")
                self.running = False

Server()
