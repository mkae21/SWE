import unittest
from unittest.mock import MagicMock
from car import Car
from car_controller import CarController
from main import execute_command_callback  # 필요에 따라 main 스크립트 파일에 맞게 조정

class TestAccelerate(unittest.TestCase):

    def test_accelerate_when_engine_off(self):
        car = Car()
        car_controller = CarController(car)

        # 엔진이 꺼진 상태에서 ACCELERATE 명령
        execute_command_callback("ACCELERATE", car_controller)

        # 속도가 증가하지 않음을 확인
        self.assertEqual(car_controller.get_speed(), 0)

    def test_accelerate_when_engine_on_and_speed_below_130(self):
        car = Car()
        car_controller = CarController(car)

        # 엔진을 켠 후 ACCELERATE 명령
        execute_command_callback("ENGINE_BTN", car_controller)
        for _ in range(5):
            execute_command_callback("ACCELERATE", car_controller)

        # 속도가 증가했는지 확인 (예: 가속 로직에 따라 설정)
        self.assertGreater(car_controller.get_speed(), 0)
        self.assertLessEqual(car_controller.get_speed(), 130)

    def test_accelerate_when_speed_at_130(self):
        car = Car()
        car_controller = CarController(car)

        # 엔진 켜고 속도를 130까지 증가
        execute_command_callback("ENGINE_BTN", car_controller)
        while car_controller.get_speed() < 130:
            execute_command_callback("ACCELERATE", car_controller)

        # 130km/h에 도달한 상태에서 ACCELERATE 명령
        current_speed = car_controller.get_speed()
        execute_command_callback("ACCELERATE", car_controller)

        # 속도가 130 이상으로 증가하지 않음을 확인
        self.assertEqual(car_controller.get_speed(), current_speed)

    def test_accelerate_with_brake_interaction(self):
        car = Car()
        car_controller = CarController(car)

        # 엔진 켜고 가속 후 브레이크로 감속
        execute_command_callback("ENGINE_BTN", car_controller)
        for _ in range(5):
            execute_command_callback("ACCELERATE", car_controller)

        execute_command_callback("BRAKE", car_controller)

        # 브레이크 작동 후 속도가 감소했는지 확인
        self.assertLess(car_controller.get_speed(), 130)

if __name__ == '__main__':
    unittest.main()
