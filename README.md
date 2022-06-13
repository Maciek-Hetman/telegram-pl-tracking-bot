# Telegram tracking bot
This is telegram bot for tracking parcels in Poland.  
It uses official APIs/webservices from carriers.  
The goal is to have bot notifying when your parcel tracking status changes.  
  
Currently supported carriers:  
    - InPost  
    - Poczta Polska  
    - DHL*

### DHL Tracking (if you want to self host this bot)
For tracking DHL packages you need to create account in DHL API Developer Portal to obtain API Key.
Bot will work without it, but DHL tracking will be disabled.

## Bot profile
At the moment there is profile @TeleTrackingBot but I use it for testing and rarely host it for longer than 
10 minutes. I'll update this section when I get VPS to host the bot.

## Usage
Project is still in heavy development.  
Currently available commands:  
```/start```  
```/help```  
```/carriers```  
```/status (tracking number) (carrier)```  
```/track_history (tracking number) (carrier)```  

## Self-hosting
You can self host your own instance of this bot.  
First you need to create your bot with BotFather (use Google or even better DuckDuckGo or SearX if you don't know how to do it).    
Now let's install dependencies:  
```pip install requests zeep python_telegram_bot```  
```python main.py <token> <dhl api key>``` 
Replace ```<token>``` with your bot token mentioned earlier and you're done.  
For dhl api key see DHL section

Note: You might have to use ```pip3``` and ```python3``` command instead of ```pip``` and ```python``` if python2 is still
default on your system (you can check it with ```python --version```). Most Linux distros
use python3 as default interpreter (so ```python --version``` should say it is 3.x.x), but MacOS
still uses python2 as default interpreter.    


## Todo
- [ ] Add DPD support  
- [ ] Add UPS support  
- [ ] Create official bot account:  
    - [ ] Create profile picture for bot  
    - [ ] Get VPS to host it  
    - [ ] Advertise it*  
- [ ] Test reliability in real long term usage  
- [ ] Add more international carriers*  

```*``` - not sure about it
