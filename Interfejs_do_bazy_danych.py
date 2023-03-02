#-*- coding: UTF-8 -*-
import os
from struct import pack
import mariadb
from datetime import date

today = date.today()
conn = mariadb.connect(user='root', password='', host='25.53.212.196', database='zoo')

def clear(): os.system('clear')

def main():
    ## PESEL Rafa³ Janow: 55090646443 HASLO: asd - przelozony
     if login():
         if supervisor_id == 'None':
             menu_supervisor()
         else:
             menu_worker()

def beautiful(what, how):
    if len(what) % 2 == 0:
        buffor = (how - len(what)) / 2
    else:
        buffor = (how - len(what) - 1) / 2
    buffor = int(buffor)

    new_string = ""
    for i in range(buffor):
        new_string = new_string + " "
    new_string = new_string + what

    new_buffor = how - len(what) - buffor
    new_buffor = int(new_buffor)
    for i in range(new_buffor):
        new_string = new_string + " "

    return str(new_string)

#       FUNKCJE LOGOWANIA        #

def login():
    cursor = conn.cursor()
    global user_pesel
    global user_id
    global supervisor_id
    #user_pesel = input("PODAJ LOGIN (PESEL): ")
    #psswrd = input("PODAJ HASLO: ")
    #(pracownik)
    # user_pesel = '80060216513'
    # psswrd = 'sadwefef'
    #(przelozony)
    user_pesel = '55090646443'
    psswrd = 'abcd'
    cursor.execute("CALL Pass_password('" + user_pesel + "')")
    results = cursor.fetchall()
    user_id = str(results[0][0])
    check = str(results[0][1])
    supervisor_id = str(results[0][2])
    if psswrd == check:
        return True
    else:
        return False

def change_password():
    print("Potwierdz swoja tozsamosc, PODAJ LOGIN I HASLO: ")
    if login():
        new_password = input("Podaj nowe haslo: ")
        modify_data('pracownicy', 'haslo', new_password, 'PESEL', str(user_pesel))

#       FUNKCJE POMOCNICZE       #

def pick():
    choice = str(input(" Wprowadz swoj wybor: "))
    return choice

def modify_data(tabela, kolumna, new_data, main_key, main_key_value):
    cursor = conn.cursor()
    cursor.execute(
        "CALL Mod_data('" + tabela + "','" + kolumna + "','" + new_data + "','" + main_key + "','" + main_key_value + "');")
    conn.commit()

def sub_menu_modify_request():
    print("Wybierz dana do modyfikacji: ")
    print("1. Pesel")
    print("2. Imie")
    print("3. Nazwisko")
    print("4. Strefa")
    print("5. Nazwa grupy")
    column = pick()
    return column

def get_workers(nazwa_grupy):
    cursor = conn.cursor()
    cursor.execute("CALL Display_workers_in_gr('" + nazwa_grupy + "');")
    restults = cursor.fetchall()
    return restults

def modify_status():
    results = show_requests()
    choice = input("Wybierz zlecenie dla ktorego chcesz dokonac modyfikacji statusu")
    show = beautiful("ID ZLECENIA", 14) + beautiful("ZLECAJACY(ID)", 20) + beautiful("GRUPA", 20) + beautiful(
        "ID ZWIERZAKA", 14) + beautiful("OBECNY HABITAT", 20) + beautiful("NOWY HABITAT", 20) + beautiful(
        "DATA ZLECENIA", 20) + beautiful("DATA WYKONANIA", 20) + beautiful("STATUS ZLECENIA", 20)
    print(show)
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        if choice == str(row[0]):
            print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                                  20) + "|" + beautiful(
                str(row[3]), 20) + "|" + beautiful(str(row[4]), 20) + "|" + beautiful(str(row[5]), 20) + "|" + beautiful(
                str(row[6]), 20) + "|" + beautiful(str(row[7]), 20) + "|" + beautiful(str(row[8]), 20))
            if supervisor_id == 'None':
                if (row[8] == 'Nie_przyjete'):
                    print("Wybierz nowy status zlecenia")
                    print("1. Zakonczone ")
                    print("2. Nie_wykonane")
                    choice = pick()
                    match int(choice):
                        case 1:
                            modify_data('zlecenia', 'Status','Zakonczone', 'ID_Zlecenia', str(row[0]))
                            modify_request()
                        case 2:
                            modify_data('zlecenia', 'Status', 'Nie_wykonane', 'ID_Zlecenia', str(row[0]))
                            modify_request()
                elif (row[8] == 'Wykonane'):
                    print("Wybierz nowy status zlecenia")
                    print("1. Zakonczone ")
                    print("2. Nie_wykonane")
                    choice = pick()
                    match int(choice):
                        case 1:
                            modify_data('zlecenia', 'Status', 'Zakonczone', 'ID_Zlecenia', str(row[0]))
                            modify_request()
                        case 2:
                            modify_data('zlecenia', 'Status', 'Nie_wykonane', 'ID_Zlecenia', str(row[0]))
                            modify_request()
            else:
                if(row[8] == 'Zlecone'):
                    print("Wybierz nowy status zlecenia")
                    print("1. Przyjete")
                    print("2. Nie przyjete")
                    choice = pick()
                    match int(choice):
                        case 1:
                            modify_data('zlecenia', 'Status', 'W_trakcie', 'ID_Zlecenia', str(row[0]))
                            menu_worker()
                        case 2:
                            modify_data('zlecenia', 'Status', 'Nie_przyjete', 'ID_Zlecenia', str(row[0]))
                            menu_worker()

                if(row[8] == 'W_trakcie'):
                    print("Wybierz nowy status zlecenia")
                    print("1. Wykonane")
                    print("2. Niewykonane")
                    choice = pick()
                    match int(choice):
                        case 1:
                            modify_data('zlecenia', 'Status', 'Wykonane', 'ID_Zlecenia', str(row[0]))
                            menu_worker()
                        case 2:
                            modify_data('zlecenia', 'Status', 'Nie_wykonane', 'ID_Zlecenia', str(row[0]))
                            menu_worker()

#        WYSWIETLANIE DANYCH          #

def show_zones():
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('strefy');")
    results = cursor.fetchall()
    zones = beautiful("ID STREFY", 14) + "|" + beautiful("NAZWA STREFY", 20)
    print(zones)
    print(
        "---------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20))
    return results

def show_workers():
    cursor = conn.cursor()
    cursor.execute("CALL Display_employee('" + user_pesel + "');")
    results = cursor.fetchall()
    worker = beautiful("PESEL", 14) + "|" + beautiful("IMIE", 20) + "|" + beautiful("NAZWISKO", 20) + "|" + beautiful("STREFA", 20) + "|" + beautiful("GRUPA", 20)
    print(worker)
    print("---------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),20) + "|" + beautiful(str(row[3]), 20) + "|" + beautiful(str(row[4]), 20))

    return results

def show_stays():
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('latest_values');")
    results = cursor.fetchall()
    show = beautiful("ID ZWIERZAKA", 14) + "|" + beautiful("GATUNEK", 40) + "|" + beautiful("LOKUM",
                                                                                            10) + "|" + beautiful(
        "DATA I GODZ POCZATKU POBYTU", 30) + "|" + beautiful("DATA I GODZ KONCA POBYTU", 30)
    print(show)
    print(
        "-------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 40) + "|" + beautiful(str(row[2]),
                                                                                              10) + "|" + beautiful(
            str(row[3]), 30) + "|" + beautiful(str(row[4]), 30))
    return results

def show_groups():
    cursor = conn.cursor()
    cursor.execute("CALL Display_group_by_ID('"+ user_id +"');")
    results = cursor.fetchall()
    show = beautiful("Nazwa_grupy", 14) + "|" + beautiful("ID_zlecajacego", 20)
    print(show)
    print(
        "------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20))
    cursor.close()
    print("Czy chcesz zobaczyc czlonkow grupy ?")
    print("1. TAK")
    print("2. NIE")
    choice = pick()
    match int(choice):
        case 1:
            choice = str(input("Wprowadz nazwe grupy do wyswietlenia liczby czlonkow: "))
            grupa = get_workers(choice)
            worker = beautiful("NAZWA GRUPY", 14) + "|" + beautiful("IMIE", 20) + beautiful("NAZWISKO",
                                                                                           20) + "|" + beautiful(
                "STREFA", 20)
            print(worker)
            print(
                "---------------------------------------------------------------------------------------------------------------------")
            for row in grupa:
                print(
                    beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20) + beautiful(str(row[2]),
                                                                                                    20) + "|" + beautiful(
                        str(row[3]), 20))
        case 2:
            return results

    return results

def show_animals():
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('zwierzeta');")
    results = cursor.fetchall()
    show = beautiful("ID ZWIERZAKA", 14) + "|" + beautiful("GATUNEK", 30) + "|" + beautiful("IMIE", 20) + beautiful("DATA URODZENIA", 24) + beautiful("PLEC", 6) + beautiful("GROMADA", 20)
    print(show)
    print("---------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 30) + "|" + beautiful(str(row[2]),
                                                                                              20) + "|" + beautiful(
            str(row[3]), 24) + "|" + beautiful(str(row[4]), 6) + "|" + beautiful(str(row[5]), 20))
    return results

def show_requests():
    cursor = conn.cursor()
    if supervisor_id == 'None':
        cursor.execute("CALL Display_jobs_supervisor('" + user_id + "');")
    else:
        cursor.execute(" Display_jobs_employee('"+ user_id +"')")
    results = cursor.fetchall()
    show = beautiful("ID ZLECENIA", 14) + beautiful("ZLECAJACY(ID)", 20) + beautiful("GRUPA", 20) + beautiful(
        "ID ZWIERZAKA", 14) + beautiful("OBECNY HABITAT", 20) + beautiful("NOWY HABITAT", 20) + beautiful(
        "DATA ZLECENIA", 20) + beautiful("DATA WYKONANIA", 20) + beautiful("STATUS ZLECENIA", 20)
    print(show)
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]),20) + "|" + beautiful(str(row[1]),20) + "|" + beautiful(str(row[2]),20) + "|" + beautiful(str(row[3]),20) + "|" + beautiful(str(row[4]),20) + "|" + beautiful(str(row[5]), 20) + "|" + beautiful(str(row[6]), 20) + "|" + beautiful(str(row[7]), 20) + "|" + beautiful(str(row[8]), 20))
    return results

def show_habitats():
    print("-------------------------------")
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('habitaty_new');")
    results = cursor.fetchall()
    show = beautiful("ID HABITATU", 14) + beautiful("NAZWA STREFY", 20) + beautiful("NAZWA BUDYNKU", 20) + beautiful(
        "NR PIETRA", 14) + beautiful("NAZWA POMIESZCZENIA", 20) + beautiful("NR POMIESZCZENIA", 20) + beautiful("DOSTEPNE MIEJSCE", 20)+ beautiful("NR HABITATU", 20)
    print(show)
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                              20) + "|" + beautiful(
            str(row[3]), 20) + "|" + beautiful(str(row[4]),30) + "|" + beautiful(str(row[5]),40) + "|" + beautiful(str(row[6]),40) + "|" + beautiful(str(row[7]),30))
    return results

def show_floors():
    print("-------------------------------")
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('pietra');")
    results = cursor.fetchall()
    show = beautiful("ID PIETRA", 14) + beautiful("NR PIETRA", 20) + beautiful("NAZWA BUDYNKU", 20) + beautiful(
        "ILOSC POMIESZCZEN", 14)
    print(show)
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                              20) + "|" + beautiful(
            str(row[3]), 20))
    return results

def show_rooms():
    print("-------------------------------")
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('pomieszczenia');")
    results = cursor.fetchall()
    show = beautiful("ID POMIESZCZENIA", 14) + beautiful("NAZWA POMIESZCZENIA", 20) + beautiful("NUMER POMIESZCZENIA", 20) +beautiful("ID PIETRA", 20)
    print(show)
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                              20) + "|" + beautiful(
            str(row[3]), 20))
    return results

def show_buildings():
    cursor = conn.cursor()
    cursor.execute("CALL Display_data('budynki');")
    results = cursor.fetchall()
    show = beautiful("ID BUDYNKU", 14) + beautiful("NAZWA BUDYNKU", 20) + beautiful("NAZWA STREFY", 20)
    print(show)
    print(
        "----------------------------------------------------------------------------------------------------------------------------------------")
    for row in results:
        print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                              20))
    return results

#       MODYFIKOWANIE DANYCH        #

def modify_animal():
    print("-------------------------------")
    print("Modyfikacja danych zwierzat: ")
    results = show_animals()
    zwierze = input("Podaj ID zwierzaka: ")
    for row in results:
        if zwierze == str(row[0]):
            show = beautiful("ID ZWIERZAKA", 14) + "|" + beautiful("GATUNEK", 20) + "|" + beautiful("IMIE",
                                                                                                    20) + beautiful(
                "DATA URODZENIA", 24) + beautiful("PLEC", 6) + beautiful("GROMADA", 20)
            print(show)
            print(
                "---------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                                  20) + "|" + beautiful(
                str(row[3]), 24) + "|" + beautiful(str(row[4]), 6) + "|" + beautiful(str(row[5]), 20))
            gatunek = str(row[1])
            imie = str(row[2])
            b_day = str(row[3])
            plec = str(row[4])
            gromada = str(row[5])
    print("Wybierz dana do modyfikacji: ")
    print("1. Gatunek")
    print("2. Imie")
    print("3. Data urodzenia")
    print("4. Plec")
    print("5. Gromada")
    column = pick()
    match int(column):
        case 1:
            new_value = input("Obecny gatunek Zwierzaka: " + gatunek + "   Podaj nowe ID Zwierzaka: ")
            modify_data('zwierzeta', 'gatunek', new_value, ' ID ', str(zwierze))
        case 2:
            new_value = input("Obecne imie Zwierzaka: " + imie + "   Podaj nowe imie Zwierzaka: ")
            modify_data('zwierzeta', 'imie', new_value, ' ID ', str(zwierze))
        case 3:
            new_value = input(
                "Obecna data urodzenia Zwierzaka: " + b_day + "   Podaj nowa date urodzenia Zwierzaka (format rrrr-mm-dd): ")
            modify_data('zwierzeta', 'data_urodzenia', new_value, ' ID ', str(zwierze))
        case 4:
            new_value = input("Obecna plec Zwierzaka: " + plec + "   Podaj nowa plec Zwierzaka: ")
            modify_data('zwierzeta', 'plec', new_value, ' ID ', str(zwierze))
        case 5:
            new_value = input("Obecna gromada Zwierzaka: " + gromada + "   Podaj nowa gromade Zwierzaka: ")
            modify_data('zwierzeta', 'gromada', new_value, ' ID ', str(zwierze))
    sub_menu_animals()

def modify_request():
    print("-------------------------------")
    print("Modyfikacja danych zlecen: ")
    show_requests()
    print("Czy chcesz zmodyfikowac dane statusu ?")
    print("1. TAK")
    print("2. NIE")
    choice = pick()
    match int(choice):
        case 1:
            modify_status()
            modify_request()
        case 2:
            results = show_requests()
    zlecenie = str(input("Wybierz zlecenie do modyfikacji: "))
    for row in results:
        if zlecenie == str(row[0]):
            print("----------------------------------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),20) + "|" + beautiful(str(row[3]), 20) + "|" + beautiful(str(row[4]), 20) + "|" + beautiful(str(row[5]), 20)  + "|" + beautiful(str(row[6]), 20)  + "|" + beautiful(str(row[7]), 20)  + "|" + beautiful(str(row[8]), 20))
            zlecenie=str(row[0])
            grupa=str(row[2])
            zwierze=str(row[3])
            habitat_old=str(row[4])
            habitat_new=str(row[5])
            date_start=str(row[6])
            date_end=str(row[7])
            status=str(row[8])
    print("Wybierz dana do modyfikacji: ")
    print("1. Grupa: ")
    print("2. Zwierze: ")
    print("3. Stary Habitat")
    print("4. Nowy Habitat")
    print("5. Data rozpoczecia zlecenia")
    print("6. Data zakonczenia zlecenia")
    print("7. WYJDZ")
    column = pick()
    match int(column):
        case 1:
            print("Chcesz wybrac czy stworzyc nowa grupe ?: ")
            print("1. NIE (wyswietlona zostanie lista grup do wyboru")
            print("2. TAK (rozpocznie sie tworzenie nowej grupy)")
            choice = pick()
            match int(choice):
                case 1:
                    print("Wybierz grupe: ")
                    show_groups()
                    new_value = input("Obecna grupa: " + grupa + "   Podaj nazwe nowej grupy do zlecenia: ")
                    modify_data('zlecenia', 'Grupa_przyjmujaca', new_value, ' ID_Zlecenia ', str(zlecenie))
                case 2:
                    new_group()
                    print("Wybierz grupe: ")
                    show_groups()
                    new_value = input("Obecna grupa: " + grupa + "   Podaj nazwe nowej grupy do zlecenia: ")
                    modify_data('zlecenia', 'Grupa_przyjmujaca', new_value, ' ID_Zlecenia ', str(zlecenie))
        case 2:
            print("Wybierz zwierze")
            show_animals()
            new_value = input("Obecne zwierze: "+ zwierze +"Podaj numer id zwierzecia ktore chcesz dodac: ")
            modify_data('zlecenia','ID_Zwierzecia',new_value,'ID_Zlecenia',str(zlecenie) )
        case 3:
            print("Wybierz jaki ma byc nowy obecny habitat")
            show_habitats()
            new_value = input("Obecny \"obecny\" habitat: " + habitat_old + ". Podaj numer id habitatu ktore chcesz dodac jako nowy \"obecny\" habitat: ")
            modify_data('zlecenia','Stary_Habitat',new_value,'ID_Zlecenia', str(zlecenie))
        case 4:
            print("Wybierz jaki ma byc nowy \"NOWY\" habitat")
            show_habitats()
            new_value = input(
                "Obecny \"nowy\" habitat: " + habitat_new + ". Podaj numer id habitatu ktore chcesz dodac jako nowy \"nowy\" habitat: ")
            modify_data('zlecenia', 'Nowy_Habitat', new_value, 'ID_Zlecenia', str(zlecenie))
        case 5:
            print("Wprowadz nowa date zlecenia")
            new_value = input("Podaj date (format: rrrr-mm-dd: ")
            modify_data('zlecenia', 'Data_zlecenia', new_value, 'ID_Zlecenia', str(zlecenie))
        case 6:
            print("Wprowadz nowa date planowanego wykonania zlecenia")
            new_value = input("Podaj date (format: rrrr-mm-dd: ")
            modify_data('zlecenia', 'Data_plan_wyk', new_value, 'ID_Zlecenia', str(zlecenie))
        case 7:
            sub_menu_requests()
    sub_menu_requests()

def modify_worker():
    print("-------------------------------")
    cursor = conn.cursor()
    print("Modyfikacja danych pracownika: ")
    show_workers()
    pracownik = str(input("Podaj PESEL pracownika ktorego dane chcesz zmodyfikowac: "))
    # pracownik = '50090819125'
    results = show_workers()
    for row in results:
        if pracownik == str(row[0]):
            show = beautiful("PESEL", 14) + "|" + beautiful("IMIE", 20) + "|" + beautiful("NAZWISKO",
                                                                                          20) + "|" + beautiful(
                "STREFA", 20) + "|" + beautiful("GRUPA", 20)
            print(show)
            print(
                "---------------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),
                                                                                                  20) + "|" + beautiful(
                str(row[3]), 20) + "|" + beautiful(str(row[4]), 20))
            pesel = row[0]
            imie = row[1]
            nazwisko = row[2]
            strefa = row[3]
            grupa = row[4]
    column = sub_menu_modify_request()
    match int(column):
        case 1:
            new_value = input("Obecny PESEL: " + pesel + "    Podaj nowy PESEL: ")
            modify_data('pracownicy', 'PESEL', new_value, ' PESEL ', str(pracownik))
        case 2:
            new_value = input("Obecne imie: " + imie + "     Podaj nowe imie: ")
            print(new_value)
            modify_data('pracownicy', 'imie', new_value, ' PESEL ', str(pracownik))
        case 3:
            new_value = input("Obecne nazwisko: " + nazwisko + "     Podaj nowe nazwisko: ")
            modify_data('pracownicy', 'nazwisko', new_value, ' PESEL ', str(pracownik))
        case 4:
            show_zones()
            new_value = input("Obecna strefa: " + strefa + "    Podaj nowa strefe: ")
            modify_data('pracownicy', 'strefa', new_value, ' PESEL ', str(pracownik))
        case 5:
            show_groups()
            new_value = input("Obecna grupa: " + grupa + "     Podaj nowa grupe: ")
            modify_data('pracownicy', 'Nazwa_grupy', new_value, ' PESEL ', str(pracownik))
    sub_menu_workers()

def modify_stay():
    print("-------------------------------")
    print("Modyfikacja danych pobytu: ")
    results = show_stays()
    pobyt = input("Podaj ID zwierzaka: ")
    for row in results:
        if pobyt == str(row[0]):
            show = beautiful("ID ZWIERZAKA", 14) + "|" + beautiful("GATUNEK", 40) + "|" + beautiful("LOKUM",
                                                                                                    10) + "|" + beautiful(
                "DATA I GODZ POCZATKU POBYTU", 30) + "|" + beautiful("DATA I GODZ KONCA POBYTU", 30)
            print(show)
            print(
                "------------------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 40) + "|" + beautiful(str(row[2]),
                                                                                                  10) + "|" + beautiful(
                str(row[3]), 30) + "|" + beautiful(str(row[4]), 30))
            date_start = str(row[3])
            date_end = str(row[4])
    print("Wybierz dana do modyfikacji: ")
    print("1. Data poczatku pobytu")
    print("2. Data konca pobytu")
    column = pick()
    match int(column):
        case 1:
            new_value = input(
                "Obecna Data i godzina rozpoczecia pobytu: " + date_start + "   Podaj nowa date i godzine rozpoczecia pobytu(format rrrr-mm-dd hh:mm:ss): ")
            modify_data('pobyty', 'data_rozp', new_value, ' zwierze ', str(pobyt))
        case 2:
            new_value = input(
                "Obecna Data i godzina zakonczenia pobytu: " + date_end + "   Podaj nowa date i godzine zakonczenia pobytu(format rrrr-mm-dd hh:mm:ss): ")
            modify_data('pobyty', 'data_zakoncz', new_value, ' zwierze ', str(pobyt))
            sub_menu_stays()

def modify_groups():
    print("-------------------------------")
    print("Modyfikacja danych grupy: ")
    results = show_groups()
    grupa = input("Podaj nazwe grupy: ")
    for row in results:
        if grupa == str(row[0]):
            show = beautiful("NAZWA GRUPY", 14) + "|" + beautiful("ID ZLECAJACEGO", 40)
            print(show)
            print(
                "------------------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]),20))
            grupa = str(row[0])
            przelozony_id = str(row[1])
    new_value = input(
        "Obecna nazwa grupy: " + grupa + "   Podaj nowa nazwe grupy: ")
    modify_data('grupy', 'Nazwa_grupy', new_value, 'Nazwa_grupy', str(grupa))
    sub_menu_groups()



#       DODAWANIE NOWYCH RECORDOW      #

def new_group():
    print("-------------------------------")
    cursor = conn.cursor()
    print("Tworzenie nowej grupy: ")
    print("-------------------------------")
    print("Wypelnij: ")
    nazwa_grupy = input("Podaj nazwe grupy: ")
    zlecajacy = user_id
    cursor.execute("INSERT INTO `grupy` ( `Nazwa_grupy`, `ID_zlecajacego` ) VALUES ( '" + nazwa_grupy + "','" + zlecajacy + "');")
    print("-------------------------------")
    print("Dodaj pracownikow do grupy")
    show_workers()
    print("-------------------------------")
    while 1:
        worker = input("Podaj pesel pracownika do dodania: ")
        modify_data('pracownicy', 'Nazwa_grupy', str(nazwa_grupy), ' PESEL ', worker )
        print("Czy chcesz dodac wiecej pracownikow  ?")
        print("1. TAK")
        print("2. NIE")
        choice = pick()
        match int(choice):
            case 1:
                continue
            case 2:
                break
    conn.commit()
    cursor.close()
    return 0

def new_worker():
    print("-------------------------------")
    cursor = conn.cursor()
    print("Rejestracja nowego pracownika: ")
    print("-------------------------------")
    print("Wypelnij: ")
    imie = input("Podaj imie nowego pracownika:")
    nazwisko = input("Podaj nazwisko nowego pracownika:")
    pesel = str(input("Podaj nr PESEL nowego pracownika:"))
    print("Wybierz numer strefy: ")
    show_zones()
    print("-------------------------------")
    strefa = pick()
    przelozony = user_id
    haslo = str(input("Podaj haslo nowego pracownika:"))
    print("-------------------------------")
    groups_check = show_groups()
    grupa = str(input("Podaj nazwe grupy (moze byc NULL):"))
    flag = True
    while flag:
        for row in groups_check:
            if grupa == str(row[0]) or grupa == 'NULL':
                if grupa == 'NULL':
                   cursor.execute(
                       "INSERT INTO `pracownicy` (`ID`,`PESEL`, `imie`, `nazwisko`, `strefa`, `przelozony`, `haslo`, `Nazwa_grupy`) VALUES ('" + "(SELECT COUNT(ID.pracownicy) FROM pracownicy) + 1" + "','" + pesel + "', '" + imie + "', '" + nazwisko + "', '" + strefa + "','" + przelozony + "', '" + haslo + "'," + grupa + ");")
                else:
                    cursor.execute(
                        "INSERT INTO `pracownicy` (`ID`,`PESEL`, `imie`, `nazwisko`, `strefa`, `przelozony`, `haslo`, `Nazwa_grupy`) VALUES ('" + "(SELECT COUNT(ID.pracownicy) FROM pracownicy) + 1" + "','" + pesel + "', '" + imie + "', '" + nazwisko + "', '" + strefa + "','" + przelozony + "', '" + haslo + "','" + grupa + "');")
                flag = False
            else:
                grupa = str(input("Podaj poprawna nazwe grupy !!!!! (moze byc NULL):"))
            break
    conn.commit()
    cursor.close()
    sub_menu_workers()

def new_stay():
    print("-------------------------------")
    cursor = conn.cursor()
    show_habitats()
    lokum = input("Podaj lokum dla nowego pobytu:")
    show_animals()
    zwierze = input("Podaj ID zwierzaka:")
    today = str(date.today())
    date_end = str(input("Podaj date zakonczenia: "))
    cursor.execute(
        "INSERT INTO `pobyty` (`lokum`, `zwierze`, `data_rozp`, `data_zakoncz`) VALUES ('" + lokum + "', '" + zwierze + "','" + today + "','" + date_end + "');")
    conn.commit()
    conn.close()
    sub_menu_stays()

def new_animal():
    print("-------------------------------")
    cursor = conn.cursor()
    gatunek = input("Podaj gatunek nowego zwierzaka:")
    imie = input("Podaj imie nowego zwierzaka:")
    data = str(input("Podaj date urodzin nowego zwierzaka w formacie RRRR-MM-DD:"))
    plec = input("Podaj plec nowego zwierzaka (F-samica, M-samiec):")
    gromada = (input("Podaj gromade nowego zwierzaka:"))
    cursor.execute(
        "INSERT INTO `zwierzeta` (`ID`, `gatunek`, `imie`, `data_urodzenia`, `plec`, `gromada`) VALUES ('" + "SELECT COUNT id.zwierzeta FROM zwierzeta + 1" + "', '" + gatunek + "', '" + imie + "', '" + data + "', '" + plec + "', '" + gromada + "');")
    conn.commit()
    cursor.close()
    conn.close()
    sub_menu_animals()

def new_request():
    print("-------------------------------")
    cursor = conn.cursor()
    print("Tworzenie nowego zlecenia: ")
    print("Chcesz wybrac czy stworzyc nowa grupe: ")
    print("1. Wybor grupy")
    print("2. Stworzenie nowej grupy")
    choice = pick()
    match int(choice):
        case 1:
            print("-------------------------------")
            print("WYBOR GRUPY: ")
            show_groups()
            print("-------------------------------")
            new_grupa = str(input("Podaj nazwe grupy ktora chcesz dodac do zlecenia: "))
        case 2:
            new_group()
            print("-------------------------------")
            print("WYBOR GRUPY: ")
            show_groups()
            print("-------------------------------")
            new_grupa = str(input("Podaj ID grupy ktora chcesz dodac do zlecenia: "))
    zlecajacy = user_id
    print("Wybierz zwierze: ")
    print("-------------------------------")
    show_animals()
    print("-------------------------------")
    zwierzak = pick()
    show_habitats()
    print("Wybierz habitat (stary): ")
    print("-------------------------------")
    habitat_old = pick()
    print("Wybierz habitat (nowy): ")
    print("-------------------------------")
    habitat_new = pick()
    data_zlecenia = str(date.today())
    data_wykonania = input("Podaj date zakonczenia zlecenia (format: rrrr-mm-dd): ")
    cursor.execute(
        "INSERT INTO `zlecenia` (`ID_Zlecenia`, `zlecajacy`, `grupa_przyjmujaca`, `ID_Zwierzecia`, `Stary_Habitat`, `Nowy_Habitat` , `Data_zlecenia`, `Data_plan_wyk`, `Status`) VALUES ('" + "(SELECT COUNT(id.zwierzeta) FROM zwierzeta) + 1" + "', '" + zlecajacy + "', '" + new_grupa + "', '" + zwierzak + "', '" + habitat_old + "','" + habitat_new + "','" + data_zlecenia + "' ,'" + data_wykonania + "','Zlecone');")
    conn.commit()
    sub_menu_requests()

#       USUWANIE RECORDOW      #

def delete_worker():
    cursor = conn.cursor()
    print("Usuwanie danych pracownika")
    print("-------------------------------")
    results = show_workers()
    pracownik = str(input("Podaj PESEL pracownika ktorego dane chcesz usunac( UWAGA !!! TEJ OPERACJI NIE MOZNA COFNAC): "))
    for row in results:
        if pracownik == str(row[0]):
            print("--------------------------------------------------------------------------------")
            show = beautiful("PESEL", 14) + "|" + beautiful("IMIE", 20) + "|" + beautiful("NAZWISKO",20) + "|" + beautiful("STREFA", 20) + "|" + beautiful("GRUPA", 20)
            print(show)
            pesel = row[0]
            print(" Usuniety pracownik: ")
            print("---------------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]), 20) + "|" + beautiful(str(row[3]), 20) + "|" + beautiful(str(row[4]), 20))
    cursor.execute("CALL Delete_record('pracownicy','PESEL','" + pesel + "');")
    conn.commit()
    menu_supervisor()

def delete_request():
    cursor = conn.cursor()
    print("Usuwanie danych zlecenia")
    print("-------------------------------")
    results = show_requests()
    zlecenie = str(input("Podaj ID zlecenia ktorego dane chcesz usunac: "))
    show = beautiful("ID ZLECENIA", 14) + beautiful("ZLECAJACY(PESEL)", 20) + beautiful("GRUPA",
                                                                                    20) + beautiful(
        "ID ZWIERZAKA", 14) + beautiful("OBECNY HABITAT", 20) + beautiful("NOWY HABITAT", 20) + beautiful(
        "DATA ZLECENIA", 20) + beautiful("DATA WYKONANIA", 20) + beautiful("STATUS ZLECENIA", 20)
    for row in results:
        if zlecenie == str(row[0]):
            print(show)
            print(
                "----------------------------------------------------------------------------------------------------------------------------------------")
            print(beautiful(str(row[0]), 20) + "|" + beautiful(str(row[1]), 20) + "|" + beautiful(str(row[2]),20) + "|" + beautiful(str(row[3]), 20) + "|" + beautiful(str(row[4]), 20) + "|" + beautiful(str(row[5]), 20))
    cursor.execute("CALL Delete_record('zlecenia','ID_Zlecenia','" + zlecenie + "');")
    conn.commit()
    sub_menu_requests()

def delete_group():
    cursor = conn.cursor()
    print("Usuwanie danych zlecenia")
    print("-------------------------------")
    results = show_groups()
    grupa = str(input("Podaj nazwe grupy ktorej dane chcesz usunac: "))
    show = beautiful("Nazwa_grupy", 14) + "|" + beautiful("ID_zlecajacego", 20)
    print(show)
    print(
        "------------------------------------------------------------------------------------------------------------")
    for row in results:
        if row[0] == grupa:
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 20))
    cursor.execute("CALL Delete_record('grupy','Nazwa_grupy','" + grupa + "');")
    conn.commit()
    sub_menu_groups()

def delete_animal():
    cursor = conn.cursor()
    print("Usuwanie danych zwierzaka")
    print("-------------------------------")
    results = show_animals()
    zwierze = str(input("Podaj ID Zwierzaka ktorego dane chcesz usunac: "))
    show = beautiful("ID ZWIERZAKA", 14) + "|" + beautiful("GATUNEK", 30) + "|" + beautiful("IMIE", 20) + beautiful(
        "DATA URODZENIA", 24) + beautiful("PLEC", 6) + beautiful("GROMADA", 20)
    print(show)
    print(
        "---------------------------------------------------------------------------------------------------------------------")

    for row in results:
        if str(row[0]) == zwierze:
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 30) + "|" + beautiful(str(row[2]),
                                                                                              20) + "|" + beautiful(
            str(row[3]), 24) + "|" + beautiful(str(row[4]), 6) + "|" + beautiful(str(row[5]), 20))
            cursor.execute("CALL Delete_record('zwierzeta','ID','" + zwierze + "');")
            break;
    conn.commit()
    sub_menu_animals()

def delete_stay():
    cursor = conn.cursor()
    print("Usuwanie danych pobytu")
    print("-------------------------------")
    results = show_stays()
    zwierze = str(input("Podaj ID Zwierzaka ktorego pobyt chcesz usunac: "))
    lokum = str(input("Podaj ID Lokum pasujace do zwierzaka: "))
    data_start = str(input("Podaj date start ktora pasuje do lokum oraz zwierzaka: "))
    show = beautiful("ZWIERZE", 14) + "|" + beautiful("GATUNEK", 30) + "|" + beautiful("LOKUM ID", 20) + beautiful(
        "DATA ROZPOCZECIA", 24)
    print(show)
    print(
        "---------------------------------------------------------------------------------------------------------------------")
    for row in results:
        if str(row[0]) == zwierze and str(row[2]) == lokum and str(row[3]) == data_start :
            print(beautiful(str(row[0]), 14) + "|" + beautiful(str(row[1]), 30) + "|" + beautiful(str(row[2]),20) + "|" + beautiful(str(row[3]), 24))

            cursor.execute("CALL Delete_stay('"+lokum+"','"+zwierze+"','"+ data_start +"');")
            break;
    conn.commit()
    sub_menu_stays()

#       MAIN MENU INTERFACE      #

def sub_menu_workers():
    print("PRACOWNICY")
    print("-------------------------------")
    print("OPCJE : ")
    print("1. Rejestracja nowego pracownika ")
    print("2. Modyfikacja danych pracownikow ")
    print("3. Usuniecie pracownika")
    print("4. Wyswietlenie dancyh pracownikow")
    print("5. WYJSCIE")
    choice = pick()
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                new_worker()
            case 2:
                print("-------------------------------")
                modify_worker()
            case 3:
                print("-------------------------------")
                delete_worker()
            case 4:
                print("-------------------------------")
                show_workers()
                sub_menu_workers()
            case 5:
                menu_supervisor()

def sub_menu_requests():
    print("ZLECENIA")
    print("-------------------------------")
    print("OPCJE : ")
    print("1. Stworzenie nowej grupy")
    print("2. Stworzenie nowego zlecenia")
    print("3. Modyfikacja zlecenia")
    print("4. Wyswietl zlecenia")
    print("5. Usun zlecenie")
    print("6. WYJSCIE")
    choice = pick()
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                new_group()
                sub_menu_requests()
            case 2:
                print("-------------------------------")
                new_request()
                sub_menu_requests()
            case 3:
                print("-------------------------------")
                modify_request()
                sub_menu_requests()
            case 4:
                show_requests()
                sub_menu_requests()
            case 5:
                print("-------------------------------")
                delete_request()
                sub_menu_requests()
            case 6:
                menu_supervisor()

def sub_menu_stays():
    print("POBYTY")
    print("-------------------------------")
    print("OPCJE : ")
    print("1. Stworzenie nowego pobytu zwierzecia")
    print("2. Wyswietlenie danych pobytow")
    print("3. Modyfikacja Danych pobytu")
    print("4. Usuwanie danych pobytu")
    print("5. WYJSCIE")
    choice = pick()
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                new_stay()
            case 2:
                print("-------------------------------")
                show_stays()
                sub_menu_stays()
            case 3:
                print("-------------------------------")
                modify_stay()
            case 4:
                print("-------------------------------")
                delete_stay()
            case 5:
                if supervisor_id == 'None':
                    menu_supervisor()
                else:
                    menu_worker()

def sub_menu_animals():
    print("ZWIERZETA")
    print("-------------------------------")
    print("OPCJE: ")
    print("1. Rejestracja nowego zwierzaka")
    print("2. Wyswietlenie danych zwierzat")
    print("3. Modyfikacja danych zwierzat")
    print("4. Usuwanie danych zwierzat")
    print("5. WYJSCIE")
    choice = pick()
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                new_animal()
            case 2:
                print("-------------------------------")
                show_animals()
                sub_menu_animals()
            case 3:
                print("-------------------------------")
                modify_animal()
            case 4:
                print("-------------------------------")
                delete_animal()
            case 5:
                if supervisor_id == 'None':
                    menu_supervisor()
                else:
                    menu_worker()

def sub_menu_groups():
    print("GRUPY")
    print("---------------------------------")
    print("OPCJE: ")
    print("1. Rejestracja nowej grupy")
    print("2. Wyswietl grupy")
    print("3. Modyfikacja danych grupy")
    print("4. Usuwanie danych grupy")
    print("5. WYJSCIE")
    choice = pick()
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                new_group()
                sub_menu_groups()
            case 2:
                print("-------------------------------")
                show_groups()
                sub_menu_groups()
            case 3:
                print("-------------------------------")
                modify_groups()
            case 4:
                print("-------------------------------")
                delete_group()
            case 5:
                if supervisor_id == 'None':
                    menu_supervisor()
                else:
                    menu_worker()

def menu_supervisor():
    print("BAZA DANYCH DO ZARZADZANIA ZOO")
    print("-------------------------------")
    print("1. PRACOWNICY")
    print("2. POBYTY")
    print("3. ZWIERZETA")
    print("4. ZLECENIA")
    print("5. GRUPY")
    print("6. ZMIANA HASLA")
    print("7. WYJSCIE")
    choice = input("Enter your choice: ")
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                sub_menu_workers()
            case 2:
                print("-------------------------------")
                sub_menu_stays()
            case 3:
                print("-------------------------------")
                sub_menu_animals()
            case 4:
                print("-------------------------------")
                sub_menu_requests()
            case 5:
                print("-------------------------------")
                sub_menu_groups()
            case 6:
                print("-------------------------------")
                change_password()
                menu_supervisor()
            case 7:
                break

def menu_worker():
    print("BAZA DANYCH DO ZARZADZANIA ZOO")
    print("-------------------------------")
    print("1. POBYTY")
    print("2. ZWIERZETA")
    print("3. ZLECENIA")
    print("4. ZMIANA HASLA")
    print("5. WYJSCIE")
    choice = input("Enter your choice: ")
    while True:
        match int(choice):
            case 1:
                print("-------------------------------")
                sub_menu_stays()
            case 2:
                print("-------------------------------")
                sub_menu_animals()
            case 3:
                print("-------------------------------")
                modify_status()
            case 4:
                print("-------------------------------")
                change_password()
                menu_worker()
            case 5:
                break

main()

# nowy_pracownik()"|")