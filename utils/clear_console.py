import os
from colorama import init
from .display_title import display_title

def clear_console(keep_title=False):
    os.system('cls' if os.name == 'nt' else 'clear')
    if keep_title:
        display_title()