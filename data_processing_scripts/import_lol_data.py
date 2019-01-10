from os import listdir
from enum import Enum

RAW_DATA_FOLDER = '/vol/bigdata2/datasets2/LoL/ExtractedData/'
OUTPUT_DATA_FOLDER = '/vol/tensusers2/wstoop/HaRe/datasets/LoL/'

MERGE_REPORTED_PLAYER = False
MAXIMUM_NUMBER_OF_PLAYERS = 1500

class PunishmentType(Enum):

    warning = 0
    time_ban = 1

PUNISHMENT_TYPE_TO_FOLDER = {None: 'nontoxic/',
							  PunishmentType.warning:'nontoxic/',
							  PunishmentType.time_ban:'toxic/'}	
	
class Player():

    def __init__(self,name):

        self.chat_messages = []
        self.punishment_type = None
        self.name = name
        self.characters = []
        self.game_outcomes = []

    def calculate_average_chat_frequency(self):

        try:
            return len(self.chat_messages) / len(self.game_outcomes)
        except ZeroDivisionError:
            return 0
	
number_of_players_processed = 0
	
for file in listdir(RAW_DATA_FOLDER):

	if number_of_players_processed >= MAXIMUM_NUMBER_OF_PLAYERS:
		break

	print('%nr player processed',number_of_players_processed)

	filename_without_extension = file.replace('.txt','')
	players_per_game = {1:{}}

	#There are multiple games in a file, keep track of which game this is
	current_game_nr = 1
	last_game_won = None

	for line_nr,line in enumerate(open(RAW_DATA_FOLDER+file)):

		if line_nr == 0:
			case_nr, total_reports, total_games, punishment, agreement, decision = line.split('|')

			if 'Warning' in punishment:
				current_punishment_type = PunishmentType.warning
			elif 'Time Ban' in punishment:
				current_punishment_type = PunishmentType.time_ban
			else:
				current_punishment_type = None

		if line.strip() in ['Game 2','Game 3','Game 4','Game 5','Game 6','Game 7','Game 8','Game 9']:
			current_game_nr = int(line[-2])
			players_per_game[current_game_nr] = {}

		elif 'Game outcome:' in line:

			last_game_won = 'Win' in line

		elif line[0] == '[':

			try:
				name, timestamp, text = line.strip().split('\t')

			#Sometimes, there are tabs in the message itself
			except ValueError:
				continue

			name = name.replace(' [All]','')
			current_character = name.split(']')[-1]

			if name not in players_per_game[current_game_nr].keys():
				new_player = Player(name)
				new_player.characters.append(current_character)
				new_player.game_outcomes.append(last_game_won)

				if '[reported]' in name:
					new_player.punishment_type = current_punishment_type

				players_per_game[current_game_nr][name] = new_player

			players_per_game[current_game_nr][name].chat_messages.append(text)

	if MERGE_REPORTED_PLAYER:

		reported_player = Player('.reported.merged')

		for game_nr, players_of_one_game in players_per_game.items():

			players_without_punishment = {}

			for player in players_of_one_game.values():

				if player.punishment_type == None:
					players_without_punishment[player.name] = player
				else:

					#Add all info of this player into the merged player
					reported_player.chat_messages += player.chat_messages
					reported_player.punishment_type = player.punishment_type
					reported_player.characters.append(player.characters[0]) #Non-merged players can only have 1 char
					reported_player.game_outcomes.append(player.game_outcomes[0])

			players_per_game[game_nr] = players_without_punishment

		#The reported player as a whole is added to the latest match
		players_per_game[game_nr][reported_player.name] = reported_player

	number_of_players_processed += 1
	
	#Save the whole thing
	for n, game in enumerate(players_per_game.values()):
		for player_name, player in game.items():
			open(OUTPUT_DATA_FOLDER+PUNISHMENT_TYPE_TO_FOLDER[player.punishment_type]+filename_without_extension+'.'+str(n)+'_'+player_name,'w').write('\n'.join(player.chat_messages))
