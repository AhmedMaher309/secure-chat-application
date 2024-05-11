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
