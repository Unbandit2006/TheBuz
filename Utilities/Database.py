import PySimpleGUI as psg
import sys
sys.path.insert(1, "C:\\Dev\\Python\\TheBuz\\Src")
from TheBuzLib import Reader, Database
import random

myReader = Reader("Src\\Config.json")
myDB = Database(myReader)
myUsers = myDB.get_users()

psg.theme("Black")

names = {}
max_width = 0
for count, user in enumerate(myUsers):
    if len(user["name"]) > max_width:
        max_width += len(user["name"])

    names[user["name"]] = count

def add_user(window: psg.Window, values):
    # TODO SETUP CHECKS TO NOT SEND BAD DATA
    name = values["NameInput"].strip()
    number = values["NumberInput"].strip()
    time = values["TimeInput"].strip()
    zipcode = values["ZipcodeInput"].strip()
    
    myDB.add_user(name, number, time, zipcode)

    # Update listbox
    myUsers = myDB.get_users()
    names = {}
    max_width = 0
    for count, user in enumerate(myUsers):
        if len(user["name"]) > max_width:
            max_width += len(user["name"])

        names[user["name"]] = count

    window["-LIST-"].update(list(names.keys()))
    window["PeopleCounter"].update(len(names))

def remove_user(window: psg.Window, values):
    # TODO: POSSIBLE POPUp FOR CONFERMING

    myDB.remove_user(values['-LIST-'][0])

    # Update listbox
    myUsers = myDB.get_users()
    names = {}
    max_width = 0
    for count, user in enumerate(myUsers):
        if len(user["name"]) > max_width:
            max_width += len(user["name"])

        names[user["name"]] = count

    window["-LIST-"].update(list(names.keys()))
    window["PeopleCounter"].update(len(names))

def generate_graph(window: psg.Window, values):
    if values["GraphType"] == "Bar Graph":
        if values["GraphValue"] == "Zipcode":
            window["GraphCanvas"].erase()
            
            zipcode_stats = sorted(myDB.get_zipcode_stats().items(), key=lambda x: x[1], reverse=True)
            
            max_val = 0
            for zipcode in zipcode_stats:
                if zipcode[1] > max_val:
                    max_val = zipcode[1]

            unit_height = 350//(max_val)
            unit_width = 500//(len(zipcode_stats))

            for count, zipcode in enumerate(zipcode_stats):
                top_left = (unit_width*count, zipcode[1]*unit_height)
                bottom_right = (unit_width*count+unit_width, 0)
                color = "%06x" % random.randint(0, 0xFFFFFF)
                window["GraphCanvas"].draw_rectangle(top_left, bottom_right, fill_color="#"+str(color))

                coords = top_left
                window["GraphCanvas"].draw_text(zipcode[0], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_BOTTOM_LEFT)

                coords = top_left
                window["GraphCanvas"].draw_text(zipcode[1], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_TOP_LEFT)

        elif values["GraphValue"] == "Service Provider":
            window["GraphCanvas"].erase()
            
            zipcode_stats = sorted(myDB.get_zipcode_stats().items(), key=lambda x: x[1], reverse=True)
            
            max_val = 0
            for zipcode in zipcode_stats:
                if zipcode[1] > max_val:
                    max_val = zipcode[1]

            unit_height = 350//(max_val)
            unit_width = 500//(len(zipcode_stats))

            for count, zipcode in enumerate(zipcode_stats):
                top_left = (unit_width*count, zipcode[1]*unit_height)
                bottom_right = (unit_width*count+unit_width, 0)
                color = "%06x" % random.randint(0, 0xFFFFFF)
                window["GraphCanvas"].draw_rectangle(top_left, bottom_right, fill_color="#"+str(color))

                coords = top_left
                window["GraphCanvas"].draw_text(zipcode[0], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_BOTTOM_LEFT)

                coords = top_left
                window["GraphCanvas"].draw_text(zipcode[1], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_TOP_LEFT)       

left_layout = [
    [psg.Text("People", font="Calibri 20 underline", expand_x=True, auto_size_text=True)],
    [psg.Listbox(list(names.keys()), size=(max_width, 20), enable_events=True, key="-LIST-", font="Calibri 13")],
    [psg.Text("Database Details", font="Calibri 20 underline")],
    [psg.Text(f"People Count: {len(names)}", font="Calibri 13", key="PeopleCounter")],
]

personal_layout = [
    # [psg.Text("Personal Information", font="Calibri 35 underline", justification="center", expand_x=True)],
    [psg.Text("Name: ", font="Calibri 13", justification="right"), psg.Input("", key="NameInput", expand_x=True, font="Calibri 13",)],
    [psg.Text("Number: ", font="Calibri 13"), psg.Input("", key="NumberInput", expand_x=True, font="Calibri 13")],
    [psg.Text("Time: ", font="Calibri 13"), psg.Input("", key="TimeInput", expand_x=True, font="Calibri 13")],
    [psg.Text("Zipcode: ", font="Calibri 13"), 
        psg.Input("", expand_x=True, font="Calibri 13", key="ZipcodeInput"),
    ],
    [psg.Text("Service provider: ", font="Calibri 13"), 
        psg.Combo(("T-Mobile", "AT&T", "Verizon"), "T-Mobile", expand_x=True, font="Calibri 13", key="ServiceProvider")
    ],
    [psg.Button("Add", button_color=("white", "green"), expand_x=True, font="Calibri 13", enable_events=True, key="AddButton"), 
        psg.Button("Remove", button_color=("white", "red"), expand_x=True, font="Calibri 13", key="RemoveButton"), 
        psg.Button("Update", button_color=("white", "blue"), expand_x=True, font="Calibri 13")
    ],
]

graph_layout = [
    [psg.Frame("", [
        [psg.Combo(("Pie Graph", "Bar Graph"), "Bar Graph", font="Calibri 13", key="GraphType"), psg.Combo(("Zipcode", "Service Provider"), "Zipcode", font="Calibri 13", key="GraphValue")],
        [psg.Graph((500,400), (0,0), (500,400),expand_x=True, expand_y=True, background_color="white", key="GraphCanvas")],
        [psg.Button('Generate', expand_x=True, key="GenerateButton", button_color=("white", "green"), font="Calibri 13")]
    ])]
]

right_layout = [
    [
        psg.TabGroup([
            [psg.Tab("Personal Information", personal_layout)],
            [psg.Tab("Graph", graph_layout)],
        ])
    ]
]

layout = [
    [psg.Col(left_layout), psg.Col(right_layout, pad=0, vertical_alignment="top", expand_y=True, expand_x=True)],
]

window = psg.Window("Database Viewer", layout, finalize=True, auto_size_buttons=False, margins=(0,0))

while True:
    event, values = window.read(timeout=600000)  # in millisecond (10 min)

    if event == psg.WIN_CLOSED:
        break

    elif event == psg.TIMEOUT_EVENT:
        break    
    
    # Listbox
    elif event in values.keys():
        user = myDB.find_user(values['-LIST-'][0])
        
        window["NameInput"].update(f"{user['name']}")
        window["NumberInput"].update(f"{user['number']}")
        window["TimeInput"].update(f"{user['time']}")
        window["ZipcodeInput"].update(f"{user['extensions']['Weather']}")
        if user['carrier'][11:] == "tmomail.net":
            window["ServiceProvider"].update("T-Mobile")        
        elif user['carrier'][11:] == "vtext.com":
            window["ServiceProvider"].update("Verizon")       
        elif user['carrier'][11:] == "txt.att.net":
            window["ServiceProvider"].update("AT&T")

    # Add button
    elif event == "AddButton":
        add_user(window, values)

    # Remove button
    elif event == "RemoveButton":
        remove_user(window, values)

    # Generate button
    elif event == "GenerateButton":
        generate_graph(window, values)

