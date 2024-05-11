# Decrypting Encrypted Text

## Find the Letter Swap:
* Grab a chunk of the encrypted text from "encrypted_text.txt".
* Head over to https://www.dcode.fr/monoalphabetic-substitution and paste it in.
* Get the subsitution from the website

## Decrypt the Whole Thing:

* Copy the letter swap info (substitution map) from the website or your own analysis.
* Open a new file (decrypt.py) and paste the following code:

```python
def substitute_text(text, mapping):
    substitution_text = ""
    for char in text:
        if char in mapping:
            substitution_text += mapping[char]
        else:
            substitution_text += char
    return substitution_text

if __name__ == "__main__":
    text_to_substitute = open("encrypted_text.txt", "r").read()
    letter_map = {}
    for first_letter, second_letter in zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "CRLJAZPHEQTKNFDOVIGBMSYUWX"):
      letter_map[first_letter] = second_letter
    substituted_text = substitute_text(text_to_substitute, letter_map)
    with open("decrypted_text.txt", "w") as f:
        f.write(substituted_text)
```

run the code with:
```
python decrypt.py
```
