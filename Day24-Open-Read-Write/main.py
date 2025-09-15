with open("./Input/Letters/starting_letter.txt") as starting_letter:
    content = starting_letter.readlines()
    new_content="".join(content)
    with open("./Input/Names/invited_names.txt") as names:
        name_content = names.readlines()
        for name in name_content:
            name = name.strip()
            save_file=new_content.replace("[name]", name)
            with open(f"./Output/ReadyToSend/Letter-to-{name}.txt", mode="w") as new_save:
                new_save.write(save_file)
