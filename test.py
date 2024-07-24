flags = {"-w": "256", "-c": "True"}

flag_list = []

for k, v in flags.items():
    flag_list += [k, v]



print(
    list(flag_list)
    )