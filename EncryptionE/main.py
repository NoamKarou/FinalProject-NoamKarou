key = "jzgklmtivrypqwnxeofahbcdsu"
msg = "hi im noam"
original = "abcdefghijklmnopqrstuvwxyz"
dict = {}
tcid = {}
for i in range(len(key)):
    dict[original[i]] = key[i]

for i in range(len(key)):
    tcid[key[i]] = original[i]

def encrypt(message):
    enc = ""
    for letter in message:
        try:
            enc += dict[letter]
        except:
            continue
    return enc

def decrypt(message):
    decrypted = ""
    for letter in message:
        decrypted += tcid[letter]
    return decrypted
'''
encrypted = encrypt(msg)
print(encrypted)
print(decrypt(encrypted))
'''

