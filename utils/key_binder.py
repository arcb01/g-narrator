import keyboard
import sys
import pprint


keys_db = {"CAPTURE": None, 
            "SWITCH_FORWARD": None, 
            "SWITCH_BACKWARD": None, 
            "REPEAT": None,
            "READ_NEAREST": None,
            "READ_OUT_LOUD": None,
            "QUIT": "esc"}

for k in keys_db.keys():
    print(f"\n **=== Press the key you would you like to use as {k} key ===**\n")
    while True:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name != "enter" and event.name != keys_db["QUIT"]:
            print(f"You pressed {(event.name).upper()} key. Press ENTER if you would like to save.")
            saved_key = event.name

        if event.event_type == keyboard.KEY_DOWN and event.name == "enter":
            try:
                print(f"\n{saved_key.upper()} was saved!")
                keys_db[k] = saved_key
                # TODO: Check for duplicates keys
                break
            except NameError:
                print("You must press a key before saving\n")


        if event.event_type == keyboard.KEY_DOWN and event.name == keys_db["QUIT"]:
            sys.exit()


pprint.pprint(keys_db)