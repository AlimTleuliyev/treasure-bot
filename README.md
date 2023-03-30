# Treasure Bot
Telegram Bot written on Python for Treasure Hunt Game.

Contact me at alim.tleuliyev@nu.edu.kz if you have any questions!
# Installation
```bash
$ git clone https://github.com/AlimTleuliyev/treasure-bot.git
$ cd treasure-bot
$ pip install -r requirements.txt
```
# Set up
1. Create a new Telegram bot using Bot Father
2. Copy and paste your new bot's api key into bot.py file
```python
68. BOT_API_KEY = "" # Put your bot's API key here
```
3. Edit the ans python dictionary in bot.py file. Each key in the dictionary represents that station name and each value of the dictionary is another dictionary of question-answer key-value pairs.
```python
ans = {
        "AAO Tutors Office" : {"Q1": "algorithm"},
        
        "6inch" : {"Q1": "1000",
        	   "Q2": "3", 
        	   "Q3": "40",
        	   "Q4": "28",
        	   "Q5":  "2",
        	   "Q6":  "3", 
        	   "Q7":  "11", 
        	   "Q8":  "330"},
        
        "Kunde" : {"Q1": "apple"},
        
        "Corner" : {"Q1": "7", 
        	    "Q2": "22",
        	    "Q3": "6",
        	    "Q4": "16",
        	    "Q5": "cone"},
        
        "Green Spot" : {"Q1": "acdc"},
        
        "AAO Fellows Office" : {"Q1": "2",
        	                "Q2": "120",
        	                "Q3": "0",
        	                "Q4": "turing",
        	                "Q5": "0.25"},
        
        "Daily Cup" : {"Q1": "pascal"},
        
        "First Floor GSB" : {"Q1": "042"}
    }
```
4. You can also edit the team id's
```python
teams = {
	  "7522" : {station: {question: False for question in ans[station]} for station in ans},
	  "4132" : {station: {question: False for question in ans[station]} for station in ans},
	  "9075" : {station: {question: False for question in ans[station]} for station in ans},
	  "2042" : {station: {question: False for question in ans[station]} for station in ans},
	  "5795" : {station: {question: False for question in ans[station]} for station in ans},
	  "4507" : {station: {question: False for question in ans[station]} for station in ans},
	  "9736" : {station: {question: False for question in ans[station]} for station in ans},
	  "1083" : {station: {question: False for question in ans[station]} for station in ans},
	  "adminteam" : {station: {question: False for question in ans[station]} for station in ans}
	}
```
5. Find this line in code and change the admin's command if you want:
```python
@bot.message_handler(commands=['17admin'])
```
  Right now if you send /17admin to the bot it will print the status of all the questions across all the teams
6. User can start the bot using /start command, after that they cannot stop. Only admins can stop by sending "quit()" or "exit"
7. Run the bot:
```python
$ python bot.py
```
9. Everything else is pretty easy to understand as you try to play with the bot. 
