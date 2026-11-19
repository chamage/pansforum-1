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

## Kontrakty i praca

Backendowe granice modułów są w core/contracts.py. Atrapy służą tylko do testów.

Ustalony kontrakt integracji UI:
- M3: posts:post_detail → /posts/<post_id>/ → templates/posts/post_detail.html
- M4: templates/comments/_list.html — kontekst: post, comments
- M5: templates/votes/_controls.html — kontekst: target_type, target_id, score, user_vote
- M6: templates/moderation/_report_action.html — kontekst: target_type, target_id

Każdy pracuje na własnym branchu feature/mX-nazwa i wrzuca zmiany przez PR. Zmiany w templates/base.html, globalnym CSS, konfiguracji lub core/contracts.py uzgadniamy z kierownikiem.
