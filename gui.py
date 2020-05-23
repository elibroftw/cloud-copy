import base64
from contextlib import suppress
from datetime import datetime
import json
import os
import platform
import sys
import time
import traceback
# import uuid
import PySimpleGUI as sg
import requests
from requests.exceptions import ConnectionError
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import pyperclip
import re
import subprocess
from subprocess import DEVNULL, PIPE
try:
    # TODO: set all data into a .prefs file

    sg.theme('DarkBlack')
    BASE_URL = 'http://167.99.191.206/'
    starting_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(starting_dir)
    VERSION = '0.1.3a'
    # BASE_URL = 'http://127.0.0.1:5000/'  # DEBUGGING PURPOSES

    layout = [[sg.Text('CloudCopy Login / Sign Up', font=('Helvetica', 17))],
              [sg.Text('Email', pad=((4, 35), (4, 4)), font=('Arial', 11)),
               sg.InputText(font=('Arial', 11), key='email')],
              [sg.Text('Password', font=('Arial', 11)),
               sg.InputText(password_char='*', font=('Arial', 11), key='password')],
              [sg.Text('Incorrect email or password', key='login_error', size=(30, 1), text_color='#ff425c',
                       font=('Arial', 11), visible=False)],
              [sg.Button('Login or Sign up', key='login', font=('Arial', 11)),
               sg.Text('forgot password', font=('Arial', 11), enable_events=True, key='forgot_password', size=(17, 1))]]

    logged_in = False

    def get_running_processes():
        # ~0.8 seconds
        # edited from https://stackoverflow.com/a/22914414/7732434
        p = subprocess.run('tasklist', shell=True, stderr=PIPE,
                            stdin=DEVNULL, stdout=PIPE)
        tasks = p.stdout.decode().splitlines()
        for task in tasks:
            m = re.match('(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*', task)
            if m is not None:
                process = {'name': m.group(1),  # Image name
                           'pid': m.group(2),
                           'session_name': m.group(3),
                           'session_num': m.group(4),
                           'mem_usage': m.group(5)}
                yield process

    def is_already_running():
        instances = 0
        for process in get_running_processes():
            process_name = process['name']
            if process_name == 'Clooud Copy.exe':
                instances += 1
                if instances > 1:
                    return True
        return False

    if is_already_running(): sys.exit()

    # create a startup shortcut
    if platform.system() == 'Windows':
        from getpass import getuser
        import win32com.client

        user = getuser()
        shortcut_path = f'C:/Users/{user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/Cloud Copy.lnk'
        if not os.path.exists(shortcut_path):
            shell = win32com.client.Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            target = starting_dir + '\\Cloud Copy.exe'
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = starting_dir
            shortcut.WindowStyle = 1
            shortcut.save()

    elif platform.system() == 'Mac OS X':
        pass

    elif platform.system() == 'Linux':
        pass

    def start_service(key, token):
        print('monitoring clipboard')
        current_text = pyperclip.paste()
        last_update = datetime.now()
        while True:
            try:
                new_copy = pyperclip.paste()
                if current_text != new_copy:
                    r = requests.post(BASE_URL + 'share-copy/',
                                      {'token': token, 'contents': encrypt(key, new_copy.encode())})
                    current_text = new_copy
                else:
                    resp = requests.get(
                        BASE_URL + f'newest-copy/?token={token}').text
                    if resp != 'false':
                        resp = json.loads(resp)
                        new_copy, timestamp = decrypt(
                            key, resp['current_copy'].encode()).decode(), resp['timestamp']
                        timestamp = datetime.strptime(
                            timestamp, '%Y-%m-%d %H:%M:%S.%f')
                        if new_copy != current_text and last_update < timestamp:
                            last_update = timestamp
                            current_text = new_copy
                            pyperclip.copy(new_copy)
                time.sleep(1.5)
            except (requests.RequestException, json.decoder.JSONDecodeError):
                print('error')
                time.sleep(60)  # wait 60 seconds before trying again
        # For every copied data, send the token with the data
        # only if no sockets ^
        # Make sure to handle no wifi
        # Socket connection might be required with the server
        # No copied notifications / sent notifications

    def encrypt(key, message: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def decrypt(key, encrypted: bytes) -> bytes:
        return Fernet(key).decrypt(encrypted)

    def generate_key(provided_password: str) -> bytes:
        password_b = provided_password.encode()  # Convert to type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # TODO: change to 256?
            salt=b'',
            iterations=100000,
            backend=default_backend())
        key = base64.urlsafe_b64encode(
            kdf.derive(password_b))  # Can only use kdf once
        with open('.key', 'wb') as f:
            f.write(key)
        return key

    if os.path.exists('.token'):
        try:
            with open('.token') as f:
                email, token = f.read().split('\n')
                url = BASE_URL + 'authenticate/'
                while True:
                    try:
                        x = requests.post(
                            url, {'email': email, 'token': token}).text
                        break
                    except ConnectionError:
                        time.sleep(60)
            if x != 'invalid token':
                logged_in = True
                if x != token:
                    with open('.token', 'w') as f:
                        f.write(email + '\n' + token)
        except ValueError:
            os.remove('.token')

    window = sg.Window('Cloud Copy - Universal Clipboard',
                       layout, return_keyboard_events=True)
    while not logged_in:
        event, values = window.read()
        if event in (None, 'Escape:27'):  # if user closes window or clicks cancel
            sys.exit()
        if event == 'forgot_password':
            print('forgot password')
        if event == 't':
            pass
        if event in ('\r', 'special 16777220', 'special 16777221', 'login'):
            email, password = values['email'], values['password']
            if not email:
                window['email'].set_focus()
            elif not password:
                window['password'].set_focus()
            else:
                window['login_error'].Update(
                    visible=False, value='Incorrect email or password')
                window['forgot_password'].Update(value='authenticating...')
                window.Read(timeout=1)
                # mac = ''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
                # NOTE: no ':' as it is a waste of data
                try:
                    resp = requests.post(
                        BASE_URL + 'authenticate/', {'email': email, 'password': password}).text
                    if resp == 'false':
                        window['login_error'].Update(visible=True)
                        window['forgot_password'].Update(
                            value='forgot password')
                    else:
                        window['login_error'].Update(visible=False)
                        window['forgot_password'].Update(
                            value='login successful')
                        window.Read(timeout=1)
                        # TODO: in 0.1.3a resp will be {'token': new_token, 'key': create_key(password)}
                        token = resp
                        with open('.token', 'w') as f:
                            f.write(email + '\n' + token)
                        generate_key(password)
                        logged_in = True
                        time.sleep(0.5)
                except ConnectionError:
                    window['login_error'].Update(
                        value='No internet connection', visible=True)
                    window['forgot_password'].Update(value='forgot password')
                # also send PC Name?
    window.close()
    with open('.key', 'rb') as f:
        # noinspection PyUnboundLocalVariable
        start_service(f.read(), token)


except Exception as e:
    if os.getenv('DEBUG'):
        raise e
    current_time = str(datetime.now())
    trace_back_msg = traceback.format_exc()
    requests.post('https://envb6z4t5yj4n.x.pipedream.net',
                  json={'TIME': current_time, 'VERSION': VERSION,
                        'OS': platform.platform(), 'TRACEBACK': trace_back_msg})
