# FOSS projektai ir tu

Ateina laikas kai devs'ai nusprendžia, kad reikia pradėti daryti pull request'us, prisidėti prie atviro kodo projektų ir technologijų pasaulio gerovės. Tačiau šioje fazėje žūsta daugelio jaunų programuotojų, vienas iš pirmųjų, dievybės kompleksų.

![Sveiki, atėjau prisidėti... Hmm, gal nereikia](/static/images/gallery/commit-dissapear.webp)

Kiekvienas atviro kodo projektas (jei jis rūpi) turi savo pull request'ų standartą, kuris paprastai gali būti rastas `commits.md` faile ar konkrečioje direktorijoje, ir gali būti nuo kelių, iki kelių dešimčių, puslapių ilgio.

Kai kurie projektai, ypač programavimo kalbų repositorijos (pvz. rust-lang), turi laikytis labai aukšto standarto, todėl, kad nuo jų priklauso daugumos kitų projektų veikimas. 

Taigi, pull request'ų gatekeeping'as turi savo privalumų: jis apriboja spaghetti kodą, noob programuotojų skaičių ir leidžia išgauti optimaliai veikiantį (kartais) kodą.

Tačiau, daugumai FOSS projektų, toks gatekeeping'as kenkia, ir to rezultatas yra akivaizdus: kai atsiranda nauji, sparčiai atnaujinami, projektai, pastarieji išeina kaip ir nauji atėjo - greitai. Kodėl? Nes laikas yra brangus.

## Meistras suklydo tūkstantį kartų

Projekto ir technologijų labui, geriau yra dažnai klysti ir po to taisyti.

Pavyzdžiui, paimkime [React](https://github.com/facebook/react) framework'o repozitoriją:

React repozitorijoje yra daugiau nei 1600 prisidėjusių. Top 6 programuotojai, pagal commit'ų skaičių, sudaro apie 50% visų commit'ų repozitorijoje. Šis fantastinis šešetas nėra jūsų standartiniai atviro kodo programuotojai. Jie dirba/dirbo Facebook, taigi, React vystymas, yra jų darbas. Tačiau jie yra maladiec, todėl, kad projektą pastoviai atnaujina ir taiso savo klaidas.

Likusia dalimi commit'ų pasidalina ~1600 žmonių. Dauguma iš jų yra "programuotojai", kurie atlieka pakeitimus tam, kad performatuotų `README.md` ir galėtų pasigirti savo kolegoms, kad "žiūrėkit, koks aš kietiakas". Bet prieš pateikdami pataisymą, kuris jiems užtruktų 2 minutes, jie turėjo perskaityti [elgesio kodeksą](https://code.fb.com/codeofconduct), tada [prisidėjimo instrukciją](https://reactjs.org/docs/how-to-contribute.html), parašyti PR pagal šiuos instruktažus ir atiduoti apie valandą laiko, kad galėtų pasijausti gerai.

Tokiu atveju, iškyla klausimas pamąstymui: kokia dalis programuotojų, kurie taiso kodo klaidas ir kuria funkcionalumą, toliau vystys React projektą, po to kai Facebook pereis prie naujos kartos [vanilla JS kompiliatorių](https://svelte.dev/)?