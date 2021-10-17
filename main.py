import json
options = ['set practice', 'multi practice', 'mega set', 'new set', 'edit set']


class AllCards:
    """This class takes in data from a json file and stores it.
    It makes a list of all available card set options.
    It also handles the selection for single, and multi card sets."""

    def __init__(self, all_data):
        self.set_options = [set_parse for set_parse in all_data]
        self.dict_data = all_data

    def call_options(self):
        for set_o in self.set_options:
            print(set_o)

    def single_set_choice(self):
        print('Select a set to practice: ')
        self.call_options()
        while True:
            user_choice = input('Enter a single selection: ')
            if user_choice in self.set_options:
                print(f'{user_choice} selected!')
                break
            else:
                print('Input invalid, please try again.')
        return self.dict_data[user_choice]

    def multi_set_choice(self):
        self.call_options()
        choices_left = self.set_options.copy()
        selected = []
        selected_choices = {}
        while True:
            poly_choice = input('Select sets to practice with, then type "quit" ')
            if poly_choice.lower() == 'quit':
                break
            elif poly_choice in selected:
                print('Set has already been added')
            elif poly_choice in choices_left:
                selected_choices.update(self.dict_data[poly_choice])
                selected.append(choices_left.pop(choices_left.index(poly_choice)))
                print(f'{poly_choice} added to multiset!')
                print(f'Options left: {choices_left}')
            else:
                print('input was not in options list\nTry entering that again!')
        return selected_choices


def start_menu():
    """Gives you the options you have and returns an integer to be passed to the
    choice select function"""
    for count, mode in enumerate(options):
        print(f'{mode.upper()} ({count + 1})')
    while True:
        select = input('type in the mode(or enter a number): ')
        if select.lower() in options:
            print(f'{select.upper()} Selected!')
            return options.index(select.lower())
        elif select.lower() == 'quit':
            return 'quit'
        elif select == '':
            print('Invalid Input')
        elif select in '12345':
            print(f'{options[int(select) - 1].upper()} Selected!')
            return int(select) - 1
        else:
            print('Invalid Input')


def card_cycle(cards_cycle):
    """Function is used to cycle through the cards when in practice mode"""
    for item in cards_cycle:
        input('View the term: ')
        print(f'\t{item}')
        input('View the definition: ')
        print(f'\t{cards_cycle[item]}')


def set_practice():
    current_set = card_sets.single_set_choice()
    card_cycle(current_set)


def multi_practice():
    current_set = card_sets.multi_set_choice()
    card_cycle(current_set)


def mega_set():
    mega_s = {}
    for item in card_sets.dict_data:
        mega_s.update(card_sets.dict_data[item])
    card_cycle(mega_s)


def new_set():
    """allows you to add new items
     had to slightly change the code to allow for the initial json file creation"""
    print('Add your term and definition\nEnter "quit" at any time')
    empty_dic = {}
    while True:
        term = input('Enter the term: ')
        if term == 'quit':
            break
        definition = input('Enter the definition: ')
        if definition == 'quit':
            break
        empty_dic[term] = definition
    set_name = input('Name your set: ')
    return set_name, empty_dic


def file_class_update(set_name, empty_dic):
    """created specifically to add new items to the AllCards class
    and adds it to the json file"""
    card_sets.dict_data[set_name] = empty_dic
    card_sets.set_options.append(set_name)
    with open('CardData.txt', 'w+') as file:
        json.dump(card_sets.dict_data, file, indent=2)


def edit_set():
    """I'm not proud of this:
    edit_set contains multiple nested functions within
    in order to have all the functionality(adding cards to a set, deleting a set, or editing cards.
    random use of x = 1 variable it to exit out of both loops"""
    print('Welcome to the editor: ')

    def edit(set_option):
        for card in card_sets.dict_data[set_option]:
            print(f'{card}: {card_sets.dict_data[set_option][card]}')
        card_choice = input('Enter a card to edit or delete: ')
        if card_choice.lower() == 'quit':
            return 'quit'
        if card_choice in card_sets.dict_data[set_option]:
            edit_delete_card = input("Would you like to 'edit' or 'delete' card? ")
            if edit_delete_card == 'edit':
                update_term = input('Hit enter to skip adding\nEnter updated term name: ')
                update_definition = input('Enter updated definition: ')
                if update_term == '':
                    update_term = card_choice
                if update_definition == '':
                    update_definition = card_sets.dict_data[set_option][card]
                card_sets.dict_data[set_option].__delitem__(card_choice)
                card_sets.dict_data[set_option][update_term] = update_definition
            elif edit_delete_card == 'delete':
                confirm_card_del = input(f'Are you sure want to delete:\n{card_choice}: {card_sets.dict_data[set_option][card_choice]}\nyes/no: ')
                if confirm_card_del == 'yes':
                    del card_sets.dict_data[set_option][card_choice]
                elif confirm_card_del == 'no':
                    print('Returning to menu')
            elif edit_delete_card == 'quit':
                pass
        else:
            print('Invalid input')

    def delete(set_delete):
        yes_no = input(f'Are you sure you want to delete(yes/no): {set_delete} ')
        if yes_no.lower() == 'yes':
            print(f'{set_delete} has been deleted')
            del card_sets.dict_data[set_delete]
            return 1
        elif yes_no.lower() == 'no':
            return 1

    def add_set_cards(set_add):
        print(f'Enter terms to add to {set_add}\nType "quit" when finished')
        while True:
            term_add = input('Enter the term name: ')
            if term_add.lower() == 'quit':
                return 1
            defi_add = input('Enter the definition for the term: ')
            if defi_add.lower() == 'quit':
                return 1
            card_sets.dict_data[set_add][term_add] = defi_add
            print(f'''{term_add} has been added to {set_add}''')

    while True:
        for item in card_sets.dict_data:
            print(item)
        select_set = input('Choose a set to edit: ')
        if select_set in card_sets.dict_data:
            print(f'{select_set} Selected')
            while True:
                edit_delete = input("Would you like to 'edit'(1) or 'delete(2)' or 'add(3)'")
                if edit_delete == 'edit' or edit_delete == '1':
                    while True:
                        x = 0
                        returned = edit(select_set)
                        if returned == 'quit':
                            x = 1
                            break
                elif edit_delete == 'delete' or edit_delete == '2':
                    x = delete(select_set)
                elif edit_delete == 'add' or edit_delete == '3':
                    x = add_set_cards(select_set)
                elif edit_delete == 'quit':
                    pass
                else:
                    print('Invalid input')
                try:
                    if x == 1:
                        break
                except UnboundLocalError:
                    pass
                if edit_delete.lower() == 'quit':
                    break
        elif select_set == 'quit':
            return 'quit'
        else:
            print('Invalid Input')


def choice_select(select):
    """This function is used to select which function will be ran"""
    if select == 0:
        set_practice()
    elif select == 1:
        multi_practice()
    elif select == 2:
        mega_set()
    elif select == 3:
        set_name, data = new_set()
        file_class_update(set_name, data)
    elif select == 4:
        edit_set()


def initialize():
    """On the first load time, if a file of 'CardData' is not found, it forces you to create your first set
    after which it loads it to the file, and then opens that file and passes it to the AllCards class
    was having trouble executing the script if the first set was not imported from the json file."""
    try:
        with open('CardData.txt', 'r') as file:
            file_load = AllCards(json.load(file))
    except FileNotFoundError:
        print('No file or contents found!\nStart by making a new set!')
        first_set, data = new_set()
        sets = {first_set: data}
        with open('CardData.txt', 'w') as file:
            json.dump(sets, file, indent=2)
        with open('CardData.txt', 'r') as file:
            file_load = AllCards(json.load(file))
    return file_load


print('Welcome to Flash Practice!\nChoose an option below:')
card_sets = initialize()
while True:
    choice = start_menu()
    if choice == 'quit':
        break
    choice_select(choice)
