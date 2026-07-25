email = input("Enter email: ")

if email.count("@") != 1:
    print("Invalid email")
    exit()

at_index = email.find("@")
dot_index = email.find(".", at_index)

if dot_index == -1:
    print("Invalid email")
    exit()

username = email[:at_index]
print("Username:", username)

last_dot = email.rfind(".")
domain = email[at_index + 1:last_dot]
print("Domain:", domain)

if email.endswith(".com"):
    print("Commercial Domain")
elif email.endswith(".edu"):
    print("Educational Domain")
else:
    print("Other Domain")