
import os
import requests

def trychain(*funcs):
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
    print(f"Trying to find {name}")
    for path in paths:
        if os.path.exists(j(path,name)):
            if input(f"Use {j(path,name)}? (y/n) ").strip().lower() == "y":
                return read(j(path,name))

    raise Exception(f"No paths were found for {name}")

def wait(name):
    ans = input(f"Cannot find {name}; can you create a file named '{name}'? (y when finished, n if no) ").strip().lower()
    if ans == "y":
        return read(name)
    else:
        raise Exception(f"User would not create {name}.")
