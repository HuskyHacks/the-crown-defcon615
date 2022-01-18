#[ Simple ShellExecute API call

    Compile:
        nim c -d:mingw --cpu:i386 shellexecute.nim

]#

import winim

let shellexec = ShellExecute(
    0,
    "open",
    "notepad",
    "",
    NULL,
    SW_SHOW
)

discard(shellexec)