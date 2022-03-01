import json
import os
import subprocess

"""Commands:
    - dead
    - alive
"""

class DaemonManager:
    def __init__(self, path='daemon'):
        if not os.path.isdir(path):
            os.mkdir(path)
        self.cmd_file = os.path.join(path, 'params.json')  # f'{path}/params.json'  # 
        self.daemon_path = os.path.abspath(os.path.join(path, 'camera_daemon.py'))
        self.process = None
        

    def isactive(self):
        return True if self.get_state() == 'alive' else False


    def start_roll(self):
        self.change_state('alive')
        args = ['python3', self.daemon_path]
        print(self.daemon_path)
        self.process = subprocess.Popen(args, stdout=subprocess.DEVNULL)


    def stop_roll(self):
        self.change_state('dead')


    def change_state(self, state):   
        data = {'state': state}       
        with open(self.cmd_file, 'w') as file_obj:
            json.dump(data, file_obj)      


    def get_state(self): 
        if os.path.isfile(self.cmd_file):
            with open(self.cmd_file, 'r') as file_obj:
                data = json.load(file_obj)
            return data['state']
        else:
            self.change_state('dead')
            return 'dead'