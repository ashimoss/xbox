import time
from xbox360controller import Xbox360Controller
from api import RobotAPI
import sys
import math
import signal

speed = 1
acceleration = 0.9

class Rozum_xbox_control():
    
    def initialization(self):
        # Инициализация робота
        addr = "localhost"
        if len(sys.argv) > 1:
            addr = sys.argv[1]
        try:
            rr = RobotAPI(ip=addr)
            rr.init_robot()
            rr.hold()
            rr.await_motion()
            print("Робот инициализирован и готов к управлению")
        except Exception as e:
            print(f"Ошибка инициализации робота: {e}")

def controller_handler(rr):
    def getActPose_deg(rr):
        act_q = list(rr.ctrl.data["act_q"])
        for i in range(6):
            act_q[i] = math.degrees(act_q[i])
        return act_q

    # ПЕРВОЕ ЗВЕНО
    def on_button_pressed_A(button):
        act_q = getActPose_deg(rr)  
        print(f'Первое звено: {act_q[0]}')

    # ВТОРОЕ ЗВЕНО
    def on_button_pressed_B(button):
        act_q = getActPose_deg(rr)  
        print(f'Второе звено: {act_q[1]}')

    def on_button_pressed_X(button): # функция кнопки Х из файла test_1 
        with Xbox360Controller() as controller:
            # controller.set_rumble(1, 0, 1000)
            # time.sleep(1)
            on_button_X() # функция перемещения которую мы вписали в функцию кнопки, то есть по факту получается функция в функции,
            # то есть мы будем брать все функции из test_1 записывать их инициализацию в try
            # КОМАНДЫ ДЛЯ РОБОТА СМОТРЕТЬ В n1
    
     
    def on_button_X():
        act_q = getActPose_deg(rr)
                  # крутим первое звено нажатием кнопки A на 10 градусов
        rr.add_wp(des_q=[math.radians(act_q[0]+10), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() # движение
        rr.await_motion()
        print(f'Первое звено преместилось: {act_q[0]}')

    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            print(f"🎮 Контроллер '{controller.name}' подключен")
            print("Нажмите кнопку A для получения текущего положения")
            print("Нажмите Ctrl+C для выхода\n")

            # Назначение обработчиков кнопок
            controller.button_a.when_pressed = on_button_pressed_A
            controller.button_b.when_pressed = on_button_pressed_B
            controller.button_x.when_pressed = on_button_pressed_X
          
            signal.pause()

    except KeyboardInterrupt:
        print("\nОтключение контроллера")

            

    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    except Exception as e:
        print(f"Ошибка контроллера: {e}")
    finally:   
        print("Робот освобожден")

if __name__ == "__main__":
    controller_handler(rr)