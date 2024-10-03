def shift_character(char):
    if(not str.isalpha(char)):
        raise ValueError("character needs to be alpha")
    shift = 3
    isupper = str.isupper(char)
    a = ord("a")
    z = ord("z")

    char = chr(ord(char) + shift)
    if(ord(char) > z):
        char = chr(a + (ord(char) - z))
    
    if isupper:
        char = char.upper()

    return char

print(shift_character('z'))