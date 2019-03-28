from os import listdir
from enum import Enum

RAW_DATA_FOLDER = '/vol/bigdata2/datasets2/LoL/ExtractedData/'
OUTPUT_DATA_FOLDER = '/vol/tensusers2/wstoop/HaRe/datasets/LoL/'

MAXIMUM_NUMBER_OF_PLAYERS = None

ANONYMOUS_NAMES = 'abcdefghijklmnopqrstuvwxyz'

conversation_file = open(OUTPUT_DATA_FOLDER + 'conversations_anon.txt', 'w')

number_of_players_processed = 0

for file in listdir(RAW_DATA_FOLDER):

    if MAXIMUM_NUMBER_OF_PLAYERS != None and number_of_players_processed >= MAXIMUM_NUMBER_OF_PLAYERS:
        break

    print('%nr player processed', number_of_players_processed)

    filename_without_extension = file.replace('.txt', '')
    pseudonyms_for_this_game = {}

    for line_nr, line in enumerate(open(RAW_DATA_FOLDER + file)):

        if line_nr == 0:
            case_nr, total_reports, total_games, punishment, agreement, decision = line.split('|')

            if 'Ban' in decision and 'Overwhelming majority' in agreement:
                pass
            else:
                continue

        elif line[0] == '[':

            try:
                name, timestamp, text = line.strip().split('\t')

            # Sometimes, there are tabs in the message itself
            except ValueError:
                continue

            if 'reported' in name:
                pseudonym = 'TOXIC'
            else:
                if name not in pseudonyms_for_this_game.keys():
                    pseudonyms_for_this_game[name] = ANONYMOUS_NAMES[len(pseudonyms_for_this_game)]

                pseudonym = pseudonyms_for_this_game[name]

            conversation_file.write(pseudonym + '\t' + text.strip() + '\n')

        elif 'Game ' in line and not 'Game type' in line:
            pseudonyms_for_this_game = {}

    number_of_players_processed += 1
    conversation_file.write('#toxic TOXIC\n\n')
