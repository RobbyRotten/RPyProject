import json
import subprocess
from datetime import datetime
    

def main():
    while True:
        with open('params.json', 'r') as file_obj:
            data = json.load(file_obj)
        state = data['state']
        if state == 'dead':
            exit(0)       
        filename = datetime.timestamp(datetime.now())
        args = ['streamer', '-o', f'images/{filename}.jpeg']
        process = subprocess.Popen(args, stdout=subprocess.DEVNULL)
        process.wait()


main()
