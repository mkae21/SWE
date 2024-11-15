import unittest
from unittest.mock import MagicMock
from car import Car
from car_controller import CarController
from main import execute_command_callback  # 필요에 따라 main 스크립트 파일에 맞게 조정


class TestEngineButton(unittest.TestCase):
    def setUp(self):
        # Car와 CarController의 mock 객체 생성
        self.mock_car = Car()
        self.mock_car_controller = CarController(self.mock_car)

        # 필요한 메서드와 속성 모의(Mock)
        self.mock_car_controller.get_speed = MagicMock(return_value=0)
        self.mock_car_controller.gear = MagicMock(return_value="P")
        self.mock_car_controller.toggle_engine = MagicMock()

        # 엔진 상태를 get_engine_status로 모의
        self.mock_car_controller.get_engine_status = MagicMock()
        self.mock_car_controller.get_engine_status.return_value = False  # 초기 상태에서 엔진이 꺼져 있음

    def test_engine_on_when_off_and_speed_zero_and_gear_p(self):
        # 엔진이 꺼져 있고, 속도가 0이며, 기어가 P일 때 엔진을 켜는 동작 테스트
        self.mock_car_controller.get_engine_status.return_value = False
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # 엔진이 켜졌는지 확인
        self.mock_car_controller.toggle_engine.assert_called_once()

    def test_engine_not_on_when_speed_not_zero(self):
        # 속도가 0이 아닐 때 엔진을 켜려고 시도하는 동작 테스트
        self.mock_car_controller.get_engine_status.return_value = False
        self.mock_car_controller.get_speed = MagicMock(return_value=10)  # 속도가 0이 아님
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # 엔진이 켜지지 않았는지 확인
        self.mock_car_controller.toggle_engine.assert_not_called()

    def test_engine_off_when_on_and_speed_zero(self):
        # 엔진이 켜져 있고, 속도가 0일 때 엔진을 끄는 동작 테스트
        self.mock_car_controller.get_engine_status.return_value = True
        self.mock_car_controller.get_speed = MagicMock(return_value=0)
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # 엔진이 꺼졌는지 확인
        self.mock_car_controller.toggle_engine.assert_called_once()

    def test_engine_not_off_when_speed_not_zero(self):
        # 속도가 0이 아닐 때 엔진을 끄려고 시도하는 동작 테스트
        self.mock_car_controller.get_engine_status.return_value = True
        self.mock_car_controller.get_speed = MagicMock(return_value=10)  # 속도가 0이 아님
        execute_command_callback("ENGINE_BTN", self.mock_car_controller)

        # 엔진이 꺼지지 않았는지 확인
        self.mock_car_controller.toggle_engine.assert_not_called()


if __name__ == '__main__':
    unittest.main()
