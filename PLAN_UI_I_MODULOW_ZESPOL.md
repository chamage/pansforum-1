# Forum — implementacja zespołowa i wspólny UI

**Cel:** sześć osób rozwija jedno forum, a każda potrafi wyjaśnić swój moduł. Dokument jest instrukcją pracy, nie promptem wymagającym kopiowania. Kod wygenerowany z pomocą LLM musi zostać zrozumiany, sprawdzony i przetestowany przez właściciela.

**Architektura z aktualnej dokumentacji:** Django + PostgreSQL + Django Templates (MPA), z jednym repozytorium i wspólnymi stylami. Przejście na React SPA byłoby osobną decyzją wymagającą aktualizacji architektury, kontraktów HTTP i dokumentacji.

## 0. Punkt startowy

Wspólny szkielet, M1 oraz wzorzec UI są gotowe na main.

- / jest wzorcem tablicy. M2 podłącza prawdziwe kategorie, M3 prawdziwe posty, wyszukiwanie i sortowanie.
- base.html, tokens.css, base.css, konfiguracja i core/contracts.py są współdzielone — zmiany tylko po uzgodnieniu z kierownikiem.
- Każdy rozwija przede wszystkim własny moduł i jego UI.
- Nie dodajemy Reacta ani drugiego systemu stylów.

## 1. Zadania dla sześciu osób

| Osoba | Backend i dane | Jej GUI | Zależności / atrapy | Warunek ukończenia |
|---|---|---|---|---|
| **1 — Kierownik: konta i UI foundation** | Rejestracja, logowanie, wylogowanie, profile, role. Integracja szkieletu. | Wzorcowe logowanie, układ strony, nagłówek, tokeny stylu. | Testy uprawnień mogą korzystać z przykładowych użytkowników. | Logowanie i profile działają, kontrola uprawnień jest testowana; zespół ma gotowy wzorzec UI. |
| **2 — Kategorie** | CRUD kategorii (administrator), przeglądanie i wybór kategorii. | Lista kategorii, nawigacja, formularz kategorii; wspiera kontrolę responsywności i spójności gotowych widoków. | Do pracy nad widokami może użyć demonstracyjnej listy kategorii; nie zmienia globalnego stylu. | Lista i CRUD działają, dostęp admina jest kontrolowany, są testy; wspólne widoki przechodzą przegląd UI. |
| **3 — Posty + wyszukiwanie** | Tworzenie, odczyt, edycja, usuwanie postów; filtr kategorii, sortowanie, wyszukiwanie. | Docelowa tablica i strona pojedynczego posta. Odpowiada za osadzenie fragmentów M4/M5/M6. | Na starcie `FakeCategoryLookup` i przykładowe posty zgodne z umówionym formatem. | Posty działają, lista i szczegóły integrują pozostałe widżety, testy przechodzą. |
| **4 — Komentarze** | Dodawanie, edycja, usuwanie własnych komentarzy; walidacja autorstwa. | `comment_list` i formularz odpowiedzi osadzane na stronie posta. | `FakePostLookup` zwraca istniejący post albo brak posta; używany w testach jednostkowych. | Fragment komentarzy można osadzić na stronie M3, testy poprawnych i błędnych przypadków działają. |
| **5 — Głosowanie** | Głosy +1/−1 na post lub komentarz; maksymalnie jeden aktywny głos użytkownika na treść; bilans. | `vote_controls` z czytelnym stanem aktualnego głosu. | `FakeContentLookup` udaje wyszukiwanie ocenianego posta/komentarza. | Obsługuje dodanie, zmianę i cofnięcie głosu; testuje również duplikaty i brak uprawnień. |
| **6 — Moderacja** | Zgłoszenie treści, rejestr oczekujących zgłoszeń, odrzucenie lub ukrycie treści, role. | `report_action` i panel moderatora. | `FakeContentLookup` i `FakePermissions` w testach; proces zgłoszenia i rozpatrzenia jest rozdzielony czasowo. | Zgłoszenia i rozpatrywanie działają, uprawnienia i statusy są testowane. |

Wszyscy przygotowują **własne podstawowe UI**, testy oraz krótkie wyjaśnienie działania swojego fragmentu. Kierownik kontroluje spójność, a nie implementuje sześciu frontendów sam.

## 2. Jak rozumieć atrapy

Atrapa zastępuje **brakującą zależność** podczas testowania modułu, nie stanowi osobnej wersji całego systemu.

Przykład: M4 (komentarze) potrzebuje sprawdzić, czy istnieje post. Zanim M3 (posty) będzie gotowy, test M4 używa `FakePostLookup`, który dla `post_id=10` zwraca przykładowy post, a dla `post_id=999` zwraca brak. Potem prawdziwa implementacja tej samej operacji odczytu wykorzystuje Django ORM. Te same przypadki należy sprawdzić testami integracyjnymi.

**Praktyka:** atrapy trzymaj w testach albo danych demonstracyjnych, a logikę aplikacji pisz pod mały, uzgodniony interfejs. W produkcyjnych widokach nie zostawiaj ukrytych zależności od Fake/Stub.

**Format uzgodnienia fragmentów UI:**
- M3 udostępnia stronę `post_detail` z kontekstem `post`.
- M4 dostarcza szablon `comments/_list.html` i oczekuje `post` oraz `comments`.
- M5 dostarcza `votes/_controls.html` i oczekuje `target_type`, `target_id`, `score`, `user_vote`.
- M6 dostarcza `moderation/_report_action.html` i oczekuje `target_type`, `target_id`.

Najpierw ustalcie nazwy danych i interfejsów, następnie można pracować równolegle. Parametry mogą się zmienić, ale wyłącznie po wspólnym uzgodnieniu.

## 3. Procedura pracy i integracji

1. **Start:** każdy tworzy `feature/m1-accounts`, `feature/m2-categories` itd. na podstawie aktualnego `main`.
2. **Mały PR:** najpierw modele lub kontrakty, potem usługi i testy, na końcu GUI. Nie czekaj z pierwszym PR do ukończenia całego modułu.
3. **Testy:** test jednostkowy poprawnego i błędnego przypadku z atrapą oraz test integracyjny z rzeczywistą bazą/warstwą widoku; liczby i rodzaje testów dopasować do arkusza bdb.
4. **Review:** właściciel pokazuje co działa i wyjaśnia najważniejszy kod. Druga osoba sprawdza PR; kierownik zatwierdza zmiany w plikach wspólnych.
5. **Integracja:** kolejność domyślna M1/M2 → M3 → M4 → M5 → M6. Moduły mogą powstawać równolegle; kolejność dotyczy scalania zależności, nie momentu rozpoczęcia pracy.
6. **Wspólny test:** po każdym merge uruchomcie migracje, testy, podstawowe ścieżki użytkownika i sprawdźcie wygląd strony posta (najwięcej integracji).

Na początek formularze HTML + POST i przekierowanie po zapisie. JavaScript tylko tam, gdzie rzeczywiście poprawia obsługę. Nie dokładaj nowego frameworka UI ani mechanizmu SPA w połowie prac.

## 4. Terminy (zajęcia co dwa tygodnie)

| Termin | Wynik |
|---|---|
| **19–24 listopada** | Kierownik udostępnia szkielet, style guide, wzorce UI i kontrakty; reszta wybiera gałęzie. |
| **1 grudnia — zajęcia** | Dokument projektowania, podział modułów, pierwsze działające szkielety/atrapy. |
| **2–14 grudnia** | Moduły, UI i PR-y; stopniowe połączenie z ORM i wspólnymi szablonami. |
| **15 grudnia — zajęcia** | Działające główne ścieżki forum, testy i integracja na jednej gałęzi. |
| **16–21 grudnia** | Poprawki, Docker, dokumentacja, próba pytań z kodu. |
| **22 grudnia — cel zespołu** | Stabilne wydanie do zaliczenia; termin trzeba potwierdzić z prowadzącym. |

## 5. Minimum przed uznaniem modułu za gotowy

- Działa samodzielnie w wspólnym repo (po `git pull`, migracjach i uruchomieniu).
- Korzysta z tokenów i istniejących wzorców UI; nie wprowadza nowej palety ani nie dubluje `base.html`.
- Ma test poprawnej ścieżki, uprawnień i ważnego błędu; brak atrap w kodzie uruchamianym produkcyjnie.
- Osoba odpowiedzialna potrafi wyjaśnić modele, przepływ żądania, walidację i testy.


## Dodatkowy kontrakt UI

M2: zasilić selektor kategorii prawdziwymi danymi. M3: zastąpić demonstracyjny widok core.views.home prawdziwymi postami i obsłużyć parametry GET category, sort=recent|top i q. Jedyny punkt dodawania postu pozostaje nad strumieniem. Nie implementować personalizacji „Dla Ciebie”. Kierownik utrzymuje wspólny layout.
