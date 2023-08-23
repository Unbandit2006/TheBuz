import imaplib, email

connection = imaplib.IMAP4_SSL("imap.gmail.com")
connection.login("TheBuzNY@gmail.com", "wafmjdaxuhhltpdn")

# for thing in connection.list("[Gmail]"):
#     for otherThing in thing:
#         print(otherThing)

print(connection.welcome)
