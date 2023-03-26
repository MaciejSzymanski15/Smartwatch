import board
import digitalio
import displayio
import time
from adafruit_display_shapes.circle import Circle
from adafruit_clue import clue


def menu():
    clue_data = clue.simple_text_display(title="MENU", title_scale=2)
    clue_data[0].text = "1.Sensors"
    clue_data[1].text = "2.Contorlling RGB with motion"
    clue_data[2].text = "3.Auto brightness"
    clue_data[3].text = "4.Soon"
    clue_data.show()
    #stime.sleep(5)
    #group = displayio.Group()
    #circle = Circle(200,200, 10,fill=0x00FF00, outline=0xFF00FF)
    #display = board.DISPLAY
    #group.append(circle)
    #display.show(group)

def sensors():
    done = 0
    while done == 0:
        clue_data = clue.simple_text_display(title="CLUE Sensor Data!", title_scale=2)
        clue_data[0].text = "Acceleration: {:.2f} {:.2f} {:.2f}".format(*clue.acceleration)
        clue_data[1].text = "Gyro: {:.2f} {:.2f} {:.2f}".format(*clue.gyro)
        clue_data[2].text = "Magnetic: {:.3f} {:.3f} {:.3f}".format(*clue.magnetic)
        clue_data[3].text = "Pressure : {:.3f} hPa".format(clue.pressure)
        clue_data[4].text = "Altidue : {:.3f} m".format(clue.altitude)
        clue_data[5].text = "Temperature : {:.1f} C".format(clue.temperature)
        clue_data[6].text = "Humidity : {:.3f} %".format(clue.humidity)
        clue_data[7].text = "Move down your hand to exit to the menu"
        clue_data.show()
        if clue.gesture == 2:
            done = 1

def RGB_contorll():
    done = 0
    while done == 0:

        clue_data = clue.simple_text_display(title="CONTROL RGB WITH MOTION!", title_scale=1)
        clue_data.show()

        norm_x, norm_y, norm_z = clue.acceleration


        clue.pixel.fill((int(norm_x),int(norm_y),int(norm_z)))

        if clue.gesture == 2:
            clue.pixel.fill((0,0,0))
            done = 1


def auto_bright():
    done = 0
    while done ==0:

        light = clue.proximity
        clue_display = board.DISPLAY

        light_ = (light/6.0)

        #clue_data = clue.simple_text_display(title="TESTING LIGHT SENSOR", title_scale=1)
        #clue_data[0].text = "{}".format(clue.proximity)
        #clue_data.show()


        if light >= 6:

            clue_display.brightness = 0
        else:
            clue_display.brightness = 1

        if clue.button_a:
            clue.pixel.fill((0,0,0))
            done = 1


while True:
    menu()

    gest = clue.gesture

    if gest == 1:
        sensors()

    if gest == 2:
        RGB_contorll()

    if clue.button_a:
        auto_bright()

    if clue.touch_0 == 1:
        break

    else:
        continue
