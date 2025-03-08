import asyncio
import aiohttp
import re
from rich.console import Console
from maxgradient import Gradient
import sys
import os
os.system('clear')
console = Console()
config = {
	'cookies': '',
	'post': ''
}
def banner():
	console.print(
		Gradient(
			"""
 $$$$$$\                                          
$$  __$$\                                         
$$ /  \__| $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\  
$$ |$$$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ 
$$ |\_$$ |$$ |  \__|$$$$$$$$ |$$$$$$$$ |$$ /  $$ |
$$ |  $$ |$$ |      $$   ____|$$   ____|$$ |  $$ |
\$$$$$$  |$$ |      \$$$$$$$\ \$$$$$$$\ \$$$$$$$ |
 \______/ \__|       \_______| \_______| \____$$ |
                                        $$\   $$ |
                                        \$$$$$$  |
                                         \______/ 
			""",
			colors=['blue','purple','blue']
		)
	)
banner()
config['cookies'] = input("\033[0mCOOKIE : \033[92m")
config['post'] = input("\033[0mPOST LINK : \033[92m")
share_count = int(input("\033[0mSHARE COUNT : \033[92m"))
if not config['post'].startswith('https://'):
	console.print(Gradient("Invalid post link",colors=['red','orange','red']));sys.exit()
elif not share_count:
	console.print(Gradient("Bobo walang count",colors=['red','orange','red']));sys.exit()

os.system("clear")
banner()
headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
	'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
	'sec-ch-ua-mobile': '?0',
	'sec-ch-ua-platform': "Windows",
	'sec-fetch-dest': 'document',
	'sec-fetch-mode': 'navigate',
	'sec-fetch-site': 'none',
	'sec-fetch-user': '?1',
	'upgrade-insecure-requests': '1'
}
class Share:
	async def get_token(self, session):
		headers['cookie'] = config['cookies']
		async with session.get('https://business.facebook.com/content_management', headers=headers) as response:
			data = await response.text()
			access_token = 'EAAG' + re.search('EAAG(.*?)","', data).group(1)
			return access_token, headers['cookie']
	async def share(self, session, token, cookie):
		headers['cookie']
		headers['sec-fetch-dest']
		headers['sec-fetch-mode']
		headers['sec-fetch-site']
		headers['sec-fetch-user']
		headers['upgrade-insecure-requests']
		headers['accept-encoding'] = 'gzip, deflate'
		headers['host'] = 'b-graph.facebook.com'
		headers['cookie'] = cookie
		count = 1
		with console.status("[bold green] Sending shares....") as status:
			while count < share_count + 1:
				async with session.post(f'https://b-graph.facebook.com/me/feed?link=https://mbasic.facebook.com/{config["post"]}&published=0&access_token={token}', headers=headers) as response:
					data = await response.json()
					if 'id' in data:
						console.log(f"({count}/{share_count}) Complete")
						count += 1
					else:
						console.log("[bold red]Cookie is blocked, ctrl c to exit !!!")
						console.log(f"[white] Total Success : [bold green]{count}")
						break
async def main(num_tasks): 
	async with aiohttp.ClientSession() as session:
		share = Share()
		token, cookie = await share.get_token(session)
		tasks = []
		for i in range(num_tasks):
			task = asyncio.create_task(share.share(session, token, cookie))
			tasks.append(task)
		await asyncio.gather(*tasks)
asyncio.run(main(1))
