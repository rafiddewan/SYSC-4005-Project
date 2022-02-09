from os import access


class WorkStation:
    
    def __init__(self):
        self.active = False
        self.timeRemaining = 0

    def getActive(self) -> bool:
        return self.active

    def setActive(self, active: bool) -> None:
        self.active = active
    
    def toggleActive(self):
        self.active = not self.active

    def getTimeRemaining(self) -> int:
        return self.timeRemaining

    def setTimeRemaining(self, timeRemaining: int) -> None:
        self.timeRemaining = timeRemaining
