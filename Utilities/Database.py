# import PySimpleGUI as psg
# import sys
# sys.path.insert(1, "C:\\Dev\\Python\\TheBuz\\Src")
# from TheBuzLib import Reader, Database
# import random

# myReader = Reader("Src\\Config.json")
# myDB = Database(myReader)
# myUsers = myDB.get_users()

# psg.theme("Black")

# names = {}
# max_width = 0
# for count, user in enumerate(myUsers):
#     if len(user["name"]) > max_width:
#         max_width += len(user["name"])

#     names[user["name"]] = count

# def add_user(window: psg.Window, values):
#     # TODO SETUP CHECKS TO NOT SEND BAD DATA
#     name = values["NameInput"].strip()
#     number = values["NumberInput"].strip()
#     time = values["TimeInput"].strip()
#     zipcode = values["ZipcodeInput"].strip()
    
#     myDB.add_user(name, number, time, zipcode)

#     # Update listbox
#     myUsers = myDB.get_users()
#     names = {}
#     max_width = 0
#     for count, user in enumerate(myUsers):
#         if len(user["name"]) > max_width:
#             max_width += len(user["name"])

#         names[user["name"]] = count

#     window["-LIST-"].update(list(names.keys()))
#     window["PeopleCounter"].update(len(names))

# def remove_user(window: psg.Window, values):
#     # TODO: POSSIBLE POPUp FOR CONFERMING

#     myDB.remove_user(values['-LIST-'][0])

#     # Update listbox
#     myUsers = myDB.get_users()
#     names = {}
#     max_width = 0
#     for count, user in enumerate(myUsers):
#         if len(user["name"]) > max_width:
#             max_width += len(user["name"])

#         names[user["name"]] = count

#     window["-LIST-"].update(list(names.keys()))
#     window["PeopleCounter"].update(len(names))

# def generate_graph(window: psg.Window, values):
#     if values["GraphType"] == "Bar Graph":
#         if values["GraphValue"] == "Zipcode":
#             window["GraphCanvas"].erase()
            
#             zipcode_stats = sorted(myDB.get_zipcode_stats().items(), key=lambda x: x[1], reverse=True)
            
#             max_val = 0
#             for zipcode in zipcode_stats:
#                 if zipcode[1] > max_val:
#                     max_val = zipcode[1]

#             unit_height = 350//(max_val)
#             unit_width = 500//(len(zipcode_stats))

#             for count, zipcode in enumerate(zipcode_stats):
#                 top_left = (unit_width*count, zipcode[1]*unit_height)
#                 bottom_right = (unit_width*count+unit_width, 0)
#                 color = "%06x" % random.randint(0, 0xFFFFFF)
#                 window["GraphCanvas"].draw_rectangle(top_left, bottom_right, fill_color="#"+str(color))

#                 coords = top_left
#                 window["GraphCanvas"].draw_text(zipcode[0], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_BOTTOM_LEFT)

#                 coords = top_left
#                 window["GraphCanvas"].draw_text(zipcode[1], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_TOP_LEFT)

#         elif values["GraphValue"] == "Service Provider":
#             window["GraphCanvas"].erase()
            
#             zipcode_stats = sorted(myDB.get_zipcode_stats().items(), key=lambda x: x[1], reverse=True)
            
#             max_val = 0
#             for zipcode in zipcode_stats:
#                 if zipcode[1] > max_val:
#                     max_val = zipcode[1]

#             unit_height = 350//(max_val)
#             unit_width = 500//(len(zipcode_stats))

#             for count, zipcode in enumerate(zipcode_stats):
#                 top_left = (unit_width*count, zipcode[1]*unit_height)
#                 bottom_right = (unit_width*count+unit_width, 0)
#                 color = "%06x" % random.randint(0, 0xFFFFFF)
#                 window["GraphCanvas"].draw_rectangle(top_left, bottom_right, fill_color="#"+str(color))

#                 coords = top_left
#                 window["GraphCanvas"].draw_text(zipcode[0], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_BOTTOM_LEFT)

#                 coords = top_left
#                 window["GraphCanvas"].draw_text(zipcode[1], coords, font="FiraSans-Medium.ttf 10 normal", text_location=psg.TEXT_LOCATION_TOP_LEFT)       

# left_layout = [
#     [psg.Text("People", font="Calibri 20 underline", expand_x=True, auto_size_text=True)],
#     [psg.Listbox(list(names.keys()), size=(max_width, 20), enable_events=True, key="-LIST-", font="Calibri 13")],
#     [psg.Text("Database Details", font="Calibri 20 underline")],
#     [psg.Text(f"People Count: {len(names)}", font="Calibri 13", key="PeopleCounter")],
# ]

# personal_layout = [
#     # [psg.Text("Personal Information", font="Calibri 35 underline", justification="center", expand_x=True)],
#     [psg.Text("Name: ", font="Calibri 13", justification="right"), psg.Input("", key="NameInput", expand_x=True, font="Calibri 13",)],
#     [psg.Text("Number: ", font="Calibri 13"), psg.Input("", key="NumberInput", expand_x=True, font="Calibri 13")],
#     [psg.Text("Time: ", font="Calibri 13"), psg.Input("", key="TimeInput", expand_x=True, font="Calibri 13")],
#     [psg.Text("Zipcode: ", font="Calibri 13"), 
#         psg.Input("", expand_x=True, font="Calibri 13", key="ZipcodeInput"),
#     ],
#     [psg.Text("Service provider: ", font="Calibri 13"), 
#         psg.Combo(("T-Mobile", "AT&T", "Verizon"), "T-Mobile", expand_x=True, font="Calibri 13", key="ServiceProvider")
#     ],
#     [psg.Button("Add", button_color=("white", "green"), expand_x=True, font="Calibri 13", enable_events=True, key="AddButton"), 
#         psg.Button("Remove", button_color=("white", "red"), expand_x=True, font="Calibri 13", key="RemoveButton"), 
#         psg.Button("Update", button_color=("white", "blue"), expand_x=True, font="Calibri 13")
#     ],
# ]

# graph_layout = [
#     [psg.Frame("", [
#         [psg.Combo(("Pie Graph", "Bar Graph"), "Bar Graph", font="Calibri 13", key="GraphType"), psg.Combo(("Zipcode", "Service Provider"), "Zipcode", font="Calibri 13", key="GraphValue")],
#         [psg.Graph((500,400), (0,0), (500,400),expand_x=True, expand_y=True, background_color="white", key="GraphCanvas")],
#         [psg.Button('Generate', expand_x=True, key="GenerateButton", button_color=("white", "green"), font="Calibri 13")]
#     ])]
# ]

# right_layout = [
#     [
#         psg.TabGroup([
#             [psg.Tab("Personal Information", personal_layout)],
#             [psg.Tab("Graph", graph_layout)],
#         ])
#     ]
# ]

# layout = [
#     [psg.Col(left_layout), psg.Col(right_layout, pad=0, vertical_alignment="top", expand_y=True, expand_x=True)],
# ]

# window = psg.Window("Database Viewer", layout, finalize=True, auto_size_buttons=False, margins=(0,0))

# while True:
#     event, values = window.read(timeout=600000)  # in millisecond (10 min)

#     if event == psg.WIN_CLOSED:
#         break

#     elif event == psg.TIMEOUT_EVENT:
#         break    
    
#     # Listbox
#     elif event in values.keys():
#         user = myDB.find_user(values['-LIST-'][0])
        
#         window["NameInput"].update(f"{user['name']}")
#         window["NumberInput"].update(f"{user['number']}")
#         window["TimeInput"].update(f"{user['time']}")
#         window["ZipcodeInput"].update(f"{user['extensions']['Weather']}")
#         if user['carrier'][11:] == "tmomail.net":
#             window["ServiceProvider"].update("T-Mobile")        
#         elif user['carrier'][11:] == "vtext.com":
#             window["ServiceProvider"].update("Verizon")       
#         elif user['carrier'][11:] == "txt.att.net":
#             window["ServiceProvider"].update("AT&T")

#     # Add button
#     elif event == "AddButton":
#         add_user(window, values)

#     # Remove button
#     elif event == "RemoveButton":
#         remove_user(window, values)

#     # Generate button
#     elif event == "GenerateButton":
#         generate_graph(window, values)

import pygame
import random
pygame.init()

window = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('TheBuz Employee Program')

background_image = pygame.image.load("C:\\Users\\Danie\\Desktop\\Logo\\Logo_1280x720_Background.png").convert()

logo_image = pygame.image.load("C:\\Users\\Danie\\Desktop\\Logo\\Logo_V4_82x60 (Custom) (Custom).png").convert_alpha()
# logo_image = pygame.transform.scale(logo_image, (82, 60))

note_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 14)
header_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 25)

colors = [
    "#071881",
    "#663cac",
    "#e56be9"
]

running = True
while running:
    # Background
    window.blit(background_image, (0, 0))

    # Top Left Logo
    window.blit(logo_image, (5, 5))

    # Note Texts
    program_title_text = note_font.render("TheBuz Employee Program", True, "Whitesmoke")
    window.blit(program_title_text, (5+logo_image.get_width()+5, 5))

    database_text = note_font.render("Database: ", True, "Whitesmoke")
    window.blit(database_text, (10+logo_image.get_width(), 10+program_title_text.get_height()))

    people_count_text = note_font.render("People Count: ", True, "Whitesmoke")
    window.blit(people_count_text, (10+logo_image.get_width(), 15+database_text.get_height()+program_title_text.get_height()))

    # Charts
    charts_panel = pygame.Surface((window.get_width()-10, window.get_height()-15-logo_image.get_height()))
    charts_panel.fill("SteelBlue")
    charts_panel.set_colorkey("SteelBlue")

    panel_width = (charts_panel.get_width()-20)//2
    panel_height = (charts_panel.get_height()-15)//2


    zipcode_panel = pygame.Rect(5, 5, panel_width, panel_height)
    pygame.draw.rect(charts_panel, "Black", zipcode_panel, border_radius=10)
    
    zipcode_header_text = header_font.render("Zipcodes Bar Graph", True, "Whitesmoke")
    charts_panel.blit(zipcode_header_text, (zipcode_panel.width//2-zipcode_header_text.get_width()//2, 15))

    zipcode_chart = pygame.Rect(10, 20+zipcode_header_text.get_height(), (zipcode_panel.width-10), (zipcode_panel.height-zipcode_header_text.get_height()-20))
    pygame.draw.rect(charts_panel, "Whitesmoke", zipcode_chart, border_radius=10)


    extensions_panel = pygame.Rect(10+panel_width, 5, panel_width, panel_height)
    pygame.draw.rect(charts_panel, "Black", extensions_panel, border_radius=10)

    extensions_header_text = header_font.render("Extensions Bar Graph", True, "Whitesmoke")
    charts_panel.blit(extensions_header_text, (zipcode_panel.width+10+(extensions_panel.width//2-extensions_header_text.get_width()//2), 15))


    services_panel = pygame.Rect(5, 10+panel_height, panel_width, panel_height)
    pygame.draw.rect(charts_panel, "Black", services_panel, border_radius=10)    

    services_header_text = header_font.render("Service Providers Horizontal Bar Graph", True, "Whitesmoke")
    charts_panel.blit(services_header_text, (services_panel.width//2-services_header_text.get_width()//2, 20+zipcode_panel.height))


    times_panel = pygame.Rect(10+panel_width, 10+panel_height, panel_width, panel_height)
    pygame.draw.rect(charts_panel, "Black", times_panel, border_radius=10)    

    times_header_text = header_font.render("Times Horizontal Bar Graph", True, "Whitesmoke")
    charts_panel.blit(times_header_text, (zipcode_panel.width+10+(times_panel.width//2-times_header_text.get_width()//2), 20+extensions_panel.height))


    window.blit(charts_panel, (5, logo_image.get_height()+10))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

