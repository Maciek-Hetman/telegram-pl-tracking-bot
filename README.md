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

