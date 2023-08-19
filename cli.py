import json
from argparse import ArgumentParser

from requests import post
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt

DEFAULT_URL = 'http://0.0.0.0:5000'
CHAT_URL = '{}/chats'

console = Console()


def chat(chat_url: str, generation_config: dict):
    prompt = Prompt.ask('[bold red]Ask me any StackExchange question')
    with console.status('[bold green]Asking...'):
        response = post(
            chat_url, json={'prompt': prompt, 'generation_config': generation_config}
        )
    markdown = Markdown(response.json()['response'])
    console.print(Panel(markdown))
    console.line()


def main():
    parser = ArgumentParser(
        prog='SEBot CLI', description='A simple script to communicate with SEBot'
    )
    parser.add_argument(
        '--host', default=DEFAULT_URL, type=str, help='URI for SEBot server.'
    )
    parser.add_argument(
        '--generation_config', default=None, help='Path to JSON config.'
    )

    args = parser.parse_args()

    generation_config = {}
    if args.generation_config:
        with open(args.generation_config) as file:
            generation_config = json.load(file)

    console.print('[bold blue]Welcome to SEBot CLI')
    try:
        while True:
            chat(CHAT_URL.format(args.host), generation_config)
    except KeyboardInterrupt:
        console.line()
        console.print('[bold blue]Exiting...')
        exit()


if __name__ == '__main__':
    main()
