def parse(filename):
    rfile = open(filename, "r")
    content = rfile.read()
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
                s[x] = s[x].removesuffix(' ')
            content.append(s)
    return content

def filter(content):
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
        
filename = str(input("filename > "))
filter(parse(filename))


"""
features:
-show all messages from user
-show all messages containing a certain string
-show all messages from user containing a certain string
-show all messages containing a certain string at a certain time
-show all messages from user containing a certain string at a certain time

-count messages from user
-count messages at a certain time time
-count messages containing a certain string
-count messages from user containing a certain string
-count messages from user containing a certain string at a certain time
-count messages containing a certain string at a certain time
"""