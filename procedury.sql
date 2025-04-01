
CREATE OR REPLACE PROCEDURE dodaj_kategorie(
	p_kategoria IN VARCHAR2)
--tu parametr musi liste produktów przekazać, ilosc do zamowienia, sposob platnosci
AS
	v_kategoria_istnieje NUMBER;
BEGIN
   	
	-- SPRAWDZENIE CZY CENA ISTNIEJE
	SELECT COUNT(*)
	INTO v_kategoria_istnieje
	FROM Kategoria_Produktu
	WHERE nazwa_kategorii = p_kategoria;

	
	IF v_kategoria_istnieje = 0 THEN
		INSERT INTO Kategoria_Produktu(nazwa_kategorii)
		VALUES (p_kategoria);
		DBMS_OUTPUT.PUT_LINE('Kategoria została dodana.');
	ELSE 
		 DBMS_OUTPUT.PUT_LINE('Ta kategoria jest już w bazie');
	END IF;
	 
  	COMMIT;

EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Blad: ' || SQLERRM);
    ROLLBACK;
END dodaj_kategorie;
/
 
CALL dodaj_kategorie('Nabial');



CREATE OR REPLACE PROCEDURE zmien_cene_sprzedazy (
	p_id_produktu IN NUMBER,
	p_nowa_cena IN NUMBER
	)
AS
	v_date_of_change TIMESTAMP := SYSTIMESTAMP;	
	v_cena_istnieje NUMBER;
	v_cena_id NUMBER;
	v_cena_aktualna NUMBER;
	v_cena_niezmienna NUMBER;

BEGIN

	--JEŻELI CENA KTORA CHCEMY DODAC JESZCZENIE ISTNIEJE DODAJEMY JA
	SELECT COUNT(*)
	INTO v_cena_istnieje
	FROM Cena
	WHERE cena = p_nowa_cena;
	
	IF v_cena_istnieje = 0 THEN
	
		INSERT INTO Cena(cena)
		VALUES (p_nowa_cena)
		RETURNING id INTO v_cena_id;
	
		DBMS_OUTPUT.PUT_LINE('Cena została dodana.');
	
	ELSE 
	
		SELECT id
		INTO v_cena_id
		FROM Cena
		WHERE cena = p_nowa_cena;
	
		DBMS_OUTPUT.PUT_LINE('Ta cena jest już w bazie');
	
	END IF;
    	

	-- sprawdzam czy faktycznie cena inna niz juz mamy
	SELECT COUNT(*)
	INTO v_cena_aktualna
	FROM Cena_produktu cp
	WHERE cp.produkt_id = p_id_produktu
			AND cp.cena_sprzedazy_id = v_cena_id
			AND v_date_of_change BETWEEN cp.od AND cp.do;
		

	--JEST AKTUALNA
	IF v_cena_aktualna > 0 THEN
		
		DBMS_OUTPUT.PUT_LINE('Ta cena jest aktuana.');

	ELSE 
		
		UPDATE Cena_produktu cp
		SET cp.do = v_date_of_change
		WHERE cp.produkt_id = p_id_produktu --ZAKTUALIZJ NAJNOWSZY RZAD
			AND cp.od = (SELECT MAX(c.od) 
							FROM Cena_produktu c
							WHERE c.produkt_id = p_id_produktu)
		RETURNING cp.cena_nabycia_id INTO v_cena_niezmienna;
		
	
		INSERT INTO Cena_produktu(
		    cena_nabycia_id, 
		    cena_sprzedazy_id, 
		    produkt_id,
		    od)
		VALUES (v_cena_niezmienna, v_cena_id, p_id_produktu, v_date_of_change);
	
		DBMS_OUTPUT.PUT_LINE('Cena została zmieniona');
	
	END IF;

	COMMIT;
  
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Blad: ' || SQLERRM);
    ROLLBACK;
END zmien_cene_sprzedazy;
/


BEGIN
	zmien_cene_sprzedazy(1, 2);
END;


CREATE OR REPLACE PROCEDURE zmien_cene_nabycia (
	p_id_produktu IN NUMBER,
	p_nowa_cena IN NUMBER
	)
AS
	v_date_of_change TIMESTAMP := SYSTIMESTAMP;	
	v_cena_istnieje NUMBER;
	v_cena_id NUMBER;
	v_cena_aktualna NUMBER;
	v_cena_niezmienna NUMBER;

BEGIN

	--JEŻELI CENA KTORA CHCEMY DODAC JESZCZENIE ISTNIEJE DODAJEMY JA
	SELECT COUNT(*)
	INTO v_cena_istnieje
	FROM Cena
	WHERE cena = p_nowa_cena;
	
	IF v_cena_istnieje = 0 THEN
	
		INSERT INTO Cena(cena)
		VALUES (p_nowa_cena)
		RETURNING id INTO v_cena_id;
	
		DBMS_OUTPUT.PUT_LINE('Cena została dodana.');
	
	ELSE 
	
		SELECT id
		INTO v_cena_id
		FROM Cena
		WHERE cena = p_nowa_cena;
	
		DBMS_OUTPUT.PUT_LINE('Ta cena jest już w bazie');
	
	END IF;
    	

	-- sprawdzam czy faktycznie cena inna niz juz mamy
	SELECT COUNT(*)
	INTO v_cena_aktualna
	FROM Cena_produktu cp
	WHERE cp.produkt_id = p_id_produktu
			AND cp.cena_nabycia_id = v_cena_id
			AND v_date_of_change BETWEEN cp.od AND cp.do;
		

	--JEST AKTUALNA
	IF v_cena_aktualna > 0 THEN
		
		DBMS_OUTPUT.PUT_LINE('Ta cena jest aktuana.');

	ELSE 
		
		UPDATE Cena_produktu cp
		SET cp.do = v_date_of_change
		WHERE cp.produkt_id = p_id_produktu --ZAKTUALIZJ NAJNOWSZY RZAD
			AND cp.od = (SELECT MAX(c.od) 
							FROM Cena_produktu c
							WHERE c.produkt_id = p_id_produktu)
		RETURNING cp.cena_sprzedazy_id INTO v_cena_niezmienna;
		
	
		INSERT INTO Cena_produktu(
		    cena_nabycia_id, 
		    cena_sprzedazy_id, 
		    produkt_id,
		    od)
		VALUES (v_cena_id, v_cena_niezmienna, p_id_produktu, v_date_of_change);
	
		DBMS_OUTPUT.PUT_LINE('Cena została zmieniona');
	
	END IF;

	COMMIT;
  
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Blad: ' || SQLERRM);
    ROLLBACK;
END zmien_cene_nabycia;
/



BEGIN
	zmien_cene_nabycia(1, 2);
END;


  
CREATE OR REPLACE PROCEDURE dodaj_produkt(
	p_cena_nabycia IN NUMBER,
	p_cena_sprzedazy IN NUMBER,
	p_nazwa IN VARCHAR2, 
	p_id_kategorii IN NUMBER
	)
AS
	v_produkt_istnieje NUMBER;
	v_id_produktu NUMBER;
	v_cena_n_istnieje NUMBER;
	v_cena_s_istnieje NUMBER;
	v_cena_n_id NUMBER;
	v_cena_s_id NUMBER;
BEGIN
   	
	-- SPRAWDZENIE CZY CENA ISTNIEJE
	SELECT COUNT(*)
	INTO v_produkt_istnieje
	FROM Produkt
	WHERE
		LOWER(REGEXP_REPLACE(nazwa, '[^a-zA-Z0-9]', ''))
		=
		LOWER(REGEXP_REPLACE(p_nazwa, '[^a-zA-Z0-9]', ''));
	
	IF v_produkt_istnieje <> 0 THEN
	
		DBMS_OUTPUT.PUT_LINE('Ten produkt jest już w bazie');
	ELSE
	
		SELECT COUNT(*)
		INTO v_cena_n_istnieje
		FROM Cena
		WHERE cena = p_cena_nabycia;
	
		SELECT COUNT(*)
		INTO v_cena_s_istnieje
		FROM Cena
		WHERE cena = p_cena_sprzedazy;
		
		IF v_cena_n_istnieje = 0 THEN
		
			INSERT INTO Cena(cena)
			VALUES (p_cena_nabycia)
			RETURNING id INTO v_cena_n_id;
		
			DBMS_OUTPUT.PUT_LINE('Cena została dodana.');
		
		ELSE 
		
			SELECT id
			INTO v_cena_n_id
			FROM Cena
			WHERE cena = p_cena_nabycia;
		
			DBMS_OUTPUT.PUT_LINE('Ta cena jest już w bazie');
		
		END IF;

	
		IF v_cena_s_istnieje = 0 THEN
		
			INSERT INTO Cena(cena)
			VALUES (p_cena_sprzedazy)
			RETURNING id INTO v_cena_s_id;
		
			DBMS_OUTPUT.PUT_LINE('Cena została dodana.');
		
		ELSE 
			
			SELECT id
			INTO v_cena_s_id
			FROM Cena
			WHERE cena = p_cena_sprzedazy;
			
			DBMS_OUTPUT.PUT_LINE('Ta cena jest już w bazie');
			
		END IF;
			
		INSERT INTO Produkt(nazwa, id_kategorii)
		VALUES(LOWER(p_nazwa), p_id_kategorii)
		RETURNING id INTO v_id_produktu;
		
		INSERT INTO Cena_produktu (
			cena_nabycia_id, 
			cena_sprzedazy_id, 
			produkt_id
			)
		VALUES(
			v_cena_n_id,
			v_cena_s_id,
			v_id_produktu); 
		DBMS_OUTPUT.PUT_LINE('Dodano produkt:' || p_nazwa);

			
	END IF;
	COMMIT;


EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Blad: ' || SQLERRM);
    ROLLBACK;
END dodaj_produkt;



BEGIN
    dodaj_produkt(100.50, 13, 'Danio', 1);
END;


--!!!!!
CREATE OR REPLACE TYPE typ_produktow AS OBJECT (
  nazwa VARCHAR2(100),
  ilosc NUMBER
);
/

CREATE OR REPLACE TYPE lista_produktow AS TABLE OF typ_produktow;
/



CREATE OR REPLACE PROCEDURE dodaj_dostawe(
  p_produkt_lista IN lista_produktow,
  p_on_off IN VARCHAR2) 
--tu parametr musi liste produktów przekazać, ilosc do zamowienia, sposob platnosci
AS
	v_na_magazynie_istnieje NUMBER;
 	v_id_dostawy NUMBER;
 	v_id_platnosci NUMBER;
	v_kwota NUMBER;
	v_czas_dostawy TIMESTAMP := SYSTIMESTAMP;
	

BEGIN
	-- koszt zamowienia
	--tutaj dodałam *z.ilosc zeby sie kasa mnozyła
	SELECT SUM(c.cena * z.ilosc)
	INTO v_kwota
	FROM TABLE(p_produkt_lista) z
		LEFT JOIN Produkt p
			ON 	LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
				=
				LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
		LEFT JOIN Cena_produktu cp
			ON cp.produkt_id = p.id
		LEFT JOIN Cena c
			ON cp.cena_nabycia_id = c.id
		WHERE cp.od = (SELECT MAX(pc.od) 
                FROM Cena_produktu pc
                WHERE pc.produkt_id = cp.produkt_id)
			;
		
	--musi wejsc do dostawy - 
		-- dodaj dostawe
	INSERT INTO Dostawa (data_dostawy)
	VALUES (v_czas_dostawy)
	RETURNING id INTO v_id_dostawy;

	--dodaj pozycje dostawy
	INSERT INTO Pozycja_Dostawy (id_dostawy, id_produktu, ilosc)
	SELECT v_id_dostawy, p.id, z.ilosc
	FROM TABLE(p_produkt_lista) z
	LEFT JOIN Produkt p ON LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
							=
							LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''));

	--musi wejsc do kosztu:			
	INSERT INTO Platnosc (
		typ_platnosci,
		on_off_line,
		kwota,
		"DATA")
	VALUES (
		'koszt',
		p_on_off,
		v_kwota,
		v_czas_dostawy
		)
	RETURNING id INTO v_id_platnosci;

	INSERT INTO Koszt (id_platnosci, id_dostawy)
	VALUES(v_id_platnosci, v_id_dostawy);
		
	-- UPDATE TYLKO PRODUKTÓW KTÓRE JUZ BYLY NA MAGAZYNIE
 
		MERGE INTO Stan_produktu sp
		USING (
		    SELECT 
		        z.ilosc AS ilosc_do_dodania,
		        p.id AS id_produktu
		    FROM TABLE(p_produkt_lista) z
		    LEFT JOIN Produkt p ON 	LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
									=
									LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
		) dane
		ON (sp.id_produktu = dane.id_produktu)
		WHEN MATCHED THEN
		    UPDATE SET sp.ilosc_magazyn = sp.ilosc_magazyn + dane.ilosc_do_dodania;


	INSERT INTO Stan_produktu (
		id_produktu,
		ilosc_magazyn,
		ilosc_sklep
	)
	SELECT 
		p.id,
		z.ilosc,
		0 -- zerowy stan w sklepie skoro nigdy wczesniej GO nie bylo
	FROM TABLE(p_produkt_lista) z 
	LEFT JOIN Produkt p
		ON 	LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
			=
			LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
	LEFT JOIN Stan_produktu sp
		ON sp.id_produktu = p.id
	WHERE sp.id IS NULL; 
	
	

  COMMIT;


  DBMS_OUTPUT.PUT_LINE('Dostawa została dodana.');
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Błąd: ' || SQLERRM);
   	ROLLBACK;

END dodaj_dostawe;


BEGIN
	dodaj_dostawe()
END;


CREATE OR REPLACE PROCEDURE dodaj_zamowienie(
  p_produkt_lista IN lista_produktow,
  p_on_off IN VARCHAR2,
  p_id_klienta IN NUMBER, 
  p_id_pracownik IN NUMBER) 
--tu parametr musi liste produktów przekazać, ilosc do zamowienia, sposob platnosci
AS
	v_czy_jest NUMBER;
	v_czy_w_sklepie NUMBER;
 	v_id_zamowienia NUMBER;
 	v_id_platnosci NUMBER;
	v_kwota NUMBER;
	v_czas_zamowienia TIMESTAMP := SYSTIMESTAMP;

BEGIN
	
		-- koszt zamowienia
	--dodałam ilosc
		SELECT SUM(c.cena * z.ilosc)
		INTO v_kwota
		FROM TABLE(p_produkt_lista) z
		LEFT JOIN Produkt p
			ON LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
				=
				LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
		LEFT JOIN Cena_produktu cp
			ON cp.produkt_id = p.id
		LEFT JOIN Cena c
			ON cp.cena_sprzedazy_id = c.id
		WHERE cp.od = (SELECT MAX(pc.od) 
                FROM Cena_produktu pc
                WHERE pc.produkt_id = cp.produkt_id)
			;
		
			
		--		 jeżeli klient zamowil wiecej ktoregokolwiek produktu niz posiada sklep CALE- 
		--		 zamowienie nie zostanie zrealizowane
		--		z.ilosc
		--		
		SELECT 
			MIN(sp.ilosc_magazyn + sp.ilosc_sklep - z.ilosc)
		INTO v_czy_jest
		FROM TABLE(p_produkt_lista) z 
		LEFT JOIN Produkt p
			ON LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
				=
				LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
		LEFT JOIN Stan_produktu sp
			ON sp.id_produktu = p.id
		; 
		

		IF v_czy_jest < 0 THEN
			ROLLBACK; --TUTAJ NIE WIEM CZY ROLLBACK KONIECZNE -> ZEBY BYLO ZAPISANE W SENSIE Z REKI BO ERROR MOZE SAM ZOBIC ROLLBACK
			RAISE_APPLICATION_ERROR(-20001, 'Brak wystarczającej ilości produktów');
		ELSE 
				
			--musi wejsc do za mowienia - 
				-- dodaj zamowienie
			INSERT INTO Zamowienie (
				id_klienta,
				id_pracownik,
				data_zamowienia)
			VALUES (p_id_klienta, p_id_pracownik, v_czas_zamowienia)
			RETURNING id INTO v_id_zamowienia;
		
			--dodaj pozycje zamowienia
			INSERT INTO Pozycja_Zamowienia(
				id_zamowienia, 
				id_produktu, 
				ilosc)
			SELECT 
				v_id_zamowienia ,
				p.id , 
				z.ilosc 
			FROM TABLE(p_produkt_lista) z
				LEFT JOIN Produkt p 
					ON 	LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
						=
						LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
				;
	
		
			INSERT INTO Platnosc (
				typ_platnosci,
				on_off_line,
				kwota,
				"DATA")
			VALUES (
				'przychod',
				p_on_off,
				v_kwota,
				v_czas_zamowienia
				)
			RETURNING id INTO v_id_platnosci;
		
			INSERT INTO Przychod (id_platnosci, id_zamowienia)
			VALUES(v_id_platnosci, v_id_zamowienia);

	
			MERGE INTO Stan_produktu sp
			USING (
			    SELECT 
			        p.id AS id_produktu,
			        CASE 
			            WHEN (sp.ilosc_sklep - z.ilosc) < 0 THEN 
			                sp.ilosc_magazyn + sp.ilosc_sklep - z.ilosc
			            ELSE 
			                sp.ilosc_magazyn
			        END AS nowa_ilosc_magazyn,
			        CASE 
			            WHEN (sp.ilosc_sklep - z.ilosc) >= 0 THEN 
			                sp.ilosc_sklep - z.ilosc
			            ELSE 
			                0
			        END AS nowa_ilosc_sklep
			    FROM TABLE(p_produkt_lista) z 
			    LEFT JOIN Produkt p
			       ON 	LOWER(REGEXP_REPLACE(z.nazwa, '[^a-zA-Z0-9]', ''))
						=
						LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
			    LEFT JOIN Stan_produktu sp
			        ON sp.id_produktu = p.id
			) dane
			ON (sp.id_produktu = dane.id_produktu)
			WHEN MATCHED THEN
			    UPDATE SET 
			        sp.ilosc_magazyn = dane.nowa_ilosc_magazyn,
			        sp.ilosc_sklep = dane.nowa_ilosc_sklep;

  			COMMIT;
  			DBMS_OUTPUT.PUT_LINE('Zamówienie zostało dodane.');
  		END IF;

EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Błąd: ' || SQLERRM);
   	ROLLBACK;

END dodaj_zamowienie;


BEGIN
	dodaj_zamowienie()
END;
 
CREATE OR REPLACE PROCEDURE przenies_produkt(
    p_nazwa_produktu IN VARCHAR2,
    p_ilosc_przeniesienia IN NUMBER
) AS
    v_id_produktu NUMBER ;
    v_ilosc_magazyn NUMBER ;
    v_ilosc_sklep NUMBER;
BEGIN
    -- Pobranie danych o produkcie
    SELECT sp.id_produktu, sp.ilosc_magazyn, sp.ilosc_sklep
    INTO v_id_produktu, v_ilosc_magazyn, v_ilosc_sklep
    FROM Produkt p
    JOIN Stan_produktu sp ON sp.id_produktu = p.id
    WHERE 	LOWER(REGEXP_REPLACE(p.nazwa, '[^a-zA-Z0-9]', ''))
			=
			LOWER(REGEXP_REPLACE(p_nazwa_produktu, '[^a-zA-Z0-9]', ''));
   

    -- Sprawdzenie dostępności w magazynie
    IF v_ilosc_magazyn < p_ilosc_przeniesienia THEN
        RAISE_APPLICATION_ERROR(-20001, 'Niewystarczająca ilość w magazynie do przeniesienia');
    END IF;

    -- Aktualizacja stanów magazynu i sklepu
    UPDATE Stan_produktu
    SET ilosc_magazyn = ilosc_magazyn - p_ilosc_przeniesienia,
        ilosc_sklep = ilosc_sklep + p_ilosc_przeniesienia
    WHERE id_produktu = v_id_produktu;

    -- Zatwierdzenie transakcji
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Przeniesiono ' || p_ilosc_przeniesienia || ' sztuk produktu "' || p_nazwa_produktu || '" z magazynu do sklepu.');

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20002, 'Produkt o nazwie "' || p_nazwa_produktu || '" nie istnieje.');
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END przenies_produkt;


CREATE OR REPLACE PROCEDURE dodaj_pracownika(
    p_imie IN VARCHAR2,
    p_nazwisko IN VARCHAR2,
    p_id_przelozonego IN NUMBER DEFAULT NULL
		) 
AS
    v_id_przelozonego_exists NUMBER;
BEGIN
    -- Sprawdzenie, czy podany przełożony istnieje
    IF p_id_przelozonego IS NOT NULL THEN
        SELECT COUNT(*)
        INTO v_id_przelozonego_exists
        FROM Pracownik
        WHERE id = p_id_przelozonego;

        IF v_id_przelozonego_exists = 0 THEN
            RAISE_APPLICATION_ERROR(-20001, 'Przełożony o podanym ID nie istnieje.');
        END IF;
    END IF;

    -- Wstawienie nowego pracownika
    INSERT INTO Pracownik (imie, nazwisko, id_przelozonego)
    VALUES (
        p_imie,
        p_nazwisko,
        p_id_przelozonego
    	);

    -- Zatwierdzenie transakcji
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Dodano nowego pracownika: ' || p_imie || ' ' || p_nazwisko);
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Błąd: ' || SQLERRM);
   	ROLLBACK;
END dodaj_pracownika;



CREATE OR REPLACE PROCEDURE dodaj_klienta(
    p_imie IN VARCHAR2,
    p_nazwisko IN VARCHAR2,
    p_adres IN VARCHAR2,
    p_email IN VARCHAR2,
    p_telefony IN SYS.ODCIVARCHAR2LIST -- Typ kolekcji dla listy telefonów
) AS
    v_id_klienta NUMBER;
BEGIN
    -- Wstawienie klienta
    INSERT INTO Klient (imie, nazwisko, adres, email)
    VALUES (
        p_imie,
        p_nazwisko,
        p_adres,
        p_email
    )
    RETURNING id INTO v_id_klienta;

    -- Dodanie numerów telefonów (jeśli są podane)
    IF p_telefony.COUNT > 0 THEN
        FOR i IN 1 .. p_telefony.COUNT LOOP
            INSERT INTO Telefony (id_klienta, numer_telefonu)
            VALUES (v_id_klienta, p_telefony(i));
        END LOOP;
    END IF;

    -- Zatwierdzenie transakcji
    COMMIT;

    DBMS_OUTPUT.PUT_LINE('Dodano nowego klienta: ' || p_imie || ' ' || p_nazwisko);
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Błąd: ' || SQLERRM);
   	ROLLBACK;
END dodaj_klienta;
/
