import time
import board
import displayio
import digitalio
import gc
from adafruit_clue import clue
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
import adafruit_ble
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_lsm6ds import Rate, AccelRange

music_bmp = "/music_bitmap.bmp"
steps_bmp = "/steps_bmp.bmp"
set_bmp = "ustaw.bmp"
big_font = "/fonts/Roboto-Black-48.bdf"

glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '

big_font = bitmap_font.load_font(big_font)
big_font.load_glyphs(glyphs)

clue_display = board.DISPLAY
clue_display.brightness = 0.25

motor = digitalio.DigitalInOut(board.D2)
motor.direction = digitalio.Direction.OUTPUT

music_ = displayio.Group()
steps_ = displayio.Group()
settime = displayio.Group()
sethour_ = displayio.Group()

music = displayio.OnDiskBitmap(open(music_bmp, "rb"))
music_tilegrid = displayio.TileGrid(music, pixel_shader = getattr(music, 'pixel_shader', displayio.ColorConverter()))
music_.append(music_tilegrid)

steps_bmp = displayio.OnDiskBitmap(open(steps_bmp, "rb"))
steps_bmp_tilegrid = displayio.TileGrid(steps_bmp, pixel_shader = getattr(steps_bmp, 'pixel_shader', displayio.ColorConverter()))
steps_.append(steps_bmp_tilegrid)

settime_bg = displayio.OnDiskBitmap(open("/ALARM.bmp", "rb"))
settime_tilegrid = displayio.TileGrid(settime_bg, pixel_shader = getattr(settime_bg, 'pixel_shader', displayio.ColorConverter()))
settime.append(settime_tilegrid)

        
sethour = displayio.OnDiskBitmap(open("/ustaw.bmp", "rb"))
sethour_tilegrid = displayio.TileGrid(sethour, pixel_shader = getattr(sethour, 'pixel_shader', displayio.ColorConverter()))
sethour_.append(sethour_tilegrid)

sensor = LSM6DS33(board.I2C())

sensor.accelerometer_range = AccelRange.RANGE_2G
sensor.accelerometer_data_rate = Rate.RATE_26_HZ
sensor.gyro_data_rate = Rate.RATE_SHUTDOWN
sensor.pedometer_enable = True

text_steps = Label(big_font, text="0", color=clue.BLACK)
text_steps.x = 50
text_steps.y = 100
steps_.append(text_steps)


def see_steps(last_step):
    
    steps = sensor.pedometer_steps
    if abs(steps-last_step) >= 0:
        last_step = steps
        kcal = steps * 0.04
        text_steps.text = '%d' % steps
        return last_step
    else:
        return 0

def music_player(radio):
    print("connected")
    clue_display.brightness = 0.25
    func_start = time.monotonic()
    clue_display.show(music_)
    while radio.connected:
        gest = 0
        gest = clue.gesture
        for connection in radio.connections:
            if not connection.paired:
                connection.pair()

            ams = connection[AppleMediaService]
            print(ams.player_name)
            if (clue.button_a):
                ams.toggle_play_pause()
                time.sleep(0.7)
            if (clue.button_b):
                ams.next_track()
                time.sleep(0.7)
            if (gest == 4):
                return [1, time.monotonic() - func_start]
            elif (gest == 3):
                return [2, time.monotonic() - func_start]

class Clock_p():

    def __init__(self,):
        # pozycje na ekranie kazdej cyfry
        self.posTab = [180, 153, 120, 93, 60, 33]
        # tablica z Labelami
        self.digit = [0,0,0,0,0,0]

        self.tabSetDigit = [0,0,0,0]
        # tablica z alarmem
        self.alarmTab = []
        # tablica do ustawiania godziny
        self.tabSet = [0, 0, 0, 0, 0, 0]
        # kursor wskazujacy na ustawiana pozycje
        self.cursor=1
        # dodawanie grupy do wyswietlania zegarka
        self.clock_ = displayio.Group()
        self.clock_bg = displayio.OnDiskBitmap(open("/zegarek.bmp", "rb"))
        self.clock_tilegrid = displayio.TileGrid(self.clock_bg, pixel_shader = getattr(self.clock_bg, 'pixel_shader', displayio.ColorConverter()))
        self.clock_.append(self.clock_tilegrid)

    def positions(self, h, min, s):
        sec_low=s%10
        sec_high=s/10
        min_low=min%10
        min_high=min/10
        hour_low=h%10
        hour_high=h/10
        return [sec_low, sec_high, min_low, min_high, hour_low, hour_high]

    def fractSec(self, s):
        min, s = divmod(s, 60)
        h, min = divmod(min, 60)
        return [h, min, s]

    def addDigits(self, ypos):
        gc.collect()
        which_font = big_font
        for i in range(0, len(self.posTab)):
            self.digit[i] = Label(which_font, text = '0', color = clue.BLACK)
            self.digit[i].x = self.posTab[i]
            self.digit[i].y = ypos
        return self.digit

    def changeDigit(self, digits):
        for i in range(0, 6):
            self.digit[i].text = '%d' % digits[i]
        return self.clock_

    def setCursor(self):
        self.digit[0].text = '%d' % self.cursor

    def updateClock(self, texture = "/zegarek.bmp"):
        if (len(self.clock_) > 1):
            for i in range(0, 6):
                self.clock_.remove(self.digit[i])

        for i in range(0, 6):
            self.clock_.append(self.digit[i])


    def setTime_(self):
        value = clue.button_b
        choose= clue.button_a
        if(value):
            if(self.cursor==1):
                self.tabSet[0] += 1
                if (self.tabSet[0] > 9):
                    self.tabSet[0] = 0

            elif(self.cursor==2):
                self.tabSet[1] += 1
                if (self.tabSet[1] >= 6):
                    self.tabSet[1] = 0

            elif(self.cursor==3):
                self.tabSet[2] += 1
                if (self.tabSet[2] > 9):
                    self.tabSet[2] = 0

            elif(self.cursor==4):
                self.tabSet[3] += 1
                if (self.tabSet[3] > 2):
                    self.tabSet[3] = 0

        if(choose):
            self.cursor+=1
            if(self.cursor>4):
                self.cursor=1
                

        alarm_sec= self.tabSet[0]*60 + self.tabSet[1]*600 + self.tabSet[2]*3600 + self.tabSet[3]*36000
        return alarm_sec

clock = Clock_p()
clock.addDigits(160)

cnt = 0
sec_alarm=0
alarmSet = True
#liczba przejsc na sekunde
frameLast = 1
#obsluga wyboru ekranu
choose = 1
#obsluga alarmu
alarmFlag = False
alarm_flag=0
play_alarm = True
play = False
work = True
set_alarm = -1
alarmIsBeingSet = False
#ustawianie godziny
timeSet = False
#zwiekszanie czasu co sekunde
countAgain = True
working_time=-1
last_step = 0
sleep_time=0
counter_ble = 0
flag_hand=True

while True:
    gc.collect()

    while(counter_ble==0):
        radio = adafruit_ble.BLERadio()
        conn = SolicitServicesAdvertisement()
        conn.solicited_services.append(AppleMediaService)
        radio.start_advertising(conn)
        counter_ble = 1
        
    while not radio.connected:
        print("czekam na polaczenie")
        time.sleep(1)
    
    if (countAgain):
        frameStart = time.monotonic()
    
    gesture = clue.gesture
    if (gesture == 4):
        choose +=1
        sleep_time=0
    elif(gesture == 3):
        choose -=1
        sleep_time=0
    
    shake = clue.shake(21)
    print(shake)
    if (shake):
        print(flag_hand)
        if(flag_hand):
            clue_display.brightness = 0.25
            flag_hand = False
        else:
            clue_display.brightness = 0
            flag_hand = True
            
    if(sleep_time>30):
            clue_display.brightness = 0.05
    elif(sleep_time==0):
            clue_display.brightness = 0.25

    if(choose>3):
        choose=1
    if(choose<1):
        choose=3

    if not (timeSet):
        gc.collect()
        set_hour = clock.setTime_()
        set_seconds = clock.fractSec(set_hour)
        set_pos = clock.positions(set_seconds[0], set_seconds[1], set_seconds[2])
        new_ = clock.changeDigit(set_pos)
        clock.updateClock()
        clock.setCursor()
        clue_display.show(new_)
        flag = clue.gesture
        if (flag == 1):
            timeSet = True
        sleep_time=0
    else:
        

        # odpowiada za liczenie sekund w glownym zegarze
        gc.collect()
        actual_time = cnt + set_hour
        if (actual_time >= 86400):
            actual_time = 0
            cnt = 0
            set_hour = 0

        fract = clock.fractSec(actual_time)

        if (choose == 2):
            last_step = see_steps(last_step)
            clue_display.show(steps_)
            

        if (choose == 3):
            choose, working_time = music_player(radio)      

        if (choose == 1):
            gc.collect()
            setAlarm = clue.button_b
            if (setAlarm):
                alarmSet = False

            if (not alarmSet):
                alarmIsBeingSet = True
                set_alarm = clock.setTime_()
                alarm_sec = clock.fractSec(set_alarm)
                alarm_pos = clock.positions(alarm_sec[0], alarm_sec[1], alarm_sec[2])
                new_alarm = clock.changeDigit(alarm_pos)
                clock.updateClock()
                clue_display.show(new_alarm)
                work = True
                sleep_time=0

                alarmFlag = clue.gesture
                if (alarmFlag == 1):
                    alarmSet = True
                    alarmIsBeingSet = False

            if not (alarmIsBeingSet):
                gc.collect()
                pos = clock.positions(fract[0], fract[1], fract[2])
                change = clock.changeDigit(pos)
                clock.updateClock()
                clue_display.show(change)
        if(set_alarm==int(actual_time) and alarmSet):
            play = True
        if (play and work):
            alarm_set = clue.button_a
            if (alarm_set == True):
                motor.value = False
                work = False
                play=False
                sleep_time = 0
            clue_display.show(settime)

 

    if (working_time > 0):
        cnt = cnt + working_time
        working_time = 0
    

    frameTime = (time.monotonic() - frameStart)
    if(frameTime >= 0.7):
        cnt2=cnt
        cnt += 1
        
        sleep_time+=1
        countAgain = True
        if (play and work and play_alarm):
            gc.collect()
            clue.start_tone(5000)
            motor.value = True
            play_alarm = False
            clue.pixel.fill((255,255,255))
            clue.white_leds = True
        else:
            clue.stop_tone()
            clue.pixel.fill((0,0,0))
            clue.white_leds = False
            motor.value = False
            play_alarm = True
        
    else:
        countAgain = False