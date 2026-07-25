message = "&&&**$gnirtS PLIO!!@1234"


core = ""
for ch in message:
    if ch.isalpha() or ch == " ":
        core += ch


words = core.split()


first_word = words[0][::-1]


second_word = ""
for ch in words[1]:
    if ch == "E":
        second_word += "A"
    elif ch == "I":
        second_word += "E"
    elif ch == "O":
        second_word += "U"
    elif ch == "U":
        second_word += "O"
    else:
        second_word += ch

print(first_word, second_word)