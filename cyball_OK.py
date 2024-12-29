import pygame
import os
import time
import keyboard

#function to output a txt file in the output_files directory PATH == C:\Cyberball\output_files (reaction times, and other experimental relevant data)
from files_to_txt import times_to_txt

from movearmsnao_cyberball import init_nao, end_nao, pushDX, pushSX

from LetturaPulsanti import LeggoPulsanti

# Initialize Pygame
pygame.init()

#Initialise NAO
init_nao()

# Screen setup constants
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
BALL_SPEED = 15
BLACK = (0, 0, 0)



class Player:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        
        
class Ball:

    def __init__(self, position, speed):
        self.position = position
        self.target = None
        self.moving = False
        self.speed = speed

    def move(self):
        if not self.moving or not self.target:
            return

        dx, dy = self.target[0] - self.position[0], self.target[1] - self.position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < self.speed:  # Snap to target if close enough
            self.position = list(self.target)
            self.moving = False
            return

        step_x = dx / distance * self.speed
        step_y = dy / distance * self.speed

        # Update position
        self.position[0] += step_x
        self.position[1] += step_y

    def is_target_reached(self, threshold=5):
        dx = self.target[0] - self.position[0]
        dy = self.target[1] - self.position[1]
        return dx * dx + dy * dy < threshold * threshold


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True

        # Load assets
        self.ball_img = self.load_ball_image()

        # Players
        self.players = {
            "player1": Player("player1", [665, 35]),
            "player2": Player("player2", [1193, 310]),
            "nao": Player("nao", [665, 630])
        }

        self.ORIGINAL_BAR_DIMENSIONS = {
            "player1": (80, 20),
            "player2": (20, 80),
            "nao": (80, 20)
        }

        self.BAR_DIMENSIONS = self.ORIGINAL_BAR_DIMENSIONS.copy()

        self.PLAYER_COLORS = {
            "player1": (255, 0, 0),  # Red  
            "player2": (0, 255, 0),  # Green
            "nao": (0, 0, 255)       # Blue
        }

        # Game state
        self.ball = Ball(self.players["player1"].position[:], BALL_SPEED)
        #game starts with ball in player1's position
        self.current_holder = "player1"
        #reaction times for player2(subject)
        self.response_times = {"to player1": [], "to NAO": []}
        #number of ball receivements for each player
        self.reclist = {"player1": 0, "player2": 0, "nao": 0}

        self.total_passages = 0
        self.start_time_set = False 
        self.start_time = None

    def resize_player_bar(self, player_name):
        width, height = self.ORIGINAL_BAR_DIMENSIONS[player_name]
        self.BAR_DIMENSIONS[player_name] = (width * 2, height * 2)
    
    def reset_player_bar(self, player_name):
        self.BAR_DIMENSIONS[player_name] = self.ORIGINAL_BAR_DIMENSIONS[player_name]

    def load_ball_image(self):
        try:
            ball_img = pygame.image.load(os.path.join('red_ball.png'))
        except pygame.error as e:
            print("Error loading ball image:", e)
            pygame.quit()
            raise SystemExit
        return pygame.transform.scale(ball_img, (60, 60))
    
    def get_time(self):
        
        return time.time()

    def update_game_state(self, buttons):
        if self.ball.moving:
            return

        if self.current_holder == "player1":
            if buttons["G1D"]:
                self.reclist["nao"] += 1
                self.set_ball_target("nao")
                
            elif buttons["G1S"]:
                self.reclist["player2"] += 1
                self.set_ball_target("player2")
                

        elif self.current_holder == "player2":
            if buttons["G3D"]:
                if self.start_time is not None:
                    elapsed = self.get_time() - self.start_time
                    self.response_times["to player1"].append(elapsed)
                    self.start_time = None  # Reset timestamp
                    self.start_time_set = False  # Ready for next round
                self.reclist["player1"] += 1
                self.set_ball_target("player1")
                

            if buttons["G3S"]:
                if self.start_time is not None:
                    elapsed = self.get_time() - self.start_time
                    self.response_times["to NAO"].append(elapsed)

                    self.start_time = None  # Reset timestamp
                    self.start_time_set = False  # Ready for next round
                self.reclist["nao"] += 1
                self.set_ball_target("nao")
                

        elif self.current_holder == "nao":
            self.total_passages += 1
            if self.total_passages < 21 and self.total_passages % 2 == 0:
                pushDX()
                time.sleep(0.1)
                self.reclist["player2"] += 1
                self.set_ball_target("player2")
            
            else:
                pushSX()
                time.sleep(0.1)
                self.reclist["player1"] += 1
                self.set_ball_target("player1")  # Always pass to player 1 after 20 passes
                
    def set_ball_target(self, target_name):
        self.ball.target = self.players[target_name].position[:]
        self.ball.moving = True

    def check_new_holder(self): #rivedere la funzione in maniera da posizionare t0 al momento adeguato
        for name, player in self.players.items():
            dx, dy = player.position[0] - self.ball.position[0], player.position[1] - self.ball.position[1]
            if dx * dx + dy * dy < 5 * 5:  # Direct inline threshold check
                if self.current_holder != name:  # Change of holder
                    if self.current_holder:
                        self.reset_player_bar(self.current_holder)

                    self.current_holder = name
                    self.resize_player_bar(name)
                    if name == "player2" and not self.start_time_set:
                        self.start_time = self.get_time()  # Record the time only once
                        self.start_time_set = True  # Prevent continuous refreshing
                break

    def draw_elements(self):
        self.screen.fill(BLACK)

        # Draw players
        for name, player in self.players.items():
            width, height = self.BAR_DIMENSIONS[name]
            color = self.PLAYER_COLORS[name]
            if name == "player1":
                pygame.draw.rect(self.screen, color, (player.position[0] - 55 , player.position[1] - 40, width, height))
            elif name == "player2":
                pygame.draw.rect(self.screen, color, (player.position[0] + 60 , player.position[1] - 55 , width, height))
            elif name == "nao":
                pygame.draw.rect(self.screen, color, (player.position[0] - 60 , player.position[1] + 60 , width, height))

        # Draw ball
        self.screen.blit(self.ball_img, self.ball.position)
        pygame.display.update()
        
    def run(self):

        while self.running:
            if keyboard.is_pressed("q") :
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            #Read buttons values; if button active then pass the ball
            buttons = LeggoPulsanti()

            self.update_game_state(buttons) 
            self.ball.move()
            self.check_new_holder()
            self.draw_elements()
            self.clock.tick(60)

        pygame.display.quit()
        pygame.quit()

        end_nao()    
        times_to_txt(self.response_times, self.reclist)
        



if __name__ == "__main__":
    game = Game() 
    game.run()
    







