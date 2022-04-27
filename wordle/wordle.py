import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        t=1
        wordle = b"magic"
        
        self.request.sendall(b"\nLet's play the wordle game!\n")

        cnt = 0

        while t<=6:
            # self.request is the TCP socket connected to the client
            self.request.sendall(b"Enter a string: ")
            self.data = self.request.recv(1024).strip()

            print("{} wrote:".format(self.client_address[0]))
            print(self.data)

            inp = self.data
            d = {}

            cnt = 0

            for i in wordle:
                if i in d:
                    d[i]+=1
                else:
                    d[i]=1

            i=0

            while i < 5:
                if inp[i] == wordle[i] and d[inp[i]] > 0:
                    d[inp[i]] -= 1
                    cnt += 1
                    msg = str.encode("The letter `{}` is present and at the correct position!\n".format(chr(inp[i])))
                elif inp[i] in d and d[inp[i]] > 0:
                    d[inp[i]]-=1
                    msg = str.encode("The letter `{}` is present but not at the correct position!\n".format(chr(inp[i])))
                else:
                    msg = str.encode("The letter `{}` is not present in the string!\n".format(chr(inp[i])))

                self.request.sendall(msg)
                i+=1

            if cnt==5:
                self.request.sendall(b"\nCongrats! The secret to the next step: dinklage\n")
                self.request.sendall(b"Cute groot is waiting for you at: http://www.nidavellir.snap/ctf-files/stormbreaker.jpeg")
                break
            else:
                self.request.sendall(b"Try again!\n")
            
            t = t + 1
        
        if cnt != 5:
            self.request.sendall(b"\nBetter luck next time!\n")

if __name__ == "__main__":
    try:
        HOST, PORT = "", 1337

        '''To avoid the error: Python[Error xx] Address already in use
        Set the class variable allow_reuse_address to true before instatiating the server'''
        socketserver.TCPServer.allow_reuse_address = True

        server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

        # while True:
        #     server.handle_request()
        server.serve_forever()
        
        # server.server_close()

    except KeyboardInterrupt:
        print('Interrupted')
        server.shutdown()
        server.server_close()
