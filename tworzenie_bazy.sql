--pracownik nie jest w żadne sposób połączony z inna tabelą 

CREATE TABLE Pracownik (
    id NUMBER PRIMARY KEY,
    imie VARCHAR2(50),
    nazwisko VARCHAR2(50),
    id_przelozonego NUMBER, -- Związek unarny
    FOREIGN KEY (id_przelozonego) REFERENCES Pracownik(id)
);



-- Tabela Klient
CREATE TABLE Klient (
    id NUMBER PRIMARY KEY,
    imie VARCHAR2(50),
    nazwisko VARCHAR2(50),
    adres VARCHAR2(255),
    email VARCHAR2(100) UNIQUE
);

-- Atrybut wielowartościowy: Telefony (dla klientów)
CREATE TABLE Telefony (
    id_klienta NUMBER,
    numer_telefonu VARCHAR2(15),
    PRIMARY KEY (id_klienta, numer_telefonu),
    FOREIGN KEY (id_klienta) REFERENCES Klient(id)
);



-- Tabela Kategoria_Produktu
CREATE TABLE Kategoria_Produktu (
    id NUMBER PRIMARY KEY,
    nazwa_kategorii VARCHAR2(50)
);





-- Tabela Produkt
CREATE TABLE Produkt (
    id NUMBER PRIMARY KEY,
    nazwa VARCHAR2(100),
    id_kategorii NUMBER NOT NULL, 
    FOREIGN KEY (id_kategorii) REFERENCES Kategoria_Produktu(id)
   
);

CREATE TABLE Cena (
    id NUMBER PRIMARY KEY,
    cena NUMBER(10,2),
    CONSTRAINT cena_check CHECK (cena > 0)
);


CREATE TABLE Cena_produktu (
    id NUMBER PRIMARY KEY,
    cena_nabycia_id NUMBER, -- wprowadzane z dostawy (cena po ktorej kupujemy do magazynu)
    cena_sprzedazy_id NUMBER, -- wprowadzane przez sklep - po ile my sprzedajemy
    produkt_id NUMBER,
    od TIMESTAMP DEFAULT SYSTIMESTAMP,
    do TIMESTAMP DEFAULT TO_DATE('9999-01-01', 'YYYY-MM-DD'),
    FOREIGN KEY (produkt_id) REFERENCES Produkt(id),
    FOREIGN KEY (cena_nabycia_id) REFERENCES Cena(id), -- Relacja do tabeli Cena
    FOREIGN KEY (cena_sprzedazy_id) REFERENCES Cena(id), -- Relacja do tabeli Cena
    CONSTRAINT cena_un UNIQUE(cena_nabycia_id, cena_sprzedazy_id, produkt_id, od)
);



-- Tabela Zamowienie
CREATE TABLE Zamowienie (
    id NUMBER PRIMARY KEY,
    id_klienta NUMBER,
  	id_pracownik NUMBER,
    data_zamowienia DATE,
    FOREIGN KEY (id_klienta) REFERENCES Klient(id),
    FOREIGN KEY (id_pracownik) REFERENCES Pracownik(id)
);

-- Tabela Pozycja_Zamowienia (pozycje w zamówieniach)
CREATE TABLE Pozycja_Zamowienia (
    id NUMBER PRIMARY KEY,
    id_zamowienia NUMBER,
    id_produktu NUMBER,
    ilosc NUMBER,
    FOREIGN KEY (id_zamowienia) REFERENCES Zamowienie(id),
    FOREIGN KEY (id_produktu) REFERENCES Produkt(id),
    UNIQUE (id_zamowienia, id_produktu), --w celu uniknięcia duplikowania produktów na paragonie 
    CONSTRAINT ilosc_chec CHECK (ilosc > 0)
);


-- Tabela Platnosc
CREATE TABLE Platnosc (
    id NUMBER PRIMARY KEY,
    typ_platnosci VARCHAR2(50), --(przychod / koszt ) 
    on_off_line VARCHAR2(50),
    kwota NUMBER(10, 2),
    data DATE DEFAULT SYSTIMESTAMP,
    CONSTRAINT kwota_check CHECK (kwota > 0),
    CONSTRAINT typ_platnosci_check CHECK (typ_platnosci in ('przychod', 'koszt')),
    CONSTRAINT line_check CHECK (on_off_line in ('gotowka', 'online'))
);



-- klient kupuje u nas
-- Tabela Przychod
CREATE TABLE Przychod (
    id_platnosci NUMBER PRIMARY KEY,
    id_zamowienia NUMBER,
    FOREIGN KEY (id_zamowienia) REFERENCES Zamowienie(id),
    FOREIGN KEY (id_platnosci) REFERENCES Platnosc(id)
);


-- Tabela koszt
CREATE TABLE Koszt (
    id_platnosci NUMBER PRIMARY KEY,
    id_dostawy NUMBER,
    --typ_platnosci VARCHAR2(50) DEFAULT 'koszt',
    --kwota NUMBER(10, 2),
    --data DATE - default data dost?,
    FOREIGN KEY (id_dostawy) REFERENCES Dostawa(id),
    FOREIGN KEY (id_platnosci) REFERENCES Platnosc(id)
    --CONSTRAINT kwota_check CHECK (kwota > 0)
);




-- Tabela Dostawa
CREATE TABLE Dostawa (
    id NUMBER PRIMARY KEY,
    data_dostawy DATE
);

-- Tabela Pozycja_Dostawy (pozycje w zamówieniach)
CREATE TABLE Pozycja_Dostawy (
    id NUMBER PRIMARY KEY,
    id_dostawy NUMBER,
    id_produktu NUMBER,
    ilosc NUMBER,
    FOREIGN KEY (id_dostawy) REFERENCES Dostawa(id),
    FOREIGN KEY (id_produktu) REFERENCES Produkt(id),
    UNIQUE (id_dostawy, id_produktu), --w celu uniknięcia duplikowania produktów na paragonie 
    CONSTRAINT dostawy_chec CHECK (ilosc > 0));
    
   

CREATE TABLE Stan_produktu(
    id NUMBER PRIMARY KEY,
    id_produktu NUMBER,
	ilosc_magazyn NUMBER,
	ilosc_sklep NUMBER,
    FOREIGN KEY (id_produktu) REFERENCES Produkt(id),
    CONSTRAINT il_check CHECK (ilosc_magazyn >= 0),	
    CONSTRAINT msc_check CHECK (ilosc_sklep >= 0)
);



   
   
-- Tworzenie sekwencji dla tabel
CREATE SEQUENCE Pracownik_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Klient_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Kategoria_Produktu_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Produkt_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Cena_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Cena_produktu_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Zamowienie_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Pozycja_Zamowienia_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Platnosc_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Dostawa_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Pozycja_Dostawy_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE Stan_produktu_seq START WITH 1 INCREMENT BY 1;


-- Tworzenie triggerów dla automatycznego przypisywania PK
CREATE OR REPLACE TRIGGER Pracownik_bi
BEFORE INSERT ON Pracownik
FOR EACH ROW
BEGIN
  SELECT Pracownik_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Klient_bi
BEFORE INSERT ON Klient
FOR EACH ROW
BEGIN
  SELECT Klient_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Kategoria_Produktu_bi
BEFORE INSERT ON Kategoria_Produktu
FOR EACH ROW
BEGIN
  SELECT Kategoria_Produktu_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Produkt_bi
BEFORE INSERT ON Produkt
FOR EACH ROW
BEGIN
  SELECT Produkt_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Cena_bi
BEFORE INSERT ON Cena
FOR EACH ROW
BEGIN
  SELECT Cena_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Cena_produktu_bi
BEFORE INSERT ON Cena_produktu
FOR EACH ROW
BEGIN
  SELECT Cena_produktu_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Zamowienie_bi
BEFORE INSERT ON Zamowienie
FOR EACH ROW
BEGIN
  SELECT Zamowienie_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Pozycja_Zamowienia_bi
BEFORE INSERT ON Pozycja_Zamowienia
FOR EACH ROW
BEGIN
  SELECT Pozycja_Zamowienia_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Platnosc_bi
BEFORE INSERT ON Platnosc
FOR EACH ROW
BEGIN
  SELECT Platnosc_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Dostawa_bi
BEFORE INSERT ON Dostawa
FOR EACH ROW
BEGIN
  SELECT Dostawa_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

CREATE OR REPLACE TRIGGER Pozycja_Dostawy_bi
BEFORE INSERT ON Pozycja_Dostawy
FOR EACH ROW
BEGIN
  SELECT Pozycja_Dostawy_seq.NEXTVAL INTO :new.id FROM dual;
END;
/


-- Trigger dla Stan_produktu
CREATE OR REPLACE TRIGGER Stan_produktu_bi
BEFORE INSERT ON Stan_produktu
FOR EACH ROW
BEGIN
  SELECT Stan_produktu_seq.NEXTVAL INTO :new.id FROM dual;
END;
/

