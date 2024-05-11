## ctf 6


here is the dcode function it do the reverse of what encode function does

if first get the difference between the char at index i and the first char then doing the same for each
two consecutive letters then combing both to create the new char this will give us the decrypted message but
then we have to try all alphapet to do the ceaser shift
```
def decode_b16(b16):
	decoded = ""
	for i in range(0, len(b16), 2):
		binary = "{0:04b}{1:04b}".format(ord(b16[i]) - START, ord(b16[i+1]) - START)
		decoded += (chr(int(binary, 2)))
	return decoded
```


we will observe that "u" is our key
and the output will be

```
The enemies are making a move. We need to act fast.
```
