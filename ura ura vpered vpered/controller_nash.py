import signal
import time
from xbox360controller import Xbox360Controller

# --- Обработчики цветных кнопок ---
def on_button_pressed_A(button):
    with Xbox360Controller() as controller:
        controller.set_led(Xbox360Controller.LED_BLINK_SLOW)
        time.sleep(1)
        controller.set_led(Xbox360Controller.LED_OFF)
    print(f'[A] Нажата')

def on_button_pressed_B(button):
    with Xbox360Controller() as controller:
        controller.set_rumble(0, 1, 1000)
        time.sleep(1)
    print(f'[B] Нажата')

def on_button_pressed_X(button):
    with Xbox360Controller() as controller:
        controller.set_rumble(1, 0, 1000)
        time.sleep(1)
    print(f'[X] Нажата')

def on_button_pressed_Y(button):
    print(f'[Y] Нажата')

# --- Обработчики бамперов ---
def on_lb_pressed(button):
    print('[LB] Левый бампер нажат')

def on_lb_released(button):
    print('[LB] Левый бампер отпущен')

def on_rb_pressed(button):
    print('[RB] Правый бампер нажат')

def on_rb_released(button):
    print('[RB] Правый бампер отпущен')

# --- Обработчики триггеров ---
TRIGGER_THRESHOLD = 0.3

def on_lt_moved(trigger):
    if trigger.value > TRIGGER_THRESHOLD:
        print(f'[LT] Левый триггер: Я работаю')
    else:
        print('[LT] Левый триггер отпущен')

def on_rt_moved(trigger):
    if trigger.value > TRIGGER_THRESHOLD:
        print(f'[RT] Правый триггер: Я РАБОТАЮ')
    else:
        print('[RT] Правый триггер отпущен')

# --- Обработчики стиков ---
def on_left_stick_moved(axis):
    print(f'[ЛЕВЫЙ СТИК] X:{axis.x:.2f} Y:{axis.y:.2f}')

def on_right_stick_moved(axis):
    print(f'[ПРАВЫЙ СТИК] X:{axis.x:.2f} Y:{axis.y:.2f}')

def on_left_stick_pressed(button):
    print('[L3] Левый стик нажат')

def on_right_stick_pressed(button):
    print('[R3] Правый стик нажат')

# --- Обработчик крестовины ---
def on_dpad_moved(axis):
    if axis.x > 0.5:
        print("▶ Стрелка вправо")
    elif axis.x < -0.5:
        print("◀ Стрелка влево")
    elif axis.y > 0.5:
        print("▲ Стрелка вверх")
    elif axis.y < -0.5:
        print("▼ Стрелка вниз")
    elif axis.x == 0 and axis.y == 0:
        print("[DPAD] Нейтрально")


# --- Основной код ---
     

try:
    with Xbox360Controller(0, axis_threshold=0.2) as controller:
        print(f"🎮 Контроллер '{controller.name}' подключен\n")
           
        # Цветные кнопки без функций
        controller.button_a.when_pressed = on_button_pressed_A
        controller.button_b.when_pressed = on_button_pressed_B
        controller.button_x.when_pressed = on_button_pressed_X
        controller.button_y.when_pressed = on_button_pressed_Y
        
        # Бамперы
        controller.button_trigger_l.when_pressed = on_lb_pressed
        controller.button_trigger_l.when_released = on_lb_released
        controller.button_trigger_r.when_pressed = on_rb_pressed
        controller.button_trigger_r.when_released = on_rb_released
        
        # Триггеры
        controller.trigger_l.when_moved = on_lt_moved
        controller.trigger_r.when_moved = on_rt_moved
        
        # Стики (движение)
        controller.axis_l.when_moved = on_left_stick_moved
        controller.axis_r.when_moved = on_right_stick_moved
        
        # Стики (нажатие)
        controller.button_thumb_l.when_pressed = on_left_stick_pressed
        controller.button_thumb_r.when_pressed = on_right_stick_pressed
        
        # Крестовина
        controller.hat.when_moved = on_dpad_moved

        # Кнопки Start и Back (Mode)
        controller.button_start.when_pressed = lambda b: print('[START] Нажата')
        controller.button_select.when_pressed = lambda b: print('[BACK] Нажата')
        controller.button_mode.when_pressed = lambda b: print('[XBOX GUIDE] Нажата')
        
        print("\nГотов к работе! Используйте:")
        print("A/B/X/Y - Основные кнопки")
        print("LB/RB - Бамперы")
        print("LT/RT - Триггеры")
        print("Левый/Правый стик - Движение")
        print("L3/R3 - Нажатие стиков")
        print("DPAD - Крестовина")
        print("Ctrl+C - Выход\n")
      
        
        signal.pause()

except KeyboardInterrupt:
    print("\nОтключение контроллера")

# Вывод информации о контроллере
with Xbox360Controller() as controller:
    controller.info()