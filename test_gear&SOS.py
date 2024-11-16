import unittest
from car import Car
from car_controller import CarController
from main import execute_command_callback

def testGear(command,car_controller):
    if command == "GEAR_P":
        if car_controller.get_speed() != 0 or car_controller.get_engine_status() == False :
            return car_controller.gear()
        
        car_controller.gear_p()
        return car_controller.gear()

    elif command =="GEAR_N":
        if car_controller.get_speed() != 0 or car_controller.get_engine_status() == False:
            return car_controller.gear()
        
        car_controller.gear_n()
        return car_controller.gear()
    
    elif command =="GEAR_R":
        if car_controller.get_speed() != 0 or car_controller.get_engine_status() == False:
            return car_controller.gear()
        
        car_controller.gear_r()
        return car_controller.gear()

    else:
        if car_controller.get_speed() != 0 or car_controller.get_engine_status() == False:
            return car_controller.gear()
        
        car_controller.gear_d()
        return car_controller.gear()



class TestSOS(unittest.TestCase):
    
    def test_sos_default(self):
        car = Car()
        car_controller = CarController(car)

        execute_command_callback("SOS", car_controller)

        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_engine_status(), False)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_trunk_status(), False)
        self.assertEqual(car_controller.gear(), "P")
    
    def test_sos_Engine_btn(self):
        car = Car()
        car_controller = CarController(car)

        execute_command_callback("ENGINE_BTN", car_controller)

        execute_command_callback("SOS", car_controller)

        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_engine_status(), False)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_trunk_status(), False)
        self.assertEqual(car_controller.gear(), "P")
    
    def test_sos_Driving(self):
        car = Car()
        car_controller = CarController(car)

        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("GEAR_D", car_controller)

        while car_controller.get_speed() < 130:
            execute_command_callback("ACCELERATE", car_controller)

        execute_command_callback("SOS", car_controller)

        self.assertEqual(car_controller.get_speed(), 0)
        self.assertEqual(car_controller.get_engine_status(), False)
        self.assertEqual(car_controller.get_left_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_right_door_lock(), "UNLOCKED")
        self.assertEqual(car_controller.get_trunk_status(), False)
        self.assertEqual(car_controller.gear(), "P")


    def test_gear_default(self):
        car = Car()
        car_controller = CarController(car)

        execute_command_callback("GEAR_P", car_controller)
        self.assertEqual(testGear("GEAR_P",car_controller), "P")

        execute_command_callback("GEAR_R", car_controller)
        self.assertEqual(testGear("GEAR_R",car_controller), "P")

        execute_command_callback("GEAR_D", car_controller)
        self.assertEqual(testGear("GEAR_D",car_controller), "P")

        execute_command_callback("GEAR_N", car_controller)
        self.assertEqual(testGear("GEAR_N",car_controller), "P")


    def test_gear_driving(self):
        car = Car()
        car_controller = CarController(car)

        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("GEAR_D", car_controller)

        if car_controller.get_speed() < 130:
            execute_command_callback("ACCELERATE", car_controller)

        execute_command_callback("GEAR_R", car_controller)
        self.assertEqual(testGear("GEAR_R",car_controller), "D")

        execute_command_callback("GEAR_N", car_controller)
        self.assertEqual(testGear("GEAR_N",car_controller), "D")

        execute_command_callback("GEAR_P", car_controller)
        self.assertEqual(testGear("GEAR_P",car_controller), "D")

    def test_gear_brake_after_accelerate(self):
        car = Car()
        car_controller = CarController(car)

        execute_command_callback("ENGINE_BTN", car_controller)
        execute_command_callback("GEAR_D", car_controller)

        while car_controller.get_speed() < 130:
            execute_command_callback("ACCELERATE", car_controller)

        while car_controller.get_speed() != 0:
            
            execute_command_callback("BRAKE", car_controller)
            # 속도가 0이 되는 순간은 실행 되지 않게 하기 위해
            if car_controller.get_speed() != 0:
                execute_command_callback("GEAR_P", car_controller)
                self.assertEqual(testGear("GEAR_P",car_controller), "D")

                execute_command_callback("GEAR_R", car_controller)
                self.assertEqual(testGear("GEAR_R",car_controller), "D")

                execute_command_callback("GEAR_N", car_controller)
                self.assertEqual(testGear("GEAR_N",car_controller), "D")


        
        execute_command_callback("GEAR_P", car_controller)
        self.assertEqual(testGear("GEAR_P",car_controller), "P")

        execute_command_callback("GEAR_R", car_controller)
        self.assertEqual(testGear("GEAR_R",car_controller), "R")

        execute_command_callback("GEAR_D", car_controller)
        self.assertEqual(testGear("GEAR_D",car_controller), "D")

        execute_command_callback("GEAR_N", car_controller)
        self.assertEqual(testGear("GEAR_N",car_controller), "N")



if __name__ == '__main__':
    unittest.main()