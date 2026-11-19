# Forum — UI style guide

**Kierunek:** spokojny, minimalistyczny interfejs inspirowany Threads. Desktop-first, responsywny. Dużo czytelnej treści, mało dekoracji. Inspiracja wizualna nie oznacza kopiowania interfejsu 1:1.

## Zasady

1. **Monochromatycznie.** Biel, niemal czerń, 2–3 odcienie szarości. Czerwień uczelni jako rzadki akcent (orientacyjnie 1–5% widoku), nie stały kolor wszystkich przycisków. Dokładny odcień do zatwierdzenia.
2. **Bez cieni.** Unikaj ramek wokół każdej sekcji i kart w kartach. Hierarchię buduj odstępami, tłem i dyskretnymi separatorami. Obramowania stosuj, gdy mają funkcję (pola formularzy, aktywny fokus).
3. **Typografia.** 14 px — standardowe elementy UI; 16 px — treść postów i komentarzy; 13 px — wyjątkowo metadane; 20–24 px — nagłówki. Nie schodź poniżej 13 px. W treściach używaj komfortowej interlinii (ok. 1.5).
4. **Gęstość pośrednia.** Ani mikroskopijne kontrolki, ani ogromne karty. Bazowe odstępy: 4 / 8 / 12 / 16 / 24 px. Główny strumień postów powinien mieć ograniczoną szerokość (około 680–760 px).
5. **Mniej tekstu pomocniczego.** Pisz etykiety i opisy tylko wtedy, gdy pomagają podjąć decyzję albo uniknąć błędu. Nie objaśniaj oczywistych działań. Ikony stosuj dla rozpoznawalnych operacji; niejednoznaczne ikony uzupełniaj tekstem lub podpowiedzią.
6. **Spójność ponad indywidualność.** Wspólne fonty, kolory, odstępy, komponenty, stany przycisków i formularzy. Każdy ekran musi wyglądać jak część tej samej aplikacji.
7. **Dostępność bez wizualnego hałasu.** Zachowaj widoczny fokus klawiatury, odpowiedni kontrast, komunikaty błędów oraz dostępne nazwy ikon (`aria-label`). Pola formularzy mają prawdziwe etykiety; placeholder ich nie zastępuje.

## Wspólne elementy

- `base.html` — układ, nagłówek i nawigacja.
- `post_card` — wzorzec pojedynczego posta na liście.
- `button`, `icon_button`, `input`, `textarea` — wspólne stany i wymiary.
- `empty_state`, `error_message` — krótkie, rzeczowe komunikaty.
- `vote_controls`, `comment_list`, `report_action` — fragmenty osadzane przez właścicieli modułów.

## Reguła przed dodaniem elementu

**Czy to potrzebne, czytelne i zgodne z istniejącym wzorcem?** Jeśli nie — usuń lub uprość. Nie dodawaj opisu tylko po to, by wypełnić przestrzeń.

## Źródło prawdy

Wspólne wartości kolorów, typografii i odstępów trzymamy w `static/css/tokens.css`, a reguły ogólne w `static/css/base.css`. Nowe ekrany korzystają z nich, bez własnych palet i bibliotek UI.
