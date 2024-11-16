import threading
from car import Car
from car_controller import CarController
from gui import CarSimulatorGUI


# execute_command를 제어하는 콜백 함수
# -> 이 함수에서 시그널을 입력받고 처리하는 로직을 구성하면, 알아서 GUI에 연동이 됩니다.

def execute_command_callback(command, car_controller):
    if command == "ENGINE_BTN":
        if car_controller.car.engine_on == False:  # 엔진이 꺼져 있을때
            if car_controller.get_speed() == 0:
                if car_controller.gear() == "P": # 속도가 0이면 브레이크가 눌린 상태로 간주, 기어는 p상태
                    car_controller.toggle_engine()  # 엔진 켜기
            else:
                print("브레이크 페달을 밟아야합니다.")  # 속도가 0이 아니면 경고 메시지 출력
        elif car_controller.car.engine_on == True:  # 엔진이 켜져 있을 경우
            if car_controller.get_speed() == 0 and car_controller.gear() == "P":  # 속도가 0이고 기어가 P일 때만
                car_controller.toggle_engine()  # 엔진 끄기
            else:
                print("엔진을 끄려면 속도가 0이고 기어가 P여야 합니다.")

    elif command == "ACCELERATE":
        if car_controller.car.engine_on == True: # 엔진이 켜져있을때만 엑셀 작동
            if car_controller.gear() in ["R", "D"]: # 기어가 R이나 D일때만 작동
                if car_controller.get_speed() < 130:  # 시속 130km 이상으로 증가하지 않도록 제한
                    car_controller.accelerate()  # 속도 +10
                    print(f"가속 페달 상태: ON, 현재 속도: {car_controller.get_speed()} km/h")

                    # 속도가 30km/h에 도달하면 모든 문을 잠금
                    if car_controller.get_speed() >= 30 and not car_controller.get_lock_status():
                        car_controller.lock_left_door() # 왼쪽문 잠금
                        car_controller.lock_right_door() # 오른쪽문 잠금
                        print("모든 문이 잠겼습니다.")
                else:
                    print("최대 속도에 도달하여 더 이상 가속할 수 없습니다.")
            else:
                print("기어가 R이나 D일때만 가속 페달이 작동합니다.")
        else:
            print("엔진이 켜져있을때만 가속 페달이 작동합니다.")

    elif command == "BRAKE":
        # 브레이크 페달을 밟았을 때의 동작
        if car_controller.get_speed() > 0:  # 시속 0km 이하로 감소하지 않도록 제한
            car_controller.brake()  # 속도 -20
            print(f"브레이크 페달 상태: ON, 현재 속도: {car_controller.get_speed()} km/h")
        else:
            print("속도가 0km/h이므로 더 이상 감속할 수 없습니다.")
    elif command == "LOCK":
        if car_controller.get_lock_status == False: # 차량 전체 잠금이 False일 때
            car_controller.lock_vehicle() # 차량잠금
            car_controller.lock_left_door() # 왼쪽문 잠금
            car_controller.lock_right_door() # 오른쪽문 잠금
    elif command == "UNLOCK":
        car_controller.unlock_vehicle() # 차량잠금해제
        if car_controller.get_lock_status: # 차량 전체 잠금이 False일 때
            car_controller.unlock_vehicle() # 차량잠금
            car_controller.unlock_left_door() # 왼쪽문 잠금해제
            car_controller.unlock_right_door() # 오른쪽문 잠금해제
    elif command == "LEFT_DOOR_LOCK":
        car_controller.lock_left_door() # 왼쪽문 잠금
    elif command == "LEFT_DOOR_UNLOCK":
        car_controller.unlock_left_door() # 왼쪽문 잠금해제
    elif command == "RIGHT_DOOR_LOCK":
        car_controller.lock_right_door() # 오른쪽문 잠금
    elif command == "RIGHT_DOOR_UNLOCK":
        car_controller.unlock_right_door() # 오른쪽문 잠금해제
    elif command == "LEFT_DOOR_OPEN":
        if car_controller.get_left_door_lock() == "UNLOCKED":
            car_controller.open_left_door() # 왼쪽문 열기
        else:
            print("왼쪽 문이 잠겨있습니다.")
    elif command == "LEFT_DOOR_CLOSE":
        car_controller.close_left_door() # 왼쪽문 닫기
    elif command == "RIGHT_DOOR_OPEN":
        if car_controller.get_right_door_lock() == "UNLOCKED":
            car_controller.open_right_door()  # 오른쪽문 열기
        else:
            print("오른쪽 문이 잠겨있습니다.")

    elif command == "RIGHT_DOOR_CLOSE":
        car_controller.close_right_door() # 오른쪽문 닫기
    elif command == "TRUNK_OPEN":
        if car_controller.gear() != "P" or car_controller.get_speed() != 0:
            print("트렁크를 열려면 기어를 'P'에 두고 차량의 속도가 0이어야 합니다.")
        elif car_controller.get_lock_status() == True: #false가 unlocked이다.
            print("트렁크를 열 수 없습니다.")
        else:
            if car_controller.get_trunk_status() == False:
                print("이미 트렁크가 열려 있습니다.")
            else:
                car_controller.open_trunk() # 트렁크 열기
                print("트렁크가 열렸습니다.")
    elif command == "TRUNK_CLOSE":
        if car_controller.get_trunk_status()== True:
            print("이미 트렁크가 닫혀 있습니다.")
        else:
            car_controller.close_trunk() # 트렁크 닫기
            print("트렁크가 닫혔습니다.")
    elif command == "SOS": 
        print("SOS 신호 수신.")
        if car_controller.get_engine_status(): # 엔진이 켜져있을 때
            while car_controller.get_speed() != 0: # 차량 속력이 0이 될 때까지
                car_controller.brake()
                print(f"속도: {car_controller.get_speed()} km/h")

        if car_controller.get_speed() == 0 and car_controller.get_engine_status(): # 차량 속력이 0이 되면
            car_controller.toggle_engine() # 엔진 정지
            print("엔진이 꺼졌습니다.")

        if car_controller.gear != "P":
            car_controller.gear_p() # 기어 P로 변경
            print("기어가 P(주차)로 변경되었습니다.")

        car_controller.unlock_left_door() # 왼쪽문 열기
        print("왼쪽문이 열렸습니다.")
        car_controller.unlock_right_door() #오른쪽문 열기
        print("오른쪽문이 열렸습니다.")
        car_controller.open_trunk() # 트렁크 열기
        print("트렁크가 열렸습니다.")

        # 기어 명령 추가
    elif command == "GEAR_P":
        if car_controller.get_speed() == 0 and car_controller.get_engine_status():
            car_controller.gear_p()  # 주차 기어로 전환
            print("기어가 P(주차)로 변경되었습니다.")
        elif car_controller.get_speed() == 0 and car_controller.get_engine_status()==False:
            print("엔진이 꺼져있습니다. 엔진을 켜주세요.")
        else:
            print("속도가 0이 아닙니다. 기어를 P로 변경하려면 속도를 0으로 줄이세요. ")

    elif command == "GEAR_R":
        if car_controller.get_speed() == 0 and car_controller.get_engine_status():
            car_controller.gear_r()  # 후진 기어로 전환
            print("기어가 R(후진)로 변경되었습니다.")
        elif car_controller.get_speed() == 0 and car_controller.get_engine_status()==False:
            print("엔진이 꺼져있습니다. 엔진을 켜주세요.")
        else:
            print("속도가 0이 아닙니다. 기어를 R로 변경하려면 속도를 0으로 줄이세요.")

    elif command == "GEAR_D":
        if car_controller.get_speed() == 0 and car_controller.get_engine_status():
            car_controller.gear_d()  # 주행 기어로 전환
            print("기어가 D(주행)로 변경되었습니다.")
        elif car_controller.get_speed() == 0 and car_controller.get_engine_status()==False:
            print("엔진이 꺼져있습니다. 엔진을 켜주세요.")
        else:
            print("속도가 0이 아닙니다. 기어를 D로 변경하려면 속도를 0으로 줄이세요.")

    elif command == "GEAR_N" and car_controller.get_engine_status():
        if car_controller.get_speed() == 0 and car_controller.get_engine_status():
            car_controller.gear_n() # 중립 기어로 전환
            print("기어가 N(중립)으로 변경되었습니다.")
        elif car_controller.get_speed() == 0 and car_controller.get_engine_status()==False:
            print("엔진이 꺼져있습니다. 엔진을 켜주세요.")
        else:
            print("속도가 0이 아닙니다. 기어를 N으로 변경하려면 속도를 0으로 줄이세요.")


# 파일 경로를 입력받는 함수
# -> 가급적 수정하지 마세요.
#    테스트의 완전 자동화 등을 위한 추가 개선시에만 일부 수정이용하시면 됩니다. (성적 반영 X)
def file_input_thread(gui):
    while True:
        file_path = input("Please enter the command file path (or 'exit' to quit): ")

        if file_path.lower() == 'exit':
            print("Exiting program.")
            break

        # 파일 경로를 받은 후 GUI의 mainloop에서 실행할 수 있도록 큐에 넣음
        gui.window.after(0, lambda: gui.process_commands(file_path))



# 메인 실행
# -> 가급적 main login은 수정하지 마세요.
if __name__ == "__main__":
    car = Car()
    car_controller = CarController(car)

    # GUI는 메인 스레드에서 실행
    gui = CarSimulatorGUI(car_controller, lambda command: execute_command_callback(command, car_controller))

    # 파일 입력 스레드는 별도로 실행하여, GUI와 병행 처리
    input_thread = threading.Thread(target=file_input_thread, args=(gui,))
    input_thread.daemon = True  # 메인 스레드가 종료되면 서브 스레드도 종료되도록 설정
    input_thread.start()

    # GUI 시작 (메인 스레드에서 실행)
    gui.start()