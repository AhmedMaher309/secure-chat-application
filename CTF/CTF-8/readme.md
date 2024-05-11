## ctf 8

using the following command to see what the wav form looks like:
```
ffplay lastcall.wav
```

observing the wave form it is obvious that this is a form of decoding
searching the internt for ways to decode a message in a wav file i found that
the following link:
[link](https://morsecode.world/international/decoder/audio-decoder-adaptive.html)

and uploading the wav file into the website it will output for us the following

THE RUSSIAN TERRORISTS ARE THE ONES WHO STARTED THIS, THEY ARE THE KEY. PLEASE YOU MUST EXTRACT M

from the problem statment we have a hint about "extracting"
now using the following command:
```
hexdump -C lastcall.wav| tail -n 15
```
we will notice a wikiebdia link

[link](https://en.wikipedia.org/wiki/Nihilist_cipher?keyword=polybius)

the alphabet is polybius
with that given now the last line has hex data, those data are enctypted as nihilist cipher (given the link)
we have the key as "RUSSIAN" compinging those and goinig for online decrypted we will have the following message

```
thankyouforsavingmetheflagismoscow
```
