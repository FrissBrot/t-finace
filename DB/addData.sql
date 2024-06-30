INSERT INTO public.bank(
	name, swift, "shortName") VALUES 
    ('Swiss Bankers Prepaid Services AG', 'SWBTCH21', 'SBPS'),
    ('Bank Cler AG', 'BCLRCHBB', 'Cler'),
    ('Obwaldner Kantonalbank', 'OBWKCH22', 'OKB');

INSERT INTO public.currency(
	name, country, "isoCode") VALUES 
    ('Schweizer Franken', 'Schweiz', 'CHF');

INSERT INTO public."transactionType"(
    name) VALUES 
    ('Startbetrag'),
    ('Ausleihe'),
    ('Kredit'),
    ('Einahme'),
    ('Ausgabe');

INSERT INTO public."transactionCategory"(
    fk_user, name, archived) VALUES 
    (1, 'Technik', false);

INSERT INTO public."bankAccount"(
	fk_user, fk_bank, fk_currency, name, "IBAN", balance)
	VALUES(1, 1, 1, 'Lohnkonto', 'CHXXXXXXX', 500);

INSERT INTO public.transaction(
	fk_user, fk_type, fk_category, "fk_bankAccount", fk_currency, date, amount, description)
	VALUES (1, 5, 1, 1, 1, '2024-06-29', 5, 'Testzahlung');
