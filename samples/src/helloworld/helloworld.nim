#[
    It's Hello World! In Nim!
    Compile:
        nim c -d:mingw --cpu:i386 helloworld.nim
]#

proc hello_world():void=
    echo "Hello World!" 


when isMainModule:
    hello_world()