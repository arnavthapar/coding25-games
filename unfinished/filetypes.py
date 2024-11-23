from random import randrange
files = {1:[[".py", ".pyt"]],
         2:[],
         3:[],
         4:[],
         5:[],
         6:[]}
desc = {1:["the file type for python code."],
         2:[],
         3:[],
         4:[],
         5:[],
         6:[]}
for i in range(6):
    print(f"Round {i+1}")
    for i in range(5):
        m = randrange(0, 11)
        answer = input(f"Type {desc[i][m]}")
        if answer in files[i][m]:
            print("Correct. Next,")
        else:
            print("That's incorrect.")
            string = ""
            idx = 0
            for i in files[i][m]:
                if idx == len(files[i][m]):
                    string += " and" + i
                else:
                    string += i + ","
                    idx += 2
            s = " was"
            print(f"The correct answer{s} {string}.")