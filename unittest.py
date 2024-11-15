import unittest
from unittest.mock import MagicMock
from car import Car
from car_controller import CarController
from main import execute_command_callback


class TestEngineButton(unittest.TestCase):
    def setUp(self):
        # Create mock objects for Car and CarController
        self.mock_car = Car()
        self.mock_car_controller = CarController(self.mock_car)

        # Mock methods to control their behavior during the test
        self.mock_car_controller.get_speed = MagicMock(return_value=0)
        self.mock_car_controller.gear = MagicMock(return_value="P")
        self.mock_car_controller.toggle_engine = MagicMock()

    def test_engine_on_when_off_and_speed_zero_and_gear_p(self):
        # Test turning on the engine when it's off, speed is 0, and gear is P
        self.mock_car.engine_on = False
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # Check if the engine was toggled on
        self.mock_car_controller.toggle_engine.assert_called_once()

    def test_engine_not_on_when_speed_not_zero(self):
        # Test trying to turn on the engine when speed is not zero
        self.mock_car.engine_on = False
        self.mock_car_controller.get_speed = MagicMock(return_value=10)  # Speed not zero
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # Check if the engine was not toggled
        self.mock_car_controller.toggle_engine.assert_not_called()

    def test_engine_off_when_on_and_speed_zero(self):
        # Test turning off the engine when it's on and speed is zero
        self.mock_car.engine_on = True
        self.mock_car_controller.get_speed = MagicMock(return_value=0)
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # Check if the engine was toggled off
        self.mock_car_controller.toggle_engine.assert_called_once()

    def test_engine_not_off_when_speed_not_zero(self):
        # Test trying to turn off the engine when speed is not zero
        self.mock_car.engine_on = True
        self.mock_car_controller.get_speed = MagicMock(return_value=10)  # Speed not zero
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # Check if the engine was not toggled
        self.mock_car_controller.toggle_engine.assert_not_called()


if __name__ == '__main__':
    unittest.main()
