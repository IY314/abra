### By @mrfoogles

import webbrowser as web
import pyperclip
import sys
import os
import requests

home = os.getenv("HOME") # The folder Desktop, Documents, etc. are in
f = "data.txt"
datapaths = [f"{home}",f"{home}/Documents",f"{home}/Desktop"]

def yn(message):
    ans = input(message).strip()
    if ans.lower() == "n":
        return False
    else:
        return ans


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
            if input(f"Use {j(path,name)}? (type y or n) ").strip().lower() == "y":
                return read(j(path,name))

    raise Exception(f"No paths were found for {name}")

def wait(name):
    ans = yn(f"Use a different {name}? (path or n) ")
    if ans:
        try:
            return read(ans)
        except Exception as e:
            print(f"Could not read {ans}: {e}")
            raise e
    else:
        raise Exception(f"User would not identify a {name}.")

def tryall(*funcs):
    if len(funcs) == 0:
        raise Exception("trychain was called with 0 args")
    arg = None
    while True:
        try:
            return funcs[0](arg)
        except Exception as e:
            if len(funcs) == 0:
                raise Exception("")
            else:
                funcs = funcs[1:]
                arg = e
    

def load_data(data):
    data = data.strip().replace("\n\n","\n")
    lines = data.split("\n")
    w = [] # words
    d = [] # definitions
    for i in range(0,len(lines),4):
        # ':-1' because each word ends in a :
        w.append(lines[i].split(" ")[1:][:-1]) # splice syntax
        d.append(lines[i+1])
    return(w,d)


def request_list():
    print("\n--Finding data.txt")

    def local_list(e):
        if os.path.isdir("lists") and os.listdir("lists") != []:
            available = str(os.listdir("lists"))[1:-1]
            print(f"Found lists in folder lists: {available}")
            ans = input("Use one of these? (type preferred list or n) ").strip()
            if ans.lower() != "n":
                return read(os.path.join("lists",ans))
            else:
                raise Exception("User declined to use lists")
        else:
            raise Exception("No lists available")

    def local_txt(e):
        if os.path.isfile(f) and yn(f"Use {f}? (type y or n)") == "y":
            return read(f)
        else:
            raise Exception("No use data.txt")

    def download_list(e):
        ans = yn("Try to download a list? (list number or n) ")
        if ans:
            if os.path.isfile("lists"):
                os.rename("lists","why_did_you_have_a_file_named_lists")
            if not os.path.isdir("lists"):
                os.mkdir("lists")
            return download(f"https://raw.githubusercontent.com/mrfoogles/abra/main/lists/{ans}",os.path.join("lists",ans))
        else:
            raise Exception("User say no")

    return tryall(
        # lists folder
        local_list,
        local_txt,
        download_list,
        # Hey, want to use the one in Desktop?
        lambda e : locate(f,datapaths),
        # Is the data somewhere I don't know?
        lambda e : wait("data.txt")
    )

if __name__ == "__main__":
    print("If something breaks, try doing 'git pull' in terminal if you downloaded this with 'git clone https://github.com/mrfoogles/abra.git'")
    print("'python3 abra.py <word>' will skip to that word")
    print("Ctrl-c will quit shell programs like this one")
    
    try:
        data = request_list()
    except Exception as e:
        if str(e) != "":
            print(f"Error: {e}")
        print("Ok, I have no clue how to find this file.  Good luck.")
        sys.exit(1)

    print("\n--Found data.txt, starting")
    # Sometimes there are extra lines of whitespace and it breaks because the number
    #  of lines is not a multiple of four
    data = data.strip()
    # Remove page breaks
    data.replace("\n\n","\n")

    words, defs = load_data(data)

    percent_done = 0.0
    increment = 100 / len(words)

    # you can do 'python3 abra.py <word>', and it skips to that word
    if len(sys.argv) > 1:
        print(f"  Skipping to {sys.argv[1]}")
        while words[0] != sys.argv[1]:
            words.pop(0)
            defs.pop(0)

            # make sure the percentage starts at right amount
            #  when you skip forward
            percent_done += increment

    def newtab(url):
        web.open(url,new=2)

    for i in range(0,len(words)):
        input("press enter for next word")

        if percent_done > 0:
            print(f"{round(percent_done,2)}% done!")

        print("Copying definition, opening tabs...")

        pyperclip.copy(defs[i])

        newtab(f"https://etymonline.com/search?q={words[i]}")
        newtab(f"https://www.google.com/search?q={words[i]}+synonyms&source=lmns&hl=en")
        newtab(f"https://www.google.com/search?q={words[i]}&tbm=isch")

        percent_done += increment
