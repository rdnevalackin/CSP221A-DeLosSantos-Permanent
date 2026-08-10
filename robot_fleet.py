from abc import ABC, abstractmethod


class Robot(ABC):
    manufacturer = "RoboTech"
    population = 0

    def __init__(self, name, battery=100):
        self.name = name
        self.battery = battery
        Robot.population += 1

    @property
    def battery(self):
        return self._battery

    @battery.setter
    def battery(self, value):
        self._battery = max(0, min(100, value))

    def __str__(self):
        return f"{self.name} ({self.battery}% battery)"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name!r}, battery={self.battery})"
        )

    @abstractmethod
    def perform_task(self):
        pass


class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=50):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity

    def perform_task(self):
        self.use_battery(20)
        return f"{self.name} cleaned the floor."