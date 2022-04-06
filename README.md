# CMDTWITCH 2

Run commands on your pc for twitch redeems.

[Join the Discord](https://discord.gg/zxDnYSvMNw) if you need help.

## Usage

1. Download this repo
2. Edit `cmdtwitch.json` to add your commands
3. Run `cmdtwitch.py` to generate the `secret.py` template
4. Create a bot using the url at the top of `secret.py`. DO NOT GIVE ANYONE YOUR BOT SECRETS.
5. Edit `secret.py`, adding your bot secrets and username
6. Run `cmdtwitch.py`
7. ...
8. Profit!

## Config

### `cmdtwitch.json`

```json
{
    "twitch-redeem-id": {
        "title": "Name of Redeem",
        "command": "script-to-run $input",
        "waitforexit": false,
        "last": "redeem-instance-id"
    }
}
```

- **The redeem ID is assigned by twitch and required to check for redemptions**. When adding a command for the first time, you can put anything for the `twitch-redeem-id`, because when the redeem id is invalid, cmdtwitch will create the redeem. If you accidentally edit your redeem id, you'll have to delete the redeem from your chanel and let cmdtwitch re-create it.

- **CMDTwitch can only track redeems it created**. This is a limitation of the twitch api, which was designed for these bots to run on internet-accessible servers (support coming eventually).

- **The title is only set when the redeem is created**. CMDTwitch will automatically pause its redeems when it exits, but otherwise only checks for redemptions after it's created.

- **You must enable viewer input after the redeem is created to use `$input` in your command**. All other properties of the redeem can be changed at will, including the title, without affecting CMDTwitch.

- **If your command takes more than a few seconds, set `waitforexit` to `false`**, otherwise all other redeems will have to wait for that command to finish.