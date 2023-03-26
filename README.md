# DesignLaboratoryEiT
Projekt wykonali: Dominik Budzyński i Maciej Szymański.
16.10.2022
W pierwszym tygodniu pracy nad projektem, zapoznaliśmy się z środowiskiem programistycznym oraz nowym dla nas CircuitPythonem.
Posiłkowaliśmy się poniższym filmem w serwisie YouTube
https://www.youtube.com/watch?v=opes_7Uf49U
Korzystaliśmy również z artykułu na stronie AdaFruit, w którym mogliśmy zapoznać się z aspektami fizycznymi oraz programistycznymi platformy Clue.
https://learn.adafruit.com/adafruit-clue/circuitpython

24.10.2022
W drugim tygodniu pracy nad projektem, znaleźliśmy przykładowe kody programowania smartwatcha. W środowisku CircuitPython zaprogramowaliśmy nasze urządzenie i próbowaliśmy przeanalizować znalezione kody programów.
Przykładowe programy jakie testowaliśmy:
Kompas: https://github.com/davedice/Adafruit-CLUE-Compass
Termometr: https://learn.adafruit.com/adafruit-clue/clue-temperature-and-humidity-monitor
CLUE Spirit Level: https://learn.adafruit.com/adafruit-clue/clue-spirit-level
CLUE Height Calculator: https://learn.adafruit.com/adafruit-clue/clue-height-calculator

30.10.2022 (tydzień 3)
Pomocna okazała się być strona circuitpython.org, gdzie pod adresem https://docs.circuitpython.org/projects/clue/en/latest/api.html znaleźliśmy przykłady obsługi czujników, przycisków, touchpadów itd. Podczas pracy z biblioteką clue zauważyliśmy, że rezerwuje ona niektóre porty na własny użytek i korzystając z niej, nie można korzystać np. z biblioteki digitalio. Napisaiśmy kilka prostych programów w których możliwe jest sterowanie diodą LED oraz RGB za pomocą przycisków, touchpadów czy za pomocą gestów.

06.11.2022 (tydzień 4)
Naszym celem było zaczęcie przygody z modułem Bluetooth. Bazowaliśmy na przykładowych kodach znajdujących się w pliku z pobranymi potrzebnymi bibliotekami, o stronę https://docs.circuitpython.org/projects/ble/en/latest/api.html#, https://learn.adafruit.com/now-playing-bluetooth-apple-media-service-display/code-the-apple-media-service-display oraz https://learn.adafruit.com/introduction-to-bluetooth-low-energy/introduction.
Na podstawie tych źródeł napisaliśmy prosty program, dzięki któremu płytka Clue steruje odtwarzaczem muzyki na urządzeniu połączonym przez bluetooth. Urządzenie musi mieć system operacyjny iOS. Oczywiście nie obyło się bez problemów, które opatrzyliśmy komentarzami w kodzie. Napisliśmy również inny prosty program, który wyświetla podstawowe informacje zbierane z czujników, pozwala na kontorlowanie koloru diody RGB za pomocą ruchu oraz realizuje funkcje wygaszania ekranu.

14.11.2022 (tydzień 5)
Z powodu braku wiekszej ilości wolnego czasu, zajęliśmy się analizą i zrozumieniem (przez testowanie na własnej płytce, krok po kroku z tutorialem) jednego z projektów udostępnionych na GitHub: https://github.com/andreamah/Adafruit-CLUE-Snake-Game. Na zrozumienie kodu poświęciliśmy dłuższą chwilę, ponieważ nie wszystko co jest tam zastosowane, było nam znane.

21.11.2022(tydzień 6) W tym tygodniu skupiliśmy się głównie na poszukiwaniu możliwości graficznego interfejsu. Znaleźliśmy wiele pomocnych programów i poradników z różnych środowisk, żeby poznać całkowite możliwości płytki CLUE. Następnie staraliśmy się samodzielnie zaprogramować płytkę do wyświetlania MENU użytkownika.
Przykłady poradników oraz repozytoriów z jakich skorzystaliśmy:
- https://www.youtube.com/watch?v=ZTE-hqM6GPo&ab_channel=JamesTobin
- https://github.com/jisforjt/CircuitPython_CLUE_Menu
- http://webcache.googleusercontent.com/search?q=cache:fFBZoZMu2_oJ:www.ulisp.com/show%3F2NWA+&cd=1&hl=en&ct=clnk&gl=us

28.11.2022 (tydzień 7) Napisaliśmy prosty program do wyświetlania godziny oraz MENU, który będziemy rozwijać w przyszłości. Jedynym problemem było dopasowanie MENU, aby było przejrzyste dla użytkownika, aspekt ten musimy nadal rozwijać ponieważ nie jesteśmy zadowoleni z efektu.

5.12.2022 (tydzień 8) Napisaliśmy program, który realizuje logikę zegarka z możliwościa ustalania godziny na własną i "zliczania" czasu, przez który użytkownik nie korzystał z ekranu zegarka. Wyświetla cyfry na tle zwenętrznej grafiki, którą można wgrać według preferencji. Kod jest narazie w formie roboczej i jest napisany tak aby działał, postaramy się zmienić go tak, aby był elegancki na tyle ile potrafimy. Przy realizacji tego zadania przydatne był strony: https://learn.adafruit.com/clue-step-counter-st-lsm6ds33, https://learn.adafruit.com/arduino-to-circuitpython/modules-and-importing, https://docs.circuitpython.org/en/latest/shared-bindings/time/index.html#. Program dodany jest do repozytorium.

12.12.2022 oraz 2.01.2023 (tydzień 9 i tydzień 10) Brak czasu na rozwój projektu

9.01.2023 (tydzień 11) Optymalizacja i gruntowna zmiana mechanizmu odpowiadającego za zegarek. Dodano klasę Clock które obsługuję wszystko to co długi i niekształtny kod z pliku clock.py. Program działa przez to sprawniej.

16.01.2023 (tydzień 12) Dodano automatyczne wygaszanie ekranu po 30 sekundach bez wykrycia czynności. Dodano mechanizm możliwości ustawienia budzika na konkretną godzinę oraz ustawienia początkowej godziny przy włączeniu urządzenia. Mimo że, nie jesteśmy zadowoleni w 100% z efektów pracy to możemy uznać, że projekt został zakończony.

Aspekty które wymagają poprawy:
-wskazywanie zmienianej pozycji godzin i minut
-zoptymalizowanie pracy na grupach wyświetlających grafikę
-działanie budzika przy włączonym ekranie odtwarzacza muzyki

Szybka instrukcja obsługi:

Pierw, należy połączyć się z płytką przez Bluetooth.
Niestety wspierane tylko urządzenia z systemem iOS.

Ekran ustawiania godziny:
przycisk B - zmiana wartości na danej pozycji
przycisk A - zmiana pozycji
gest w górę - zatwierdzenie (warto spróbować kilka razy)
cyfra po prawej
Ekran główny (ekran zegarka)
przycisk B - ustawienie budzika (jak w ustawianiu godziny)
gest w lewo/prawo - przejście do innego ekranu

Ekran odtwarzacza muzyki
przycisk A - stop/start odtwaraznia
przycisk B - kolejny utwór

Budzik
przycisk A - wyłączenie budzika

