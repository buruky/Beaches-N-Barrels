
import pygame

from CustomEvents import CustomEvents

from .EventManager import EventManager
from .Door import Door


class CollisionComparator():

    def changeCurrentRoom(self, theDoor:Door):
        newRoom = theDoor.getConnectedRoom(self.currentRoom)
        self.currentRoom = newRoom
        self.activateRoom(self.currentRoom)
        event = pygame.event.Event(
                EventManager.event_types[CustomEvents.CHANGED_ROOM],
                {
                    "roomName": self.currentRoom.getRoomType(),
                    "direction": theDoor.getConnectedDoorDirection(self.currentRoom)
                }
            )
        pygame.event.post(event)
    def activateRoom(self, theCurrentRoom):
        """Lets know doors and entities in room that should be shown on screen"""
    def check_collision(self, rect, ignore=None):
        """Check if a given rectangle collides with any obstacle or enemy."""
        # for obstacle in self.obstacles:
        #     if rect.colliderect(obstacle):
        #         print(f"Collision with obstacle at {obstacle}")  # Debugging
        #         return True  # Collision detected

        for enemy in self.enemies:
            if enemy != ignore:  # Don't check collision with itself
                enemy_rect = pygame.Rect(enemy.getPositionX(), enemy.getPositionY(), 50, 50)
                if rect.colliderect(enemy_rect):
                    if ignore in self.player:
                        ignore.Dies()
                    print(f"Collision with another enemy at ({enemy.getPositionX()}, {enemy.getPositionY()})")  # Debugging
                    return True
                
        for player in self.player:
            if player != ignore:  # Don't check collision with itself
                my_rect = pygame.Rect(player.getPositionX(), player.getPositionY(), 50, 50)
                if rect.colliderect(my_rect):
                    if ignore in self.currentRoom.getEnemyList():
                        player.Dies()
                    print(f"Collision with the player at ({player.getPositionX()}, {player.getPositionY()})")  # Debugging
                    return True
                
        for door in self.__myFloor.getDoorList():
            if player != ignore:  # Don't check collision with itself
                my_rect = pygame.Rect(door.getPositionX(), door.getPositionY(), 50, 50)
                if rect.colliderect(my_rect):
                
                        
                    print(f"Collision with door at ({player.getPositionX()}, {player.getPositionY()})")  # Debugging
                    return True
        
        
            return False  # No collision
    def collideWithDoor(self, theRect):
        for door in self.__myFloor.getDoorList():
            my_rect = pygame.Rect(door.getPositionX(), door.getPositionY(), 50, 50)
            if theRect.colliderect(my_rect):
                self.changeCurrentRoom(door)