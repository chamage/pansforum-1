# PANS Forum — UI style guide

**Kierunek:** minimalistyczny, desktop-first, charakter zbliżony do Threads (bez kopiowania interfejsu 1:1).

## Zasady

1. **Dwa tła:** jasnoszare tło aplikacji i biała powierzchnia strumienia. Separatory zamiast cieni i kart w kartach.
2. **Oszczędny kolor:** niemal czerń, biel i szarości. Czerwień #9e1b32 tylko do ważnych aktywnych stanów lub błędów.
3. **Tekst:** 14 px w UI i metadanych, 16 px w treści, 18 px dla tytułu posta, 24 px dla nagłówków formularza. Nie używamy fontów 13 px.
4. **Kontrolki:** przyciski i pola około 42 px wysokości, klikalne ikony około 42 × 42 px. Duże odstępy między postami, mniejsze między powiązanymi informacjami.
5. **Minimum objaśnień:** nie wstawiamy instrukcji do oczywistych operacji; dajemy czytelne ikony, krótkie nazwy i odpowiednie odstępy. Ikony mają aria-label.
6. **Brak zbędnej dekoracji:** bez cieni, czerwonych kropek, stopki w strumieniu, wielokrotnych ramek i dużych bloków pomocniczego tekstu.
7. **Dostępność:** widoczny focus-visible, etykiety pól formularzy, kontrast i stany błędów.
8. **Optyczne wyrównanie:** text-box: trim-both cap alphabetic przez @supports tylko dla krótkich etykiet, z fallbackiem dla starszych przeglądarek.

## Wspólne elementy i strony

- static/css/tokens.css — źródło kolorów, odstępów i rozmiarów.
- static/css/base.css — wspólny layout i klasy komponentów.
- templates/base.html — boczna nawigacja, powierzchnia strony i nagłówek.
- templates/partials/post_card.html — wzorzec wpisu.
- templates/partials/comment_item.html — wzorzec komentarza.
- / — wzorzec tablicy; obecnie dane demonstracyjne, docelowo dane M2/M3.
- /ui-components/ — osobna galeria formularzy, komentarzy i stanów.
- Widoki podglądu działają tylko przy DEBUG=True.

Każdy moduł M1–M6 korzysta z tych klas. Właściciel modułu robi własny ekran; kierownik zatwierdza zmiany we wspólnym layoucie i tokenach.

## Nawigacja i integracja

- Sidebar wyśrodkowany w pionie: tablica, wyszukiwanie, profil. Bez osobnej ikony dodawania postu.
- Nagłówek strumienia wybiera kategorię; obok sortowanie „Najnowsze” / „Najlepiej oceniane”.
- Kategoria przy wpisie ma neutralny styl pill.
- Logowanie i rejestracja używają odrębnego układu accounts/auth_base.html.
- / wyświetla dane demonstracyjne tylko w DEBUG=True. M3 podłączy prawdziwe posty, M2 kategorie.
- Litera P to placeholder na logo SVG przygotowane przez kierownika.
