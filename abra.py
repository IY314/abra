
import webbrowser as web
import pyperclip
import sys
from os import getenv
try:
    from locate import *
except:
    raise ImportError("This file needs locate.py to work: check https://github.com/mrfoogles/abra for more info.")

def load_data(data):
    lines = data.split("\n")
    w = [] # words
    d = [] # definitions
    for i in range(0,len(lines),4):
        # ':-1' because each word ends in a :
        w.append(lines[i].split(" ")[1][:-1]) # splice syntax
        d.append(lines[i+1])
    return(w,d)

home = getenv("HOME") # The folder Desktop, Documents, etc. are in
f = "data.txt"
datapaths = [f"{home}",f"{home}/Documents",f"{home}/Desktop"]


import os
import requests

def yn(message):
    ans = input(message).strip()
    if ans.lower() == "n":
        return False
    else:
        return ans

def tryall(*funcs):
    if len(funcs) == 0:
        raise Exception("trychain was called with 0 args")
    arg = None
    while True:
        try:
            return funcs[0](arg)
        except Exception as e:
            if len(funcs) == 0:
                raise Exception("All functions in trychain failed")
            else:
                funcs = funcs[1:]
                arg = e

def pull(f):
    status = os.system("git pull")
    if status != 0:
        print(f"git pull exited with status {status}")
        raise Exception("Could not git pull")
    return read(f)

def read(name):
    with open(name) as f:
        return f.read()

def github(user,repo):
    return f"https://github.com/{user}/{repo}.git"

def clone(url):
    os.system(f"git clone {url}")

def download(url,dest=None):
    print(f"Downloading {dest} from {url}")
    response = requests.get(url)
    try:
        response.raise_for_status()
    except Exception as e:
        print(e)
        raise Exception(f"Could not download {url}")

    if dest:
        with open(dest,mode="w") as f:
            f.write(response.text)
    return response.text

def locate(name,paths=[]):
    j = os.path.join
    for path in paths:
        if os.path.exists(j(path,name)):
            if input(f"Use {j(path,name)}? (y/n) ").strip().lower() == "y":
                return read(j(path,name))

    raise Exception(f"No paths were found for {name}")

def wait(name):
    ans = input(f"Use a different {name}? (path or n) ").strip()
    if ans.lower() != "n":
        try:
            return read(name)
        except Exception as e:
            print(f"Could not read {ans}: {e}")
            raise e
    else:
        raise Exception(f"User would not identify a {name}.")

def clone_abra(e):
    if input("Clone repository to get data.txt? (y/n) ").strip().lower() != "n":
        if os.path.exists("abra"):
            print("The repository already exists; run abra/abra.py")
            sys.exit(0)
        else:
            status = clone(github("mrfoogles","abra"))
            if status == 0:
                sys.exit(0)
            else:
                print("Could not clone repo")
                raise Exception("Could not clone repo")
    else:
        raise Exception("User declined to clone repo")

def uselists(e):
    if os.path.isdir("lists") and os.listdir("lists") != []:
        available = str(os.listdir("lists"))[1:-1]
        print(f"Found lists in folder lists: {available}")
        ans = input("Use one of these? (list name, or n) ").strip()
        if ans.lower() != "n":
            return read(os.path.join("lists",ans))
        else:
            raise Exception("User declined to use lists")
    else:
        raise Exception("No lists available")

def datatxt(e):
    if os.path.isfile(f) and input(f"Use {f}? (y/n) ").strip().lower() == "y":
        return read(f)
    else:
        raise Exception("No use data.txt")

def getlist(e):
    ans = yn("Try to download a list? (list number or n) ")
    if ans:
        if os.path.isfile("lists"):
            os.rename("lists","why_did_you_have_a_file_named_lists")
        if not os.path.isdir("lists"):
            os.mkdir("lists")
        return download(f"https://raw.githubusercontent.com/mrfoogles/abra/main/lists/{ans}",os.path.join("lists",ans))
    else:
        raise Exception("User say no")

if __name__ == "__main__":
    print("If something breaks, try doing 'git pull' in terminal if you downloaded this with 'git clone https://github.com/mrfoogles/abra.git'")
    print("--Finding data.txt\n")
    try:
        data = tryall(
            # lists folder
            uselists,
            datatxt,
            getlist,
            # Hey, want to use the one in Desktop?
            lambda e : locate(f,datapaths),
            # Is the data somewhere I don't know?
            lambda e : wait("data file"),
            clone_abra
        )
    except Exception as e:
        print(f"Error: {e}")
        print("Ok, I have no clue how to find this file.  Good luck.")
        sys.exit(1)
    print("--Found data.txt, starting\n")
    # Sometimes there are extra lines of whitespace and it breaks because the number
    #  of lines is not a multiple of four
    data = data.strip()
    #  \n means start a new line
    #  what this means:
    #   hello\n
    #   a greeting\n
    #   \n # inserted by google docs as a page break
    #   - hello, person!
    #  ...
    #  number of lines is now not a multiple of four because there's an extra
    data.replace("\n\n","\n")

    words, defs = load_data(data)

    percent_done = 0.0
    increment = 100 / len(words)
    print(f"Percent: {round(percent_done,2)}")
    print(f"Increment: {increment}")

    # you can do 'python3 abra.py <word>', and it skips to that word
    if len(sys.argv) > 1: # sys.argv[0] = <program name>
        while words[0] != sys.argv[1]:
            print(f"Skipping {words.pop(0)}")
            defs.pop(0)

            # make sure the percentage starts at right amount
            #  when you skip forward
            percent_done += increment
        print(f"Starting at {round(percent_done,2)}%")

    def newtab(url):
        web.open(url,new=2)

    for i in range(0,len(words)):
        input("press enter for next word")

        print(f"Now {round(percent_done,2)}% done")
        percent_done += increment

        print(words[i])

        pyperclip.copy(defs[i])
        print("copied definition")

        newtab(f"https://etymonline.com/search?q={words[i]}")
        newtab(f"https://www.google.com/search?q={words[i]}+synonyms&source=lmns&hl=en")
        newtab(f"https://www.google.com/search?q={words[i]}&tbm=isch")
