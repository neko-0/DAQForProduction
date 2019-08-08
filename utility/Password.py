'''
a simple user-password class
'''

from hashlib import sha256
import getpass
import os

class Password:

    def __init__(self):
        self.class_name = "Password"

    @staticmethod
    def generate_user(username):
        with open("{user}_daqPW.dat".format(user=username), "wb") as f:
            pw = getpass.getpass("Please enter your password: \n")
            encrypted_pw = sha256(pw.rstrip()).hexdigest()
            f.write(encrypted_pw)

    @staticmethod
    def check_login():
        user = ""
        while user=="":
            user = str(raw_input("USER NAME:"))
            user_pw_file = "/home/yuzhan/DAQForProduction/{username}_daqPW.dat".format(username=user)
            if os.path.exists(user_pw_file):
                with open(user_pw_file, "rb") as f:
                    pw = getpass.getpass("Please enter your password: \n")
                    decode_pw = sha256(pw.rstrip()).hexdigest()
                    stored_pw = f.read()
                    if decode_pw == stored_pw:
                        print("Okay")
                        return True
                    else:
                        print("error re-try")
                        user = ""
            else:
                print("cannot find login file.")
                return False