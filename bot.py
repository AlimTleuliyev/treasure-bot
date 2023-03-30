from datetime import datetime

current_time = lambda: datetime.now()
print("Current Time =", current_time())



file = open("log.txt", "a")
file.write(f"\n\n\n\n\n\n\nNEW_SESSION {current_time()} ------------------------------------------------\n\n\n")
print(f"\n\n\n\n\n\n\nNEW_SESSION {current_time()} ------------------------------------------------\n\n\n")
file.close()

import telebot
from telebot import types
print("Bot started")

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

num_of_questions = sum(len(station) for station in ans.values())

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


users = {}
admins = set()

BOT_API_KEY = "" # Put your bot's API key here

bot = telebot.TeleBot(BOT_API_KEY)

def display_stations():
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for point in ans:
		button = types.KeyboardButton(point)
		keyboard.add(button)
		
	button = types.KeyboardButton("Go Back")
	keyboard.add(button)

	button = types.KeyboardButton("Status")
	keyboard.add(button)

	return keyboard

def display_questions(station):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	for question in ans[station]:
		button = types.KeyboardButton(question)
		keyboard.add(button)

	button = types.KeyboardButton("Go Back")
	keyboard.add(button)
	return keyboard

def display_answers_status(team_id):
	res = f"Team {team_id} answers:\n"
	res += f"Solved {sum(sum(station.values()) for station in teams[team_id].values())} out of {num_of_questions}.\n"
	
	for station in teams[team_id]:
		res += f"Station {station}\n"
		for question in teams[team_id][station]:
			res += f"    {question}: " + ("✅" if teams[team_id][station][question] else "❌") + "\n"
	return res

@bot.message_handler(commands=['17admin'])
def display_all(message):
	admins.add(message.chat.id)
	res = ""

	for team_id in teams:
		res += f"Team {team_id}: {sum(sum(station.values()) for station in teams[team_id].values())} / {num_of_questions}\n"

	for team_id in teams:
		res += f"\n{display_answers_status(team_id)}"
	bot.send_message(message.chat.id, res)


@bot.message_handler(commands=['start'])
def start(message):
	name = message.from_user.first_name + (" " + message.from_user.last_name if message.from_user.last_name else "")
	bot.send_message(message.chat.id, f"Hello, {name}! Thank you for participating in Treasure Hunt by AAO!")
	message = bot.send_message(message.chat.id, "What is your team ID? Type 4-digits", reply_markup=types.ReplyKeyboardRemove())
	bot.register_next_step_handler(message, register_user)
	return

def register_user(message):
	if message.text == "exit()" or message.text == "quit()":
		bot.send_message(message.chat.id, "Admin Exit!", reply_markup=types.ReplyKeyboardRemove())
		return

	team_id = message.text

	if team_id in teams:
		users[message.chat.id] = team_id

		if sum(sum(station.values()) for station in teams[team_id].values()) == num_of_questions:
			message = bot.send_message(message.chat.id, "Congratulations!👏🏻🎉 \nYou have solved all the questions!", reply_markup=types.ReplyKeyboardRemove())
			bot.register_next_step_handler(message, finished)
			return

		name = message.from_user.first_name + (" " + message.from_user.last_name if message.from_user.last_name else "")
		username = message.from_user.username
		file = open("log.txt", "a")
		file.write(f"\nNEW_USER LOGGED IN {current_time()} -----------\n")
		file.write(f"Name: {name}\n")
		file.write(f"Username: {username}\n")
		file.write(f"Team ID: {team_id}\n")
		print(f"\nNEW_USER LOGGED IN {current_time()} -----------\n")
		print(f"Name: {name}\n")
		print(f"Username: {username}\n")
		print(f"Team ID: {team_id}\n")
		file.close()
		
		keyboard = display_stations()

		message = bot.send_message(message.chat.id, "Choose the station you are currently at (press the button)\n\n(Press 'Go Back' to go back to choosing the teamID)\n\n(Press 'Status' to check the status of your answers)", reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_station)
		return
	else:
		message = bot.send_message(message.chat.id, f"Team ID {team_id} doesn't exist, try again!\n\nWhat is your group ID? (4-digits)")
		bot.register_next_step_handler(message, register_user)
		return

def choose_station(message):
	if message.text == "exit()" or message.text == "quit()":
		bot.send_message(message.chat.id, "Admin Exit!", reply_markup=types.ReplyKeyboardRemove())
		return

	station = message.text

	if message.text == "Status":
		bot.send_message(message.chat.id, display_answers_status(users[message.chat.id]))
		keyboard = display_stations()
		message = bot.send_message(message.chat.id, "Choose the station you are currently at (press the button)\n\n(Press 'Go Back' to go back to choosing the teamID)\n\n(Press 'Status' to check the status of your answers)")
		bot.register_next_step_handler(message, choose_station)
		return

	if station == "Go Back":
		message = bot.send_message(message.chat.id, "What is your team ID? Type 4-digits", reply_markup=types.ReplyKeyboardRemove())
		bot.register_next_step_handler(message, register_user)
		return
		
	if station in ans:
		if sum(teams[users[message.chat.id]][station].values()) == len(teams[users[message.chat.id]][station]):
			bot.send_message(message.chat.id, f"You have already solved every problem at station {station}")
			keyboard = display_stations()
			message = bot.send_message(message.chat.id, "Choose the station you are currently at (press the button)\n\n(Press 'Go Back' to go back to choosing the teamID)\n\n(Press 'Status' to check the status of your answers)", reply_markup=keyboard)
			bot.register_next_step_handler(message, choose_station)
			return

		keyboard = display_questions(station)

		message = bot.send_message(message.chat.id, f"Which question do you want to submit?\n\n(Press 'Go Back' to go back to choose the station)",reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_question, station)
		return
	else:
		message = bot.send_message(message.chat.id, f"Station {station} doesn't exist! Try again!\n\nChoose the station you are currently at (press the button)\n\n(Press 'Go Back' to go back to choosing the teamID)\n\n(Press 'Status' to check the status of your answers)")
		bot.register_next_step_handler(message, choose_station)
		return


def choose_question(message, station):
	if message.text == "exit()" or message.text == "quit()":
		bot.send_message(message.chat.id, "Admin Exit!", reply_markup=types.ReplyKeyboardRemove())
		return

	question = message.text
	if question == "Go Back":
		keyboard = display_stations()
		message = bot.send_message(message.chat.id, "Choose the station you are currently at (press the button)\n\n(Press 'Go Back' to go back to choosing the teamID)\n\n(Press 'Status' to check the status of your answers)", reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_station)
		return

	if question in ans[station]:
		if teams[users[message.chat.id]][station][question] == True:
			bot.send_message(message.chat.id, "You have already answered this question!")
			keyboard = display_questions(station)
			message = bot.send_message(message.chat.id, f"Which question do you want to submit?\n\n(Press 'Go Back' to go back to choose the station)",reply_markup=keyboard)
			bot.register_next_step_handler(message, choose_question, station)
			return

		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button = types.KeyboardButton("Go Back")
		keyboard.add(button)
		
		message = bot.send_message(message.chat.id, f"Enter your answer to {question} at station {station} (press 'Go back' if you want to go back to choosing the qeustion'):",reply_markup=keyboard)
		bot.register_next_step_handler(message, check_answer, station, question)
		return
	else:
		keyboard = display_questions(station)
		message = bot.send_message(message.chat.id, f"No such question {question}. Try pressing the button!\nWhich question do you want to submit?\n\n(Press 'Go Back' to go back to choose the station)",reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_question, station)
		return

def check_answer(message, station, question):
	if message.text == "exit()" or message.text == "quit()":
		bot.send_message(message.chat.id, "Admin Exit!", reply_markup=types.ReplyKeyboardRemove())
		return

	answer = message.text

	if question == "Go Back":
		keyboard = display_questions(station)
		message = bot.send_message(message.chat.id, f"Which question do you want to submit at station {station}?\n\n(Press 'Go Back' to go back to choosing the station)",reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_question, station)
		return
	
	answer = answer.lower().strip()
	
	if ans[station][question] == answer:
		team_id = users[message.chat.id]
		teams[team_id][station][question] = True
		
		bot.send_message(message.chat.id, "Your answer is correct!")
		bot.send_message(message.chat.id, display_answers_status(team_id))


		file = open("log.txt", "a")
		file.write(f"\nNEW_SOlUTION {current_time()} -----------\n")
		file.write(f"TEAM {team_id} SOLVED {question} AT {station}\n")
		file.write(display_answers_status(team_id))
		print(f"\nNEW_SOlUTION {current_time()} -----------\n")
		print(f"TEAM {team_id} SOLVED {question} AT {station}\n")
		print(display_answers_status(team_id))
		file.close()

		if sum(sum(station.values()) for station in teams[team_id].values()) == num_of_questions:
			
			for admin in admins:
				bot.send_message(admin, f"⚠️⚠️⚠️TEAM_{team_id}_FINISHED {current_time()} -----------\n")


			file = open("log.txt", "a")
			file.write(f"\n⚠️⚠️⚠️TEAM_{team_id}_FINISHED {current_time()} -----------\n")
			print(f"\n⚠️⚠️⚠️TEAM_{team_id}_FINISHED {current_time()} -----------\n")
			file.close()
			
			message = bot.send_message(message.chat.id, "Congratulations!👏🏻🎉 \nYou have solved all the questions!", reply_markup=types.ReplyKeyboardRemove())
			bot.register_next_step_handler(message, finished)
			return


		keyboard = display_questions(station)
		message = bot.send_message(message.chat.id, f"Which question do you want to submit at station {station}?\n\n(Press 'Go Back' to go back to choosing the station)",reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_question, station)
		return
	else:
		keyboard = display_questions(station)
		message = bot.send_message(message.chat.id, f"Answer is incorrect! Try again! \nWhich question do you want to submit?\n\n(Press 'Go Back' to go back to choosing the station)",reply_markup=keyboard)
		bot.register_next_step_handler(message, choose_question, station)
		return

def finished(message):
	if message.text == "exit()" or message.text == "quit()":
		bot.send_message(message.chat.id, "Admin Exit!", reply_markup=types.ReplyKeyboardRemove())
		return
	message = bot.send_message(message.chat.id, "You have already finished! Now, relax 😮‍💨", reply_markup=types.ReplyKeyboardRemove())
	bot.register_next_step_handler(message, finished)
	return

print("polling")
bot.polling(none_stop=True, interval=0)
