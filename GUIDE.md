# How this works

To get the words and their definitions, abra.py needs a list.  If you copy from the first word to the last example of an abra list and save in a file, it can parse that and get the information it needs.

Once it has them, it:
  - prints percentage done
  - prints the word
  - copies the definition of the word into your clipboard (you can just ctrl/cmd-v the definition without having to ctrl/cmd-c)
  - searches etymonline.com, google synonyms, and google images

Then, you can press enter to make it do the next word.

### How to use, if you haven't used python from the terminal before

1. Open a terminal app
  - Windows: Command Prompt
  - Mac: Terminal
2. Get into the folder you downloaded (you may have to unzip the file first)
  - cd Downloads/abra
3. Run abra.py with python 3
  - Type 'python3 abra.py' and press enter
  - If that doesn't work:
    - Mac: You need to install python 3 from https://python.org
    - Windows: 'python abra.py' will work if 'python --version' prints 3.*something*; otherwise, you need to install python 3

### Alternative ways that use other apps

Open the abra folder with VSCode, install the python extension, and press the run button with abra.py open

Open the abra.py file with IDLE 3, and press F5
