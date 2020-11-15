import db
import colorama
from colorama import Fore, Back, Style

colorama.init()


def out_red(text): print(Fore.RED + text)


def out_green(text): print(Fore.GREEN + text)


def out_white(text): print(Fore.WHITE + text)


def out_yelow(text): print(Fore.YELLOW + text)


def draw_data(): out_yelow(str(db.get_data()))
