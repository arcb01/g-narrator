import tkinter
import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("860x580")
app.title("Narrator")


def button_callback():
    print("Do something...")


def slider_callback(value):
    #progressbar_1.set(value)
    value = int(value * 100)
    # TODO: Get this value and set it to Narrator speed

def language_callback(value):
    # TODO: Get this value and set it to OCR language
    pass

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

#progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
#progressbar_1.pack(pady=10, padx=10)

label_1 = customtkinter.CTkLabel(master=frame_1, text="Select narrator voice speed", justify=tkinter.LEFT)
label_1.pack(pady=10, padx=10)
slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=1)
slider_1.pack(pady=10, padx=10)
slider_1.set(0.5)

#entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="CTkEntry")
#entry_1.pack(pady=10, padx=10)

#optionmenu_1.pack(pady=10, padx=10)
#optionmenu_1.set("CTkOptionMenu")

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, command=language_callback, values=["Enlgish", "Spanish"])
label_2 = customtkinter.CTkLabel(master=frame_1, text="Select language for OCR detection", justify=tkinter.LEFT)
label_2.pack(pady=10, padx=10)
combobox_1 = customtkinter.CTkComboBox(frame_1, command=language_callback, values=["Enlgish", "Spanish"])
combobox_1.pack(pady=10, padx=10)
optionmenu_1.set("CTkComboBox")


button_1 = customtkinter.CTkButton(master=frame_1, text="Start", command=button_callback)
button_1.pack(pady=10, padx=10)


#checkbox_1 = customtkinter.CTkCheckBox(master=frame_1)
#checkbox_1.pack(pady=10, padx=10)

#radiobutton_var = tkinter.IntVar(value=1)

#radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=1)
#radiobutton_1.pack(pady=10, padx=10)

#radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, variable=radiobutton_var, value=2)
#radiobutton_2.pack(pady=10, padx=10)

#switch_1 = customtkinter.CTkSwitch(master=frame_1)
#switch_1.pack(pady=10, padx=10)

#text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=70)
#text_1.pack(pady=10, padx=10)
#text_1.insert("0.0", "CTkTextbox\n\n\n\n")

#segmented_button_1 = customtkinter.CTkSegmentedButton(master=frame_1, values=["CTkSegmentedButton", "Value 2"])
#segmented_button_1.pack(pady=10, padx=10)

#tabview_1 = customtkinter.CTkTabview(master=frame_1, width=200, height=70)
#tabview_1.pack(pady=10, padx=10)
#tabview_1.add("CTkTabview")
#tabview_1.add("Tab 2")

app.mainloop()