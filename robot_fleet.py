from abc import ABC, abstractmethod
from functools import wraps
import logging


logging.basicConfig(level=logging.INFO)


class InsufficientBatteryError(Exception):
    def __init__(self, robot_name, required, available):
        self.robot_name = robot_name
        self.required = required
        self.available = available

        message = (
            f"{robot_name} needs {required}% battery for this task "
            f"but only has {available}%."
        )

        super().__init__(message)


def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info("Starting %s", func.__name__)

        result = func(*args, **kwargs)

        logging.info("Finished %s", func.__name__)

        return result

    return wrapper


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

    def use_battery(self, amount):
        if self.battery < amount:
            raise InsufficientBatteryError(
                self.name,
                amount,
                self.battery
            )

        self.battery -= amount

    @abstractmethod
    def perform_task(self, **kwargs):
        pass

    @classmethod
    def from_config(cls, config):
        return cls(
            name=config["name"],
            battery=config.get("battery", 100)
        )


class CleaningRobot(Robot):
    def __init__(self, name, battery=100, dust_capacity=50):
        super().__init__(name, battery)
        self.dust_capacity = dust_capacity
        self.cleaning_mode = "standard"

    @log_action
    def perform_task(self, **kwargs):
        """Clean an area using the cleaning robot."""
        amount = kwargs.get("amount", 20)

        self.use_battery(20)

        return f"{self.name} cleaned {amount} square meters of floor."


class DroneRobot(Robot):
    def __init__(self, name, battery=100, max_altitude=100):
        super().__init__(name, battery)
        self.max_altitude = max_altitude

    def perform_task(self, **kwargs):
        """Fly the drone to a specified altitude."""
        altitude = kwargs.get("altitude", 50)

        self.use_battery(30)

        return f"{self.name} flew to {altitude} meters."


def fleet_report(robots):
    for robot in robots:
        print(str(robot))


def run_task_safely(robot, **kwargs):
    try:
        result = robot.perform_task(**kwargs)

    except InsufficientBatteryError as error:
        logging.error(error)

    else:
        print(result)

    finally:
        print(f"{robot.name} current battery: {robot.battery}%")


# ---------------------------------------------------------
# Mutable Class Attribute Trap Demonstration
# ---------------------------------------------------------

class BadRobotStorage:
    robots = []

    def add_robot(self, name):
        self.robots.append(name)


bad_robot_1 = BadRobotStorage()
bad_robot_2 = BadRobotStorage()

bad_robot_1.add_robot("Robot A")

print("Mutable class attribute bug:")
print("Robot 1:", bad_robot_1.robots)
print("Robot 2:", bad_robot_2.robots)


class GoodRobotStorage:
    def __init__(self):
        self.robots = []

    def add_robot(self, name):
        self.robots.append(name)


good_robot_1 = GoodRobotStorage()
good_robot_2 = GoodRobotStorage()

good_robot_1.add_robot("Robot A")

print("Corrected version:")
print("Robot 1:", good_robot_1.robots)
print("Robot 2:", good_robot_2.robots)


# ---------------------------------------------------------
# Main Program
# ---------------------------------------------------------

if __name__ == "__main__":

    cleaner = CleaningRobot(
        "Roomba",
        battery=100,
        dust_capacity=75
    )

    drone = DroneRobot.from_config({
        "name": "Aqua-Drone",
        "battery": 15
    })

    robots = [cleaner, drone]

    print("\n--- Fleet Report ---")
    fleet_report(robots)

    print("\n--- Cleaning Task ---")
    run_task_safely(cleaner, amount=25)

    print("\n--- Drone Task ---")
    run_task_safely(drone, altitude=50)

    print("\n--- Insufficient Battery Test ---")
    run_task_safely(drone, altitude=100)

    print("\n--- Robot Population ---")
    print(Robot.population)

    print("\n--- String Representation ---")
    print(str(cleaner))

    print("\n--- Developer Representation ---")
    print(repr(cleaner))

    print("\n--- Decorator Check ---")
    print(CleaningRobot.perform_task.__name__)