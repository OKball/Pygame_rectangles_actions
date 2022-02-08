
import pygame

WIN_WIDTH = 900
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
REFRESH_RATE = 60
SCREEN_CENTER = WIN_WIDTH / 2 , WIN_HEIGHT / 2
pygame.display.set_caption("jumping square")


class trackingSquare():

    listOfAllObjects = []
    listOfAllLines = []

    def __init__(self, position_x, position_y, numberOfTrackingSquares):
        self.size = 1
        self.color = [255, 255, 255]
        self.position_x = position_x 
        self.position_y = position_y
        self.__class__.listOfAllObjects.append(self)
        self.__class__.listOfAllLines.append([self.position_x, self.position_y])

        if len(self.__class__.listOfAllObjects) > numberOfTrackingSquares:
            del self.__class__.listOfAllObjects[0]
        if len(self.__class__.listOfAllLines) > numberOfTrackingSquares:
            del self.__class__.listOfAllLines[0]

    def spawning(self):
        pygame.draw.rect(WIN, self.color,
         pygame.Rect(self.position_x, self.position_y, self.size, self.size))

def main():
    RUN = True
    CLOCK = pygame.time.Clock()
    rectangle = pygame.rect.Rect(450 ,400 ,21 ,21)
    rectangle_draging = False
    color = (255, 0 ,0)
    VELOCITY_Y = -150
    VELOCITY_X = 0
    speedListX = [0, 0]
    speedListY = [0, 0]

    while RUN:

        CLOCK.tick(REFRESH_RATE)
        speedListX.append(rectangle.x)
        speedListY.append(rectangle.y)
        del speedListX[0]
        del speedListY[0]
        NEW_VELOCITY_X = int(speedListX[1]) - int(speedListX[0])
        NEW_VELOCITY_Y = int(speedListY[1]) - int(speedListY[0])
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                pygame.quit()
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:            
                    if rectangle.collidepoint(event.pos):
                        rectangle_draging = True
                        mouse_x, mouse_y = event.pos
                        offset_x = rectangle.x - mouse_x
                        offset_y = rectangle.y - mouse_y
                        VELOCITY_Y = 0
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:            
                    rectangle_draging = False
                    VELOCITY_X = NEW_VELOCITY_X * 10
                    VELOCITY_Y = NEW_VELOCITY_Y * 10

            elif event.type == pygame.MOUSEMOTION:
                if rectangle_draging:
                    mouse_x, mouse_y = event.pos
                    rectangle.x = mouse_x + offset_x
                    rectangle.y = mouse_y + offset_y
        if rectangle_draging:
            if rectangle.x > WIN_WIDTH - rectangle.w:
                rectangle.x = WIN_WIDTH - rectangle.w
            elif rectangle.x < 0:
                rectangle.x = 0
            elif rectangle.y > WIN_HEIGHT - rectangle.h:
                rectangle.y = WIN_HEIGHT - rectangle.h

        if rectangle_draging == False:    
            GRAVITYFORCE = 4
            FRICTION = 5

            if rectangle.y == WIN_HEIGHT - rectangle.h:
                GRAVITYFORCE = 0
            elif rectangle.y > WIN_HEIGHT - rectangle.h:
                rectangle.y = WIN_HEIGHT - rectangle.h
                VELOCITY_Y = round(VELOCITY_Y / 2) * -1
            
            if rectangle.x > WIN_WIDTH - rectangle.w or rectangle.x < 0:
                VELOCITY_X = VELOCITY_X * -1
            VELOCITY_Y = VELOCITY_Y + GRAVITYFORCE 

            if VELOCITY_X > 0 and rectangle.y == WIN_HEIGHT - rectangle.h:
                VELOCITY_X = VELOCITY_X - FRICTION
            elif VELOCITY_X < 0 and rectangle.y == WIN_HEIGHT - rectangle.h:
                VELOCITY_X = VELOCITY_X + FRICTION   
            
            if rectangle.x == 0 or rectangle.x == WIN_WIDTH - rectangle.w:
                FRICTION = 0
            rectangle.y = rectangle.y + int(VELOCITY_Y / 10)
            rectangle.x = rectangle.x + int(VELOCITY_X / 10)
        WIN.fill((0,0,0))
        trackingSquare(rectangle.x + rectangle.w //2, rectangle.y + rectangle.h //2, 80)
        for object in trackingSquare.listOfAllObjects:
            trackingSquare.spawning(object)
        for line in range(len(trackingSquare.listOfAllLines)):
            if line >= 1:
                pygame.draw.line(WIN, (255,255,255), trackingSquare.listOfAllLines[line-1],
                 trackingSquare.listOfAllLines[line])
            else:
                pass
        pygame.draw.rect(WIN, color, rectangle)
        pygame.display.update()

        

if __name__ == "__main__":
    main()