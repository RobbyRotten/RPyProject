from fileinput import filename
import json
import subprocess
from datetime import datetime
import os
    

def main():
    cnt = 0
    params_path = os.path.abspath('daemon/params.json') 
    images_path = os.path.abspath('daemon/images')
    while True:
           
        print(params_path)    
        with open(params_path, 'r') as file_obj:
            data = json.load(file_obj)
        state = data['state']
        if state == 'dead':
            exit(0)       
        # filename = datetime.timestamp(datetime.now())
        elif state == 'alive':
            filename = os.path.join(images_path, f'file{cnt}.jpeg')
            args = ['streamer', '-o', filename]
            process = subprocess.Popen(args, stdout=subprocess.DEVNULL)
            process.wait()
            cnt += 1


main()
