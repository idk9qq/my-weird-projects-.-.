import os

filename = input("Which file? ")

if not os.path.isfile(filename):
    print(f"Error: The file '{filename}' does not exist.")
else:
    confirmation = input("Are you sure? (Y/N) ").strip().lower()
    if confirmation in ("y", "yes"):
        try:
            with open(filename, 'w') as f:
                print(f"What do you want to rewrite '{filename}' to? (Press Enter twice to finish)")
                lines = []
                while True:
                    line = input()
                    if line == "":
                        break
                    lines.append(line)
                f.write("\n".join(lines))
            print("Alright, done. Bye!")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Alright, bye!")
