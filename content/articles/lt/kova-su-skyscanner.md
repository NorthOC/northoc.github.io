# Reverse-engineerinam Skyscanner

## Kontekstas

Artėja gegužės mėnesis, o tai reiškias pirmasis šių metų pigiausių bilietų sezonas. Man smalsu nes pasiilgau kelionių (paskutinį kartą buvau išskridęs Lapkritį). Taigi, nueinu į Skyscanner svetaine, pasirenku skristi iš `Lietuvos` į `Everywhere`, spaudžiu ant laiko nu ir ką... nebėra pasirinkimo `Cheapest month`!

![Kiniečiai pašalino cheapest month?](/static/images/kova_su_skyscanner/skscanner-months.png)

Galvojau mano naršyklė grybauja, bet ne. Reddite jau senokai visi skundžiasi, kad Skyscanner pašalino šią funkciją. Kiniečių darbas, if you ask me (Skyscanner 2016-ais parduotas buvo kiniečiams). Taigi, nusprendžiau, kad jie perlenkė lazdą ir užsinorėjau sau šią funkciją susigražinti.

![ASCII Pepe](/static/images/kova_su_skyscanner/pepe-matrix.gif)

## Koks šansas, kad funkcionalumas yra tik paslėptas?

Skyscanner turi savo API, todėl jie negali keisti funkcionalumo kaip papuola, kadangi daug įmoniu naudojasi jų paslaugomis. Todėl mano pirmoji hipotezė buvo tai, jog funkcionalumas nėra išimtas, jis tik paslėptas.

Pabandžiau analizuoti URL, kai atliekama pirmoji paieška:

`https://www.skyscanner.net/transport/flights-from/lt/?qp_prevScreen=HOMEPAGE&adultsv2=1&cabinclass=economy&childrenv2=&ref=home&is_banana_refferal=true&rtn=1&preferdirects=false&outboundaltsenabled=false&inboundaltsenabled=false&oym=2304&iym=2305`

Svarbiausios dalys yra pati nuoroda `flights-from/lt` ir `oym=2304&iym=2305` parametrai. Pirmasis rodo, kad skrydžiai ieškomi pagal šalies kodą (LT, LV, DE ir tt.) jeigu paieškoje buvo suvesta šalis, o parametrai `oym` ir `iym` nustato paieškos mėnesius. Visa kita yra jovalas. Taigi, idėja tokia, jog ištrinus parametrus po `flights-from/lt`, skyscanner turėtų kažką daryti įdomaus. Ištryniau parametrus ir štai kas liko:

`https://www.skyscanner.net/transport/flights-from/lt/`

Perkroviau puslapį. Kažkodėl išliko tas pats. Keista. Pakrapščiau smegenus ir supratau, kad jie šiems duomenims atkurti naudoja mano sesiją, ir iš praeito URL išsaugojo parametrus. Taigi, pasileidau URL su incognito režimų (jis skirtas ne tik porno žiūrėjimui, jūs išdykėliai) ir voila - hipotezė pasiteisino. Vis dėl to funkcionalumas buvo tiesiog paslėptas nuo vartotojų!

![Pavyko!](/static/images/kova_su_skyscanner/sk_cheap_flights.jpg)

## Lendam gilyn

Viskas, gavau ko norėjau. Bet pala, šitie duomenys iš kažkur pareina. Lendam gilyn su F12 dev-tools'ais. Sklityje tinklas galim peržiūrėti kokie requestai vyksta puslapio krovimo metu ir pastebėti kokia informacija atkeliauja. Bet visko man ten nereikia, svarbiausia tekstiniai failai, `.json`, `.xml` arba `.txt` formatu. Dažniausiai API būna `.json` formato. Taigi, reloadinu puslapi, sugrupuoju pagal dydį ir štai rezultatas:

![Ilgas URL ir didžiausias dydžiu](/static/images/kova_su_skyscanner/sk_network.jpg)

Pats pirmas URL iškart patraukė akį, todėl atsidariau. Jackpot.

![Neturėčiau čia būti, bet public API yra public ¯\_(ツ)_/¯](/static/images/kova_su_skyscanner/sk_api1.jpg)

Paanalizavus API URL svarbiausios dalys buvo `/LT/anywhere/anytime/anytime/` ir `?apikey=8aa374f4e28e4664bf268f850f767535`. Pirmoji dalis nusako API serveriui parametrus pagal kuriuos sugeneruoti informacija, o antroji yra viešas API raktas, kuris autentifikuoja mano requestą serveriui. 

Paanalizavus API objektus susidariau tokį įspūdį:

* `Id`: yra šalies kodas
* `Direct`: nusako ar skrydis tiesioginis
* `Name`: yra šalies pavadinimas
* `IndirectPrice`: Pigiausio netiesioginio skrydžio kaina
* `DirectPrice`: Pigiausio tiesioginio skrydžio kaina
* `IndirectQuoteDateTime`: Kada paskutinį kartą atnaujinta netiesioginių skrydžių kaina
* `DirectQuoteDateTime`: Kada paskutinį kartą atnaujinta tiesioginių skrydžių kaina

Kilo idėja.

## Reverse-engineerinam API su Pitonu

Taigi, susidariau skyscanner veiksmų eigą kaip atliekama standartinė paieška, kuri atrodo taip:

1. Pasirenki iš kurios šalies skrendi
2. Pasirenki į kurią šalį skrendi
3. Pasirenki į kurią šalį skrendi oro uostą
4. Pasirenki iš kurios šalies skrendi oro uostą
5. Pasirenki skrydžio datas
6. Gauni up-to-date kainas ir laiką

Apsirašiau `class Skyscanner` ir susidėliojau veiksmų eigą vienoje funkcijoje:

![Workflow pseudokodas](/static/images/kova_su_skyscanner/sk_workflow.jpg)

### Pirmas žingsnis: šalis iš kurios skrendi

Šios funkcijos tikslas yra parinkti išskridimo vietą. Skyscanner turi tam specialų API.

`https://www.skyscanner.net/g/autosuggest-search/api/v1/search-flight/UK/en-GB/{PAIEŠKOS QUERY}?isDestination=false&enable_general_search_v2=false`

Paieškos API call vyksta kiekvieną kartą paspaudus mygtuką (aka. OnKeyPress event), jeigu paieškoje yra bent dvi raidės, o rezultatai yra sugeneruojami serveryje.

![Paieškos API gražinami duomenys](/static/images/kova_su_skyscanner/sk_search_api.jpg)

Kiek neaišku buvo kaip atskirti šalį, nuo oro uosto, bet sugalvojau labai paprastai: jeigu objekto pavadinimas (PlaceName) sutampa su šalies pavadinimu (CountryName), tai yra šalis.

Kodas neįpatingas, kadangi apskaičiavimus atlieka pats API serveris, ir gražina json objektą:

![Pasirinkus gražinamas objektas](/static/images/kova_su_skyscanner/sk_search.jpg)

### Antras žingsnis: šalis į kurią skrendi

Čia prasideda smagumas. 

Šios funkcijos tikslas yra sugeneruoti šalių, į kurias galima skristi, sąrašą, išrikiuoti jas pagal pigiausias, bei nustatyti ar skrydis yra tiesioginis ar ne. Jau prieš tai minėjau, jog skyscanner turi tam specialų API.

`https://www.skyscanner.net/g/browse-view-bff/dataservices/browse/v3/bvweb/LT/EUR/en-GB/destinations/{ŠALIES ARBA ORO UOSTO KODAS}/anywhere/anytime/anytime/?apikey=8aa374f4e28e4664bf268f850f767535`

Taigi, dabar API duomenys būtų sugeneruoti pagal bet kurią šalį iš kurios nori išskristi ir iš to galima sudaryti šalių sąrašą. 

Tačiau kai kurioms šalims skrydžių kainų nėra, todėl gautą sąrašą reikėtų perfiltruoti. Tai yra, jeigu skrydžio kaina 0, reiškias skrydis neegzistuoja. Kitu atveju reikia patikrinti ar egzistuoja tuo pačiu metu tiesioginiai ir netiesiogiai skrydžiai į šalį, ir pasirinkti pigesnį variantą. Šį filtrą sudėjau į atskirą funkciją. Tuomet išrikiavau šalis su custom funkcija pagal kainą.

Spausdinimo metu, taip pat padariau, kad rodytų ar skrydis iš šalies yra tiesioginis ar ne, kadangi tai yra nurodyta pačiame API.

![Pasirinkimai iš Lietuvos](/static/images/kova_su_skyscanner/sk_to_country.jpg)

### Trečiasis žingsnis: Oro uostas į šalį kurią skrendi

Tolimesniems veiksmams reikalingas tikslumas. Todėl, prieš tai minėtame URL, vietoje `/anywhere/`, reikia įterpti šalį. Tokiu atveju API sugeneruoja oro uostus.

![Oro uostai Švedijoje](/static/images/kova_su_skyscanner/sk_api2.jpg)

Kodas daugmaž analogiškas praeitam žingsniui. 

Galiu pasakyti tai, kad Skyscanner turi gerus API dizainerius.

![Iš Lietuvos į Švediją](/static/images/kova_su_skyscanner/sk_to_airport.jpg)

### Ketvirtas žingsnis: Oro uostas iš kurios skrendi

Jeigu pradžioje buvo pasirinkta ne šalis, o oro uostas, ši funkcija yra praleidžiama, tačiau jos tikslas yra analogiškas praeitai. Taigi, toliau keičiasi tik pats API URL į:

`https://www.skyscanner.net/g/browse-view-bff/dataservices/browse/v3/bvweb/LT/EUR/en-GB/destinations/{ŠALIES_KODO_KINTAMASIS}/{ORO_UOSTAS_Į_KURĮ_SKRENDI}/anytime/anytime/?apikey=8aa374f4e28e4664bf268f850f767535`

Tuomet API sugeneruoja oro uostus tai šaliai iš kurios iškrendi:

![Iš Lietuvos oro uostai](/static/images/kova_su_skyscanner/sk_from_airport.png)

### Penktas žingsnis: pasirenki skrydžio datas

Kalendorius, kuriame gali pasirinkti skrydžių dienas, irgi turi savo atskira API.

`https://www.skyscanner.net/g/browse-view-bff/dataservices/browse/v3/bvweb/LT/EUR/en-GB/destinations/{ORO_UOSTAS_IŠ_KURIO_SKRENDI}/{ORO_UOSTAS_Į_KURĮ_SKRENDI}/anytime/anytime/?apikey=8aa374f4e28e4664bf268f850f767535`

Atsidarius šitą URL buvo toks pirmas what the fuck moment. Atrodo mistika. 

![Nu panašu į duomenis](/static/images/kova_su_skyscanner/sk_wtf.jpg)

![Čia tai wtf](/static/images/kova_su_skyscanner/sk_wtf2.jpg)

Tie `Traces` dar panašu į duomenis, bet kur `PriceGrid` tai atrodo kosmosas. Gal tas pricegrids yra koordinatės? Vėl reikėjo prisiversti pasukti smegeninę. Ir tada atradau šitą:

![Hmm, kas čia?](/static/images/kova_su_skyscanner/sk_api3.jpg)

Direct, tai turbūt skrydis. Okey, Balandžio mėnesis turi 30 dienų, skaičiavimas prasideda nuo 0 ir baigiasi su 29 - tai yra 30 variantų. Okey, pasirinksiu skyscanner rodomam kainų kalendoriuje kažkuri diena yra 12-ta, o kita 2-a. Nu ir rimtai, pirmasis skaičius yra išvykimo diena, o antras atvykimo, ir kai tomis dienomis skrydis yra, rodoma kaina!

Dabar galiu sugeneruoti visas kainas pigiausiam skrydžių laikotarpiui į tą šalį, ir išrikiuoti juos visus pagal kainą:

![Pigiausi skrydžiai iš Kauno į Gothenburgą](/static/images/kova_su_skyscanner/sk_dates_by_price.jpg)

Čia tas pats kas rankomis kalendoriuje paspausti ant kiekvienos atvykimo/išvykimo dienos tą mėnesį ir susirašyti visus į lentelę pagal kainą.

### Šeštas žingsnis: up-to-date-kainos

Šios funkcijos tikslas yra sugeneruoti URL ir leisti peržiūrėti skrydžio bilietus pirkimo taške. Čia buvo lengviausia dalis.

![Url į pirkimo tašką](/static/images/kova_su_skyscanner/sk_url.jpg)

## Papildomas funkcionalumas: visi skrydžiai metams išrikiuoti pagal kainą

Kalendoriaus API man atrodė kaip smėlio dėžė. 

Labiau įsigilinęs supratau, jog galiu išplėsti funkcionalumą ir padaryti, kad išsitraukčiau skrydžių kainas ne tik pigiausiam mėnesiui, bet ir **ILGESNIAM LAIKOTARPIUI** (paprastai tas laikotarpis yra iki vienerių metų) į priekį, pradedant nuo dabartinio mėnesio.

Įsivaizduok dabar save einantį per visą Skyscanner kalendorių vienam skrydžiui, paspaudžiant ant kiekvienos atvykimo ir išvykimo dienos, nusirašant ranka skrydžių kainas ir po to, jas sugrupuojant pagal kainas. Neabejoju, kad tokių žmonių yra, ypač kai reikia planuotis atostogas aplink darbą, bet laiko kiekis kurį šis naujas funkcionalumas leidžia sutaupyti yra milžiniškas.

![Skenuoja metų skrydžius iš Vilniaus į Atėnus](/static/images/kova_su_skyscanner/sk_calendar_scan.jpg)

Nuotraukoje matosi kaip nuskenuojami visi šių metų rodomi skrydžiai iš Vilniaus į Atėnus. Tada skirtingi skrydžiai (kurių yra virš 800 iš Vilniaus į Atėnus) yra surikiuojami pagal kainą - belieka išsirinkti patogiausią datą. ***TAI YRA NAUJAS FUNKCIONALUMAS, KURIO PAPRASTI VARTOTOJAI NIEKADA NEMATĖ IR NEMATYS!***. Tolimesnėje nuotraukoje, matosi pirmų keturių pigiausių skrydžių skirtumas kuris yra mažiau nei 10 eurų, tačiau datos, viena nuo kitos, vienoje vietoje skiriasi net 5-iais mėnesiais.

![Keli variantai gegužę ir vienas spalį. Skirtumas iki 10 eurų](/static/images/kova_su_skyscanner/sk_year_cheapest.jpg)

Skyscanner atstovai, jeigu skaitote, galite mane jau pasisamdyti freelance darbams.

## Pabaiga ir nuoroda į projektą

Taigi, kol kas čia yra kelionės su Skyscanner API pabaiga. Jeigu kas mokate spoofint POST requestus su Python (ne vaikiškai), parašykit.

Tiems kas norit pasižaisti su kodu arba pasiplanuoti savo atostogas į ateitį efektyviausiu būdu, štai projekto linkas: [https://github.com/NorthOC/fast_scanner](https://github.com/NorthOC/fast_scanner)