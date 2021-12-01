# Distribuirani računarski sistemi u elektroenergetici

## Autori

<table>
  <tr>
    <td>Nevena Stefanović</td>
    <td>PR 77/2017</td>
  </tr>
  <tr>
    <td>Petar Stefanović</td>
    <td>PR 22/2017</td>
  </tr>
  <tr>
    <td>Nebojša Vasić</td>
    <td>PR 93/2016</td>
  </tr>
  <tr>
    <td>Đorđe Lazarević</td>
    <td>PR 147/2016</td>
  </tr>
  </table>
  
  # Zadatak
  
  Implementirati projekat koji simulira crypto menjačnicu i online crypto račun za lične uplate.
  
  Implementacija treba da sadrži 3 komponente:
  1. Korisnički interfejs (UI)
  2. Servis za obradu zahteva i podataka (Engine)
  3. Bazu podataka (DB)

## Korisnički interfejs (UI)

Korisnički interfejs je Flash web aplikacija koja treba da opsluži korisnika u interakciji sa platnim prometom.

Akcije koje treba podržati na korisničkom interfejsu:
* Registracija novog korisnika
* Logovanje postojećeg korisnika
* Izmena korisničkog profila
* Pregled stanja
* Ubacivanje sredstava putem platne kartice na online crypto račun
* Pregled istorije transakcija sa mogućnošću filtriranja i sortiranja
* Iniciranje nove transakcije drugom korisniku (koji ima otvoren online crypto račun)
* Izbor crypto valuta - sa osvežavanjem kursne liste sa interneta prema glavnoj valuti $
* Zamena valute

Korisnik se registruje unoseći:
* Ime
* Prezime
* Adresu
* Grad
* Državu
* Broj telefona
* Email
* Lozinku

Korisnik se loguje koristeći Email i Lozinku.

Novi korisnik ima stanje 0. On tada treba da zatraži verifikaciju naloga. Za verifikaciju je potrebno da unese svoju platnu karticu i biće mu skinuto $1. Nakon toga, korisnik može da uplati sredstva sa kartice na svoj online račun.


Test platna kartica:
```
Broj: 4242 4242 4242 4242
Ime: *Ime korisnika*
Datum isteka kartice: 02/23
Sigurnosni kod: 123
```

Korisnik inicira transakciju drugom korisniku unoseći njegovu email adresu, ukoliko korisnik ima registrovan nalog.
  
Kad se inicira transakcija, ona treba da se obradi na strani Engine-a. Transakcija ima stanja:
1. U obradi
2. Obrađeno
3. Odbijeno

Potrebno vreme da se transakcija majnuje (validira) je 5min. Za to vreme sistem mora da bude sposoban da odgovori na ostale zahteve. Svaka transakcija mora da ima svoj hash (ID), koji je znak da je zapisana u blockchain-u. Za hash-ovanje koristiti KECCAK256 funkciju.

U hash stringu treba da bude:
* Pošiljalac transakcije
* Primalac transakcije
* Iznos
* Random.int

Konverzija crypto valute se vrši po principu da korisnik uplaćuje sa kartice sa online racun u dolarima. Kursna lista se dovlači sa eksternog API-a kursne liste. Nakon dobijanja liste, korisnik bira valutu i iznos. Nakon uspešne konverzije korisnik ima novo stanje u novoj crypto valuti. Korisnik može da ima neograničen broj valuta i stanja računa u crypto valutama.

## Servis za obradu zahteva i podataka (Engine)

Engine je servis implementiran kao flask API aplikacija. Engine ima svoje endpointe koje prikazuje eksternom svetu (UI aplikaciji) za korišćenje. UI deo poziva endpointe Engine-a radi obrade raznih zahteva i podataka. Pri tome samo Engine komunicira sa bazom, a UI sa Engine-om.

## Baza podataka (DB)

Baza podataka je u komunikaciji sa Engine-om za svrhu skladištenja podataka o aplikaciji. U bazi se skladište svi esencijalno bitni podaci za rad aplikacije. 

Model baze kao i tip baze (NoSQL, SQL) je proizvoljan.

# Način ocenjivanja

1.	Aplikacija je funkcionalna i postoji Flask aplikacija – 51 poen
a.	Aplikacija se sastoji od 1 aplikacije bez baze koja je potpuno funkcionalna
2.	Implementiran Engine kao posebna Flask aplikacija gde UI komunicira sa Engine-om putem API-a – 10 poena
3.	Implementirana je baza sa kojom komunicira Engine – 9 poena
4.	Korišćenje niti prilikom implementacije – 10 poena
5.	Korišćenje procesa prilikom implementacije – 10 poena
6.	Dokerizacija aplikacije i pokretanje na više računara (distribuiran sistem) – 10 poena

•	Deploy aplikacije na Heroku – gratis 5 poena (moguće samo ako je svih 6 tačaka implementirano)
