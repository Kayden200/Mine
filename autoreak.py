import re
import requests
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import colorama

colorama.init()

def show_credits():
    credits = """
    \033[1;35m===========================================\033[0m
    \033[1;36mCredits: Joshua Apostol | Explored by Shiki\033[0m
    \033[1;35m===========================================\033[0m
    """
    print(credits)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_logo():
    logo = """
    \033[1;34m░█████╗░██╗░░░██╗████████╗░█████╗░
    ██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗
    ███████║██║░░░██║░░░██║░░░██║░░██║
    ██╔══██║██║░░░██║░░░██║░░░██║░░██║
    ██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝
    ╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░\033[0m
    \033[1;32mbest website pornhub.com\033[0m
    """
    print(logo)

def countdown(delay):
    icons = ['X    ', ' X   ', '  X  ', '   X ', '    X']
    while delay > 0:
        for i in range(5):
            print(f"\033[1;37m[DELAY][{icons[i]}][{delay} seconds]", end='\r')
            sleep(0.2)
        delay -= 1

class Machine:
    def __init__(self):
        self.session_list = []
        self.delay = 0
        self.url = None
        self.reactions_dict = {
            '1': 'like', 
            '2': 'love', 
            '3': 'care', 
            '4': 'haha', 
            '5': 'wow', 
            '6': 'sad', 
            '7': 'angry'
        }
        self.selected_reactions = []
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.5',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Linux; Android 12; SM-A037F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36',
        }

    def boost_reaction(self, session):
        try:
            get_token = session.get('https://machineliker.net/auto-reactions').text
            token = re.search(r'name="_token" value="(.*?)"', get_token).group(1)
            hash_ = re.search(r'name="hash" value="(.*?)"', get_token).group(1)

            data = {
                'url': self.url,
                'limit': '20',
                'reactions[]': self.selected_reactions,
                '_token': token,
                'hash': hash_
            }

            response = session.post('https://machineliker.net/auto-reactions', headers=self.headers, data=data).text
            
            if "Error!" in response and "please try again after" in response:
                minutes = int(re.search(r'please try again after (\d+) minutes', response).group(1))
                self.delay = minutes * 60
                print(f"\033[1;91mCooldown: Please wait {self.delay} seconds more\033[0m")
            elif 'Order Submitted' in response:
                print(f"\033[1;92mSuccessfully increased reactions from {session}\033[0m")
                self.delay = 1200
            else:
                print("\033[1;91mUnexpected error occurred\033[0m")
        except Exception as e:
            print(f"\033[1;91mError boosting reaction: {e}\033[0m")

    def main(self):
        clear_console()
        display_logo()
        show_credits()

        print("\nLogged in accounts:")
        
        self.url = input("\033[1;34mEnter the URL of the post to boost reactions: \033[0m")
        print("\033[1;32mChoose the reaction type(s) to boost (e.g., 123 for like, love, and care):\033[0m")
        print("\033[1;32m1: like\n2: love\n3: care\n4: haha\n5: wow\n6: sad\n7: angry\033[0m")
        choices = input("Enter the numbers: ")
        self.selected_reactions = [self.reactions_dict[x] for x in choices]

        while True:
            for session in self.session_list:
                self.boost_reaction(session)
            countdown(self.delay)

if __name__ == '__main__':
    clear_console()
    display_logo()
    Machine().main()
