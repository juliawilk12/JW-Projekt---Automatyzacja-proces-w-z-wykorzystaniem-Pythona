# Solver Równań Różniczkowych

Ten program rozwiązuje równania różniczkowe typu y' = param * x * y 
Rozwiązania są generowane dla zadanych przez użytkownika wartości parametrów i raportowane w formie plików PDF.

## Wymagania

Uruchomienie programu wymaga bibliotek:

- numpy
- matplotlib
- tkinter
- fpdf
- PyPDF2
- pickle


# KORZYSTANIE Z PROGRAMU

1. Po uruchomieniu programu pojawi się okno GUI.

2. Wprowadź wartości parametrów w odpowiednie pola tekstowe.

3. Kliknij przycisk "Rozwiąż równania" - program rozwiąże równania różniczkowe dla podanych parametrów.

3. Wybierz plik PDF za pomocą przycisku "Wybierz PDF", aby odczytać dane tabeli z istniejącego raportu
    i wyświetlić wykres rozwiązania równania.

4. Wybierz plik PKL za pomocą przycisku "Wybierz PKL", aby odczytać dane z pliku PKL.

## Generowanie raportów

Po rozwiązaniu równań różniczkowych dla każdego parametru, program generuje raporty w formie plików PDF. 
Każdy raport zawiera:

- Strona 1: Nagłówek z informacją o parametrze oraz opis teoretyczny równań różniczkowych.

- Strona 2: Wykres z rozwiązania równania różniczkowego.

- Strony 3 i dalsze: Tabela z danymi punktów tworzących wykres.

Raporty są zapisywane w plikach PDF o nazwie "report_param_{param}.pdf", gdzie "{param}" to wartość parametru.

## Serializacja danych

Dane z rozwiązania równań różniczkowych są serializowane do plików PKL. Każdy plik PKL zawiera:

- Wartość parametru.
- Tablica x_data zawierająca wartości x.
- Tablica y_data zawierająca wartości y.

Dane są zapisywane w plikach o nazwie "data_param_{param}.pkl", gdzie "{param}" to wartość parametru.
