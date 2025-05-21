# 1. Používanie hardcoded hodnôt v ETL procesoch pre biznis pravidlá
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Hardcoded hodnoty sú nepružné, zvyšujú riziko chýb pri zmene pravidiel a komplikujú údržbu. Napríklad zmena prahu pre výpočet (napr. 10 % na 15 %) vyžaduje úpravu kódu a nové nasadenie.
## Odporúčanie: 
Ukladajte biznis pravidlá v konfiguračných súboroch, databázových tabuľkách alebo parametroch ETL nástroja. To umožňuje dynamické zmeny bez úpravy kódu.
## Osobná skúsenosť: 
Hardcored daňové sadzby v projekte, ktkoré museli byť menené.
# 2. Neindexovanie stĺpcov, ktoré sú často dotazované vo veľkých tabuľkách
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Zlé výkonnostné výsledky dotazov, zvýšené časy odozvy a vyššia spotreba zdrojov. Napríklad full table scan na miliónoch riadkov spomaľuje reporty.
## Odporúčanie: 
Vytvorte indexy (napr. B-tree alebo bitmap) na stĺpce používané vo WHERE, JOIN alebo GROUP BY. Pravidelne analyzujte plány dotazov.
## Osobná skúsenosť: 
V dátovom sklade sme zaznamenali 10-násobné spomalenie kvôli chýbajúcim indexom na kľúčových stĺpcoch. Po ich pridaní sa čas spracovania skrátil z minút na sekundy.
# 3. Ukladanie logov a záloh na rovnaký server ako produkčná databáza
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Riziko straty dát pri zlyhaní servera, preťaženie disku a zníženie výkonu databázy. Napríklad výpadok disku môže zničiť logy aj zálohy.
## Odporúčanie: 
Ukladajte logy a zálohy na oddelené servery alebo cloudové úložiská (napr. S3, Azure Blob). Implementujte geograficky redundantné zálohovanie.

# 4. Používanie zdieľaných servisných účtov na pripojenie k databázam v ETL nástrojoch
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Znížená bezpečnosť, nemožnosť sledovať individuálne akcie a riziko zneužitia. Napríklad únik hesla ohrozí celý systém.
## Odporúčanie: 
Používajte individuálne účty s minimálnymi oprávneniami a spravujte ich cez IAM (Identity and Access Management). Implementujte rotáciu hesiel.

# 5. Budovanie dátových kanálov bez implementácie mechanizmov na opakovanie alebo zotavenie pri zlyhaní
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Zlyhanie kanála spôsobí výpadky, manuálne zásahy a oneskorenia. Napríklad sieťový výpadok zastaví celý proces.
## Odporúčanie: 
Implementujte mechanizmy opakovania (retry) a zotavenia (napr. checkpointy, idempotentné operácie). Používajte nástroje ako Apache Airflow s retry politikami.
## Osobná skúsenosť: 
Kanál bez retry zlyhal kvôli dočasnému výpadku API. Po pridaní automatických opakovaní sa stabilita výrazne zlepšila.
# 6. Povoľovanie priameho prístupu ku zdrojovým dátam všetkým členom tímu bez kontroly prístupu
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Riziko neoprávnených zmien, únikov dát a chýb. Napríklad nesprávny dotaz môže zmazať produkčné dáta.
## Odporúčanie: 
Implementujte role-based access control (RBAC) a povoľte prístup iba cez read-only účty alebo staging vrstvy.
## Osobná skúsenosť: 
Raz člen tímu omylom upravil zdrojové dáta, čo spôsobilo nesprávne reporty.
# 7. Vynechanie validácie schémy pri načítavaní externých dát
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Chybné alebo nekonzistentné dáta môžu narušiť downstream procesy. Napríklad zmena formátu stĺpca spôsobí zlyhanie ETL.
## Odporúčanie: 
Implementujte validáciu schémy (napr. pomocou JSON Schema alebo nástrojov ako Great Expectations) pred načítaním dát.
## Osobná skúsenosť: 
Externý dodávateľ zmenil dátový formát bez upozornenia, čo zlomilo náš kanál. Validácia schémy by tento problém odhalila skôr.
# 8. Používanie zastaraných ETL procesov bez pravidelných revízií optimalizácie
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Neefektívne procesy, vyššie náklady a pomalé spracovanie. Napríklad starý skript nemusí zvládať väčší objem dát.
## Odporúčanie: 
Pravidelne revidujte a optimalizujte ETL procesy (napr. každých 6 mesiacov). Používajte moderné nástroje ako dbt alebo Spark.

# 9. Nepremazanie alebo neodstránenie zastaraných tabuliek a pohľadov z dátového skladu
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Zvýšené náklady na úložisko, zmätok v dokumentácii a riziko použitia starých dát.
## Odporúčanie: 
Implementujte politiku životného cyklu dát (data lifecycle) a pravidelne archivujte alebo mažte zastarané objekty.

# 10. Nenastavenie upozornení na zlyhané úlohy alebo oneskorenia kanálov
## Osvedčený postup? 
**Nie.**
# Negatívny výsledok: 
Oneskorená reakcia na chyby, čo môže viesť k výpadkom alebo nesprávnym dátam. Napríklad zlyhanie kanála zostane nepovšimnuté.
## Odporúčanie: 
Nastavte upozornenia cez nástroje ako PagerDuty, Slack alebo email pre zlyhania a oneskorenia.
## Osobná skúsenosť: 
V priebehu projektu trvalo nemilo dlho kým sme si v tíme uveodmili zlyhania úloh, keďže sme pracovali na ďalších zadaniach.
# 11. Ukladanie citlivých údajov bez šifrovania pri ukladaní alebo prenose
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Riziko úniku dát, porušenie GDPR a pokuty. Napríklad nešifrované dáta môžu byť zachytené pri prenose.
## Odporúčanie: 
Používajte šifrovanie na úrovni úložiska (AES-256) a prenosu (TLS). Implementujte tokenizáciu pre citlivé polia.

# 12. Ignorovanie obmedzení dátových typov pri vytváraní schém v dátovom sklade
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Nekonzistentné dáta, chyby pri spracovaní a neefektívne úložisko. Napríklad text v numerickom stĺpci spôsobí zlyhanie.
## Odporúčanie: 
Definujte striktné dátové typy a validujte ich pri načítavaní (napr. INT pre ID, DATE pre dátumy).
## Osobná skúsenosť: 
Voľné dátové typy spôsobili chyby v agregáciách. Po zavedení striktných typov sme zvýšili spoľahlivosť reportov.
# 13. Povoľovanie kruhových závislostí medzi ETL úlohami
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Zacyklenie úloh, zlyhania kanála a komplikovaná údržba. Napríklad úloha A čaká na B, ktorá čaká na A.
## Odporúčanie: 
Navrhnite DAG (Directed Acyclic Graph) bez kruhových závislostí. Používajte orchestrátory ako Airflow na ich detekciu.
## Osobná skúsenosť: 
Kruhové závislosti zastavili môj kanál. 
# 14. Vykonávanie transformácií priamo na produkčných databázach namiesto staging vrstiev
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Riziko poškodenia produkčných dát, zníženie výkonu a obtiažna obnova. Napríklad chybná transformácia môže pokaziť dáta.
## Odporúčanie: 
Používajte staging vrstvy na transformácie a produkčné dáta iba čítajte.

# 15. Výber dátového modelu (napr. hviezdica vs. snehová vločka) bez zohľadnenia použitia
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Neefektívne dotazy alebo komplikované modely. Napríklad snehová vločka spomaľuje jednoduché reporty.
## Odporúčanie: 
Vyberte model podľa potrieb (hviezda pre jednoduché reporty, snehová vločka pre komplexné analýzy). Validujte s používateľmi.
## Osobná skúsenosť: 
Snehová vločka bola príliš zložitá pre náš tím. Prechod na hviezdicový model zjednodušil dotazy.
# 16. Používanie VARCHAR(MAX) ako predvoleného dátového typu pre textové polia
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Neefektívne úložisko, pomalšie dotazy a komplikované validácie. Napríklad zbytočne veľké stĺpce zvyšujú I/O.
## Odporúčanie: 
Používajte špecifické dĺžky (napr. VARCHAR(50)) podľa dát. Analyzujte dáta pred návrhom schémy.
## Osobná skúsenosť: 
VARCHAR(MAX) spôsobil nárast úložiska o 30 %.
# 17. Pridávanie všetkých stĺpcov zo zdrojového systému do dátového skladu bez ohľadu na ich relevantnosť
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Zbytočné úložisko, pomalšie spracovanie a zmätok v analýzach. Napríklad nepoužívané stĺpce zahlcujú tabuľky.
## Odporúčanie: 
Mapujte iba relevantné stĺpce na základe požiadaviek. Dokumentujte výber.
## Osobná skúsenosť: 
Import všetkých stĺcov spôsobil preplnenie skladu. Po selektívnom výbere sa výkon zlepšil.
# 18. Vynechanie partitioningu alebo clusteringu pre veľké faktové tabuľky
## Osvedčený postup?
**Nie.**
## Negatívny výsledok: 
Pomalé dotazy a vysoká spotreba zdrojov. Napríklad skenovanie celej tabuľky namiesto malej podmnožiny.
## Odporúčanie: 
Implementujte partitionovanie (napr. podľa dátumu) a clustering (napr. podľa kľúča). Testujte stratégie.

# 19. Vývoj a nasadenie zmien v pipeline bez verzovania alebo testovania
## Osvedčený postup? 
**Nie.**
## Negatívny výsledok: 
Chyby v produkcii, nemožnosť vrátenia zmien a strata dôvery. Napríklad chybný kód pokazí dáta.
## Odporúčanie: 
Používajte verzovanie (napr. Git) a testovanie (unit testy, integračné testy) pred nasadením.
