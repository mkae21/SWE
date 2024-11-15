import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback  # execute_command_callback 함수가 작성된 파일

class TestExecuteCommandCallback(unittest.TestCase):
    def setUp(self):
        self.car = Car()
        self.car_controller = CarController(self.car)

    def test_trunk_open_when_gear_is_not_p(self):   #기어가 P가 아닌 경우 Trunk Open
        self.car.gear_d()  # 기어를 D로 변경
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertTrue(self.car.trunk_status)  # 트렁크는 여전히 닫혀 있어야 함

    def test_trunk_open_when_locked(self):  #기어가 P이지만 자동차가 잠겨있을때 Trunk Open
        self.car.unlock_vehicle()  # 잠금을 해제했다가 다시 잠금
        self.car.lock_vehicle()
        self.car.gear_p()  # 기어를 P로 설정
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertTrue(self.car.trunk_status)  # 트렁크는 여전히 닫혀 있어야 함 / true가 closed이다.

    def test_trunk_open_when_already_open(self): #기어가 P이고 잠금이 해제된 상태이며 트렁크가 이미 열려있는 상황
        self.car.gear_p()  # 기어를 P로 설정
        self.car.unlock_vehicle()  # 잠금을 해제
        self.car.open_trunk()  # 트렁크를 미리 열어 둠
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car.trunk_status)  # 트렁크는 이미 열린 상태

    def test_trunk_open_successfully(self): #기어가 P이고 잠금이 해제된 상태이며 트렁크가 닫혀있는 상황
        self.car.gear_p()  # 기어를 P로 설정
        self.car.unlock_vehicle()  # 잠금을 해제
        self.car.close_trunk()  # 트렁크를 닫아 둠
        execute_command_callback("TRUNK_OPEN", self.car_controller)
        self.assertFalse(self.car.trunk_status)  # 트렁크가 열린 상태여야 함

    def test_trunk_close_when_already_closed(self): #트렁크가 이미 닫혀있을대 Trunk Close
        self.car.close_trunk()  # 트렁크를 닫아 둠
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car.trunk_status)  # 트렁크는 여전히 닫혀 있어야 함

    def test_trunk_close_successfully(self):    #트렁크가 열려있는 상황에서 Trunk Close
        self.car.open_trunk()  # 트렁크를 열어 둠
        execute_command_callback("TRUNK_CLOSE", self.car_controller)
        self.assertTrue(self.car.trunk_status)  # 트렁크가 닫힌 상태여야 함

# 테스트 실행
if __name__ == '__main__':
    unittest.main()
