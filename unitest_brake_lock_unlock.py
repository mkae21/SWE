import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback


class TestBrakeAndLock(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_brake_when_speed_is_0(self):
        execute_command_callback("BRAKE", self.car_controller)
        self.assertEqual(self.car_controller.get_speed(), 0, "속도가 0이면 브레이크를 밟아도 0이여야 함.")


    def test_brake_does_not_reduce_below_zero(self):
        execute_command_callback("ENGINE_BTN", self.car_controller)
        for _ in range(5):  # 여러 번 브레이크 실행
            execute_command_callback("BRAKE", self.car_controller)
        self.assertGreaterEqual(self.car_controller.get_speed(), 0, "속도는 아무리 브레이크를 밟아도 0이하로 감소되면 안됨.")


    def test_accelerate_then_brake(self):
    # 엔진을 켬
        execute_command_callback("ENGINE_BTN", self.car_controller)
        self.assertTrue(self.car_controller.get_engine_status(), "엔진이 켜져 있어야 합니다.")

    # 기어를 'D'로 설정
        execute_command_callback("GEAR_D", self.car_controller)
        self.assertEqual(self.car_controller.gear(), "D", "기어가 D로 설정되어야 합니다.")

    # 가속
        for _ in range(3):
            execute_command_callback("ACCELERATE", self.car_controller)

    # 속도 확인
        initial_speed = self.car_controller.get_speed()
        self.assertGreater(initial_speed, 0, "가속 후 속도는 0보다 커야 합니다.")

    # 브레이크
        execute_command_callback("BRAKE", self.car_controller)
        self.assertLess(self.car_controller.get_speed(), initial_speed, "가속 후에 브레이크를 밟으면 속도가 감소해야 함.")

    def test_brake_decreases_by_10_each_time(self):
        """브레이크를 밟을 때마다 속도가 10씩 감소하는지 확인합니다."""
        execute_command_callback("ENGINE_BTN", self.car_controller)  # 엔진을 켬
        execute_command_callback("ACCELERATE", self.car_controller)  # 가속 (속도 10 km/h 예상)

        initial_speed = self.car_controller.get_speed()
        execute_command_callback("BRAKE", self.car_controller)  # 브레이크 작동
        expected_speed = max(0, initial_speed - 10)
        self.assertEqual(self.car_controller.get_speed(), expected_speed, f"브레이크 후 속도는 {expected_speed}이어야 합니다.")

    def test_lock_unlock_vehicle_system(self):
        # 초기 상태: 차량 전체가 잠겨 있어야 함
        self.car_controller.lock_vehicle()
        self.assertTrue(self.car_controller.get_lock_status(), "True, 차량 잠금 상태여야합니다.")

        # 차량 잠금 해제 명령 실행
        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_lock_status(), "False, 차량 잠금 해제 상태여야 합니다.")

        # 다시 잠금 확인
        self.car_controller.lock_vehicle()
        self.assertTrue(self.car_controller.get_lock_status(), "True, 차량 잠금 상태여야합니다.")


if __name__ == "__main__":
    unittest.main()