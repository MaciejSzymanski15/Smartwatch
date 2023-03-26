import time
import adafruit_ble
from digitalio import DigitalInOut, Direction, Pull
from adafruit_ble.advertising.standard import SolicitServicesAdvertisement
from adafruit_ble_apple_media import AppleMediaService
from adafruit_clue import clue

radio = adafruit_ble.BLERadio()                     #"dostarcza" interfejs BLE w celu wyszukiwania urzadzen lub olgaszania
a = SolicitServicesAdvertisement()                  #funkcja do wybierania jakiego typu usluge urzadzenie chce wykorzystywac podczas polaczenia
a.solicited_services.append(AppleMediaService)      #wybranie uslugi AppleMediaService
radio.start_advertising(a)                          #rozpoczyna oglaszanie urzadzenia (clue)
    
while not radio.connected:                          #petla wykonuje sie dopoki clue nie polaczy sie z urzadzeniem
    print("Waiting for connection")
    time.sleep(3)
    continue
    
print("connected")


i = 0

while radio.connected:
    for connection in radio.connections:
        if not connection.paired:                   
            connection.pair()
            print("paired")
            
        ams = connection[AppleMediaService]
        
        #przy wyswietlaniu tekstu program bardzo czesto ma problemy z alokacją pamieci
        #potrzebne bedzie znalezienie bledu lub innej metody wyswietlania danych na ekran
        clue_data = clue.simple_text_display(title="Bluetooth music device", title_scale=1)
        clue_data[0].text = "App: {}".format(ams.player_name)
        clue_data[1].text = "Title: {}".format(ams.title)
        clue_data[2].text = "Album: {}".format(ams.album)
        clue_data[3].text = "Artist: {}".format(ams.artist)
        clue_data[4].text = "Move your hand up to play/pause song"         
        clue_data[5].text = "Move right your hand to play next song"
        clue_data[6].text = "Move left your hand to play previous song"
        clue_data.show()
        
        gest = clue.gesture
        
        if gest == 1:
            clue.pixel.fill((50,0,0))
            ams.toggle_play_pause()
            time.sleep(0.5)
            clue.pixel.fill((0,0,0))
            gest = 0
            
        if gest == 3:
            clue.pixel.fill((0,50,0))
            ams.previous_track()
            time.sleep(0.5)
            clue.pixel.fill((0,0,0))
            gest = 0
            
        if gest == 4:
            clue.pixel.fill((0,0,50))
            ams.next_track()
            time.sleep(0.5)
            clue.pixel.fill((0,0,0))
            gest = 0
