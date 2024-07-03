import json
import os
import random
import shutil
from io import StringIO
import argparse


def add():
    add_term = input('The card:\n')
    memory_file.write(add_term + "\n")
    while add_term in flashcard_dict.keys():
        duplicate_card = f'The card "{add_term}" already exists. Try again:'
        memory_file.write(duplicate_card)
        print(duplicate_card)
        add_term = input('The card:\n')

    add_definition = input('The definition of the card:\n')
    memory_file.write(add_definition + "\n")

    while f'{add_definition}' in definition_list:
        duplicate_definition = f'The definition "{add_definition}" already exists. Try again:'
        memory_file.write(duplicate_definition)
        print(duplicate_definition)
        add_definition = input('The definition of the card:\n')
        memory_file.write(add_definition + "\n")

    definition_list.append(add_definition)
    flashcard_dict[add_term] = {'card_definition': add_definition, 'mistakes_number': 0}
    card_def_pair = f'The pair ("{add_term}":"{add_definition}") has been added.'
    memory_file.write(card_def_pair + "\n")
    print(card_def_pair)


def remove():
    card_to_remove = input('Which card?\n')
    memory_file.write(card_to_remove + "\n")

    if card_to_remove in flashcard_dict.keys():
        del flashcard_dict[card_to_remove]
        removed_card = 'The card has been removed'
        memory_file.write(removed_card + "\n")
        print(removed_card)
    else:
        missing_card = f"Can't remove {card_to_remove}: there is no such card."
        memory_file.write(missing_card + "\n")
        print(missing_card)


def _import(file_name):
    global flashcard_dict
    memory_file.write(file_name + "\n")

    if os.path.isfile(file_name):
        try:
            with open(file_name, 'r') as file:
                import_dict = json.loads(file.read())
                cards_loaded = f'{len(import_dict)} cards have been loaded.'
                memory_file.write(cards_loaded + "\n")
                print(cards_loaded)
                flashcard_dict.update(import_dict)
        except ValueError:
            pass
    else:
        memory_file.write('File not found.\n')
        print('File not found.')


def _export(file_name_export):
    memory_file.write(file_name_export + "\n")

    with open(file_name_export, 'w') as add_file:
        json.dump(flashcard_dict, add_file)

    cards_saved = f'{len(flashcard_dict)} cards have been saved.'
    memory_file.write(cards_saved + "\n")
    print(cards_saved)


def ask():
    try:
        number_of_cards = int(input('How many times to ask?:\n'))
        memory_file.write(str(number_of_cards) + "\n")
        for x in range(number_of_cards):
            random_card = random.choice(list(flashcard_dict.keys()))
            failed = False
            answer = input(f'Print the definition of "{random_card}"\n')
            memory_file.write(answer + "\n")

            if answer == flashcard_dict[random_card]['card_definition']:
                memory_file.write('Correct!\n')
                print('Correct!')
            else:
                for d in flashcard_dict:
                    if answer != flashcard_dict[d]['card_definition']:
                        continue
                    else:
                        wrong_card_g = (f'Wrong. The right answer is {flashcard_dict[random_card]["card_definition"]}, '
                                        f'but your definition is correct for {d}')
                        memory_file.write(wrong_card_g + "\n")
                        print(wrong_card_g)
                        flashcard_dict[random_card]['mistakes_number'] += 1
                        failed = True

                if not failed:
                    wrong_card = f'Wrong. The right answer is {flashcard_dict[random_card]["card_definition"]}'
                    memory_file.write(wrong_card + "\n")
                    print(wrong_card)
                    flashcard_dict[random_card]['mistakes_number'] += 1
    except ValueError:
        memory_file.write('The value for the ask option must be an integer\n')
        print('The value for the ask option must be an integer')


def log():
    log_name = input("File name:\n")
    memory_file.write(log_name + "\n")

    with open(log_name, "w") as log_file:
        memory_file.seek(0)
        shutil.copyfileobj(memory_file, log_file)
        memory_file.write('The log has been saved.\n')
        print('The log has been saved.')


def hardest_card():
    max_value = 0
    hardest_cards = []
    for i in flashcard_dict:
        if flashcard_dict[i]['mistakes_number'] > max_value:
            max_value = flashcard_dict[i]['mistakes_number']
            hardest_cards = [i]
        elif flashcard_dict[i]['mistakes_number'] == max_value and max_value != 0:
            hardest_cards.append(i)
        else:
            continue
    if max_value == 0:
        memory_file.write('There are no cards with errors.\n')
        print('There are no cards with errors.')

    elif len(hardest_cards) == 1:
        hard_card = f'The hardest card is "{hardest_cards[0]}". You have {max_value} errors answering it'
        memory_file.write(hard_card + "\n")
        print(hard_card)

    else:
        card_string = ', "'.join(hardest_cards)
        hard_cards = f'The hardest cards are "{card_string}". You have {max_value} errors answering them'
        memory_file.write(hard_cards + "\n")
        print(hard_cards)


def reset_stats():
    for i in flashcard_dict:
        flashcard_dict[i]['mistakes_number'] = 0
    memory_file.write('Card statistics have been reset.\n')
    print('Card statistics have been reset.')


def exit_func():
    print('Bye bye!')


flashcard_dict = {}
definition_list = []

memory_file = StringIO()
memory_file.read()

parser = argparse.ArgumentParser()
parser.add_argument("--import_from", help="This argument import the initial flashcard data from a file"
                                          "at the beginning of the script")
parser.add_argument("--export_to", help="This argument exports the initial flashcard data to a file"
                                        "at the end of the script")
args = parser.parse_args()
import_file = args.import_from
export_file = args.export_to

if import_file is not None:
    _import(import_file)

action = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)\n')
memory_file.write(action + "\n")
exit_bool = True

while action != 'exit':
    while action not in ('add', 'remove', 'import', 'export', 'ask', 'log', 'hardest card', 'reset stats', 'exit'):
        print('Please select one of the requested actions. Other words are not valid.')
        action = input('add, remove, import, export, ask, exit, log, hardest card, reset stats)\n')

    if action == 'add':
        add()
    elif action == 'remove':
        remove()
    elif action == 'import':
        import_file = input('File name:\n')
        _import(import_file)
    elif action == 'export':
        export_file = input('File name:\n')
        _export(export_file)
    elif action == 'ask':
        ask()
    elif action == 'hardest card':
        hardest_card()
    elif action == 'reset stats':
        reset_stats()
    elif action == 'log':
        log()
    else:
        exit_bool = False

    if exit_bool is True:
        action = input('Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats)\n')
        memory_file.write(action + "\n")
else:
    memory_file.write("exit\n"
                      "Bye bye!\n")
    exit_func()
    if export_file is not None:
        _export(export_file)
