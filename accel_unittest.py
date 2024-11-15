import unittest
from unittest.mock import MagicMock
from car import Car
from car_controller import CarController
from main import execute_command_callback  


class TestAccelerateCommand(unittest.TestCase):
    def setUp(self):
        # Car와 CarController의 mock 객체 생성
        self.mock_car = Car()
        self.mock_car_controller = CarController(self.mock_car)

        # 필요한 메서드와 속성 모의(Mock)
        self.mock_car_controller.get_speed = MagicMock(return_value=0)
        self.mock_car_controller.accelerate = MagicMock()
        self.mock_car_controller.get_lock_status = MagicMock(return_value=False)
        self.mock_car_controller.lock_left_door = MagicMock()
        self.mock_car_controller.lock_right_door = MagicMock()
        self.mock_car_controller.car.engine_on = True  # 엔진이 켜져 있는 상태로 설정

    def test_accelerate_when_engine_on_and_speed_below_130(self):
        # 엔진이 켜져 있고, 속도가 130km/h 미만일 때 가속 동작 테스트
        self.mock_car_controller.get_speed = MagicMock(return_value=20)  # 초기 속도 20km/h
        execute_command_callback("ACCELERATE", self.mock_car_controller)

        # 가속 메서드가 호출되었는지 확인
        self.mock_car_controller.accelerate.assert_called_once()

        # 속도가 30km/h 이상이고 문이 잠겨 있지 않으면 문 잠금 호출 확인
        self.mock_car_controller.lock_left_door.assert_called_once()
        self.mock_car_controller.lock_right_door.assert_called_once()

    def test_accelerate_does_not_work_when_engine_off(self):
        # 엔진이 꺼져 있을 때 가속 동작 테스트
        self.mock_car_controller.car.engine_on = False
        execute_command_callback("ACCELERATE", self.mock_car_controller)

        # 가속 메서드가 호출되지 않았는지 확인
        self.mock_car_controller.accelerate.assert_not_called()

    def test_no_acceleration_above_130(self):
        # 속도가 130km/h 이상일 때 가속 동작 테스트
        self.mock_car_controller.get_speed = MagicMock(return_value=130)  # 초기 속도 130km/h
        execute_command_callback("ACCELERATE", self.mock_car_controller)

        # 가속 메서드가 호출되지 않았는지 확인
        self.mock_car_controller.accelerate.assert_not_called()

    def test_no_door_lock_when_already_locked(self):
        # 속도가 30km/h 이상일 때 문 잠금 동작 테스트
        self.mock_car_controller.get_speed = MagicMock(return_value=35)  # 초기 속도 35km/h
        self.mock_car_controller.get_lock_status = MagicMock(return_value=True)  # 문이 이미 잠겨 있음
        execute_command_callback("ACCELERATE", self.mock_car_controller)

        # 문 잠금 메서드가 호출되지 않았는지 확인
        self.mock_car_controller.lock_left_door.assert_not_called()
        self.mock_car_controller.lock_right_door.assert_not_called()


if __name__ == '__main__':
    unittest.main()
