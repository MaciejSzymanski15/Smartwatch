import time
import board
import displayio
from adafruit_clue import clue
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label

bmp1_ = "/photos-icon.bmp"
bmp2_ = "/Data-Clock-icon.bmp"
bmp3_ = "/menu_.bmp"
big_font = "/fonts/Roboto-Black-48.bdf"
med_font = "/fonts/Roboto-Bold-24.bdf"

glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.: '

big_font = bitmap_font.load_font(big_font)
big_font.load_glyphs(glyphs)

med_font = bitmap_font.load_font(med_font)
med_font.load_glyphs(glyphs)

clue_display = board.DISPLAY
clue_display.brightness = 0.25

clock_ = displayio.Group()
menu_ = displayio.Group()

clue_bg = displayio.OnDiskBitmap(open(bmp2_, "rb"))
clue_tilegrid = displayio.TileGrid(
    clue_bg, pixel_shader=getattr(clue_bg, 'pixel_shader', displayio.ColorConverter())
)

my_menu = displayio.OnDiskBitmap(open(bmp3_, "rb"))
my_menu_tilegrid = displayio.TileGrid(
    my_menu, pixel_shader=getattr(my_menu, 'pixel_shader', displayio.ColorConverter())
)

menu_.append(my_menu_tilegrid)
clock_.append(clue_tilegrid)


def clock_p(counter_h_high, counter_h, counter_min_high, counter_min,counter_sec_high,counter_sec):
    """Returns (time_on_clock, time_off_clock), time_off_clock - time_on_clock = time while clock was opened"""
    time_on_clock = time.monotonic()
    sek_jed = Label(big_font, text = '0', color = clue.GREEN)
    sek_jed.x = 180
    sek_jed.y = 187
    clock_.append(sek_jed)

    sek_d = Label(big_font, text = '0', color = clue.GREEN)
    sek_d.x = 153
    sek_d.y = 187
    clock_.append(sek_d)

    min_jed = Label(big_font, text = '0', color = clue.GREEN)
    min_jed.x = 120
    min_jed.y = 187
    clock_.append(min_jed)

    min_d = Label(big_font, text = '0', color = clue.GREEN)
    min_d.x = 93
    min_d.y = 187
    clock_.append(min_d)

    hour_jed = Label(big_font, text = '0', color = clue.GREEN)
    hour_jed.x = 60
    hour_jed.y = 187
    clock_.append(hour_jed)

    hour_d = Label(big_font, text = '0', color = clue.GREEN)
    hour_d.x = 33
    hour_d.y = 187
    clock_.append(hour_d)


    clue_display.show(clock_)

    hh = counter_h_high
    hl = counter_h
    mh = counter_min_high
    ml =  counter_min
    sh = counter_sec_high
    sl = counter_sec

    while True:
        counter_sec += 1

        if (counter_sec == 10):
            counter_sec = 0
            counter_sec_high += 1

        if (counter_sec_high == 6):
            counter_sec_high = 0
            counter_min += 1

        if (counter_min == 10):
            counter_min_high += 1
            counter_min = 0

        if (counter_min_high == 6):
            counter_h += 1
            counter_min_high = 0

        if (counter_h == 10):
            counter_h_high += 1
            counter_h = 0

        if (counter_h_high == 2 and counter_h == 4):
            counter_sec = 0
            counter_sec_high = 0
            counter_min = 0
            counter_min_high = 0
            counter_h = 0
            counter_h_high = 0

        sek_jed.text = '%d' % counter_sec
        sek_d.text = '%d' % counter_sec_high
        min_jed.text = '%d' % counter_min
        min_d.text = '%d' % counter_min_high
        hour_jed.text = '%d' % counter_h
        hour_d.text = '%d' % counter_h_high
        time.sleep(1)
        if clue.button_b:
            break

    clock_.remove(sek_d)
    clock_.remove(min_jed)
    clock_.remove(min_d)
    clock_.remove(hour_jed)
    clock_.remove(hour_d)
    clock_.remove(sek_jed)

    time_off_clock = time.monotonic()
    return (time_on_clock, time_off_clock)



opt1 = Label(med_font, text = 'Clock', color = clue.BLACK)
opt1.x = 20
opt1.y = 45
menu_.append(opt1)

opt2 = Label(med_font, text = "Music player", color = clue.BLACK)
opt2.x = 20
opt2.y = 70
menu_.append(opt2)

arrow = Label(med_font, text = ':', color = clue.RED)
arrow.x = 8
arrow.y = 44
menu_.append(arrow)


time_off = 0
time_on = 0
time_add = 0

hour_high = 0
hour_low = 0
min_high = 0
min_low = 0

zegarek = 0

hour_set_high = 2
hour_set = 3
min_set_high = 5
min_set = 9
sec_set_high = 3
sec_set = 0
counter_add = 0

def positions(time_add):
    """Zwraca 6 pozycji czasowych,
    sec_low, sec_high, min_low, min_high, hour_low, hour_high,
    przyjmuje ilosc sekund"""
    hour = time_add // 3600                     #godziny w roznicy odpalen zegarka
    time_add = time_add % 3600                  #wyłuskanie minut i sekund z wyniku

    min_ = time_add // 60                        #uzyskanie minut (liczby calkowitej)
    time_add = time_add % 60                    #wyłuskanie sekund
    sec = time_add // 1                         #sekundy calkowite

    min_low = min_ % 10                      #wyłuskanie liczby jednosci minut
    min_high = min_ // 10                    #liczba dziesiatek minut

    hour_low = hour % 10                    #liczba jednosci godzin
    hour_high = hour // 10                  #liczba dziesiatek godzin

    sec_low = sec % 10                      #liczba jednosci sekund
    sec_high = sec // 10

    return(sec_low, sec_high, min_low, min_high, hour_low, hour_high)

while True:


    if clue.button_a:
        zegarek = 1

    if(zegarek == 1):
        clue_display.show(menu_)
        time_on = time.monotonic()
        if(time_off == 0):
            pass
        else:
            time_add = time_on - time_off

        add_sec_low, add_sec_high, add_min_low, add_min_high, add_hour_low, add_hour_high = positions(time_add)

        #czas ktory minal z czasem ustawionym
        if (counter_add == 0):
            hour_high= hour_set_high + add_hour_high
            hour_low= hour_set + add_hour_low
            min_high= min_set_high + add_min_high
            min_low= min_set + add_min_low
            sec_high=sec_set_high + add_sec_high
            sec_low= sec_set + add_sec_low
            counter_add = 1

        else:
            sec_low_clk, sec_high_clk, min_low_clk, min_high_clk, hour_low_clk, hour_high_clk = positions(time_when_clock_on)
            hour_high= hour_set_high + add_hour_high + hour_high_clk
            hour_low= hour_set + add_hour_low + hour_low_clk
            min_high= min_set_high + add_min_high + min_high_clk
            min_low= min_set + add_min_low + min_low_clk
            sec_high= sec_set_high + add_sec_high + sec_high_clk
            sec_low= sec_set + add_sec_low + sec_low_clk

        if (sec_low >= 10.0):
            sec_high += sec_low // 10
            sec_low = sec_low % 10

        if (sec_high >= 6.0):
            min_low += sec_high // 6
            sec_high = sec_high % 6

        if (min_low >= 10.0):
            min_high += min_low // 10
            min_low = min_low % 10

        if (min_high >= 6.0):
            hour_low += min_high // 6
            min_high = min_high % 6

        if (hour_low >= 10.0):
            hour_high += hour_low // 10
            hour_low = hour_low % 10

        if(hour_high > 2.0 or (hour_high == 2.0 and hour_low >= 4.0)):
            hour=0

            for n in range(0,hour_high*10.0,1):
                hour+=1
            for n in range(0,hour_low,1):
                hour+=1

            hour = hour % 24
            hour_low = hour % 10
            hour_high = hour // 10

        hour_set_high = hour_high
        hour_set = hour_low
        min_set_high = min_high
        min_set = min_low
        sec_set_high = sec_high
        sec_set = sec_low

        time_when_clkon, time_when_clkoff = clock_p(hour_high, hour_low, min_high, min_low, sec_high, sec_low)
        time_when_clock_on = time_when_clkoff - time_when_clkon

        if (clue.button_b):
            time_off = time.monotonic()
            zegarek = 0

    time.sleep(1)

    # clue_display.show(menu_)
    # if clue.button_b:
    #     if (arrow.y >= 219):
    #         pass
    #     else:
    #         arrow.y += 25
    #     time.sleep(0.2)
    # if clue.button_a:
    #     if (arrow.y <= 44):
    #         pass
    #     else:
    #         arrow.y -= 25
    #     time.sleep(0.2)
