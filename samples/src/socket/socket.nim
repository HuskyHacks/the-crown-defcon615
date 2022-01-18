#[  Simple echo server in Nim.
    Sources: 
        - https://nim-lang.org/docs/net.html#examples-creating-a-server
        - https://gist.github.com/mttaggart/d119b13b248cdc7c9df264e432e60892

    Compile for Linux:
        nim c socket.nim
    
    Compile for Windows x86:
        nim c -d:mingw --cpu:i386 socket.nim
]#
import net

let port = Port(1738)
let sock = newSocket()

sock.bindAddr(port)
sock.setSockOpt(OptReuseAddr, true)
sock.listen()
echo "[+] Echo server online!"

var client: Socket
var address = ""
let prompt = "echo > "

sock.acceptAddr(client, address)
echo "[+] Connection from: " & address
let greeting = "[*] Hello from the echo server!\n"
client.send(prompt)
client.send(greeting)

while true:
    try:
        let received = client.recvLine()
        if received == "":
            discard
        else:
            echo "[*] " & received
            client.send("[*] Echo! -> " & received & "\n")
            client.send(prompt)
    finally:
        sock.close()



