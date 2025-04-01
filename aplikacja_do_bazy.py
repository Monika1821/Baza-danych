from tkinter.ttk import Label, Entry, Button


import oracledb
import tkinter as tk
from tkinter import ttk, messagebox

# Dane połączenia z bazą danych Oracle
DB_HOST = "localhost"
DB_PORT = "1521"
DB_SERVICE_NAME = "XEPDB1"
DB_USER = "MOJA_BAZA"
DB_PASSWORD = "Baza"


# Funkcja łącząca się z bazą danych
def connect_to_database():
    try:
        dsn = oracledb.makedsn(DB_HOST, DB_PORT, service_name=DB_SERVICE_NAME)
        connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd połączenia", f"Błąd połączenia z bazą danych: {e}")
        return None

# Funkcja wywołująca procedurę dodaj_kategorie
def dodaj_kategorie(kategoria):
    try:
        # Łączenie z bazą danych
        connection = connect_to_database()
        if connection is None:
            return

        # Tworzenie kursora
        cursor = connection.cursor()

        # Wywołanie procedury dodaj_kategorie z parametrem
        cursor.callproc('dodaj_kategorie', [kategoria])

        # Zatwierdzenie zmian
        connection.commit()

        # Pokazanie komunikatu o powodzeniu
        messagebox.showinfo("Sukces", f'Kategoria "{kategoria}" została dodana lub już istnieje w bazie.')

        # Zamknięcie kursora i połączenia
        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd: {e}")


# Funkcja obsługująca kliknięcie przycisku "Dodaj Kategorię"
def on_add_category():
    kategoria = entry_kategoria.get()
    if kategoria:
        dodaj_kategorie(kategoria)
    else:
        messagebox.showwarning("Uwaga", "Proszę wprowadzić nazwę kategorii!")






# Funkcja do pobierania kategorii z bazy danych
def get_kategorie():
    try:
        connection = connect_to_database()
        if connection is None:
            return []

        cursor = connection.cursor()
        cursor.execute("SELECT id, nazwa_kategorii FROM Kategoria_Produktu")
        kategorie = cursor.fetchall()

        cursor.close()
        connection.close()

        return kategorie
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd pobierania kategorii: {e}")
        return []

# Funkcja wywołująca procedurę dodaj_produkt
def dodaj_produkt(cena_nabycia, cena_sprzedazy, nazwa, id_kategorii):
    try:
        connection = connect_to_database()
        if connection is None:
            return

        cursor = connection.cursor()
        cursor.callproc('dodaj_produkt', [cena_nabycia, cena_sprzedazy, nazwa, id_kategorii])

        connection.commit()
        messagebox.showinfo("Sukces", f'Produkt "{nazwa}" został dodany do bazy danych.')

        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd: {e}")

# Funkcja do otwierania okna dodawania produktu
def open_add_product_window():
    # Nowe okno formularza do dodawania produktu
    add_product_window = tk.Toplevel(root)
    add_product_window.title("Dodaj Produkt")

    # Pole do wprowadzenia nazwy produktu
    tk.Label(add_product_window, text="Nazwa produktu:").grid(row=0, column=0)
    name_entry = tk.Entry(add_product_window)
    name_entry.grid(row=0, column=1)

    # Pole do wprowadzenia ceny nabycia
    tk.Label(add_product_window, text="Cena nabycia:").grid(row=1, column=0)
    purchase_price_entry = tk.Entry(add_product_window)
    purchase_price_entry.grid(row=1, column=1)

    # Pole do wprowadzenia ceny sprzedaży
    tk.Label(add_product_window, text="Cena sprzedaży:").grid(row=2, column=0)
    sale_price_entry = tk.Entry(add_product_window)
    sale_price_entry.grid(row=2, column=1)

    # Pole do wyboru kategorii
    tk.Label(add_product_window, text="Wybierz kategorię:").grid(row=3, column=0)
    categories = get_kategorie()
    category_combobox = ttk.Combobox(add_product_window, values=[f"{cat[0]} - {cat[1]}" for cat in categories])
    category_combobox.grid(row=3, column=1)

    # Funkcja do dodania produktu
    def submit_product():
        try:
            name = name_entry.get()
            purchase_price = float(purchase_price_entry.get())
            sale_price = float(sale_price_entry.get())
            category_id = int(category_combobox.get().split()[0])  # Pobieranie ID kategorii z comboboxa

            dodaj_produkt(purchase_price, sale_price, name, category_id)
            add_product_window.destroy()  # Zamknięcie okna po dodaniu produktu
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas dodawania produktu: {e}")

    # Przyciski
    submit_button = tk.Button(add_product_window, text="Zatwierdź", command=submit_product)
    submit_button.grid(row=4, column=0, columnspan=2)


#dodawanie produktu
# Funkcja do obsługi dodawania nowego produktu
def on_add_new_product():
    def add_product_to_db():
        try:
            cena_nabycia = float(entry_cena_nabycia.get())
            cena_sprzedazy = float(entry_cena_sprzedazy.get())
            nazwa = entry_nazwa_produktu.get()
            id_kategorii = int(combo_kategoria.get().split(" - ")[0])  # Wybierz kategorię na podstawie id

            dodaj_produkt(cena_nabycia, cena_sprzedazy, nazwa, id_kategorii)
            window_add_product.destroy()
        except ValueError:
            messagebox.showwarning("Błąd", "Proszę poprawnie wprowadzić ceny oraz identyfikator kategorii!")

    # Tworzenie okna do dodania nowego produktu
    window_add_product = tk.Toplevel(root)
    window_add_product.title("Dodaj Nowy Produkt")

    tk.Label(window_add_product, text="Nazwa Produktu:").pack(pady=10)
    entry_nazwa_produktu = tk.Entry(window_add_product, width=30)
    entry_nazwa_produktu.pack(pady=5)

    tk.Label(window_add_product, text="Cena Nabycia:").pack(pady=10)
    entry_cena_nabycia = tk.Entry(window_add_product, width=30)
    entry_cena_nabycia.pack(pady=5)

    tk.Label(window_add_product, text="Cena Sprzedaży:").pack(pady=10)
    entry_cena_sprzedazy = tk.Entry(window_add_product, width=30)
    entry_cena_sprzedazy.pack(pady=5)

    tk.Label(window_add_product, text="Wybierz Kategorię:").pack(pady=10)
    combo_kategoria = ttk.Combobox(window_add_product, values=[f"{i[0]} - {i[1]}" for i in get_kategorie()])
    combo_kategoria.pack(pady=5)

    tk.Button(window_add_product, text="Dodaj Produkt", command=add_product_to_db).pack(pady=20)



# Funkcja do pobierania produktów i ich stanów
# Funkcja do pobierania produktów i ich stanów
def get_produkty_stany():
    try:
        connection = connect_to_database()
        if connection is None:
            return []

        cursor = connection.cursor()
        cursor.execute("""
            SELECT p.nazwa, sp.ilosc_magazyn, sp.ilosc_sklep
            FROM Produkt p
            JOIN Stan_produktu sp ON sp.id_produktu = p.id
        """)
        produkty = cursor.fetchall()

        cursor.close()
        connection.close()

        # Zwrócenie listy produktów w formacie: "nazwa produktu - magazyn: X, sklep: Y"
        produkty_formatowane = [
            f"{produkt[0]} - Magazyn: {produkt[1]}, Sklep: {produkt[2]}"
            for produkt in produkty
        ]

        return produkty_formatowane
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd pobierania produktów: {e}")
        return []

# Funkcja do otwierania okna z produktami i ich stanami
def open_products_window():
    window_products = tk.Toplevel(root)
    window_products.title("Produkty i Ich Stany")

    # Pobranie produktów i ich stanów
    produkty_stany = get_produkty_stany()

    # Tworzenie widoku produktów
    if produkty_stany:
        treeview = ttk.Treeview(window_products, columns=("Produkt", "Ilość Magazyn", "Ilość Sklep"), show="headings")
        treeview.heading("Produkt", text="Produkt")
        treeview.heading("Ilość Magazyn", text="Ilość w Magazynie")
        treeview.heading("Ilość Sklep", text="Ilość w Sklepie")

        for produkt in produkty_stany:
            treeview.insert("", "end", values=produkt)

        treeview.pack(padx=20, pady=20, fill="both", expand=True)
    else:
        messagebox.showwarning("Brak danych", "Brak danych do wyświetlenia.")


# Funkcja wywołująca procedurę przenies_produkt
def przenies_produkt(nazwa_produktu, ilosc_przeniesienia):
    try:
        connection = connect_to_database()
        if connection is None:
            return

        cursor = connection.cursor()
        cursor.callproc('przenies_produkt', [nazwa_produktu, ilosc_przeniesienia])

        connection.commit()
        messagebox.showinfo("Sukces", f'Przeniesiono {ilosc_przeniesienia} sztuk produktu "{nazwa_produktu}" z magazynu do sklepu.')

        cursor.close()
        connection.close()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd: {e}")


# Funkcja do otwierania okna przenoszenia produktów
    # Funkcja do otwierania okna przenoszenia produktów
def open_move_product_window():
    window_move_product = tk.Toplevel(root)
    window_move_product.title("Przenieś Produkt")

    # Pobranie listy produktów z ich stanami
    produkty_stany = get_produkty_stany()

    if produkty_stany:
        tk.Label(window_move_product, text="Wybierz produkt:").pack(pady=10)

        # Stworzenie listy rozwijanej z produktami i ich stanami
        combo_produkt = ttk.Combobox(window_move_product, values=produkty_stany, width=50)
        combo_produkt.pack(pady=5)

        tk.Label(window_move_product, text="Podaj ilość do przeniesienia:").pack(pady=10)
        entry_ilosc = tk.Entry(window_move_product, width=30)
        entry_ilosc.pack(pady=5)

        def on_move_product():
            produkt = combo_produkt.get()
            ilosc = entry_ilosc.get()

            if produkt and ilosc:
                try:
                    # Wyodrębnienie nazwy produktu z wybranej opcji
                    produkt_nazwa = produkt.split(" - ")[0]
                    ilosc = int(ilosc)
                    przenies_produkt(produkt_nazwa, ilosc)
                    window_move_product.destroy()
                except ValueError:
                    messagebox.showwarning("Błąd", "Proszę wprowadzić poprawną ilość!")
            else:
                messagebox.showwarning("Uwaga", "Proszę wybrać produkt i podać ilość.")

        tk.Button(window_move_product, text="Przenieś Produkt", command=on_move_product).pack(pady=20)

        # Wyświetlanie stanu produktu po wybraniu produktu z listy rozwijanej
        def show_product_state(event):
            produkt = combo_produkt.get()
            if produkt:
                # Wyodrębnienie nazwy produktu z wybranej opcji
                produkt_nazwa = produkt.split(" - ")[0]
                # Pobranie stanu produktu z bazy danych
                for p in produkty_stany:
                    if p.startswith(produkt_nazwa):
                        ilosc_magazyn = p.split("Magazyn: ")[1].split(",")[0]
                        ilosc_sklep = p.split("Sklep: ")[1]
                        messagebox.showinfo("Stan Produktu",
                                            f"Stan produktu '{produkt_nazwa}':\nIlość w magazynie: {ilosc_magazyn}\nIlość w sklepie: {ilosc_sklep}")
                        break

        # Dodanie funkcjonalności, żeby po wybraniu produktu pokazywał się jego stan
        combo_produkt.bind("<<ComboboxSelected>>", show_product_state)
    else:
        messagebox.showwarning("Brak produktów", "Brak dostępnych produktów do przeniesienia.")


# Funkcja wywołująca okno do dodawania pracownika
def open_add_employee_window():
    add_employee_window = tk.Toplevel(root)
    add_employee_window.title("Dodaj Pracownika")

    tk.Label(add_employee_window, text="Imię:").grid(row=0, column=0)
    tk.Label(add_employee_window, text="Nazwisko:").grid(row=1, column=0)
    tk.Label(add_employee_window, text="ID Przełożonego (opcjonalne):").grid(row=2, column=0)

    imie_entry = tk.Entry(add_employee_window)
    nazwisko_entry = tk.Entry(add_employee_window)
    id_przelozonego_entry = tk.Entry(add_employee_window)

    imie_entry.grid(row=0, column=1)
    nazwisko_entry.grid(row=1, column=1)
    id_przelozonego_entry.grid(row=2, column=1)

    def add_employee():
        imie = imie_entry.get()
        nazwisko = nazwisko_entry.get()
        id_przelozonego = id_przelozonego_entry.get()

        if not imie or not nazwisko:
            messagebox.showerror("Błąd", "Proszę podać imię i nazwisko.")
            return

        connection = connect_to_database()
        if connection is None:
            return

        try:
            with connection.cursor() as cursor:
                cursor.callproc(
                    "dodaj_pracownika",
                    [imie, nazwisko, int(id_przelozonego) if id_przelozonego else None]
                )
            connection.commit()
            messagebox.showinfo("Sukces", f"Pracownik {imie} {nazwisko} dodany.")
            add_employee_window.destroy()
        except oracledb.DatabaseError as e:
            error, = e.args
            messagebox.showerror("Błąd", f"Błąd bazy danych: {error.message}")
        finally:
            connection.close()

    tk.Button(add_employee_window, text="Dodaj Pracownika", command=add_employee).grid(row=3, columnspan=2)


# Funkcja wywołująca okno do dodawania klienta
def open_add_customer_window():
    add_customer_window = tk.Toplevel(root)
    add_customer_window.title("Dodaj Klienta")

    tk.Label(add_customer_window, text="Imię:").grid(row=0, column=0)
    tk.Label(add_customer_window, text="Nazwisko:").grid(row=1, column=0)
    tk.Label(add_customer_window, text="Adres:").grid(row=2, column=0)
    tk.Label(add_customer_window, text="Email:").grid(row=3, column=0)
    tk.Label(add_customer_window, text="Telefony (oddzielone przecinkami):").grid(row=4, column=0)

    imie_entry = tk.Entry(add_customer_window)
    nazwisko_entry = tk.Entry(add_customer_window)
    adres_entry = tk.Entry(add_customer_window)
    email_entry = tk.Entry(add_customer_window)
    telefony_entry = tk.Entry(add_customer_window)

    imie_entry.grid(row=0, column=1)
    nazwisko_entry.grid(row=1, column=1)
    adres_entry.grid(row=2, column=1)
    email_entry.grid(row=3, column=1)
    telefony_entry.grid(row=4, column=1)

    def add_customer():
        imie = imie_entry.get()
        nazwisko = nazwisko_entry.get()
        adres = adres_entry.get()
        email = email_entry.get()
        telefony = telefony_entry.get().split(',')

        if not imie or not nazwisko or not adres or not email:
            messagebox.showerror("Błąd", "Proszę podać wszystkie wymagane dane.")
        else:
            # Tutaj wywołujesz funkcję dodaj_klienta z poprzedniej odpowiedzi
            # add_customer(imie, nazwisko, adres, email, telefony)
            messagebox.showinfo("Sukces", f"Klient {imie} {nazwisko} dodany.")
            add_customer_window.destroy()

        tk.Button(add_customer_window, text="Dodaj Klienta", command=add_customer).grid(row=5, columnspan=2)# Funkcja wywołująca okno do dodawania klienta
def open_add_customer_window():
    add_customer_window = tk.Toplevel(root)
    add_customer_window.title("Dodaj Klienta")

    tk.Label(add_customer_window, text="Imię:").grid(row=0, column=0)
    tk.Label(add_customer_window, text="Nazwisko:").grid(row=1, column=0)
    tk.Label(add_customer_window, text="Adres:").grid(row=2, column=0)
    tk.Label(add_customer_window, text="Email:").grid(row=3, column=0)
    tk.Label(add_customer_window, text="Telefony (oddzielone przecinkami):").grid(row=4, column=0)

    imie_entry = tk.Entry(add_customer_window)
    nazwisko_entry = tk.Entry(add_customer_window)
    adres_entry = tk.Entry(add_customer_window)
    email_entry = tk.Entry(add_customer_window)
    telefony_entry = tk.Entry(add_customer_window)

    imie_entry.grid(row=0, column=1)
    nazwisko_entry.grid(row=1, column=1)
    adres_entry.grid(row=2, column=1)
    email_entry.grid(row=3, column=1)
    telefony_entry.grid(row=4, column=1)

    def add_customer():
        imie = imie_entry.get()
        nazwisko = nazwisko_entry.get()
        adres = adres_entry.get()
        email = email_entry.get()
        telefony = [telefon.strip() for telefon in telefony_entry.get().split(',') if telefon.strip()]

        if not imie or not nazwisko or not adres or not email:
            messagebox.showerror("Błąd", "Proszę podać wszystkie wymagane dane.")
            return

        connection = connect_to_database()
        if connection is None:
            return

        try:
            cursor = connection.cursor()

            # Pobranie typu SYS.ODCIVARCHAR2LIST
            typ_telefonów = connection.gettype("SYS.ODCIVARCHAR2LIST")

            # Utworzenie instancji tego typu
            telefony_list = typ_telefonów.newobject()
            for telefon in telefony:
                telefony_list.append(telefon)

            # Wywołanie procedury dodaj_klienta
            cursor.callproc(
                "dodaj_klienta",
                [
                    imie,
                    nazwisko,
                    adres,
                    email,
                    telefony_list
                ]
            )
            connection.commit()
            messagebox.showinfo("Sukces", f"Klient {imie} {nazwisko} dodany.")
            add_customer_window.destroy()

        except oracledb.DatabaseError as e:
            messagebox.showerror("Błąd", f"Błąd podczas dodawania klienta: {e}")
            if connection:
                connection.rollback()
        finally:
            if connection:
                connection.close()

    tk.Button(add_customer_window, text="Dodaj Klienta", command=add_customer).grid(row=5, columnspan=2)



def pobierz_produkty():
    """Pobiera dostępne produkty z bazy danych."""
    connection = connect_to_database()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = """
        SELECT p.id, p.nazwa, sp.ilosc_sklep
        FROM Produkt p
        JOIN Stan_produktu sp ON p.id = sp.id_produktu
        WHERE sp.ilosc_sklep > 0
        """
        cursor.execute(query)
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd podczas pobierania produktów: {e}")
        return []
    finally:
        connection.close()

def pobierz_pracownikow():
    """Pobiera listę pracowników z bazy danych."""
    connection = connect_to_database()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = "SELECT id, imie || ' ' || nazwisko FROM Pracownik"
        cursor.execute(query)
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd podczas pobierania pracowników: {e}")
        return []
    finally:
        connection.close()

def pobierz_klientow():
    """Pobiera listę klientów z bazy danych."""
    connection = connect_to_database()
    if connection is None:
        return []

    try:
        cursor = connection.cursor()
        query = "SELECT id, imie || ' ' || nazwisko FROM Klient"
        cursor.execute(query)
        return cursor.fetchall()
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd podczas pobierania klientów: {e}")
        return []
    finally:
        connection.close()

def dodaj_zamowienie(produkty, metoda_platnosci, id_klienta, id_pracownika):
    """Dodaje zamówienie do bazy danych."""
    connection = connect_to_database()
    if connection is None:
        return

    try:
        cursor = connection.cursor()

        # Tworzenie listy produktów jako typ Oracle
        typ_produktu = connection.gettype("TYP_PRODUKTOW")
        lista_produktow = connection.gettype("LISTA_PRODUKTOW")
        produkty_oracle = lista_produktow.newobject()

        for nazwa, ilosc in produkty:
            produkt = typ_produktu.newobject()
            produkt.NAZWA = nazwa
            produkt.ILOSC = ilosc
            produkty_oracle.append(produkt)

        cursor.callproc("DODAJ_ZAMOWIENIE", [produkty_oracle, metoda_platnosci, id_klienta, id_pracownika])
        connection.commit()
        messagebox.showinfo("Sukces", "Zamówienie zostało pomyślnie dodane.")
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Błąd podczas dodawania zamówienia: {e}")
        connection.rollback()
    finally:
        connection.close()

def otworz_okno_zamowienia():
    """Otwiera okno do wypełniania zamówienia."""
    produkty_lista = []

    def dodaj_produkt_do_listy():
        selected_index = combobox_produkty.current()
        ilosc = entry_ilosc.get()

        if selected_index != -1 and ilosc.isdigit() and int(ilosc) > 0:
            produkt_id, nazwa, stan = produkty_z_bazy[selected_index]
            if int(ilosc) > stan:
                messagebox.showwarning("Błąd", "Przekroczono dostępną ilość produktu.")
                return
            produkty_lista.append((nazwa, int(ilosc)))
            listbox_produkty.insert(tk.END, f"{ilosc}x {nazwa}")
            entry_ilosc.delete(0, tk.END)
        else:
            messagebox.showwarning("Błąd", "Wybierz produkt i wprowadź prawidłową ilość.")

    def usun_produkt_z_listy():
        selected_index = listbox_produkty.curselection()
        if selected_index:
            listbox_produkty.delete(selected_index)
            produkty_lista.pop(selected_index[0])

    def zatwierdz_zamowienie():
        metoda_platnosci = var_platnosci.get()
        klient_index = combobox_klienci.current()
        pracownik_index = combobox_pracownicy.current()

        if not produkty_lista:
            messagebox.showwarning("Błąd", "Lista produktów jest pusta.")
            return

        if klient_index == -1:
            messagebox.showwarning("Błąd", "Wybierz klienta.")
            return

        if pracownik_index == -1:
            messagebox.showwarning("Błąd", "Wybierz pracownika.")
            return

        id_klienta = klienci_z_bazy[klient_index][0]
        id_pracownika = pracownicy_z_bazy[pracownik_index][0]

        dodaj_zamowienie(produkty_lista, metoda_platnosci, id_klienta, id_pracownika)
        okno_zamowienia.destroy()

    produkty_z_bazy = pobierz_produkty()
    pracownicy_z_bazy = pobierz_pracownikow()
    klienci_z_bazy = pobierz_klientow()

    okno_zamowienia = tk.Toplevel(root)
    okno_zamowienia.title("Dodaj zamówienie")

    frame_produkty = tk.Frame(okno_zamowienia)
    frame_produkty.pack(pady=10)

    tk.Label(frame_produkty, text="Wybierz produkt: ").grid(row=0, column=0)
    combobox_produkty = ttk.Combobox(frame_produkty, values=[f"{p[1]} (Stan: {p[2]})" for p in produkty_z_bazy])
    combobox_produkty.grid(row=0, column=1)

    tk.Label(frame_produkty, text="Ilość: ").grid(row=0, column=2)
    entry_ilosc = tk.Entry(frame_produkty)
    entry_ilosc.grid(row=0, column=3)

    tk.Button(frame_produkty, text="Dodaj produkt", command=dodaj_produkt_do_listy).grid(row=0, column=4)
    tk.Button(frame_produkty, text="Usuń produkt", command=usun_produkt_z_listy).grid(row=1, column=4)

    listbox_produkty = tk.Listbox(okno_zamowienia, height=10, width=50)
    listbox_produkty.pack(pady=10)

    frame_dane = tk.Frame(okno_zamowienia)
    frame_dane.pack(pady=10)

    tk.Label(frame_dane, text="Klient: ").grid(row=0, column=0)
    combobox_klienci = ttk.Combobox(frame_dane, values=[k[1] for k in klienci_z_bazy])
    combobox_klienci.grid(row=0, column=1)

    tk.Label(frame_dane, text="Pracownik: ").grid(row=0, column=2)
    combobox_pracownicy = ttk.Combobox(frame_dane, values=[p[1] for p in pracownicy_z_bazy])
    combobox_pracownicy.grid(row=0, column=3)

    tk.Label(okno_zamowienia, text="Metoda płatności: ").pack(pady=5)
    var_platnosci = tk.StringVar(value="gotowka")
    tk.Radiobutton(okno_zamowienia, text="Gotówka", variable=var_platnosci, value="gotowka").pack()
    tk.Radiobutton(okno_zamowienia, text="Online", variable=var_platnosci, value="online").pack()

    btn_zatwierdz = tk.Button(okno_zamowienia, text="Zatwierdź zamówienie", command=zatwierdz_zamowienie)
    btn_zatwierdz.pack(pady=20)





# Funkcja do przełączenia na formularz dodawania produktu
def show_add_product_form():
    frame_add_product.pack(padx=20, pady=20)


def fetch_data_from_table(connection, table_name):
    """Pobieranie danych z wybranej tabeli."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        return columns, rows
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać danych z tabeli {table_name}: {e}")
        return None, None


def delete_row_from_table(connection, table_name, row_id):
    """Usuwanie wiersza z tabeli na podstawie ID."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE id = :id", {"id": row_id})
        connection.commit()
        messagebox.showinfo("Sukces", f"Wiersz o ID {row_id} został usunięty z tabeli {table_name}.")
    except oracledb.DatabaseError as e:
        messagebox.showerror("Błąd", f"Nie udało się usunąć wiersza: {e}")


def show_table_data(connection, table_name):
    """Wyświetlanie danych z wybranej tabeli w nowym oknie."""

    def delete_selected_row():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showwarning("Brak wyboru", "Wybierz wiersz do usunięcia.")
            return
        row_id = tree.item(selected_item, "values")[0]
        delete_row_from_table(connection, table_name, row_id)
        refresh_table()

    def refresh_table():
        for item in tree.get_children():
            tree.delete(item)
        columns, rows = fetch_data_from_table(connection, table_name)
        for row in rows:
            tree.insert("", "end", values=row)

    columns, rows = fetch_data_from_table(connection, table_name)
    if columns is None or rows is None:
        return

    window = tk.Toplevel()
    window.title(f"Tabela: {table_name}")

    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True)

    for row in rows:
        tree.insert("", "end", values=row)

    delete_button = ttk.Button(window, text="Usuń zaznaczony wiersz", command=delete_selected_row)
    delete_button.pack(pady=10)

    refresh_button = ttk.Button(window, text="Odśwież", command=refresh_table)
    refresh_button.pack(pady=5)


def open_table_buttons_window(connection):
    """Otwiera okno z listą tabel i przyciskami do ich przeglądania."""
    window = tk.Toplevel()
    window.title("Wybór tabeli do przeglądania i usuwania")

    label = tk.Label(window, text="Wybierz tabelę:")
    label.pack(pady=10)

    tables = [
        "Pracownik",
        "Klient",
        "Telefony",
        "Kategoria_Produktu",
        "Produkt",
        "Cena",
        "Cena_produktu",
        "Zamowienie",
        "Pozycja_Zamowienia",
        "Platnosc",
        "Przychod",
        "Koszt",
        "Dostawa",
        "Pozycja_Dostawy",
        "Stan_produktu",
    ]

    for table in tables:
        button = ttk.Button(window, text=table, command=lambda t=table: show_table_data(connection, t))
        button.pack(fill="x", pady=5, padx=20)

def dodaj_dostawe(connection, produkty, typ_platnosci):
    """Dodaje dostawę do bazy danych"""
    try:
        cursor = connection.cursor()

        # Tworzenie typów danych Oracle
        typ_produktow = connection.gettype("TYP_PRODUKTOW")
        lista_produktow = connection.gettype("LISTA_PRODUKTOW")

        produkty_oracle = lista_produktow.newobject()
        for nazwa, ilosc in produkty:
            produkt = typ_produktow.newobject()
            produkt.NAZWA = nazwa
            produkt.ILOSC = ilosc
            produkty_oracle.append(produkt)

        cursor.callproc("DODAJ_DOSTAWE", [produkty_oracle, typ_platnosci])
        connection.commit()
        messagebox.showinfo("Sukces", "Dostawa została pomyślnie dodana.")
    except oracledb.Error as error:
        print(f"Wystąpił błąd: {error}")
        connection.rollback()
        messagebox.showerror("Błąd", f"Wystąpił błąd: {error}")
    finally:
        cursor.close()

def pobierz_produkty(connection):
    """Pobiera dostępne produkty z bazy danych."""
    query = "SELECT id, nazwa FROM Produkt"
    cursor = connection.cursor()
    cursor.execute(query)
    produkty = cursor.fetchall()
    cursor.close()
    return produkty

def otworz_okno_dostawy():
    """Otwiera nowe okno do wprowadzania dostawy."""
    def dodaj_produkt():
        selected_product_index = combobox_produkty.current()
        ilosc = entry_ilosc.get()

        if selected_product_index != -1 and ilosc.isdigit():
            produkty_lista.append((produkty_z_bazy[selected_product_index][1], int(ilosc)))
            listbox_produkty.insert(tk.END, f"{ilosc} szt. - {produkty_z_bazy[selected_product_index][1]}")
            entry_ilosc.delete(0, tk.END)
        else:
            messagebox.showwarning("Błąd", "Proszę wybrać produkt i podać prawidłową ilość.")

    def usun_produkt():
        selected_item = listbox_produkty.curselection()
        if selected_item:
            listbox_produkty.delete(selected_item)
            produkty_lista.pop(selected_item[0])

    def zatwierdz_dostawe():
        typ_platnosci = var_platnosci.get()
        if produkty_lista:
            connection = connect_to_database()
            if connection:
                dodaj_dostawe(connection, produkty_lista, typ_platnosci)
                connection.close()
                okno_dostawy.destroy()
            else:
                messagebox.showerror("Błąd", "Nie udało się połączyć z bazą danych.")
        else:
            messagebox.showwarning("Błąd", "Proszę dodać przynajmniej jeden produkt.")

    # Tworzenie okna dostawy
    okno_dostawy = tk.Toplevel(root)
    okno_dostawy.title("Dodaj Dostawę")

    produkty_lista = []

    # Pobieranie produktów z bazy
    connection = connect_to_database()
    produkty_z_bazy = []
    if connection:
        produkty_z_bazy = pobierz_produkty(connection)
        connection.close()

    # Sekcja wyboru produktów
    frame_produkty = tk.Frame(okno_dostawy)
    frame_produkty.pack(pady=10)

    tk.Label(frame_produkty, text="Wybierz produkt:").grid(row=0, column=0)
    produkty_nazwa = [produkt[1] for produkt in produkty_z_bazy]
    combobox_produkty = ttk.Combobox(frame_produkty, values=produkty_nazwa)
    combobox_produkty.grid(row=0, column=1)

    tk.Label(frame_produkty, text="Ilość:").grid(row=1, column=0)
    entry_ilosc = tk.Entry(frame_produkty)
    entry_ilosc.grid(row=1, column=1)

    btn_dodaj_produkt = tk.Button(frame_produkty, text="Dodaj produkt", command=dodaj_produkt)
    btn_dodaj_produkt.grid(row=2, columnspan=2, pady=5)

    # Lista dodanych produktów
    listbox_produkty = tk.Listbox(okno_dostawy, height=8, width=50)
    listbox_produkty.pack(pady=10)

    btn_usun_produkt = tk.Button(okno_dostawy, text="Usuń wybrany produkt", command=usun_produkt)
    btn_usun_produkt.pack(pady=5)

    # Wybór typu płatności
    frame_platnosci = tk.Frame(okno_dostawy)
    frame_platnosci.pack(pady=10)

    tk.Label(frame_platnosci, text="Typ płatności:").grid(row=0, column=0)

    var_platnosci = tk.StringVar(value="online")
    rb_online = tk.Radiobutton(frame_platnosci, text="Online", variable=var_platnosci, value="online")
    rb_online.grid(row=0, column=1)
    rb_gotowka = tk.Radiobutton(frame_platnosci, text="Gotówka", variable=var_platnosci, value="gotowka")
    rb_gotowka.grid(row=0, column=2)

    # Przycisk do zatwierdzenia dostawy
    btn_zatwierdz = tk.Button(okno_dostawy, text="Zatwierdź dostawę", command=zatwierdz_dostawe)
    btn_zatwierdz.pack(pady=20)

# Główne okno aplikacji
root = tk.Tk()
root.title("Zarządzanie Produktem i Dostawą")
root.geometry("1000x1000")  # Zwiększenie rozmiaru okna


# Etykieta i pole tekstowe do wprowadzenia nazwy kategorii
label_kategoria = Label(root, text="Podaj nazwę kategorii:")
label_kategoria.pack(pady=10)

entry_kategoria = Entry(root, width=30)
entry_kategoria.pack(pady=5)

# Przycisk do dodania kategorii
button_dodaj = Button(root, text="Dodaj Kategorię", command=on_add_category)
button_dodaj.pack(pady=20)


# Frame dla formularza dodawania produktu
frame_add_product = tk.Frame(root)

tk.Label(frame_add_product, text="Podaj nazwę produktu:").pack(pady=10)
entry_nazwa = tk.Entry(frame_add_product, width=30)
entry_nazwa.pack(pady=5)

tk.Label(frame_add_product, text="Podaj cenę nabycia:").pack(pady=10)
entry_cena_nabycia = tk.Entry(frame_add_product, width=30)
entry_cena_nabycia.pack(pady=5)

tk.Label(frame_add_product, text="Podaj cenę sprzedaży:").pack(pady=10)
entry_cena_sprzedazy = tk.Entry(frame_add_product, width=30)
entry_cena_sprzedazy.pack(pady=5)

tk.Label(frame_add_product, text="Wybierz kategorię:").pack(pady=10)
combo_kategoria = ttk.Combobox(frame_add_product, values=[f"{i[0]} - {i[1]}" for i in get_kategorie()])
combo_kategoria.pack(pady=5)

tk.Button(frame_add_product, text="Dodaj Produkt", command=on_add_new_product).pack(pady=20)







# Buttony do przełączania formularzy
# Przycisk do otwierania okna dodawania produktu
add_product_button = tk.Button(root, text="Dodaj Produkt", command=open_add_product_window)
add_product_button.pack(pady=20)


btn_dodaj_dostawe = tk.Button(root, text="Dodaj Dostawę", command=otworz_okno_dostawy)
btn_dodaj_dostawe.pack(pady=20)



# Button do otwierania okna przenoszenia produktów
tk.Button(root, text="Przenieś Produkt", command=open_move_product_window).pack(pady=10)




tk.Button(root, text="Dodaj Pracownika", command=open_add_employee_window).pack(pady=20)
tk.Button(root, text="Dodaj Klienta", command=open_add_customer_window).pack(pady=20)

# Przycisk do otwierania okna dodawania zamówienia
btn_dodaj_zamowienie = tk.Button(root, text="Dodaj zamówienie", command=otworz_okno_zamowienia)
btn_dodaj_zamowienie.pack(pady=20)

# Ukrywanie formularzy na głównej stronie
frame_add_product.pack_forget()
# frame_add_delivery.pack_forget()

# Tworzenie ramki dla widżetów
frame_main = tk.Frame(root, padx=20, pady=20)
frame_main.pack()

tk.Label(frame_main, text="Przeglądanie i usuwanie danych z bazy").pack(pady=10)

connection = connect_to_database()
button_przegladanie = tk.Button(
    frame_main,
    text="Otwórz przeglądanie i usuwanie",
    command=lambda: open_table_buttons_window(connection),
    width=30
)
button_przegladanie.pack(pady=5)

# Uruchomienie aplikacji
root.mainloop()
