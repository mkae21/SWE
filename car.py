class Car:
    def __init__(self, engine_on=False, speed=0, lock=True, trunk_status=True):
        self.__engine_on = engine_on  # True = ON / False = OFF
        self.__speed = speed  # km/h
        self.__lock = lock  # True = Locked / False = Unlocked
        self.__trunk_status = trunk_status  # True = Closed / False = Opened
        self.__left_door_status = "CLOSED"  # "OPEN" or "CLOSED"
        self.__right_door_status = "CLOSED"  # "OPEN" or "CLOSED"
        self.__left_door_lock = "LOCKED"  # "LOCKED" or "UNLOCKED"8
        self.__right_door_lock = "LOCKED"  # "LOCKED" or "UNLOCKED"
        self.__brake_status = "ON"  # 브레이크 상태, 'ON' 또는 'OFF'

    # 엔진 상태 읽기
    @property
    def engine_on(self):
        return self.__engine_on

    # 속도 읽기
    @property
    def speed(self):
        return self.__speed

    @property
    def lock(self):
        return self.__lock

    # 차량 전체 잠금/잠금 해제
    def lock_vehicle(self):
        self.__lock = True

    def unlock_vehicle(self):
        self.__lock = False

    # 트렁크 상태 읽기
    @property
    def trunk_status(self):
        return self.__trunk_status

    # 좌측 도어 상태 읽기
    @property
    def left_door_status(self):
        return self.__left_door_status

    # 우측 도어 상태 읽기
    @property
    def right_door_status(self):
        return self.__right_door_status

    # 좌측 도어 잠금 상태 읽기
    @property
    def left_door_lock(self):
        return self.__left_door_lock

    # 우측 도어 잠금 상태 읽기
    @property
    def right_door_lock(self):
        return self.__right_door_lock

    # 엔진 토글
    def toggle_engine(self):
        self.__engine_on = not self.__engine_on

    # 가속
    def accelerate(self):
        if self.__engine_on:
            self.__speed += 10

    # 브레이크
    @property
    def brake_status(self):
        return self.__brake_status

    def ON_brake(self):
        self.__brake_status = "ON"  # 브레이크 눌림 상태
        self.__speed = max(0, self.__speed - 10)  # 브레이크가 눌리면 속도를 줄임

    def OFF_brake(self):
        self.__brake_status = "OFF"  # 브레이크 떼짐 상태

    def start_acceleration(self):
        #속도를 초당 3km씩 증가시키고, 최대 15km로 제한(엑셀 OFF)
        if self.__brake_status == "OFF":  # 브레이크 상태가 OFF일 때만 가속
            while self.__speed <= 15:  # 시속 15km에 도달할 때까지
                self.__speed += 3  # 초당 시속 3km씩 증가
            self.__speed = 15  # 속도는 15km로 유지
            return True
        return False

    # 트렁크 열기
    def open_trunk(self):
        self.__trunk_status = False

    # 트렁크 닫기
    def close_trunk(self):
        self.__trunk_status = True

    # 좌측 도어 열기/닫기
    def open_left_door(self):
        self.__left_door_status = "OPEN"

    def close_left_door(self):
        self.__left_door_status = "CLOSED"

    # 우측 도어 열기/닫기
    def open_right_door(self):
        self.__right_door_status = "OPEN"

    def close_right_door(self):
        self.__right_door_status = "CLOSED"

    # 좌측 도어 잠금/잠금 해제
    def lock_left_door(self):
        self.__left_door_lock = "LOCKED"

    def unlock_left_door(self):
        self.__left_door_lock = "UNLOCKED"

    # 우측 도어 잠금/잠금 해제
    def lock_right_door(self):
        self.__right_door_lock = "LOCKED"

    def unlock_right_door(self):
        self.__right_door_lock = "UNLOCKED"
