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

## Self-hosting
You can self host your own instance of this bot.  
First you need to create your bot with BotFather (use Google or even better DuckDuckGo or SearX if you don't know how to do it).    
Now let's install dependencies:  
```pip install requests zeep python_telegram_bot```  
```python main.py <token>``` 
Replace ```<token>``` with your bot token mentioned earlier and you're done.  
  
Note: You might have to use ```pip3``` and ```python3``` command instead of ```pip``` and ```python``` if python2 is still
default on your system (you can check it with ```python --version```). Most Linux distros
use python3 as default interpreter (so ```python --version``` should say it is 3.x.x), but MacOS
still uses python2 as default interpreter.    
