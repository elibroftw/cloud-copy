import PySimpleGUI as sg
import sys
import uuid

sg.theme('DarkBlack')
BASE_URL = '167.99.191.206'

layout = [[sg.Text('Log into Cloud Copy', font=('Helvetica', 18))],
          [sg.Text('Email', font=('Arial', 11)), sg.InputText(font=('Arial', 11), key='email')],
          [sg.Text('Password', font=('Arial', 11)),
           sg.InputText(password_char='*', font=('Arial', 11), key='password')],
          [sg.Text('Incorrect email or password', key='log_in_error', size=(30, 1), text_color='#ff425c',
                   font=('Arial', 11), visible=False)],
          [sg.Button('Log in or Sign up', key='log_in', font=('Arial', 11)),
           sg.Text('forgot password', font=('Arial', 11), enable_events=True, key='forgot_password')]]

logged_in = False
# Create the Window
window = sg.Window('Cloud Copy - Universal Clipboard', layout, return_keyboard_events=True)

# Event Loop to process "events" and get the "values" of the inputs
while not logged_in:
    event, values = window.read()
    if event in (None, 'Escape:27'):  # if user closes window or clicks cancel
        sys.exit()
    if event == 'forgot_password':
        print('forgot password')
    if event == 't':
        print(window.find_element_with_focus())
    if event in ('\r', 'special 16777220', 'special 16777221', 'log_in'):
        email, password = values['email'], values['password']
        if not email:
            window['email'].set_focus()
        elif not password:
            window['password'].set_focus()
        else:
            window['log_in_error'].Update(visible=False)
            window['forgot_password'].Update(value='authenticating...')
            # mac = ''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
            # NOTE: no ':' as it is a waste of data
            # also send PC Name
            # authenticate user
            # if authenticated:
            #     # do stuff
            # else: window['log_in_error'].Update(visible=True)
            #     logged_in = True
            # window['forgot_password'].Update(value='forgot password')
    # print(event)
window.close()
