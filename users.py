import subprocess
from time import sleep as sl
def if_root():
    """
    Check if the user has root access
    :return: True is has access else False
    """
    out = subprocess.Popen(['sudo', 'echo', '"testroot"'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = out.communicate()[0]
    out = str(out, 'utf8')
    if 'testroot' in out:
        return True
    return False


def read_list_of_usres_to_add(path):
    """
    Read list of users to add 
    :param path: path to file
    :return: (list) [[username1, group1], ... , [usernamen, groupn]]
    """
    try:
        new_users = open(path)
        list_users_groups = new_users.readlines()
        list_users_groups = [i.split(':') for i in list_users_groups]
        print(f"Z pliku odczytano {len(list_users_groups)} użytkownika/ów z pliku.")
    except:
        print("TAKI PLIK NIE ISTNIEJE")
        exit()
    return list_users_groups


def remove_break_line(users_list):
    """
    Remove '\n'
    :param users_list: list of users
    :return: list without '\n'
    """
    for index, i in enumerate(users_list):
        if len(users_list[index]) != 2:
            pass
        elif '\n' in i[1]:
            users_list[index][1] = i[1][:len(i[1])-1]
    print("Z pliku usunięto znaki łamania linii")
    return users_list

def list_of_users_in_system():
    """
    Load the list of the users in the system
    :rerurn: list of the users in the system
    """
    out = subprocess.Popen(['sed', 's/:.*//', '/etc/passwd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = out.communicate()[0]
    out = str(out, 'utf8')
    out = out.split()
    return out

def list_of_groups_in_system():
    """
    Load the list of the groups in the system
    :rerurn: list of the groups in the system
    """
    out = subprocess.Popen(['getent', 'group'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = out.communicate()
    out = list(out)
    for i in range(len(out)- 1):
    	out[i] = str(out[i], 'utf8')
    out = out[0].split('\n')
    for i in range(len(out)):
    	out[i] = out[i].split(':')[0]
    return out

def if_user_already_exists(username):
    """
    Check if the user exitst
    :param username: username
    :return: True if exitsts else False
    """
    if username in list_of_users_in_system():
        return True
    return False

def if_group_already_exists(groupname):
    """
    Check if the group exitst
    :param group: username
    :return: True if exitsts else False
    """
    if groupname in list_of_groups_in_system():
        return True
    return False

def create_user(username):
    """
    create user
    :param username: username
    """
    subprocess.Popen(['sudo', 'useradd', f'{username}', '--badnames'])

def create_group(groupname):
    """
    create group
    :para groupname: name of gorup
    """
    subprocess.Popen(['sudo', 'addgroup', f'{groupname[0]}', '--force-badname'])

def add_user_to_group(username, groupname):
    """
    Add user to group
    :param username: username
    :param groupname: groupname
    """
    subprocess.Popen(['sudo', 'addgroup', f'{username}', f'{groupname}'])


if __name__ == "__main__":
    if if_root():
        new_users = 0
        new_groups = 0
        iteration = 0
        list_of_users_to_add = read_list_of_usres_to_add('lista_uzytkownikow.txt')
        list_of_users_to_add = remove_break_line(list_of_users_to_add)
        for i in list_of_users_to_add:
            if not if_group_already_exists(i[1]):
                create_group([i[1]])
                new_groups += 0
                sl(0.5)
            if not if_user_already_exists(i[0]):
                create_user(i[0])
                add_user_to_group(i[0], i[1])
                new_users += 1
            iteration += 1
        print(f"Dodano {new_users} nowych użytkowników.")
        print(f"Dodano {new_groups} nowych grup.")
        print(f"Pominięto {iteration - new_users} użytkowników.")
    else:
        print("ODMOWA DOSTĘPU")
