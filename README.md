# PANS Forum

Forum studenckie w Django + PostgreSQL. Interfejs oparty na Django Templates.

## Start

    cp .env.example .env
    uv sync
    uv run python manage.py migrate
    uv run python manage.py runserver

Jeśli używasz Dockera do bazy:

    docker compose up -d

## Sprawdzenie

    uv run python manage.py check
    uv run python manage.py makemigrations --check --dry-run
    uv run python manage.py test

## Moduły

- M1 accounts — konta, profile, role — gotowe
- M2 categories — kategorie
- M3 posts — posty, tablica, wyszukiwanie i sortowanie
- M4 comments — komentarze
- M5 votes — głosowanie
- M6 moderation — zgłoszenia i moderacja

/ jest wzorcem docelowej tablicy na danych demonstracyjnych. M2 i M3 mają podłączyć do istniejącego UI prawdziwe dane, bez przebudowy wspólnego layoutu.

## Zasady pracy

Przed pracą przeczytaj swój przydział w PLAN_UI_I_MODULOW_ZESPOL.md. Wygląd opisuje STYLE_GUIDE.md.

Wspólne kontrakty są w core/contracts.py. Atrapy służą do testów; nie importujemy ich do kodu produkcyjnego.

Każdy pracuje na własnym branchu feature/mX-nazwa i wrzuca zmiany przez PR. Zmiany w templates/base.html, globalnym CSS, konfiguracji lub kontraktach najpierw uzgadniamy.
