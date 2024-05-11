## CTF 7

simply using the command steghide with the help of this article: [article](https://osintteam.blog/using-steghide-for-hiding-and-extracting-data-213a5bd03123)


run the following command
```
steghide extract -sf pepo_evil.jpg
```
you will be prompted to entere a passphrase
write 
"HIDING"
and the flag will be written to file flat.txt

to see the flag
run the folloing command
```
cat flag.txt
```
