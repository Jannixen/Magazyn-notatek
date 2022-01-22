# Magazyn-notatek
Projekt bezpiecznej aplikacji webowej do przechowywania notatek tworzony w ramach przedmiotu ,,Ochrona danych w systemach informatycznych''

Sposoby uruchomienia:

python manage.py runserver lub docker-compose up

Aby uruchomić konieczne jest dodanie pliku .env oraz certyfikatów SSL (nieuwzględnione w repozytorium).

Aplikacja umożliwia:
- dodawanie notatek normalych oraz szyfrowanych (zabezpieczonych dodatkowo hasłem)
- udostępnianie notatek innym użytkownikom
- podstawowe stylowanie notatek jak w markdown
- podgląd wszystkich posiadanych notatek

Zabezpieczenia:
- walidacja hasła (czy nie na liście najpowszechniejszych/pwned, czy hasło ma conajmniej 8 znaków w tym 1 dużą literę, 1 symbol, 1 cyfrę)
- połączenie przez https
- czyszczenie treści pod kątem XSS attack
- blokowanie podglądu do notatek do których dany użytkownik nie ma dostępu
- weryfikacja csrf
- szyfrowanie haseł/notatek
- blokowanie konta po nieudanych próbach logowania
