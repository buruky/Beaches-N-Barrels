from typing import Final
import pygame
import math
from ViewUnits import ViewUnits
from .MModel import MModel
from Model.Dolphin import Dolphin
from Model.Buddha import Buddha
from Model.Astronaut import Astronaut
from Model.Projectile import Projectile
from Model import *
from View import *
from CustomEvents import CustomEvents
from View.TitleScreen import TitleScreen
from GameSaver import GameSaver

class MController:
    
    def __init__(self):
        """Initializes the game controller, handling input, events, and game state."""
        self.__myKeyMap: Final = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT"
        }
        self.__mySign = 1
        self.__myView: Final = MView()
        self.__InitalizeEvents()
        self.__myIsRunning = True
        self.shoot_cooldown = 500  # 300ms = 0.3 seconds between shots
        self.last_shot_time = 0  # Time of last shot
        
        # Show title screen and get character selection
        title_screen = TitleScreen(self.__myView.screen)
        selected_character = title_screen.run()
        
        # Load or create new game
        
        if selected_character == "Load":
            print()
            self.__myWorld = GameSaver.load_game()
            self.__myPlayer = self.__myWorld.getPlayer()
        else:
            self.__setup_new_game(selected_character)

    def __setup_new_game(self, selected_character):
        """Creates a new game with the chosen character."""
        self.__myWorld = GameWorld.getInstance()
        character_map = {
            "Dolphin": Dolphin,
            "Buddha": Buddha,
            "Astronaut": Astronaut
        }

        self.__myPlayer = character_map.get(selected_character, Dolphin)()
        self.__myWorld.setPlayer(self.__myPlayer)

    def ControllerTick(self):
        """Main game loop tick, handling events, updating entities, and checking abilities."""
        self.__handleEvents()
        self.__handle_keyboard()
        self.__handle_mouse(self.__mySign)
        self.__myWorld.tick()

        if self.__myPlayer._ability:
            self.__myPlayer._ability.update()
        if self.__myPlayer._item_Ability:
            self.__myPlayer._item_Ability.update()
        return self.__myIsRunning
    
    def __InitalizeEvents(self):
        """Registers game-related events."""
        EventManager.RegisterExistingEvent(CustomEvents.QUIT, pygame.QUIT, self.__quitGame)
        EventManager.RegisterExistingEvent(CustomEvents.MOUSE_BUTTON_DOWN, pygame.MOUSEBUTTONDOWN, self.__mouseButtonDown)
        EventManager.RegisterExistingEvent(CustomEvents.MOUSE_BUTTON_UP, pygame.MOUSEBUTTONUP, self.__mouseButtonUp)

        EventManager.registerEvent(CustomEvents.CHARACTER_MOVED, self.__myView.update_entity)
        EventManager.registerEvent(CustomEvents.CHARACTER_STOPPED, self.__myView.update_entity)
        EventManager.registerEvent(CustomEvents.PLAYER_DIED, self.__handle_character_death)
        EventManager.registerEvent(CustomEvents.CHANGED_ROOM, self.__myView.updateRoom)
        EventManager.registerEvent(CustomEvents.SHOOT_PROJECTILE, self.__shoot_projectile)
        EventManager.registerEvent(CustomEvents.HEALTH, self.__myView.updateHealthUI)
        EventManager.registerEvent(CustomEvents.PICKUP_ITEM, self.__myView.updateInventoryUI)
        EventManager.registerEvent(CustomEvents.UPDATE_PROJECTILE, self.__myView.remove_projectile)

    def __handle_character_death(self, event):
        """Displays 'Game Over' and stops the game loop."""
        self.__myView.display_game_over()
        self.__myIsRunning = False  

    def __quitGame(self, event) -> bool:
        """Handles quitting the game, ensuring state is saved."""
        self.__myIsRunning = False
        return self.__myIsRunning

    def __handleEvents(self):
        """Processes all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                print("Saving game...")  # Press "L" to save anytime
                GameSaver.save_game()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                self.__myWorld.testRandomKillEnemy()
                self.__myView.redrawCharacter()
            
            EventManager.dispatch_event(event)

    def __handle_keyboard(self):
        """Handles keyboard input for moving the player and activating abilities."""
        keys = pygame.key.get_pressed()
        directions = []

        # Handle activating abilities
        if keys[pygame.K_e]:  # Press 'E' to activate ability
            self.__myPlayer.activate_ability()
        elif keys[pygame.K_t]:  # Press 'T' to use an item
            self.__myPlayer.use_item()
        
        # Handle shooting projectiles with cooldown
        current_time = pygame.time.get_ticks()  # Get current time in milliseconds
        if current_time - self.last_shot_time >= self.shoot_cooldown:  # Check if cooldown has passed
            # Determine angle based on WASD keys
            angle = None
            
            if keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                angle = math.radians(225)  # Top-left diagonal (increase Y and decrease X)
            elif keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                angle = math.radians(315)  # Top-right diagonal (increase Y and increase X)
            elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                angle = math.radians(135)  # Bottom-left diagonal (decrease Y and decrease X)
            elif keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                angle = math.radians(45)  # Bottom-right diagonal (decrease Y and increase X)
            elif keys[pygame.K_UP]:
                angle = math.radians(270)  # Up (decrease Y)
            elif keys[pygame.K_DOWN]:
                angle = math.radians(90)  # Down (increase Y)
            elif keys[pygame.K_LEFT]:
                angle = math.radians(180)  # Left (decrease X)
            elif keys[pygame.K_RIGHT]:
                angle = math.radians(0)  # Right (increase X)
            
            if angle is not None:
                # Send a shooting event with the calculated angle
                event = pygame.event.Event(
                    EventManager.event_types["SHOOT_PROJECTILE"],
                    {
                        "shooter": self.__myPlayer.getName(),
                        "direction": angle,  # Pass the angle for direction
                        "damage": self.__myPlayer.getAttackDamage(),
                        "positionX": self.__myPlayer.getPositionX(),
                        "positionY": self.__myPlayer.getPositionY(),
                        "speed": 10,  # Modify the speed value as needed
                        "isEnemy": False
                    }
                )
                pygame.event.post(event)
                self.last_shot_time = current_time  # Update last shot time

        # Handle movement with WASD keys
        for key, direction in self.__myKeyMap.items():
            if keys[key]:
                directions.append(direction)
        
        # If there are any movement directions, move the player
        if directions:
            self.__myPlayer.moveCharacter(directions)


    def __shoot_projectile(self, event: pygame.event.Event):
        """Handles shooting a projectile in the given direction."""
        shooterName = "Projectile" + event.shooter
        if event.shooter:
            # Create the projectile using the angle provided by the event
            projectile = Projectile(
                name=shooterName,
                shooter=event.shooter,
                attackDamage=event.damage,  # Get attack damage from player
                angle=event.direction,  # Pass angle instead of predefined direction
                speed=event.speed,  # Set an appropriate speed
                positionX=event.positionX,
                positionY=event.positionY,
                isEnemy = event.isEnemy
            )
            
            self.__myWorld.addProjectile(projectile)  # Add to the game world
                
    def __mouseButtonUp(self, theEvent):
        """Handles mouse button release."""
        if theEvent.button in [1, 3]:  # Left or right click
            self.__myIsHoldingClick = False

    def __mouseButtonDown(self, theEvent):
        """Handles mouse button press."""
        if theEvent.button in [1, 3]:  # Left or right click
            self.__myIsHoldingClick = True
            self.__mySign = 1 if theEvent.button == 1 else -1

    def __handle_mouse(self, theSign: int):
        """Handles mouse input (future implementation)."""
        pass
