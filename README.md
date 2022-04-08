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
        "title": "Initial Redeem Name",
        "command": "script-to-run $input",
        "waitforexit": false,
        "update":"STATUS",
        "last": "redeem-instance-id"
    }
}
```

| Key Name | Key Description | Valid Values |
| -------- | --------------- | ------------ |
| twitch-redeem-id | identifier for this redeem | inital value can be anything, this field is updated from twitch when the redeem is created |
| title | display name for redeem | inital value is used to create the redeem, not used or updated afterwards |
| command | command to run on redemtion | this can be any single line, which will be executed by your operating system. Use `$input` to include user input in the command line. |
| waitforexit | optional, whether to wait for the command to exit | true to wait for command to exit, false to continue immediately (default) |
| update | optinal, status to assign to redemption instance | Can be either FULFILLED or CANCELED. Updating to CANCELED will refund the user their Channel Points. |
| last | identifier for the last processed redemption | this field is updated from twitch when a redemption is processed, do not add/edit/remove this field. |