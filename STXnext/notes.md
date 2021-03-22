#Books REST API

##TRESC:

Na podstawie danych znajdującej się na stronie https://www.googleapis.com/books/v1/volumes?q=Hobbit zaprojektować i stworzyć aplikację w wybranym przez siebie frameworku, która będzie posiadała proste REST API:

1.GET /books - lista wszystkich książek (widok powinien pozwalać na filtrowanie i sortowanie po roku przykład : /books?published_date=1995, /books?sort=-published_date)

2.GET /books?author="Jan Kowalski"&author="Anna Kowalska" - lista książek zadanych autorów

3.GET /books/<bookId> - wybrana książka 
{
    "title": "Hobbit czyli Tam i z powrotem",
    "authors": ["J. R. R. Tolkien"],
    "published_date": "2004",
    "categories": [
        "Baggins, Bilbo (Fictitious character)"
      ],
    "average_rating": 5,
    "ratings_count": 2,
    "thumbnail": "http://books.google.com/books/content?id=YyXoAAAACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api",
}

4.POST /db z body {"q": "war"}
ściągnąć data set z https://www.googleapis.com/books/v1/volumes?q=war
wrzucić do bazy danych wpisy (aktualizując już istniejące)



##DO ZAPAMIETANIA:

- GITHUB: dodaj opis projektu jaki jezyk biblioteki itp oraz plik readme
- view decorators
- requirements.txt

##STEPS:
 ### - models, views, urls, configuration
0. Skonfiguruj baze danych - SQlite3 ✔
   

1. Zrób modele Autor, Ksiazka: ✔


2. Napisz zautomatyzowane testy do modeli ✔



3. Zrob funkcje w widokach ktora zapisuje wszystkie UNIKALNE ksiazki z nazwą "hobbit" do bazy  ✔
   

4. Napisz testy do pomocniczych funkcji oraz widoków ✔
   

6. Stwórz bazowy template oraz inne ktore po nim dziedzicza, dodaj do niego messages ✔
   


### - Rest api:
7. Filtrowanie i sortowanie po roku wydania ✔



8. Lista książek zadanych autorów ✔



9. GET /books/<bookId> - wybrana książka ✔



10. POST /db z body {"q": "war"}
ściągnąć data set z https://www.googleapis.com/books/v1/volumes?q=war
wrzucić do bazy danych wpisy ✔
    


### - Frontend:
11. Dodanie linkow do przemieszczania sie po aplikacji w html 
12. dodanie css i stylizacja ✔
  


### - Deployment:
13. Wrzuć aplikacje na heroku X

