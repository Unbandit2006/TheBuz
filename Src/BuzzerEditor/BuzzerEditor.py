
from Codebase import *
pygame.init()

window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption('Buzzer Editor')
clock = pygame.time.Clock()      
        

create_buzzer_panel = CreateBuzzerPanel(window)

def close_all():
    create_buzzer_panel.drawn = False

def graceful_quit():
    pygame.quit()
    quit()

def create_a_buzzer():
    create_buzzer_panel.drawn = True

menu = Menu(window)

file_menu = Menu(window)
file_menu.add("Create A Buzzer", create_a_buzzer)
file_menu.add("Quit", graceful_quit)
menu.add("File", file_menu)

add_menu = Menu(window)
add_menu.add("Static Text", graceful_quit)
add_menu.add("Variable Text", graceful_quit)
menu.add("Add", add_menu)

window_menu = Menu(window)
window_menu.add("Clear Screen", close_all)
menu.add("Window", window_menu)

help_menu = Menu(window)
help_menu.add("About Us", close_all)
help_menu.add("Teach Me", graceful_quit)
menu.add("Help", help_menu)

default_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 15)
running = True
while running:
    window.fill("#121212")

    menu.draw()
    create_buzzer_panel.draw()

    clock.tick(60)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        menu.handle_event(event)
        create_buzzer_panel.handle_event(event)

