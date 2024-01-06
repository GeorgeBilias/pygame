import pygame
from settings import *
from timer import Timer
from sprites import *
from support import *
from overlay import Overlay

class Menu:
    def __init__(self, player, toggle_menu):

        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        # options
        self.width = 400
        self.space = 10
        self.padding = 8

        self.upgrades = {
            'sword': 1,
            'axe': 1,
        }


        # entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())+ list(self.upgrades.keys())
        print(self.options)
        self.sell_border = len(self.player.item_inventory) - 1  # divides sellable and non sellable items in inventory
        self.sword_index = 6
        self.axe_index = 7
        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

        self.upgrde_sound = pygame.mixer.Sound("Animations_stolen/Animations/audio/upgrade.mp3")


    def display_money(self):
        text_surf = self.font.render(f'${self.player.money}', False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2,SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface,'White',text_rect.inflate(10,10),0,6)

        self.display_surface.blit(text_surf, text_rect)


    def setup(self):

        # create text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            print('item')
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH/2 - self.width/2,self.menu_top,self.width,self.total_height)

        #buy and sell text surface
        self.buy_text = self.font.render('buy',False,'Black')
        self.sell_text = self.font.render('sell',False,'Black')

        self.axe_text = self.font.render('upgrade',False,'Black')
        self.sword_text = self.font.render('upgrade',False,'Black')

        self.axe_full_text = self.font.render('max',False,'Black')
        self.sword_full_text = self.font.render('max',False,'Black')



    def input(self):

        keys = pygame.key.get_pressed() # close menu with ESC
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:

            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                #get item
                curent_item = self.options[self.index]
                print(curent_item)

                if self.index == self.sword_index:
                    if self.upgrades['sword'] == 1:
                        if self.player.money >= UPGRADE_PRICES['sword']:
                            self.player.money -= UPGRADE_PRICES['sword']
                            self.upgrades['sword'] += 1
                            self.upgrde_sound.play()
                            self.player.sword_lvl +=1
                    elif self.upgrades['sword'] == 2:
                        if self.player.money >= UPGRADE_PRICES2['sword']:
                            self.player.money -= UPGRADE_PRICES2['sword']
                            self.upgrades['sword'] += 1
                            self.upgrde_sound.play()
                            self.player.sword_lvl +=1
                    elif self.upgrades['sword'] == 3:
                        if self.player.money >= UPGRADE_PRICES3['sword']:
                            self.player.money -= UPGRADE_PRICES3['sword']
                            self.upgrades['sword'] += 1
                            self.upgrde_sound.play()
                            self.player.sword_lvl +=1
                    elif self.upgrades['sword'] == 4:
                        if self.player.money >= UPGRADE_PRICES4['sword']:
                            self.player.money -= UPGRADE_PRICES4['sword']
                            self.upgrades['sword'] += 1
                            self.upgrde_sound.play()
                            self.player.sword_lvl +=1
                elif self.index == self.axe_index:
                    if self.upgrades['axe'] == 1:
                        if self.player.money >= UPGRADE_PRICES['axe']:
                            self.player.money -= UPGRADE_PRICES['axe']
                            self.upgrades['axe'] += 1
                            self.upgrde_sound.play()
                            self.player.axe_lvl +=1
                    elif self.upgrades['axe'] == 2:
                        if self.player.money >= UPGRADE_PRICES2['axe']:
                            self.player.money -= UPGRADE_PRICES2['axe']
                            self.upgrades['axe'] += 1
                            self.upgrde_sound.play()
                            self.player.axe_lvl +=1
                    elif self.upgrades['axe'] == 3:
                        if self.player.money >= UPGRADE_PRICES3['axe']:
                            self.player.money -= UPGRADE_PRICES3['axe']
                            self.upgrades['axe'] += 1
                            self.upgrde_sound.play()
                            self.player.axe_lvl +=1
                    elif self.upgrades['axe'] == 4:
                        if self.player.money >= UPGRADE_PRICES4['axe']:
                            self.player.money -= UPGRADE_PRICES4['axe']
                            self.upgrades['axe'] += 1
                            self.upgrde_sound.play()
                            self.player.axe_lvl +=1
                else:

                        #SELL
                    if self.index <= self.sell_border:
                        if self.player.item_inventory[curent_item]>0:
                                self.player.item_inventory[curent_item]-= 1
                                self.player.money +=SALE_PRICES[curent_item]
                    else:
                        #BUY
                        seed_price = PURCHASE_PRICES[curent_item]
                        if self.player.money >= seed_price:
                            self.player.item_inventory[curent_item] +=1
                            self.player.money -= PURCHASE_PRICES[curent_item]

        # clamp values
        if self.index < 0:
            self.index = len(self.options) -1

        if self.index > len(self.options) -1:
            self.index = 0


    def show_entry(self, text_surf, amount, top, selected):

        # background
        bg_rect = pygame.Rect(self.main_rect.left,top,self.width,text_surf.get_height() + (self.padding*2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)


        # text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left+20,bg_rect.centery))
        self.display_surface.blit(text_surf,text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20,bg_rect.centery))
        self.display_surface.blit(amount_surf,amount_rect)

        # selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black',bg_rect,4,4)

            if self.index == self.axe_index:
                if self.upgrades['axe'] == 5:
                    pos_rect = self.axe_full_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
                    self.display_surface.blit(self.axe_full_text,pos_rect)
                else:
                    pos_rect = self.axe_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
                    self.display_surface.blit(self.axe_text,pos_rect)
            elif self.index == self.sword_index:
                if self.upgrades['sword'] == 5:
                    pos_rect = self.sword_full_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
                    self.display_surface.blit(self.sword_full_text,pos_rect)
                else:
                    pos_rect = self.sword_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
                    self.display_surface.blit(self.sword_text,pos_rect)
            else:


                if self.index<= self.sell_border: #sell
                    pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))
                    self.display_surface.blit(self.sell_text,pos_rect)
                else: #buy
                    pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150,bg_rect.centery))

                    self.display_surface.blit(self.buy_text,pos_rect)


    def update(self):
        self.input()
        self.display_money()

        for text_index, text_surf in enumerate(self.text_surfs):

            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding *2 ) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values()) + list(self.upgrades.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf,amount ,top, self.index == text_index)



