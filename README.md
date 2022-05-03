# Telegram tracking bot
This is telegram bot for tracking parcels in Poland.  
It uses official APIs/webservices from carriers.  
The goal is to have bot notyfying about parcel updates.  
For now you can only check parcel status and history via commands.   
Currently supported carriers:  
    - InPost  
    - Poczta Polska 

## Usage
Project is still in heavy development.  
Currently available commands:  
/track (tracking number) (carrier)  
/track_history (tracking number) (carrier)
/help
/carriers

### Examples
/track (number) Poczta Polska  
/track (number) InPost  
/track (number) inpost  
/track (number) pp  

## Self-hosting
You can self host your own instance of this bot.  
First you need to create your bot with BotFather.  
You'll get from it token to access Telegram API - save it somewhere, we'll need it later.  
Now let's install dependencies:  
```pip install requests zeep python_telegram_bot```  
Note: You might have to use ```pip3``` command instead of ```pip``` if python2 is still
default on your system (you can check it with ```python --version```). Most Linux distros
use python3 as default interpreter (so ```python --version``` should say it 3.x.x), but MacOS
still uses python2 as default interpreter.  
Moving on, we can now start the bot:  
```python main.py <token>``` 
Replace ```<token>``` with your bot token mentioned earlier.  
Now you can message with your bot.
 