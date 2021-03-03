import os


def fetch_logs():
    """
    Function to fetch the logs from otitsunii-server
    Requires ssh keys and passwordless to be setup for the computer and server used
    Otitsunii-credentials also required
    """
    name = input("Insert logged channel name > ") + ".log"
    username = input("Insert your username > ")
    os.system("scp {}@otitsunii.oulu.fi:~/irclogs/IRCnet/{} {}".format(username, name, os.path.dirname(os.path.realpath(__file__))))

def parse(filename):
    """
    Function to parse the log file and make it into a list that is formatted in the following way:
    [name1, message1, time1], [name2, message2, time2], ...
    """
    rfile = open(filename, "r")
    content = rfile.read()
    rfile.close()

    content = content.split("\n")
    temp = []
    while content:
        line = content.pop()
        if '---' in line or '-!-' in line:
            continue
        else:
            temp.append(line)
    temp.reverse()
    for n in temp:
        t = n.split('<')
        if len(t) > 1:
            s = t[1].split('>')
            s.append(t[0])
            for x in range(len(s)):
                s[x] = s[x].removeprefix(' ')
                s[x] = s[x].removeprefix('@')
                s[x] = s[x].removesuffix(' ')
            content.append(s)
    return content

def filter(content):
    """
    Function to filter the parsed content and display it message by message in the console
    """
    edit_content = content.copy()
    while True:
        temp = []
        what = input("""How do you want to filter the content? | (r)eset | (q)uit
(n)ame
(s)tring
(t)ime
> """)
        if what == 'n':
            how = str(input("Insert name > "))
            for n in edit_content:
                if n[0] == how:
                    temp.append(n)
        elif what == 's':
            how = str(input("Insert string > "))
            for n in edit_content:
                if how in n[1]:
                    temp.append(n)
        elif what == 't':
            how = str(input("Insert time (HH:MM) > "))
            for n in edit_content:
                if n[2] == how:
                    temp.append(n)
        elif what == 'r':
            print("Resetting...")
            edit_content = content.copy()
            continue
        elif what == 'q':
            print("Quitting...")
            break
        else:
            print("Invalid input!")
            continue
        for n in temp:
            print("{time} | {name} | {content}".format(time=n[2], name=n[0], content=n[1]) )
        print("Number of messages: ", len(temp))
        edit_content = temp.copy()

def dictionarize(content):
    """
    Function to turn the messages into a dictionary that displays the name of user
    and the amount of criteria-fulfilling messages form said user
    """
    counts = {}
    while True:
        what = input("""How do you want to filter the content to list?
(s)tring
(t)ime
(st)ring and time
> """)
        if what == "s":
            how = input("Insert string > ")
            for n in content:
                if n[0] not in counts and how in n[1]:
                    counts[n[0]] = 1
                elif n[0] in counts and how in n[1]:
                    counts[n[0]] += 1
                else:
                    continue
            break
        elif what == "t":
            how = input("Insert time (HH:MM) > ")
            for n in content:
                if n[0] not in counts and n[2] == how:
                    counts[n[0]] = 1
                elif n[0] in counts and n[2] == how:
                    counts[n[0]] += 1
                else:
                    continue
            break
        elif what == "st":
            show = input("Insert string > ")
            thow = input("Insert time (HH:MM) > ")
            for n in content:
                if n[0] not in counts and show in n[1] and n[2] == thow:
                    counts[n[0]] = 1
                elif n[0] in counts and show in n[1] and n[2] == thow:
                    counts[n[0]] += 1
                else:
                    continue
            break
        else:
            print("Invalid input!")
            continue

    countlist = sorted(counts.items(), key=lambda x:x[1])
    sortdict = dict(countlist)
    for n in sortdict:
        print(n, sortdict[n])
        


while True:
    what = input("Do you want to fetch logs from (s)erver or parse (l)ocal files? > ")
    if what == "s":
        fetch_logs()
    elif what == "l":
        filename = input("Insert log file name > ")
        parsed = parse(filename)
        option = input("""What do you want to do?
(d)ictionarize
(f)ilter
> """)
        if option == "f":
            filter(parsed)
        elif option == "d":
            dictionarize(parsed)
        else:
            continue
        break
    else:
        print("Invalid input")
