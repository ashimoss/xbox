import time
from xbox360controller import Xbox360Controller
from api import RobotAPI
import sys
import math
import signal
import runpy
import socket

  
speed = 1
acceleration = 0.9

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


# def free_port(api) -> None:
#     """
#     Освобождает порт, *не отключая* питание робота:
#     • корректно рвём текущий TCP-сеанс;
#     • обнуляем ссылку api.socket, чтобы RobotAPI создал
#         новое соединение при следующем _connect().
#     """
#     if api.socket:
#         try:
#             print("Освобождаем порт для нового подключения …")
#             api.socket.shutdown(socket.SHUT_RDWR)
#         except Exception:
#             pass
#         try:
#             api.socket.close()
#         finally:
#             api.socket = None  # важно для повторной инициализации

def controller_handler(rr):
    def getActPose_deg(rr):
        act_q = list(rr.ctrl.data["act_q"])
        for i in range(6):
            act_q[i] = math.degrees(act_q[i])
        return act_q

    # # ПЕРВОЕ ЗВЕНО
    # def on_button_pressed_A(button):
    #     act_q = getActPose_deg(rr)  
    #     print(f'Первое звено: {act_q[0]}')

    # # ВТОРОЕ ЗВЕНО
    # def on_button_pressed_B(button):
    #     act_q = getActPose_deg(rr)  
    #     print(f'Второе звено: {act_q[1]}')

# ПЕРВОЕ ЗВЕНО
    def on_button_pressed_X(button): # функция кнопки Х из файла test_1 
        with Xbox360Controller() as controller:
            controller.set_rumble(1, 0, 1000)
    
            on_button_X() # функция перемещения которую мы вписали в функцию кнопки, то есть по факту получается функция в функции,
            # то есть мы будем брать все функции из test_1 записывать их инициализацию в try
            # КОМАНДЫ ДЛЯ РОБОТА СМОТРЕТЬ В n1
    
    def on_button_X():
        act_q = getActPose_deg(rr)
                  # функция создает точку в которую нужно перместиться (для первого звена)
        rr.add_wp(des_q=[math.radians(act_q[0]+10), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() #движение
        rr.await_motion()
        print(f'Первое звено переместилось: {act_q[0]}')

# ВТОРОЕ ЗВЕНО
    def on_button_pressed_Y(button): 
        with Xbox360Controller() as controller:
    
            on_button_Y()
        
    def on_button_Y():
        act_q = getActPose_deg(rr)
        rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]+10), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() #движение
        rr.await_motion()
        print(f'Второе звено переместилось: {act_q[1]}')

# ТРЕТЬЕ ЗВЕНО
    def on_button_pressed_B(button): 
        with Xbox360Controller() as controller:
    
            on_button_B()
        
    def on_button_B():
        act_q = getActPose_deg(rr)
        rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]+10), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() #движение
        rr.await_motion()
        print(f'Третье звено переместилось: {act_q[2]}')

# ЧЕТВЕРТОЕ ЗВЕНО
    def on_button_pressed_A(button): 
        with Xbox360Controller() as controller:
    
            on_button_A() 
        
    def on_button_A():
        act_q = getActPose_deg(rr)
        rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]+10), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() #движение
        rr.await_motion()
        print(f'Четвертое звено преместилось: {act_q[3]}')

# ПЯТОЕ ЗВЕНО
    def on_lb_pressed(button): 
        with Xbox360Controller() as controller:
    
            on_left_bumper() 
        
    def on_left_bumper():
        act_q = getActPose_deg(rr)
        rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]+10), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() #движение
        rr.await_motion()
        print(f'Пятое звено преместилось: {act_q[4]}')

# ШЕСТОЕ ЗВЕНО
    def on_rb_pressed(button): 
        with Xbox360Controller() as controller:
    
            on_right_bumper() 
        
    def on_right_bumper():
        act_q = getActPose_deg(rr)
        rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5]+10)], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
        rr.run_wps() #движение
        rr.await_motion()
        print(f'Шестое звено преместилось: {act_q[5]}')

# ОТКРЫТИЕ И ЗАКРЫТИЕ СХВАТА

    # def on_lt_moved(trigger): 
    #     with Xbox360Controller() as controller:
    #         print(trigger.value)
    #         if trigger.value > 0.5:
    #             rr.write_dig_output(8, 1)
    #             print('Открытие: выход вкл')
    #         else:
    #             rr.write_dig_output(8, 0)
    #             print('Открытие: выход выкл')
                
    # def on_rt_moved(trigger): 
    #     with Xbox360Controller() as controller:
    #         if trigger.value > 0.5:
    #             rr.write_dig_output(9, 1)
    #             print('Закрытие: выход вкл')
    #         else:
    #             rr.write_dig_output(9, 0)
    #             print('Закрытие: выход выкл')

    # ВКЛЮЧЕНИЕ ZERO GRAVITY
    # def set_io_func(self, hold_in, zg_in):

    #     if hold_in[1]:
    #         hold_in[0] |= 0x80000000
    #     if zg_in[1]:
    #         zg_in[0] |= 0x80000000

    #     self._cmd(CTRLR_COMS_SET_IO_FUNC, struct.pack("2I", hold_in[0], zg_in[0]))

    def on_lt_moved(trigger):
        with Xbox360Controller() as controller:
            if trigger.value > 0.5:
                rr.zg(1)
                print('Лови меня')
            else:
            #rr.zg(0)
                print('держусь')
        #print(f'Лови меня')


    # ВКЛЮЧЕНИЕ И ВЫКЛЮЧЕНИЕ РОБОТА 
    def on_start_pressed(button):
        with Xbox360Controller() as controller:
            on_button_start()
        
    def on_button_start():
        rr.run()
        print(f'Робот проснулся')


    def on_back_pressed (button):
        with Xbox360Controller() as controller:
           on_button_back()     

    def on_button_back():
        rr.off()
        print(f'Робот уснул')

    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            print(f"🎮 Контроллер '{controller.name}' подключен")
            print("Нажмите кнопку A для получения текущего положения")
            print("Нажмите Ctrl+C для выхода\n")

            # Назначение обработчиков кнопок
            controller.button_a.when_pressed = on_button_pressed_A
            controller.button_b.when_pressed = on_button_pressed_B
            controller.button_x.when_pressed = on_button_pressed_X
            controller.button_y.when_pressed = on_button_pressed_Y
            controller.button_trigger_l.when_pressed = on_lb_pressed
            controller.button_trigger_r.when_pressed = on_rb_pressed

             # Триггеры
            controller.trigger_l.when_moved = on_lt_moved
            # controller.trigger_r.when_moved = on_rt_moved

            # Кнопка start
            controller.button_start.when_pressed = on_start_pressed
            controller.button_select.when_pressed = on_back_pressed
            #controller.button_mode.when_pressed = on_xbox_pressed

            signal.pause()

    except KeyboardInterrupt:
        print("\nОтключение контроллера")

            

    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    except Exception as e:
        print(f"Ошибка контроллера: {e}")
    finally:
        
        print("Добби свободен")

if __name__ == "__main__":
    controller_handler(rr)