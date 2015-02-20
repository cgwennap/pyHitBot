# pyHitBot

This is a simple python template for programming a bot to read and interact with the hitbox.tv chat interface. The goal of this program is to support the hitbox community and get programmers past the specifics of the hitbox websocket protocol and programming actual functionality for a bot.

## External Dependencies

To install websocket library, use the command `sudo pip install websocket-client`. Do NOT use pip install websocket, as this is a different library which has name conflicts.

## To run

1. Change values in botvalues.json to match your bot's username and password, as well as the channel it will be joining.

2. run "python testsocket.py"

Upon successful connection, the bot should join the correct channel, post "BOT IS ONLINE", and echo all incoming chats from other users with the preface "BOT -".

## To modify

Every time the program receives a message from hitbox, the function "on_message(ws, message)" gets called. 95% of all modification should occur within this function.

You may also wish to change the channel joining message, found in "on_join".

Any runtime error will be caught and redirected to the function "on_error", common actions are to "raise error" or "print error" depending on how forgiving the program should be.

Finally, websocket.enableTrace(True) is extremely useful when debugging protocol errors. However, in ordinary circumstances, enableTrace is set to False to clean up its .
