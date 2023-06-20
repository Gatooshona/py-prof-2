import re
import csv

# Читаем адресную книгу в формате CSV в список contacts_list:
with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    # pprint(contacts_list)


new_contacts_list = []
final_contact_list = []


def fix_names():
    for contact in contacts_list:
        for index, value in enumerate(contact):
            if index == 0:
                first_cell = value.split(' ')
                if len(first_cell) == 3:
                    contact[2] = first_cell[2]
                    contact[1] = first_cell[1]
                    contact[0] = first_cell[0]
                if len(first_cell) == 2:
                    contact[1] = first_cell[1]
                    contact[0] = first_cell[0]

            if index == 1:
                second_cell = value.split(' ')
                if len(second_cell) == 2:
                    contact[2] = second_cell[1]
                    contact[1] = second_cell[0]
        new_contacts_list.append(contact)
    print('Names fixed')


def change_phones():
    pattern_phone = r'(\+7|8)\s*\D?(\d{3})\D?\s*(\d{3})\D?\s*(\d{2})\D?\s*(\d{2})\s*\(?([а-я]{0,3}\.)?\s*(\d{4})?\)?'
    subs_phone = r'+7(\2)\3-\4-\5 \6\7'
    for i, el in enumerate(new_contacts_list):
        el[5] = re.sub(pattern_phone, subs_phone, el[5])
        new_contacts_list[i] = el

    print('Phones fixed')


def del_doubles():
    names_list = {}

    for i, contact in enumerate(new_contacts_list[1:]):
        key = contact[0] + contact[1]

        if key not in names_list:
            names_list.update({key: contact})

        if key in names_list:
            for idx, entity in enumerate(names_list[key]):

                if entity == '':
                    names_list[key][idx] = contact[idx]

    final_contact_list.append(list(names_list.values()))
    print('Doubles deleted')


if __name__ == '__main__':
    fix_names()
    change_phones()
    del_doubles()


with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(final_contact_list[0])
