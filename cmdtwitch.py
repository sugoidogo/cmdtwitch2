try:
    import tee
    tee.Tee('cmdtwitch.log', 'w')

    try:
        import pip, os
        args=['install','requests']
        if os.name == 'nt':
            args.append('pywin32')
        pip.main(args)
    except Exception as e:
        print('an error occured during dependency checks')
        from traceback import print_exc
        print_exc()
        print('if you encounter issues, make sure requests is installed')

    import requests
    import signal
    import sys
    import atexit
    import traceback
    import subprocess
    import time
    import json
    import webbrowser
    import http.server
    from urllib.parse import urlparse, parse_qs

    try:
        import secret
    except:
        secret=open('secret.py','x')
        secret.writelines(['# https://dev.twitch.tv/console/apps \n','client_id="" \n','client_secret="" \n','username="" \n'])
        secret.close()
        input('please edit secret.py and include your app secrets and channel name')
        exit(1)

    class OAuthRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write('<script>close();</script>'.encode())
            secret.auth_code=parse_qs(urlparse(self.path).query)['code'][0]
            self.server.shutdown()

    webbrowser.open(requests.Request('GET','https://id.twitch.tv/oauth2/authorize',
        params={
            'client_id':secret.client_id,
            'redirect_uri':'http://localhost:2000',
            'response_type':'code',
            'scope':'channel:manage:redemptions channel:read:redemptions'
        }
    ).prepare().url)

    http.server.ThreadingHTTPServer(('localhost',2000),OAuthRequestHandler).serve_forever()

    def request(url:str,method='GET',**kwargs):
        response=requests.request(method, url, **kwargs)
        if(response.status_code>=400):
            raise Exception(response.content)
        return json.loads(response.content)


    secret.access_token=request('https://id.twitch.tv/oauth2/token','POST',
        params={
            'client_id':secret.client_id,
            'client_secret':secret.client_secret,
            'code':secret.auth_code,
            'grant_type':'authorization_code',
            'redirect_uri':'http://localhost:2001'
        }
    )['access_token']

    secret.auth_header={
        'Authorization':'Bearer '+secret.access_token,
        'Client-Id':secret.client_id
    }

    secret.broadcaster_id=request('https://api.twitch.tv/helix/users',
        params={
            'login':secret.username
        },
        headers=secret.auth_header
    )['data'][0]['id']

    commandsFile=open('cmdtwitch.json','r+')
    commands=json.load(commandsFile)
    for id, redeem in commands.copy().items():
        try:
            request('https://api.twitch.tv/helix/channel_points/custom_rewards','PATCH',
                headers=secret.auth_header,
                params={
                    'broadcaster_id':secret.broadcaster_id,
                    'id':id
                },
                json={
                    'is_paused':False
                }
            )
        except:
            commands.pop(id)
            id=request('https://api.twitch.tv/helix/channel_points/custom_rewards','POST',
                headers=secret.auth_header,
                params={
                    'broadcaster_id':secret.broadcaster_id
                },
                json={
                    'title':redeem['title'],
                    'cost':1
                }
            )['data'][0]['id']
            redeem['last']=''
            commands[id]=redeem

    def updateCommands():
        commandsFile.seek(0)
        commandsFile.truncate()
        json.dump(commands, commandsFile, indent=4)
        commandsFile.flush()
    updateCommands()

    def shutdown(*args):
        print("pausing all redeems before exit")
        for id in commands:
            request('https://api.twitch.tv/helix/channel_points/custom_rewards','PATCH',
                headers=secret.auth_header,
                params={
                    'broadcaster_id':secret.broadcaster_id,
                    'id':id
                },
                json={
                    'is_paused':True
                }
            )
        print("closing files")
        commandsFile.close()
        print("clean shutdown complete")
    atexit.register(shutdown)
    signal.signal(signal.SIGINT, shutdown)
    if os.name=='nt':
        try:
            import win32.win32api as win32api
            win32api.SetConsoleCtrlHandler(shutdown,True)
        except:
            print('failed to create window close handler, please exit with Ctrl+C instead')

    def sanitize(input:str)->str:
        from string import printable
        filter='<|>;\t\n\r\x0b\x0c'
        return ''.join(char for char in input if char in printable and char not in filter)

    print('startup complete, awaiting redeems')

    while True:
        for id, redeem in commands.items():
            reward=request('https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions',
                headers=secret.auth_header,
                params={
                    'broadcaster_id':secret.broadcaster_id,
                    'reward_id':id,
                    'status':'UNFULFILLED',
                    'after':commands[id]['last'],
                    'first':1
                }
            )
            if 'cursor' not in reward['pagination']:
                time.sleep(1)
                continue
            print(reward)
            commands[id]['last']=reward["pagination"]["cursor"]
            input=sanitize(reward["data"][0]["user_input"])
            command=redeem['command'].replace("$input",input)
            if('waitforexit' in redeem and redeem["waitforexit"]):
                subprocess.run(command)
            else:
                subprocess.Popen(command)
            updateCommands()
            if "update" in redeem:
                request('https://api.twitch.tv/helix/channel_points/custom_rewards/redemptions','PATCH',
                    headers=secret.auth_header,
                    params={
                        'id':reward['data'][0]['id'],
                        'broadcaster_id':secret.broadcaster_id,
                        'reward_id':id
                    },
                    json={
                        'status':redeem['update']
                    }
                )
except Exception as e:
    from tkinter import messagebox
    from traceback import format_exc
    messagebox.showerror('CMDTwitch',format_exc())
    raise e