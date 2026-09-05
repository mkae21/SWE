# SWE - Vehicle Control Simulator

Python으로 구현한 **차량 제어 요구사항 시뮬레이터**입니다.

차량의 엔진, 기어, 가속/감속, 도어, 트렁크, 잠금, SOS 기능을 구현하고,
**현재 차량 상태에 따라 명령 수행 가능 여부를 판단**하도록 설계했습니다.

GUI와 시나리오 파일을 통해 차량 상태 변화를 확인할 수 있으며,
Unit Test를 통해 정상/예외 상황을 검증합니다.

---

## 주요 기능

* Engine ON / OFF
* P / R / N / D Gear 변경
* 차량 가속 / 감속
* 최대 속도 `130 km/h` 제한
* `30 km/h` 이상 주행 시 Door 자동 잠금
* Door Open / Close / Lock / Unlock
* Trunk Open / Close
* Vehicle Lock / Unlock
* SOS 긴급 정지 기능
* Scenario 기반 명령 실행
* Python `unittest` 기반 기능 검증

---

## 차량 제어 예시

차량 명령은 현재 상태에 따라 실행 여부가 결정됩니다.

예를 들어 가속은 다음 조건에서만 가능합니다.

```text
Engine == ON
Gear == D or R
Speed < 130 km/h
```

따라서 다음 상태에서는:

```text
Engine : ON
Gear   : P
Speed  : 0 km/h
```

`ACCELERATE` 명령을 입력해도 차량은 가속하지 않습니다.

---

## SOS

주행 중 `SOS` 명령이 입력되면 차량을 안전 상태로 변경합니다.

```text
SOS
 ↓
감속
 ↓
Speed = 0
 ↓
Engine OFF
 ↓
Gear = P
 ↓
Door Unlock
 ↓
Trunk Open
```

---

## 구조

```text
Scenario File
      ↓
   main.py
      ↓
Requirement Validation
      ↓
CarController
      ↓
     Car
      ↓
     GUI
```

### 주요 파일

```text
SWE/
├── main.py
├── car.py
├── car_controller.py
├── gui.py
│
├── accel_unittest.py
├── test_engine_btn.py
├── testTrunk.py
├── test_gear&SOS.py
├── unitest_brake_lock_unlock.py
│
└── example_*
```

| File                | 역할              |
| ------------------- | --------------- |
| `car.py`            | 차량 상태 관리        |
| `car_controller.py` | 차량 상태 변경 인터페이스  |
| `main.py`           | 명령 처리 및 요구사항 검증 |
| `gui.py`            | 차량 상태 GUI       |
| `test_*.py`         | 기능별 Unit Test   |
| `example_*`         | 차량 제어 시나리오      |

---

## 사용 기술

* Python 3
* Tkinter
* unittest
* threading

---

## 실행

```bash
git clone https://github.com/mkae21/SWE.git
cd SWE

python main.py
```

실행 후 테스트할 Scenario 파일명을 입력합니다.

```text
Please enter the command file path:
```

예:

```text
example_sos_default_S
```

파일에 작성된 차량 명령이 순차적으로 실행되며 GUI에서 상태 변화를 확인할 수 있습니다.

---

## Scenario Example

```text
UNLOCK
BRAKE ENGINE_BTN
GEAR_D
ACCELERATE
ACCELERATE
ACCELERATE
BRAKE
BRAKE
BRAKE
GEAR_P
BRAKE ENGINE_BTN
```

각 명령 실행 전 현재 차량 상태를 검사하고,
요구사항을 만족하는 경우에만 상태를 변경합니다.

---

## Test

각 기능은 Python `unittest`를 이용하여 검증했습니다.

주요 검증 항목:

* Engine ON / OFF 조건
* 주행 중 Gear 변경 방지
* Engine OFF 상태에서 가속 방지
* 최대 속도 제한
* 30 km/h 이상 Door 자동 잠금
* Trunk Open 조건
* Lock / Unlock
* SOS 긴급 정지

예:

```bash
python accel_unittest.py
python test_engine_btn.py
python testTrunk.py
```

---

## 핵심 구현 포인트

이 프로젝트에서는 차량 기능 자체보다 **상태에 따른 요구사항 검증**에 중점을 두었습니다.

```text
Command
   ↓
현재 차량 상태 확인
   ↓
Pre-condition 검증
   ↓
명령 실행 / 거부
   ↓
차량 상태 변경
```

이를 통해 정상 동작뿐 아니라 잘못된 명령 순서와 예외 상황도 함께 테스트할 수 있도록 구현했습니다.
