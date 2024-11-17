import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback


class TestEngineButton(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_engine_on(self):
        execute_command_callback("ENGINE_BTN", self.car_controller)

        # 엔진이 켜졌는지 확인
        self.assertEqual(self.car_controller.get_engine_status(), True)

    def test_engine_off(self):
        self.car_controller.toggle_engine()  # 엔진을 무조건 켬 (초기 상태에서 켜진 상태로)
        execute_command_callback("ENGINE_BTN", self.car_controller)

        # 엔진이 꺼졌는지 확인
        self.assertEqual(self.car_controller.get_engine_status(), False)

    def test_engine_off_speed_not_zero(self):
        # 상태 설정: 속도가 0이 아님, 엔진을 켬
        self.car_controller.toggle_engine()  # 엔진을 무조건 켬 (초기 상태에서 켜진 상태로)
        self.car_controller.accelerate()  # 속도 증가

        execute_command_callback("ENGINE_BTN", self.car_controller)

        # 엔진이 꺼지지 않았는지 확인
        self.assertEqual(self.car_controller.get_engine_status(), True)


if __name__ == '__main__':
    unittest.main()
