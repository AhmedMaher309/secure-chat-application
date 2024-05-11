## ctf 2


this is big file containg post and get requests so we can grep through the file and searchign for "text"

```
cat packets.pcapng | grep -a "text"
```
we will see the output of this command

```
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Content-Type: text/html
Content-Type: text/plain
```

searching through the file on these patterns i personally used vim

and found the folloing interesting message

```
Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs}
```

using cesier cipher with key 13

running the folloiwng command 
```
echo Gur synt vf cvpbPGS{c33xno00_1_f33_h_qrnqorrs} | tr '[A-Za-z]' '[N-ZA-Mn-za-m]'
```

you will have the flag :-)
```
The flag is picoCTF{p33kab00_1_s33_u_deadbeef}
```
