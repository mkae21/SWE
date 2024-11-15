import unittest
from car import Car
from car_controller import CarController

class TestCarController(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_brake(self):
        # 엔진을 켜고 가속 후 브레이크 테스트
        self.car.toggle_engine()  # 엔진을 켬
        self.car.accelerate()  # 속도 증가 (10)
        self.car.accelerate()  # 속도 증가 (20)
        # 브레이크 작동
        self.car_controller.brake()
        self.assertEqual(self.car.speed, 10, "10 km/h")
        # 다시 브레이크 작동
        self.car_controller.brake()
        self.assertEqual(self.car.speed, 0, "0 km/h")
        # 속도가 0일 때 브레이크 동작 확인 - 0km/h 유지인지
        self.car_controller.brake()
        self.assertEqual(self.car.speed, 0, "0 km/h, 음수가 되면 안됨")

    def test_lock_vehicle(self):
        # 차량 초기 상태 확인 -> 잠금 상태여야함
        self.assertTrue(self.car.lock, "True, 잠금 상태여야함.")
        # 잠금 해제
        self.car.unlock_vehicle()
        self.assertFalse(self.car.lock, "False인지 확인")
        # 다시 잠금
        self.car_controller.lock_vehicle()
        self.assertTrue(self.car.lock, "True인지 확인")

    def test_unlock_vehicle(self):
        # 초기 상태: 차량 및 전체 시스템이 잠겨 있어야 함
        self.car_controller.lock_vehicle()
        self.assertTrue(self.car_controller.get_lock_status(), "True, 차량 및 시스템이 잠겨 있어야 합니다.")

        # 차량 잠금 해제 명령 실행
        self.car_controller.unlock_vehicle()
        self.assertFalse(self.car_controller.get_lock_status(), "False, 차량 및 시스템 잠금 해제 상태여야 합니다.")

        # 다시 잠금 확인
        self.car_controller.lock_vehicle()
        self.assertTrue(self.car_controller.get_lock_status(), "True, 차량 및 시스템이 다시 잠겨 있어야 합니다.")

if __name__ == "__main__":
    unittest.main()