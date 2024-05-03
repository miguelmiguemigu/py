Quizzy

Tento kód je pre jednoduchú kvízovú aplikáciu napísanú v Python pomocou knižnice tkinter. Umožňuje používateľom absolvovať kvíz s viacerými možnosťami odpovedí.

Požiadavky

Python 3
Knižnica tkinter (zvyčajne predinštalovaná)
Súbor quiz_data.py obsahujúci zoznam otázok a odpovedí (nie je súčasťou tohto kódu)
Spustenie aplikácie

Uistite sa, že máte nainštalovaný Python 3.
Vložte tento súbor a súbor quiz_data.py do rovnakého adresára.
Otvorte terminál alebo príkazový riadok a prejdite do tohto adresára.
Spustite aplikáciu pomocou nasledujúceho príkazu:
python quiz_app.py
Súbor quiz_data.py

Súbor quiz_data.py by mal obsahovať zoznam otázok a odpovedí vo formáte Pythonu. Každá otázka by mala byť slovníkom s nasledujúcimi kľúčmi:

question: Text samotnej otázky.
options: Zoznam štyroch reťazcov predstavujúcich možné odpovede.
correct: Index (číslo medzi 0 a 3) správnej odpovede v zozname options.
Funkcie aplikácie

Uvítacia obrazovka: Používateľ zadá svoje meno a môže si vybrať počet otázok, ktoré chce absolvovať (maximálny počet je daný počtom otázok v súbore quiz_data.py).
Kvízová obrazovka: Zobrazuje sa otázka a štyri možnosti odpovedí. Používateľ vyberie odpoveď a klikne na tlačidlo "Ďalšia otázka". Po zodpovedaní všetkých otázok sa zobrazí tlačidlo "Ukončiť".
Výsledná obrazovka: Zobrazí sa meno používateľa a jeho dosiahnuté skóre. Používateľ môže kliknúť na tlačidlo "Reštartovať kvíz", aby začal znova.
Uloženie odpovedí

Aplikácia ukladá odpovede používateľa do textového súboru s časovou pečiatkou, ktorá obsahuje meno používateľa, otázky, zvolené odpovede a dosiahnuté skóre.