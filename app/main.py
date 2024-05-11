import os

import peer as peer
from deffie_helman import DeffieHellman
from ElGamal import ElGamal

def retrieve_dh(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            lines = file.readlines()
            p = int(lines[0].strip())
            g = int(lines[1].strip())
    else:
        dh = DeffieHellman()
        p = dh.p
        g = dh.g
    
    return p, g
def retrieve_gm(file_path):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as file:
            lines = file.readlines()
            q = int(lines[0].strip())
            a = int(lines[1].strip())
    else:
        gm = ElGamal()
        q = gm.q
        a = gm.a
    
    return q, a
    

def main():
    mode = input("start a peer using start command\n")
    if mode == "start":
        p, g = retrieve_dh("DH.txt")
        q,a=retrieve_gm("gamal.txt")
        peer.start_peer(p,g,q,a)

if __name__ == "__main__":
    main()

