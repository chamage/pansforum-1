# Forum — implementacja zespołowa i wspólny UI

**Cel:** sześć osób rozwija jedno forum, a każda potrafi wyjaśnić swój moduł.

**Architektura:** Django + PostgreSQL + Django Templates (MPA), jedno repozytorium i wspólne style.

**Ważne:** kontrakty między modułami są już ustalone przez kierownika w `core/contracts.py`. Podczas robienia atrap wystarczy je wykorzystać.

## Zadania dla sześciu osób

| Osoba | Backend i dane | Jej GUI | Zależności / atrapy | Warunek ukończenia |
|---|---|---|---|---|
| **1 — Kierownik: konta i UI foundation** | Rejestracja, logowanie, wylogowanie, profile, role; implementacja `AccessChecker`. Integracja szkieletu. | Logowanie, profil, wspólny layout i style. | Dostarcza `DjangoAccessChecker`; `Profile.role` steruje rolami forum. | Konta i profile działają, kontrola uprawnień jest testowana; wspólny UI jest stabilny. |
| **2 — Kategorie** | CRUD kategorii dla administratora, przeglądanie i wybór kategorii; implementacja `CategoryCatalog`. | Lista/wybór kategorii i formularz kategorii. | Dostarcza `CategoryCatalog`; sprawdzanie admina przez `AccessChecker`, nie przez samo `is_staff`. | Lista i CRUD działają, dostęp admina jest kontrolowany, są testy. |
| **3 — Posty + wyszukiwanie** | Tworzenie, odczyt, edycja i usuwanie postów; `category`, `q`, `sort=recent|top`, okres `t`; implementacja `PostReader`, `ContentLookup` i ukrywania postów dla `ContentModeration`. | Docelowa tablica i `post_detail`; integruje partiale M4/M5/M6. | Konsumuje `CategoryCatalog`; zanim M2 jest gotowe używa `FakeCategoryCatalog` w testach. | Posty, tablica, szczegóły, filtrowanie, wyszukiwanie i sortowanie działają; testy przechodzą. |
| **4 — Komentarze** | Dodawanie, edycja i usuwanie własnych komentarzy; implementacja odczytu komentarzy dla `ContentLookup` i ukrywania komentarzy dla `ContentModeration`. | Lista komentarzy i formularz odpowiedzi na stronie posta. | Konsumuje `PostReader`; przed integracją używa fake implementującego `PostReader`. | Komentarze działają na stronie M3, autorstwo i błędy są testowane. |
| **5 — Głosowanie** | Głos +1/−1 na post lub komentarz; maksymalnie jeden aktywny głos użytkownika na cel; zmiana i cofnięcie głosu; bilans. | Kontrolki głosowania dla posta i komentarza. | Konsumuje `ContentLookup` i `AccessChecker`; w testach używa fake implementacji tych kontraktów. | Dodanie, zmiana i cofnięcie głosu działają; duplikaty, brak celu i uprawnienia są testowane. |
| **6 — Moderacja** | Zgłaszanie treści, lista oczekujących zgłoszeń, odrzucenie zgłoszenia lub ukrycie treści. | Akcja zgłoszenia + panel moderatora. | Konsumuje `ContentLookup`, `AccessChecker` i `ContentModeration`; w testach używa ich fake implementacji. | Zgłoszenia i rozpatrywanie działają, role i statusy są testowane. |

Wszyscy przygotowują własne UI, testy oraz krótkie wyjaśnienie działania swojego fragmentu.

## Atrapy

Atrapa zastępuje brakującą zależność podczas tworzenia i testowania modułu równolegle z innymi.

Przykład: M4 potrzebuje sprawdzić, czy istnieje post. Dopóki M3 nie jest gotowe, test M4 używa fake implementującego `PostReader`. Po integracji ten sam kod korzysta z prawdziwej implementacji M3.

**Źródło prawdy dla backendu:** `core/contracts.py`.

Ustalone zależności:
- M2 dostarcza `CategoryCatalog`; M3 go używa.
- M3 dostarcza `PostReader`; M4 go używa.
- M3 i M4 dostarczają `ContentLookup`; M5 i M6 go używają.
- M1 dostarcza `AccessChecker`; M2–M6 używają go do uprawnień.
- M3 i M4 dostarczają `ContentModeration`; M6 używa go do ukrywania treści.

### Ustalony kontrakt integracji UI

- **M3:** URL/view `posts:post_detail`, ścieżka `/posts/<post_id>/`, szablon `templates/posts/post_detail.html`, kontekst `post`.
- **M4:** `templates/comments/_list.html`, kontekst `post`, `comments`.
- **M5:** `templates/votes/_controls.html`, kontekst `target_type`, `target_id`, `score`, `user_vote`.
- **M6:** `templates/moderation/_report_action.html`, kontekst `target_type`, `target_id`.

M3 osadza partiale M4/M5/M6 na stronie szczegółów posta.

## Procedura pracy i integracji

1. Każdy tworzy własny branch `feature/m2-categories`, `feature/m3-posts`, itd. z aktualnego `main`.
2. Implementuje swój moduł pod istniejące kontrakty z `core/contracts.py`. Brakujące zależności zastępuje fake'ami tylko w testach.
3. Dodaje testy poprawnej ścieżki, ważnego błędu i uprawnień.
4. Dodaje swoje UI zgodnie z ustalonymi ścieżkami szablonów i wspólnym `STYLE_GUIDE.md`.
5. Robi mały PR. Kierownik zatwierdza zmiany w `base.html`, globalnym CSS, konfiguracji i `core/contracts.py`.
6. Po merge uruchamiamy migracje, pełne testy i podstawowe ścieżki użytkownika.

Moduły mogą powstawać równolegle. Domyślna kolejność integracji zależności: M1/M2 → M3 → M4 → M5/M6.

## Terminy

| Termin | Wynik |
|---|---|
| **19 listopada – 1 grudnia** | Repo i podział modułów gotowe; pierwsze działające moduły/testy z atrapami. |
| **2–15 grudnia** | Implementacja, UI, PR-y i stopniowa integracja z prawdziwymi zależnościami. |
| **16–22 grudnia** | Poprawki, Docker, dokumentacja, próba pytań z kodu i stabilne wydanie. |

## Minimum przed uznaniem modułu za gotowy

- Korzysta z istniejących kontraktów i wspólnych wzorców UI.
- Nie importuje atrap do kodu produkcyjnego.
- Ma test poprawnej ścieżki, uprawnień i ważnego błędu.
- Integruje się z zależnymi modułami.
- Osoba odpowiedzialna potrafi wyjaśnić modele, przepływ żądania, walidację i testy.
