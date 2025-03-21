from typing import Final
import os
import math
import pygame
from Model import *
from Model.Dolphin import Dolphin
from Model.Buddha import Buddha
from Model.Astronaut import Astronaut
from Model.Projectile import Projectile
from View import *
from View.TitleScreen import TitleScreen
from CustomEvents import CustomEvents
from GameSaver import GameSaver

class MController:
    """
    The MController class manages the core gameplay logic, including handling user input, 
    managing events, and updating the game state. It acts as the main game loop controller, 
    orchestrating interactions between the player, the game world, and the view.
    """
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
        
        
        self.__setup_new_game(selected_character)

    def __setup_new_game(self, selected_character):
        """Creates a new game with the chosen character."""
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets/sounds")

        mainTheme = pygame.mixer.Sound(os.path.join(assets_path, "mainTheme.mp3"))  # Beach wave sound
        wave_sound = pygame.mixer.Sound(os.path.join(assets_path, "waves.mp3"))  # A sound effect

        # Set individual sound volumes
        mainTheme.set_volume(0.05)
        wave_sound.set_volume(0.2)  # Half volume

        # Play a sound effect when an event happens
        mainTheme.play()
        wave_sound.play()  # Plays the wave sound once

        # If you want to loop a sound effect indefinitely:
        wave_sound.play(-1)  # Loop wave sound infinitely
        self.gameWon = False
        if selected_character == "Load":
            print()
            self.__myWorld = GameSaver.load_game()
            self.__myPlayer = self.__myWorld.getPlayer()
                

        else:
            self.__myWorld = GameWorld.getInstance()
            character_map = {
                "Dolphin": Dolphin,
                "Buddha": Buddha,
                "Astronaut": Astronaut
                
            }
            character_shoot_map = {
                "Dolphin": 300,
                "Buddha": 600,
                "Astronaut": 500
                
            }
            if "Demo" in selected_character:
                self.__myWorld.setDemo()
                selected_character = selected_character.replace("Demo", "")
                self.__myPlayer = character_map.get(selected_character, Buddha)()
                self.__myWorld.setPlayer(self.__myPlayer)
                self.shoot_cooldown = character_shoot_map.get(selected_character, 500)

            else:
                self.__myPlayer = character_map.get(selected_character, Dolphin)()
                self.__myWorld.setPlayer(self.__myPlayer)
                self.shoot_cooldown = character_shoot_map.get(selected_character, 500)

    def __InitalizeEvents(self):
        """
        Sets up a new game instance with the chosen character.

        :param selected_character: The character chosen by the player.
        """
        EventManager.RegisterExistingEvent(CustomEvents.QUIT, pygame.QUIT, self.__quitGame)
        EventManager.RegisterExistingEvent(CustomEvents.MOUSE_BUTTON_DOWN, pygame.MOUSEBUTTONDOWN, self.__mouseButtonDown)
        EventManager.RegisterExistingEvent(CustomEvents.MOUSE_BUTTON_UP, pygame.MOUSEBUTTONUP, self.__mouseButtonUp)
        
        EventManager.registerEvent(CustomEvents.CHARACTER_MOVED, self.__myView.update_entity)
        EventManager.registerEvent(CustomEvents.CHARACTER_STOPPED, self.__myView.update_entity)
        EventManager.registerEvent(CustomEvents.PLAYER_DIED, self.__handle_character_death)
        EventManager.registerEvent(CustomEvents.GAME_WON, self.gameWon)
        EventManager.registerEvent(CustomEvents.CHANGED_ROOM, self.__myView.updateRoom)
        EventManager.registerEvent(CustomEvents.SHOOT_PROJECTILE, self.__shoot_projectile)
        EventManager.registerEvent(CustomEvents.HEALTH, self.__myView.updateHealthUI)
        EventManager.registerEvent(CustomEvents.BOSS_ROOM, self.__myView.updateBossHealthUI)
        EventManager.registerEvent(CustomEvents.SONG_CHANGE, self.change_music)
        EventManager.registerEvent(CustomEvents.PICKUP_ITEM, self.__myView.updateInventoryUI)
        EventManager.registerEvent(CustomEvents.PICKUP_KEY, self.__myView.updateKeyInventoryUI)
        EventManager.registerEvent(CustomEvents.UPDATE_PROJECTILE, self.__myView.remove_projectile)
    
    def ControllerTick(self):
        """
        Runs the main game loop tick, handling events, updating entities, and checking abilities.

        :return: True if the game is still running, False otherwise.
        """
        self.__handleEvents()
        if self.gameWon:
            self.__myView.update_game_won_screen()  # Keep animating the victory screen
        else:
            self.__handle_keyboard()
            # self.__handle_mouse(self.__mySign)
            self.__myWorld.tick()
            self.__myView.process_updates()
            if self.__myPlayer._ability:
                self.__myPlayer._ability.update()
            if self.__myPlayer._item_Ability:
                self.__myPlayer._item_Ability.update()
            if self.__myPlayer._item_Invincibility:
                self.__myPlayer._item_Invincibility.update()
            if self.__myPlayer._item_Speed:
                self.__myPlayer._item_Speed.update()
            if self.__myPlayer._invincibility.update:
                self.__myPlayer._invincibility.update()

        return self.__myIsRunning    

    def __handleEvents(self):
        """Processes all pygame events."""
        for event in pygame.event.get():
            if self.gameWon:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Restart game
                        self.gameWon = False  # Reset game state
                        self.__reset_game()

                        title_screen = TitleScreen(self.__myView.screen)
                        selected_character = title_screen.run()
                        self.__setup_new_game(selected_character)
                        self.__myIsRunning = True  

                    elif event.key == pygame.K_ESCAPE:  # Quit game
                        pygame.quit()
                        exit()
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                    GameSaver.save_game()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    self.__myWorld.testRandomKillEnemy()
                    event = pygame.event.Event(
                    EventManager.event_types["BOSS_ROOM"],
                    {"name": "",
                    "health": 0,
                    "maxHealth": 0,
                    "isdead":True
                    }        
                    )
                    pygame.event.post(event)
                    
            EventManager.dispatch_event(event)

    def __handle_keyboard(self):
        """Handles keyboard input for moving the player and activating abilities."""
        keys = pygame.key.get_pressed()
        directions = []
        
        # Handle activating abilities
        if keys[pygame.K_SPACE]:  # Press 'E' to activate ability
            self.__myPlayer.activate_ability()
            self.__myView.redrawCharacter()
        elif keys[pygame.K_1]:  # Press 'T' to use an item
            self.__myPlayer.use_item(0)
            self.__myView.redrawCharacter()
        elif keys[pygame.K_2]:  # Press 'T' to use an item
            self.__myPlayer.use_item(1)
            self.__myView.redrawCharacter()
        elif keys[pygame.K_3]:  # Press 'T' to use an item
            self.__myPlayer.use_item(2)
            self.__myView.redrawCharacter()
        elif keys[pygame.K_4]:  # Press 'T' to use an item
            self.__myPlayer.use_item(3)
            self.__myView.redrawCharacter()
        elif keys[pygame.K_r]:  # Press 'T' to use an item
            self.__myPlayer.takeDamage(0.1)
            self.__myPlayer.setDamage(1000)
            self.__myView.redrawCharacter()
        elif keys[pygame.K_p]:  # Press 'T' to use an item
            self.__myPlayer.keyCount = 2
            self.__myPlayer.update("PICKUP_KEY")
            self.__myPlayer.setMaxKeys()
            self.__myView.redrawCharacter()
        elif keys[pygame.K_DELETE]:
            # self.__myView.onScreenChar.clear
        
            self.__reset_game()
            
            title_screen = TitleScreen(self.__myView.screen)
            selected_character = title_screen.run()
            

            self.__setup_new_game(selected_character)
            self.__myIsRunning = True
        
        
        
        # Handle minimap visibility change
        new_minimap_state = keys[pygame.K_LSHIFT]  # True if M is held, False otherwise
        if new_minimap_state != self.__myView.showMinimap:
            self.__myView.showMinimap = new_minimap_state
            self.__myView.redrawCharacter()  # Only redraw when state changes


        
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
    
    def __handle_character_death(self, event):
        """
        Handles what happens when the player dies.
        Displays the game-over screen and stops the game loop.

        :param event: The event that triggered the death.
        """
        self.change_gamewon_music("womp.mp3")
        self.__myView.display_game_over()
        self.__myIsRunning = False  
    
    def gameWon(self, event):
        """
        Handles when the player wins the game.

        :param event: The event triggering game completion.
        """
        self.gameWon = True
        self.change_gamewon_music("victory.mp3")
        
        self.__myView.display_game_won()
    
    def __quitGame(self, event) -> bool:
        """
        Handles quitting the game, ensuring the game state is saved.

        :param event: The quit event.
        :return: False, indicating that the game should exit.
        """
        self.__myIsRunning = False
        return self.__myIsRunning
    
    def __shoot_projectile(self, event: pygame.event.Event):
        """
        Handles shooting a projectile in the given direction.

        :param event: The event containing information about the projectile.
        """
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
    
    def __reset_game(self):
        """Handles resetting the game view and clearing the screen."""
        pygame.mixer.stop()
        self.__myView.reset_view()  # Call reset method in MView
        GameWorld.reset_instance()  # Reset game world singleton
        pygame.display.update()  # Ensure changes are displayed
    
    def __mouseButtonUp(self, theEvent):
        """
        Handles mouse button press events.

        :param theEvent: The mouse button down event.
        """
        if theEvent.button in [1, 3]:  # Left or right click
            self.__myIsHoldingClick = False
    
    def __mouseButtonDown(self, theEvent):
        """
        Handles mouse button release events.

        :param theEvent: The mouse button up event.
        """
        if theEvent.button in [1, 3]:  # Left or right click
            self.__myIsHoldingClick = True
            self.__mySign = 1 if theEvent.button == 1 else -1
    
    def change_gamewon_music(self, song):
        """
        Changes the background music to a new song based on an event.
        :param event: Event containing `event.song` (string, e.g., "battleTheme.mp3")
        """
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets/sounds")
        new_song_path = os.path.join(assets_path, song)  # Get song filename from event

        # Stop current music
        pygame.mixer.stop()  # Stops all currently playing sounds

        try:
            # Load and play the new music
            new_music = pygame.mixer.Sound(new_song_path)
            new_music.set_volume(0.05)  # Adjust volume as needed
            new_music.play(-1)  # Loop indefinitely
            self.current_music = new_music  # Store reference to track current music


        except Exception as e:
            print(f"Error loading music: {song} - {e}")
   
    def change_music(self, event):
        """
        Changes the background music to a new song based on an event.
        :param event: Event containing `event.song` (string, e.g., "battleTheme.mp3")
        """
        assets_path = os.path.join(os.path.dirname(__file__), "..", "Assets/sounds")
        new_song_path = os.path.join(assets_path, event.song)  # Get song filename from event

        # Stop current music
        pygame.mixer.stop()  # Stops all currently playing sounds

        try:
            # Load and play the new music
            new_music = pygame.mixer.Sound(new_song_path)
            new_music.set_volume(0.05)  # Adjust volume as needed
            new_music.play(-1)  # Loop indefinitely
            self.current_music = new_music  # Store reference to track current music


        except Exception as e:
            print(f"Error loading music: {event.song} - {e}")

 
    
    
               
        