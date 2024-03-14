import datetime
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

'''
A mi programunk a károsanyag kibocsátását számolja egy adott autónak és ezt összehasonlítja egy hasonló távot megtett
busszal, repülőgéppel, és az otthoni fűtéssel.
'''

'''
Ez az autó osztályunk, ami azért hasznos, mert több autót is lehetne inicializálni, azaz több tárgyat hozhatunk létre,
amelyeknek ugyanilyen értékei és függvényei vannak.
'''


class Car:
    MAX_CAR_TYPE_LENGTH = 60

    '''
    
    '''

    def __init__(self):
        self.manufacturer = None
        self.type = None
        self.registration_year = None
        self.registration_month = None
        self.fuel_type = None
        self.distance = None

    def set_manifacturer(self, manifacturer):
        self.manufacturer = manifacturer

    def set_type(self, type):
        if len(type) > self.MAX_CAR_TYPE_LENGTH:
            self.type = None
        else:
            self.type = type

    def set_registration_year(self, year):
        self.registration_year = year

    def set_registration_month(self, month):
        self.registration_month = month

    def set_fuel_type(self, fuel_type):
        self.fuel_type = fuel_type

    def set_distance(self, distance):
        self.distance = distance

    '''
    Ez a függvény kiírja, hogy a felhasználó milyen értékeket adott meg.
    @:param self: Az adott tárgy, azaz autó, amely értékeit ismerjük, mert megkaptuk a felhasználótól
    '''

    def overall_info(self):
        print("----------------------------------------------------------------")
        print("Autója adatai: ")
        print(f"gyártó: {self.manufacturer} ")
        print(f"gyártási év: {self.registration_year} ")
        print(f"gyártási hónap: {self.registration_month} ")
        print(f"üzemanyag típusa: {self.fuel_type} ")
        print(f"megtett kilóméter: {self.distance} ")
        print("----------------------------------------------------------------")

    '''
    Ebben a függvényben az autót a megfelelő Euro kategóriához hozzárendeli
    @:param self: Az adott tárgy, azaz autó, amelyhez keressük az Euro kategóriát
    @:return: Azt adjuk vissza amelyik kategóriába tartozik az adott autó, amelyikre felhívtuk a függvényt a main-ben
    '''

    def determine_euro_category(self):
        global euro_category
        euro_categories = [
            (1885, 1, "Unknown"),
            (1992, 7, "Euro 1"),
            (1996, 1, "Euro 2"),
            (2000, 1, "Euro 3"),
            (2005, 1, "Euro 4"),
            (2009, 9, "Euro 5"),
            (2014, 9, "Euro 6")
        ]

        registration_date = datetime(self.registration_year, self.registration_month, 1)

        for category_year, category_month, category_name in euro_categories:
            category_date = datetime(category_year, category_month, 1)
            if category_date is None or registration_date >= category_date:
                euro_category = category_name
            else:
                break
        return euro_category

    EURO_CO_EMISSION_FACTORS = {
        "diesel": {
            "Euro 1": 2.72,
            "Euro 2": 1.0,
            "Euro 3": 0.66,
            "Euro 4": 0.50,
            "Euro 5": 0.50,
            "Euro 6": 0.50
        },
        "gasoline": {
            "Euro 1": 2.72,
            "Euro 2": 2.2,
            "Euro 3": 2.3,
            "Euro 4": 1.0,
            "Euro 5": 1.0,
            "Euro 6": 1.0
        }
    }

    '''
    Ez a függvény az autó CO kibocsájtását számolja ki, amelyhez az autó Euro értéke alapján keresi ki a megfelelő
    adott számot az EURO_CO_EMISSION_FACTORS-ból
    @:param self: Az adott tárgy, azaz autó, amellyel számolunk
    @:return: co_emission, ami a kiszámolt CO értéket adja vissza kg-ban
    '''

    def calculate_CO_emission(self):
        category = self.determine_euro_category()
        if category == "Unknown":
            return None
        emission_factor = self.EURO_CO_EMISSION_FACTORS[self.fuel_type][category]
        co_emission = emission_factor * self.distance / 100
        return co_emission

    EURO_NOx_EMISSION_FACTORS = {
        "diesel": {
            "Euro 1": 404,
            "Euro 2": 404,
            "Euro 3": 0.5,
            "Euro 4": 0.25,
            "Euro 5": 0.18,
            "Euro 6": 0.08
        },
        "gasoline": {
            "Euro 1": 404,
            "Euro 2": 404,
            "Euro 3": 0.15,
            "Euro 4": 0.8,
            "Euro 5": 0.6,
            "Euro 6": 0.6
        }
    }

    '''
    Ez a függvény az autó NOx kibocsájtását számolja ki, amelyhez az autó Euro értéke alapján keresi ki a megfelelő
    adott számot az EURO_NOx_EMISSION_FACTORS-ból
    @:param self: Az adott tárgy, azaz autó, amellyel számolunk
    @:return: nox_emission, ami a kiszámolt NOx értéket adja vissza kg-ban
    '''

    def calculate_NOx_emission(self):
        category = self.determine_euro_category()
        if category == "Unknown":
            return None
        emission_factor = self.EURO_NOx_EMISSION_FACTORS[self.fuel_type][category]
        if emission_factor == 404:
            return None
        nox_emission = emission_factor * self.distance / 100  # TODO: kg-ban adja vissza az értéket
        return nox_emission

    EURO_PM_EMISSION_FACTORS = {
        "diesel": {
            "Euro 1": 0.14,
            "Euro 2": 0.08,
            "Euro 3": 0.05,
            "Euro 4": 0.025,
            "Euro 5": 0.0045,
            "Euro 6": 0.0045
        },
        "gasoline": {
            "Euro 1": 404,
            "Euro 2": 404,
            "Euro 3": 404,
            "Euro 4": 404,
            "Euro 5": 0.005,
            "Euro 6": 0.0045
        }
    }

    '''
    Ez a függvény az autó PM kibocsájtását számolja ki, amelyhez az autó Euro értéke alapján keresi ki a megfelelő
    adott számot az EURO_PM_EMISSION_FACTORS-ból
    @:param self: Az adott tárgy, azaz autó, amellyel számolunk
    @:return: pm_emission, ami a kiszámolt PM értéket adja vissza kg-ban
    '''

    def calculate_PM_emission(self):
        category = self.determine_euro_category()
        if category == "Unknown":
            return None
        emission_factor = self.EURO_PM_EMISSION_FACTORS[self.fuel_type][category]
        if emission_factor == 404:
            return None
        pm_emission = emission_factor * self.distance / 100
        return pm_emission


'''
Ez a függvény beolvassa az autógyártókat a Manifacturers.txt fájlból és egy szettet készít, úgy hogy a beolvasott
gyártókat átírja kisbetűkre, enter nélkül, azért hogy a későbbiekben könnyebb legyen a felhasználó által beírt gyártóval
összehasonlítani. A try-except blokkot azért használjuk, hogy ha esetlegesen nem lehet beolvasni a függvénynek 
átadott fájlt, akkor ezt tudathassuk a felhasználóval.
@:param filename: Ez a függvény paraméterként a fájl nevét, ebben az esetben ez a Manifacturers.txt lesz, várja,
                  amit feldolgoz.
@:return: Egy szettet ad vissza, amit majd a mainben használni tudunk a beírt gyártóval való összehasonlításhoz.
'''


def read_manufacturers_from_file(filename):
    manufacturers = set()
    try:
        with open(filename, 'r') as file:
            for line in file:
                manufacturers.add(line.strip().lower())
    except FileNotFoundError:
        print(f"A fájl '{filename}' nem található.")
    return manufacturers


'''
Itt nézzük meg, hogy a beírt gyártó, létezik-e, úgy hogy az előző függvény által beolvasott listán iterálunk végig.
@:param user_input: A felhasználó által beírt gyártó.
@:param: manufacturers: Beolvasott lista az összes létező autógyártóval.
@:return: True, ha létezik a keresett gyártó, False, ha nem létezik.
'''


def check_manufacturer(user_input, manufacturers):
    return user_input.lower() in manufacturers


# '''
# Az első autót 1886-ban gyártották és a legutolsót ebben az évben helyezték forgalomba, így lecsekkoljuk, hogy a user
# valid értéket adott-e meg.
# @:param year: A vizsgálandó év.
# @:return: True, ha helyes az év, False, ha nem.
# '''
#
#
# def check_valid_year(year):
#     try:
#         year = int(year)
#         return 1886 <= year <= 2024
#     except ValueError:
#         return False
#
#
# '''
# A beírt hónapot is megnzézzük, hogy lehetséges érték lett-e megadva.
# @:param month: A vizsgálandó hónap.
# @:return: True, ha helyes a hónap, False, ha nem.
# '''
#
#
# def check_valid_month(month):
#     try:
#         month = int(month)
#         return 1 <= month <= 12
#     except ValueError:
#         return False


# '''
# A beírt távot csekkoljuk, nehogy negatív érték legyen megadva.
# @:param distance: A vizsgálandó táv.
# @:return: True, ha helyes a táv, False, ha nem.
# '''
#
#
# def is_valid_distance(distance):
#     return distance > 0
#

'''
A megadott inputot csekkoljuk, hogy szám lett-e megadva.
@:param user_input: A vizsgálandó input. Ha szám, akkor rögtön konvertáljuk int-re az értéket (egész számra).
                    Ha nem szám, akkor az except kiírja, hogy rossz érték lett beírva és újra kéri az értéket.
@:return: True, ha szám, False, ha nem.
'''


def input_integer(user_input):
    while True:
        try:
            value = int(input(user_input))
            return value
        except ValueError:
            print("Csak szám lehet a beírt érték!")


'''
A megadott inputot csekkoljuk, hogy szám lett-e megadva.
@:param user_input: A vizsgálandó input. Ha szám, akkor rögtön konvertáljuk float-ra az értéket. Ha nem szám, akkor az
                    except kiírja, hogy rossz érték lett beírva és újra kéri az értéket.
@:return: True, ha szám, False, ha nem.
'''


def input_float(user_input):
    while True:
        try:
            value = float(input(user_input))
            return value
        except ValueError:
            print("Csak szám lehet a beírt érték!")


'''
Ez itt a fő függvényünk, ami mindent kezel és itt hívjuk fel a többi függvényt.
'''

manufacturers = read_manufacturers_from_file('Manufacturers.txt')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    manufacturers = read_manufacturers_from_file('Manufacturers.txt')
    if request.method == 'POST':
        manufacturer = request.form['manufacturer']
        year = request.form['year']
        month = request.form['month']
        distance = request.form['distance']
        fuel_type = request.form['fuel_type']

        if not manufacturer.lower() in manufacturers:
            error = "Nincs ilyen autógyártó!"
        elif not (1886 <= int(year) <= 2024):
            if int(year) > 2024:
                error = "Egyelőre 2024-et írunk!"
            else:
                error = "Az első autót 1885-ben gyártották, Benz Patent-Motorwagen néven!"

        elif not (1 <= int(month) <= 12):
            error = "A világnaptár szerint 1-től 12-ig léteznek hónapok!"
        elif not (float(distance) > 0):
            error = "Érvénytelen távolság!"
        else:
            my_car = Car()
            my_car.set_manifacturer(manufacturer)
            my_car.set_registration_year(int(year))
            my_car.set_registration_month(int(month))
            my_car.set_fuel_type(fuel_type)
            my_car.set_distance(float(distance))

            euro_category_of_my_car = my_car.determine_euro_category()
            co_emission = my_car.calculate_CO_emission()
            nox_emission = my_car.calculate_NOx_emission()
            pm_emission = my_car.calculate_PM_emission()
            total_emission = sum(filter(None, [co_emission, nox_emission, pm_emission]))

            return render_template('result.html', manufacturer=manufacturer, euro_category=euro_category_of_my_car,
                                   co_emission=co_emission, nox_emission=nox_emission, pm_emission=pm_emission,
                                   total_emission=total_emission)

    return render_template('index.html', error=error)

if __name__ == '__main__':
    app.run(debug=True)

# def main():
#     file = 'Manufacturers.txt'
#     manufacturers = read_manufacturers_from_file(file)
#     my_car = Car()
#
#     print(f"----------------------------------------------------------------")
#     print(f"Üdvözöllek a károsanyag kibocsátást számoló programunkban!")
#     print(f"A program nem használható elektromos és hibrid működésű autókra.")
#     print(f"----------------------------------------------------------------")
#
#     while True:
#         my_car.manufacturer = input("~ Ki a jármű gyártója?")
#         if not check_manufacturer(my_car.manufacturer, manufacturers):
#             print("Nincs ilyen autógyártó!")
#             continue
#         else:
#             break
#
#     while True:
#         my_car.registration_year = input_integer("~ Melyik évben gyártották a járművet? (YYYY)")
#         if not check_valid_year(my_car.registration_year):
#             if my_car.registration_year < 1885:
#                 print("Az első autót 1885-ben gyártották, Benz Patent-Motorwagen néven.")
#             elif my_car.registration_year > 2024:
#                 print("Egyelőre 2024-et írunk!")
#             continue
#         else:
#             break
#
#     while True:
#         my_car.registration_month = input_integer("~ Melyik hónapban gyártották a járművet? (MM)")
#         if not check_valid_month(my_car.registration_month):
#             print("A világnaptár szerint 1-től 12-ig léteznek hónapok!")
#             continue
#         else:
#             break
#
#     while True:
#         my_car.distance = input_float("~ Mennyi km van kerekítve az autóban?")
#         if not is_valid_distance(my_car.distance):
#             print("Érvénytelen adat!")
#             continue
#         else:
#             break
#
#     print("Üzemanyag típusok:")
#     print("1. Dízel")
#     print("2. Benzin")
#
#     while True:
#         fuel_choice = input("~ Kérjük, válasszon üzemanyag típust (1 vagy 2): ")
#         fuel_type_mapping = {"1": "diesel", "2": "gasoline"}
#         fuel_choice = fuel_type_mapping.get(fuel_choice)
#         if fuel_choice is None:
#             print("Érvénytelen választás.")
#             continue
#         else:
#             my_car.fuel_type = fuel_choice
#             break
#
#     my_car.overall_info()
#     euro_category_of_my_car = my_car.determine_euro_category()
#     if euro_category_of_my_car == "Unknown":
#         print("Az Ön autójára nem vonatkoznak kibocsájtási előírások!")
#     else:
#         print(f"Az Ön autója az {euro_category_of_my_car} kategóriába tartozik.")
#         print(f"Az autód CO kibocsájtása {my_car.calculate_CO_emission()} kg az eddig megtett km-ek alatt.")
#
#         nox_emission = my_car.calculate_NOx_emission()
#         pm_emission = my_car.calculate_PM_emission()
#         if nox_emission is not None:
#             print(f"Az autód NOx kibocsájtása {nox_emission} kg az eddig megtett km-ek alatt.")
#         else:
#             print("Az Ön autójára nincsenek elérhető NOx kibocsátási normák!")
#         if pm_emission is not None:
#             print(f"Az autód PM kibocsájtása {pm_emission} kg az eddig megtett km-ek alatt.")
#         else:
#             print("Az Ön autójára nincsenek elérhető PM kibocsátási normák!")
#
#     # összeszámoljuk az összes károsanyag kibocsájtást.
#     emissions = [value for value in
#                  [my_car.calculate_CO_emission(), my_car.calculate_NOx_emission(), my_car.calculate_PM_emission()] if
#                  value is not None]
#     total_emission = sum(emissions)
#
#     if total_emission:
#         print(f"A jármű összes ismert kibocsátása: {total_emission} kg az eddig megtett km-ek alatt.")
#     else:
#         print("Nem tudjuk kiszámolni a jármű összes kibocsátását.")
#
#
# if __name__ == "__main__":
#     main()
