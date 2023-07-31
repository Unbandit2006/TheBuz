import pygame
import os
pygame.init()

class Menu:
    def __init__(self, parent: pygame.surface.SurfaceType):
        self.parent = parent

        self.inactive_color = "Gray"
        self.active_color = "Yellow"

        self.font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 15)

        self.height = 2 + self.font.get_height() + 2
        self.width = self.parent.get_width()

        self.items = [] # [item_name, item_callback, status, x, y]

    def add(self, item_name: str, item_callback):
        self.items.append([item_name, item_callback, False, 0, 2])

    def draw(self):
        self.width = self.parent.get_width()

        background = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(self.parent, self.inactive_color, background)

        total_widths = 0
        for count, item in enumerate(self.items):
            item_name, item_callback, item_status, item_x, item_y = item

            text = self.font.render(item_name, True, "Black", self.active_color) if item_status == True else self.font.render(item_name, True, "Black", self.inactive_color)
            self.parent.blit(text, (12+(10*count)+total_widths, item_y))
            item_x = 12+(10*count)+total_widths
            
            total_widths += text.get_width()
            self.items[count][3] = item_x

            if item_status == True and type(item_callback) == Menu:
                self._draw_options(item, item_x)
    
    def _draw_options(self, item, x):
        item_name, item_callback, item_status, item_x, item_y = item

        if type(item_callback) == Menu:

            max_width = 0
            for inner_item in item_callback.items:
                width = 5 + self.font.render(inner_item[0], True, "black", "black").get_width() + 5
                if max_width < width:
                    max_width = width

            for count, inner_item in enumerate(item_callback.items,1):
                inner_item_name, inner_item_callback, inner_item_status, inner_item_x, inner_item_y = inner_item
                
                text = self.font.render(inner_item_name, True, "Black", self.active_color) if inner_item_status == True else self.font.render(inner_item_name, True, "Black", self.inactive_color)
                background = pygame.Rect(x, inner_item_y+(count*self.font.get_height())+4, max_width, self.font.get_height()+4)
                
                if inner_item_status is True:
                    pygame.draw.rect(self.parent, self.active_color, background)
                else:
                    pygame.draw.rect(self.parent, self.inactive_color, background)

                self.parent.blit(text, (x+5, inner_item_y+(count*self.font.get_height())+4))

                if background.collidepoint(pygame.mouse.get_pos()) == True and pygame.mouse.get_pressed()[0] == True:
                    inner_item_callback()
        
        else:
            item_callback()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            for count, item in enumerate(self.items):
                item_name, item_callback, item_status, item_x, item_y = item

                temp_rect = pygame.rect.Rect(item_x, item_y, self.font.render(item_name, True, "black", "black").get_width(), self.font.get_height())

                if temp_rect.collidepoint(event.pos[0], event.pos[1]) and event.button == 1 and item_status==False:
                    item_status = True
                    self._draw_options(item, 0)
                
                elif temp_rect.collidepoint(event.pos[0], event.pos[1]) and event.button == 1 and item_status == True:
                    item_status = False
                
                else:
                    item_status = False

                self.items[count] = [item_name, item_callback, item_status, item_x, item_y]


class FileExplorer:
    def __init__(self, parent: pygame.surface.SurfaceType) -> None:
        self.parent = parent
        self.drawn = False

        self.height = self.parent.get_height() * 0.80
        self.width = self.parent.get_width() * 0.80
        self.x = self.parent.get_width() * 0.1
        self.y = self.parent.get_height() * 0.1

        self.font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 13)
        self.big_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 20)
        self.entry_color_passive = "#181a1f"
        self.entry_color_active = "#252830"

        self.surface = pygame.Surface((self.width, self.height))
        
        self.location_entry = pygame.Surface((self.surface.get_width()-20, self.font.get_height()+4))
        self.location_entry_rect = self.location_entry.get_rect()
        self.location_entry_text = "C:\\"
        self.location_entry_color = self.entry_color_passive
        self.location_entry_selected = False

        self.folder_panel = pygame.Surface((self.surface.get_width()-20, self.font.get_height()+4))
        self.folder_rect = self.folder_panel.get_rect()
        self.scroll_multiplier = 0
        self.default_y = 60+self.location_entry.get_height()+10

        self.folders = []
        for filename in os.listdir("C:\\\\"):
            if os.path.isdir("C:\\\\" + filename):
                self.folders.append([filename, 0, pygame.Rect(0,0,0,0)])

    def draw(self):
        if self.drawn is True:
            self.height = self.parent.get_height() * 0.80
            self.width = self.parent.get_width() * 0.80
            self.x = self.parent.get_width() * 0.1
            self.y = self.parent.get_height() * 0.1
            self.surface = pygame.Surface((self.width, self.height))

            self.surface.fill("Gray")

            window_title = self.big_font.render(f"Select a folder to save Buzzer to.", True, "Black")
            self.surface.blit(window_title, (self.surface.get_width()//2-window_title.get_width()//2, 5))

            location_label = self.font.render("Location: ", True, "Black")
            self.surface.blit(location_label, (5, window_title.get_height()+7))

            self.location_entry = pygame.Surface((self.surface.get_width()-location_label.get_width()-20, self.font.get_height()+4))
            self.location_entry_rect = self.location_entry.get_rect(topleft=(self.x+location_label.get_width()+10, window_title.get_height()+self.y+5))
            self.location_entry.fill(self.location_entry_color)
            self.surface.blit(self.location_entry, (location_label.get_width()+10, window_title.get_height()+5))

            text = self.font.render(self.location_entry_text, True, "White", self.location_entry_color)
            self.surface.blit(text, (location_label.get_width()+10+2, window_title.get_height()+7))

            self.folder_panel = pygame.Surface((self.surface.get_width()-15, self.surface.get_height()-(window_title.get_height()+self.location_entry.get_height()+16)))
            self.folder_panel.fill(self.entry_color_active)
            self.surface.blit(self.folder_panel, (5, window_title.get_height()+self.location_entry.get_height()+8))
            self.folder_rect = self.folder_panel.get_rect(topleft=(self.x+5, self.y+window_title.get_height()+self.location_entry.get_height()+8))

            default_x = 7
            self.default_y = window_title.get_height()+self.location_entry.get_height()+10+self.scroll_multiplier

            for count, folder in enumerate(self.folders):

                if folder[1]%2 == 0 and folder[1] != 0:

                    pygame.draw.rect(self.surface, self.entry_color_passive, pygame.Rect(default_x, self.default_y+(count*self.font.get_height()), self.folder_panel.get_width()-2, self.font.get_height()))
                    new_text = self.font.render(folder[0], True, "White", self.entry_color_passive)

                    self.surface.blit(new_text, (default_x, self.default_y+(count*self.font.get_height())))
                    collider_rect = new_text.get_rect(width=self.folder_panel.get_width(), topleft=(self.x+default_x, self.y+self.default_y+(count*self.font.get_height())))
                    
                    self.folders[count] = [folder[0], folder[1], collider_rect]
                    
                    self.location_entry_text += f"{folder[0]}\\"

                    self.folders.clear()
                    for filename in os.listdir(f"{self.location_entry_text}"):
                        if os.path.isdir(f"{self.location_entry_text}" + filename):
                            self.folders.append([filename, 0, pygame.Rect(0,0,0,0)])

                else:

                    if self.default_y+(count*self.font.get_height()) >= window_title.get_height()+self.location_entry.get_height()+8 and self.default_y+(count*self.font.get_height())+self.font.get_height() <=  window_title.get_height()+self.location_entry.get_height()+8 + self.folder_panel.get_height():                
                        new_text = self.font.render(folder[0], True, "White", self.entry_color_active)

                        self.surface.blit(new_text, (default_x, self.default_y+(count*self.font.get_height())))
                        collider_rect = new_text.get_rect(width=self.folder_panel.get_width(), topleft=(self.x+default_x, self.y+self.default_y+(count*self.font.get_height())))
                        self.folders[count] = [folder[0], folder[1], collider_rect]

            self.parent.blit(self.surface, (self.x, self.y))
        
    def handle_event(self, event: pygame.event.EventType):
        if self.drawn is True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.drawn = False

                if self.location_entry_selected is True:
                    keyboard = pygame.key.get_pressed()
                    print(keyboard)
                    if event.type == pygame.K_BACKSPACE:
                        self.location_entry_text = self.location_entry_text[:-1]


                    elif event.key == pygame.K_RETURN:
                        self.location_entry_color = self.entry_color_passive
                        self.location_entry_selected = False

                        self.folders.clear()
                        for filename in os.listdir(f"{self.location_entry_text}"):
                            if os.path.isdir(f"{self.location_entry_text}" + filename):
                                self.folders.append([filename, 0, pygame.Rect(0,0,0,0)])

                    elif event.key == pygame.K_ESCAPE:
                        pass

                    else:
                        self.location_entry_text += event.unicode
            

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.location_entry_rect.collidepoint(event.pos[0], event.pos[1]):
                    self.location_entry_color = self.entry_color_active
                    self.location_entry_selected = True

                else:
                    self.location_entry_color = self.entry_color_passive
                    self.location_entry_selected = False

                if event.button == 1 and self.folder_rect.collidepoint(event.pos):
                    for count, folder in enumerate(self.folders):
                        if folder[2].collidepoint(event.pos):
                            self.folders[count] = [folder[0], folder[1]+1, folder[2]]

                        else:
                            self.folders[count] = [folder[0], 0, folder[2]]
            
            if event.type == pygame.MOUSEWHEEL:
                if event.y >= 0:
                    self.scroll_multiplier += self.font.get_height()
                
                else:
                    self.scroll_multiplier -= self.font.get_height()
            
            # if event.type == pygame.MOUSEBUTTONUP

class CreateBuzzerPanel:
    def __init__(self, parent: pygame.surface.SurfaceType) -> None:
        self.parent = parent
        self.drawn = False

        self.height = 300
        self.width = self.parent.get_width()//3
        self.x = self.parent.get_width()//2 - self.width//2
        self.y = self.parent.get_height()-self.height//2

        self.surface = pygame.Surface((self.width, self.height))

        self.background_color = "Gray"
        self.text_color = "Black"
        self.foreground_color = "#181a1f"
        self.entry_color_active = "#252830"
        self.entry_color_passive = "#181a1f"

        self.title_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 30)
        self.entry_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 20)
        self.location_font = pygame.font.Font("C:\\Dev\\Python\\TheBuz\\Assets\\FiraSans-Medium.ttf", 14)

        self.name_entry = pygame.Surface((100, 100))
        self.name_entry_rect = self.name_entry.get_rect()
        self.name_entry_text = "My New Buzzer"
        self.name_entry_color = self.entry_color_passive
        self.name_entry_selected = False

        self.file_location_collision_rect = self.name_entry.get_rect()

        self.file_explorer = FileExplorer(self.parent)

    def draw(self):
        if self.drawn is True:
            self.x = self.parent.get_width()//2 - self.width//2
            self.y = self.parent.get_height()//2 - self.height//2
            self.surface = pygame.Surface((self.width, self.height))

            self.surface.fill(self.background_color)

            title_surf = self.title_font.render("Create A Buzzer", True, self.text_color, self.background_color)
            self.surface.blit(title_surf, (self.surface.get_width()//2-title_surf.get_width()//2, 0))

            name_label = self.entry_font.render("Buzzer Name: ", True, self.text_color)
            self.surface.blit(name_label, (10, title_surf.get_height()+10))

            if self.name_entry_selected is False:
                self.name_entry_color = self.entry_color_passive
            
            else:
                self.name_entry_color = self.entry_color_active

            self.name_entry = pygame.Surface((self.surface.get_width()-name_label.get_width()-10-5, self.entry_font.get_height()+4))
            self.name_entry_rect = self.name_entry.get_rect(topleft=(self.x+name_label.get_width()+10, self.y+title_surf.get_height()+10))
            self.name_entry.fill(self.name_entry_color)
            self.surface.blit(self.name_entry, (10 + name_label.get_width(), title_surf.get_height() + 10))

            text = self.entry_font.render(self.name_entry_text, True, "White", self.name_entry_color)
            text_x = 10 + name_label.get_width()+2
            text_y = title_surf.get_height() + 10 + 2
            self.surface.blit(text, (text_x, text_y))

            location_label = self.entry_font.render("Buzzer Location: ", True, self.text_color)
            self.surface.blit(location_label, (10, title_surf.get_height()+name_label.get_height()+20))

            file_icon = pygame.image.load("BuzzerEditor\\Assets\\folder.png")
            file_icon = pygame.transform.scale(file_icon, (25, 25))
            self.surface.blit(file_icon, (10+location_label.get_width()+((self.surface.get_width()-location_label.get_width()-15)//2-25//2), title_surf.get_height()+name_label.get_height()+20))

            file_button_rect = pygame.Rect(10+location_label.get_width(), title_surf.get_height()+name_label.get_height()+20-2, (self.surface.get_width()-location_label.get_width())-15, file_icon.get_height()+4)
            pygame.draw.rect(self.surface, "Black", file_button_rect, 1)

            self.file_location_collision_rect = pygame.Rect(self.x+10+location_label.get_width(), self.y+title_surf.get_height()+name_label.get_height()+20-2, (self.surface.get_width()-location_label.get_width())-15, file_icon.get_height()+4)

            file_location_text = self.location_font.render(f"Location: {self.file_explorer.location_entry_text}", True, "Black")
            self.surface.blit(file_location_text, (self.surface.get_width()//2-file_location_text.get_width()//2, file_button_rect.y+file_button_rect.height+10))

            self.parent.blit(self.surface, (self.x, self.y))
            self.file_explorer.draw()

    def handle_event(self, event: pygame.event.EventType):
        if self.drawn is True:
            if self.file_explorer.drawn is False:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and self.name_entry_rect.collidepoint(event.pos):
                        self.name_entry_selected = True
                    else:
                        self.name_entry_selected = False

                    if event.button == 1 and self.file_location_collision_rect.collidepoint(event.pos):
                        self.file_explorer.drawn = True 

                if event.type == pygame.KEYDOWN:
                    if self.name_entry_selected is True:
                        if event.key == pygame.K_BACKSPACE:
                            self.name_entry_text = self.name_entry_text[:-1]
                        
                        elif event.key == pygame.K_RETURN:
                            self.name_entry_selected = False

                        else:
                            self.name_entry_text += event.unicode

                    if event.key == pygame.K_ESCAPE:
                        self.drawn = False
            
            else:
                self.file_explorer.handle_event(event)

