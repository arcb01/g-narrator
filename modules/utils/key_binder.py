import keyboard
import sys
import pprint, json

def key_binder():
    
    keys_db = {"CAPTURE": None, 
                "SWITCH_FORWARD": None, 
                "SWITCH_BACKWARD": None, 
                "REPEAT": None,
                "READ_NEAREST": None,
                "READ_OUT_LOUD": None,
                "QUIT": None}

    for k in keys_db.keys():
        print(f"\n **=== Press the key you would you like to use as {k} key. Press Q to quit ===**\n")
        while True:
            event = keyboard.read_event()

            if event.event_type == keyboard.KEY_DOWN and event.name != "enter" and event.name != "q":
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


            if event.event_type == keyboard.KEY_DOWN and event.name == "q":
                sys.exit()

    # Save keys to json file
    with open("./config/keys.json", "w") as f:
        json.dump(keys_db, f, indent=4)

    print("\n\t === Key binding finished succesfully ===\n")

if __name__ == "__main__":
    key_binder()
