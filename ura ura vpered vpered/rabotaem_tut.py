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
moved = 0
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
        # print('act_q =', act_q)
        for i in range(6):
            act_q[i] = math.degrees(act_q[i])
        # print(act_q)
        return act_q
            
#  # ВТОРОЕ ЗВЕНО
#     def on_button_pressed_Y(button):
#         with Xbox360Controller() as controller:
#             on_button_Y()

#     def on_button_Y():
#         act_q = getActPose_deg(rr)
#         rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]+90), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
#         rr.run_wps() #движение
#         print(f'Второе звено переместилось: {act_q[1]}')

#     def on_button_released_Y(button):
#         with Xbox360Controller() as controller:
#             off_button_Y()
            
#     def off_button_Y():
#         rr.hold()
#         rr.await_motion()



# ПЕРВОЕ ЗВЕНО
    def on_left_stick_moved(axis):
        global moved
        # print(f'[ЛЕВЫЙ СТИК] X:{axis.x:.2f} Y:{axis.y:.2f}')
        with Xbox360Controller() as controller:
            if axis.x >= 0.4 and axis.x <=1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]+45), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Первое звено переместилось: {act_q[0]:.1f}')
                    moved=1
            elif axis.x < -0.4 and axis.x >=-1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]-45), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Первое звено переместилось: {act_q[0]:.1f}')
                    moved=1           
# ВТОРОЕ ЗВЕНО                    
            elif axis.y >= 0.4 and axis.y <=1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]+45), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Второе звено переместилось: {act_q[1]:.1f}')
                    moved=1
                    
            elif axis.y < -0.4 and axis.y >=-1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]-45), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Второе звено переместилось: {act_q[1]:.1f}')
                    moved=1
            else:
                moved=0
                rr.hold()
                rr.await_motion()

# ТРЕТЬЕ ЗВЕНО
    def on_dpad_moved(axis):
        global moved
        with Xbox360Controller() as controller:
            if axis.x > 0.5: # "▶ Стрелка вправо"
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]+20), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    print(f'Третье звено переместилось: {act_q[2]:.1f}')
                    moved=1
            elif axis.x < -0.5: # "◀ Стрелка влево"
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]-20), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    print(f'Третье звено переместилось: {act_q[2]:.1f}')
                    moved=1
# ЧЕТВЕРТОЕ ЗВЕНО
            elif axis.y > 0.5: # "▲ Стрелка вверх"
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]+20), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    print(f'Четвертое звено переместилось: {act_q[3]:.1f}')
                    moved=1
            elif axis.y < -0.5: # "▼ Стрелка вниз"
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]-20), math.radians(act_q[4]), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    print(f'Четвертое звено переместилось: {act_q[3]:.1f}')
                    moved=1
            else:
                moved=0
                rr.hold()
                rr.await_motion()

# ПЯТОЕ ЗВЕНО
    def on_right_stick_moved(axis):
        global moved
        with Xbox360Controller() as controller:
            if axis.x > 0.5 and axis.x <=1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]+45), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Пятое звено переместилось: {act_q[4]:.1f}')
                    moved=1
            elif axis.x < -0.5 and axis.x >=-1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]-45), math.radians(act_q[5])], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Пятое звено переместилось: {act_q[4]:.1f}')
                    moved=1
# ШЕСТОЕ ЗВЕНО                       
            elif axis.y > 0.5 and axis.y <=1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5]+45)], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Шестое звено переместилось: {act_q[5]:.1f}')
                    moved=1
                    
            elif axis.y < -0.5 and axis.y >=-1:
                if moved==0:
                    act_q = getActPose_deg(rr)
                    rr.add_wp(des_q=[math.radians(act_q[0]), math.radians(act_q[1]), math.radians(act_q[2]), math.radians(act_q[3]), math.radians(act_q[4]), math.radians(act_q[5]-45)], vmax_j=speed, amax_j=acceleration, rblend=0.7) # правильная команда
                    rr.run_wps() #движение
                    #print(f'Шестое звено переместилось: {act_q[5]:.1f}')
                    moved=1
            else:
                moved=0
                rr.hold()
                rr.await_motion()

# ОТКРЫТИЕ И ЗАКРЫТИЕ СХВАТА

    def on_lt_moved(trigger):
        with Xbox360Controller() as controller:
            print(trigger.value)
            if trigger.value > 0.5:
                rr.write_dig_output(8, 1)
                print('Открытие: выход вкл')
            else:
                rr.write_dig_output(8, 0)
                print('Открытие: выход выкл')

    def on_rt_moved(trigger):
        with Xbox360Controller() as controller:
            if trigger.value > 0.5:
                rr.write_dig_output(9, 1)
                print('Закрытие: выход вкл')
            else:
                rr.write_dig_output(9, 0)
                print('Закрытие: выход выкл')

    # ВКЛЮЧЕНИЕ ZERO GRAVITY
    def on_right_stick_pressed(button):
        with Xbox360Controller() as controller:
            print('Правый стик нажат')
            on_right_stick()

    def on_right_stick_released(button):
        with Xbox360Controller() as controller:
            print('Правый стик отпущен')


    def on_right_stick():
        rr.zg(1)

    # ВКЛЮЧЕНИЕ И ВЫКЛЮЧЕНИЕ РОБОТА
    def on_start_pressed(button):
        with Xbox360Controller() as controller:
            on_button_start()

    def on_button_start():
        rr.init_robot()
        rr.run()
        print(f'Робот проснулся')


    def on_back_pressed (button):
        with Xbox360Controller() as controller:
           on_button_back()

    def on_button_back():
        rr.off()
        rr._disconnect()
        print(f'Робот уснул')

    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            print(f"🎮 Контроллер '{controller.name}' подключен")
            print("Нажмите кнопку A для получения текущего положения")
            print("Нажмите Ctrl+C для выхода\n")

            # Назначение обработчиков кнопок
            #controller.button_a.when_pressed = on_button_pressed_A
            #controller.button_b.when_pressed = on_button_pressed_B
            #controller.button_x.when_pressed = on_button_pressed_X
            # controller.button_y.when_pressed = on_button_pressed_Y
            # controller.button_y.when_released = on_button_released_Y

            # Триггеры
            controller.trigger_l.when_moved = on_lt_moved
            controller.trigger_r.when_moved = on_rt_moved

            # Стики
            controller.button_thumb_r.when_pressed = on_right_stick_pressed
            controller.button_thumb_r.when_released = on_right_stick_released

            # Кнопка start
            controller.button_start.when_pressed = on_start_pressed
            controller.button_select.when_pressed = on_back_pressed

             # Стики (движение)
            controller.axis_l.when_moved = on_left_stick_moved
            controller.axis_r.when_moved = on_right_stick_moved

            # Крестовина (движение)
            controller.hat.when_moved = on_dpad_moved

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