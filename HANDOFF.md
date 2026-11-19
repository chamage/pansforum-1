# PANS Forum — HANDOFF

**Stan:** start nowego repozytorium, 19.11.2026. **Cel:** forum jednej uczelni, gotowe do przeglądu i wyjaśnienia przez 6 osób. Planowany termin: **22.12.2026** (termin zespołu, do potwierdzenia).

## 0. Jak korzystać z tego pliku

To instrukcja zarówno dla osoby inicjalizującej projekt (także z pomocą AI), jak i dla zespołu po udostępnieniu repozytorium.

**Najpierw wykonaj ETAP 0, potem dopiero rozpocznij sześć modułów.** Nie generuj całej aplikacji podczas inicjalizacji.

Pozostałe dokumenty w katalogu głównym:

- [`PLAN_UI_I_MODULOW_ZESPOL.md`](PLAN_UI_I_MODULOW_ZESPOL.md) — zadania sześciu osób, wymagania modułów i zasady integracji. **Aktualna instrukcja prac zespołu.**
- [`UI_STYLE_GUIDE.md`](UI_STYLE_GUIDE.md) — zasady wizualne obowiązujące na wszystkich ekranach.
- Raport „Forum — projektowanie systemu” — zaakceptowany plan architektury, ERD, modułów i wdrożenia; to dokument prezentacyjny, nie lista rzeczy do implementacji jednocześnie.

Stary `Forum_plan_zespolu_zadania_na_osobe.pdf` nie jest aktualną instrukcją zespołową.

## 1. Stałe decyzje

- **Architektura:** jeden projekt **Django + Django Templates (MPA)**, PostgreSQL, HTML/CSS, minimalny JavaScript. **Bez React SPA.**
- **Współpraca:** jedno repozytorium, sześć aplikacji i sześć gałęzi funkcjonalnych. `main` ma zawsze uruchamiać się i przechodzić testy.
- **Zależności:** użyj **uv + `pyproject.toml` + `uv.lock`** jako jednego powtarzalnego środowiska lokalnego. Nie dodawaj Poetry ani drugiego lockfile. Wersje Pythona i Django dobierz jako zgodne, wspierane i przypnij.
- **Zakres do zaliczenia:** konta/profile, kategorie, posty/wyszukiwanie, komentarze, głosy, zgłoszenia/moderacja. Bez komunikatora, znajomych, czatu na żywo czy funkcji „na zapas”.
- **UI:** lider ustala styl i tworzy przykład; właściciele modułów tworzą docelowe ekrany w tym stylu.
- **Atrapy:** w testach jednostkowych i przykładowym UI. W docelowych widokach nie mogą ukrywać brakującej integracji.
- **Kontrola jakości:** każdy musi umieć wyjaśnić kod swojego modułu; testy obejmują happy path, odmowę dostępu i istotny błąd. Końcowe kryteria bdb sprawdzamy oddzielnie według arkusza Bazana.

## 2. ETAP 0 — polecenie dla osoby/AI inicjalizującego repo (tylko lider)

**Cel etapu:** dostarczyć działający, niewielki szkielet. Nie realizuj jeszcze biznesowych widoków M1–M6 i nie kopiuj gotowego prototypu `PansForum`.

1. Utwórz projekt Django z `config/` i aplikacjami: `apps/accounts`, `apps/categories`, `apps/posts`, `apps/comments`, `apps/votes`, `apps/moderation`; dodaj `core/` na wspólne kontrakty i widok demonstracyjny. Zadbaj o poprawne `AppConfig`, `INSTALLED_APPS` oraz przestrzenie nazw URL.
2. Przygotuj PostgreSQL jako usługę `db` w `compose.yaml`; w `.env.example` umieść wymagane zmienne. Lokalny Django może działać przez `uv run python manage.py runserver`. Docelowy Nginx + Django + PostgreSQL w trzech kontenerach dodamy na etapie wdrożenia.
3. Ustal **minimalne modele i relacje zgodne z ERD**, tak aby każdy moduł mógł bazować na wspólnych nazwach. Użyj standardowego `django.contrib.auth` User oraz osobnego `Profile` z rolą. Utwórz i przetestuj bazowe migracje. Bez implementacji usług CRUD na tym etapie.
4. Utwórz `core/contracts.py`: małe, zrozumiałe kontrakty (patrz sekcja 3). Nie wdrażaj frameworka DI ani dużej warstwy abstrakcji.
5. Przygotuj `templates/base.html`, `static/css/tokens.css`, `static/css/base.css` i maksymalnie kilka wspólnych elementów: nawigacja, przyciski, formularze, stany focus/błąd. Korzystaj z `UI_STYLE_GUIDE.md`.
6. Zrób stronę **`/ui-preview/` dostępną tylko przy `DEBUG=True`**: przykładowy post, metadane, przyciski głosowania, komentarz, formularz logowania. Zasil ją **statycznymi danymi demonstracyjnymi**, bez importowania modeli innych modułów i bez udawania działającej funkcji. To *wzorzec UI*, nie docelowa tablica postów. Prawdziwą tablicę później tworzy M3.
7. Dodaj jeden **mały przykład atrapy zależności** w `tests/fakes.py`, np. `FakeCategoryCatalog.category_exists(id)`, oraz test jednostkowy użycia tej atrapy. Atrapy nie mogą być importowane z produkcyjnych widoków ani usług.
8. Dodaj `README.md` z komendami instalacji, uruchomienia i testów; `.gitignore`, `.env.example`, test dymny `/ui-preview/` i prosty CI (jeśli nie wymaga dodatkowej konfiguracji). **Nie dodawaj zbędnych bibliotek.**

**Warunek zakończenia:** od świeżego klona i skopiowanego `.env.example` można uruchomić bazę, migracje, testy, serwer oraz otworzyć czytelną stronę `/ui-preview/`. Wszystkie zmiany etapu 0 są w `main`; dopiero wtedy lider ogłasza `BOOTSTRAP READY`.

### Oczekiwana struktura (orientacyjna)

```text
config/                        # settings, root urls
core/contracts.py              # wspólne typy/kontrakty
core/views.py                  # tylko UI preview / wspólne strony
apps/
  accounts/ categories/ posts/ comments/ votes/ moderation/
    models.py  services.py  views.py  urls.py  tests/
templates/
  base.html
  core/ui_preview.html         # przykład, nie produkcyjny feed
static/css/
  tokens.css  base.css
static/js/                     # tylko gdy potrzebny
  
tests/fakes.py                # atrapy do testów
compose.yaml
pyproject.toml  uv.lock
.env.example  .gitignore  README.md
HANDOFF.md  UI_STYLE_GUIDE.md  PLAN_UI_I_MODULOW_ZESPOL.md
```

> To nie jest wymóg tworzenia pustych plików wszędzie. Nie buduj infrastruktury ponad potrzeby sześciu modułów.

## 3. Kontrakty i dane — zamrozić przed pracą równoległą

| Kto potrzebuje | Kontrakt | Zachowanie |
|---|---|---|
| M3 → M2 | `category_exists(category_id) -> bool` | `False` dla brakującej kategorii |
| M4 → M3 | `get_post(post_id) -> PostRef | None` | `None` gdy brak/niepubliczny |
| M5/M6 → M3/M4 | `get_target(kind, id) -> ContentRef | None` | `kind` = `post` / `comment` |
| M3–M6 → M1 | `is_author(user_id, target)` i `has_role(user_id, role)` | jawna odmowa dostępu, gdy brak uprawnień |
| M6 → M3/M4 | `hide_content(kind, id) -> bool` | ukrywa treść, nie zakłada fizycznego DELETE |

`PostRef` zawiera minimum `id, author_id, category_id, hidden`; `ContentRef`: `kind, id, author_id, hidden`. Zastosuj prostą, testowalną reprezentację. Nie zmieniaj nazw ani semantyki bez krótkiego PR i zgody zależnych modułów.

**Bazowe modele:** `Profile`, `Category`, `Post`, `Comment`, `Vote`, `Report`. `Vote` i `Report` wskazują **dokładnie jeden** cel (post XOR komentarz), zgodnie z ERD. `Vote` ma wartość ±1 i maksymalnie jeden aktywny głos na cel/użytkownika; walidacja ma działać również po stronie bazy. Nie dodawaj wspólnej, wymyślonej tabeli `Content`.

**Przykład atrapy:** M4 potrzebuje `get_post(10)`. W teście `FakePostReader` zwraca `PostRef` dla 10 i `None` dla 999. Po integracji podmieniamy zależność na realne odczyty ORM; testy integracyjne korzystają z prawdziwej bazy. **Nie trzeba wdrażać kolejki zadań** do moderacji: zapisane `Report(status=OCZEKUJĄCE)` czeka na późniejsze odczytanie przez moderatora.

## 4. Po `BOOTSTRAP READY` — instrukcja dla wszystkich

1. Sklonuj repo; przeczytaj `README.md`, własny wiersz w `PLAN_UI_I_MODULOW_ZESPOL.md` i `UI_STYLE_GUIDE.md`.
2. Uruchom aplikację i `/ui-preview/`, potem testy. Jeśli projekt nie startuje, **zgłoś blocker przed tworzeniem nowego szkieletu**.
3. Z `main` utwórz swoją gałąź: `feature/m1-accounts`, `feature/m2-categories`, `feature/m3-posts`, `feature/m4-comments`, `feature/m5-votes` lub `feature/m6-moderation`.
4. Najpierw pokaż działającą **usługę i test z atrapą** zależności, potem widok/formularz i fragment UI, a po scaleniu zależnych modułów — testy integracyjne z ORM. Korzystaj z istniejących modeli; migracje tylko za zgodą właściciela kontraktu.
5. Zrób mały Pull Request. Opisz: **co działa, jak uruchomić, co testowano, jakie pliki i API zmieniono, co pozostaje do zrobienia**; dla UI dodaj zrzut ekranu. Kod w PR musi dać się obronić bez asystenta.
6. Drugi członek zespołu robi review; lider zatwierdza zmiany wspólne i kolejność scalenia. Po merge aktualizujesz gałąź względem `main`.

**Własność UI:** lider utrzymuje `base.html`, globalną nawigację i `tokens.css`; każdy tworzy własne szablony pod `apps/<moduł>/templates/`. Na stronie pojedynczego posta M3 osadza fragmenty M4 (komentarze), M5 (głosowanie), M6 (zgłaszanie). Nie nadpisuj czyjegoś `urls.py`, globalnych stylów ani kontraktów bez uzgodnienia.

**Krytyczne zasady:** bez pushowania wprost do `main`; bez równoległego przepisywania `settings.py`; bez pełnego kopiowania prototypu; bez fake'ów w aplikacji produkcyjnej; bez deklarowania gotowych funkcji, których jeszcze nie zintegrowano.

## 5. Terminy robocze

| Kiedy | Co ma być widoczne |
|---|---|
| **19–23.11** | Lider: ETAP 0, `/ui-preview/`, repo na GitHubie, `BOOTSTRAP READY` |
| **24–30.11** | Każdy: gałąź, kontrakt, pierwszy PR z usługą/atrapą/testami; M1/M2 rozpoczynają integrację |
| **1.12 — zajęcia** | Projektowanie, podział odpowiedzialności, działający szkielet i kontrolowany postęp |
| **2–14.12** | Funkcje M1–M6, ekrany według style guide, integracja z bazą i testy |
| **15.12 — zajęcia** | Działające główne scenariusze, testy i omówienie fragmentów kodu |
| **16–21.12** | Stabilizacja, docelowy Docker, audyt arkusza bdb, próba obrony |
| **22.12 — cel zespołu** | Stabilne wydanie, gotowe do zaliczenia (termin do potwierdzenia) |

**Gotowe do pierwszej pracy zespołowej =** repo uruchamia się, kontrakty są niezmienne, UI preview istnieje, każdy zna swój moduł i potrafi rozpocząć pracę bez czekania na kolegów.
