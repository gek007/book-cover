import requests
from IPython.display import Image
import os
from dotenv import load_dotenv


pushover_url = "https://api.pushover.net/1/messages.json"

class Book:

   def __init__(
        self,
        title: str = "",
        author: str = "",
        year: int = 0,
        isbns: str = "",
    ):
        self.title = title
        self.author = author
        self.year = year
        self.isbns = isbns
        load_dotenv(override=True)
        self.pushover_user = os.getenv("PUSHOVER_USER")
        self.pushover_token = os.getenv("PUSHOVER_TOKEN")

   def __str__(self) -> str:
        return f"{self.title} — {self.author} ({self.year}) ISBN: {self.isbns}"

   def push(self, message: str) -> None:
        payload = {
            "user": self.pushover_user,
            "token": self.pushover_token,
            "message": message,
        }
        requests.post(pushover_url, data=payload)


   @classmethod
   def get_books(cls, my_query: str, limit: int = 5) -> list["Book"]:
        """Get books from Open Library API. Uses cls so subclasses get their type."""
        url = "https://openlibrary.org/search.json"
        params = {
            "q": my_query,
            "limit": limit,
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        books = []

        for doc in data["docs"]:
            isbns = doc.get("isbn")
            if not isbns and "ia" in doc:
                isbns = [s[5:] for s in doc["ia"] if isinstance(s, str) and s.startswith("isbn_")]
            isbn_str = ", ".join(isbns) if isbns else "—"

            book = cls(
                title=doc.get("title", ""),
                author=", ".join(doc.get("author_name", [])),
                year=doc.get("first_publish_year") or 0,
                isbns=isbn_str,
            )
            books.append(book)


        for book in books:
            print(book)

        return books




   @staticmethod
   def get_book_cover_image(isbn: str) -> Image | None:
        """Get book cover image from Open Library. No class/instance needed."""

        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

        response = requests.get(url)

        # this function return image . 
        # display this image if status ok
        if response.status_code == 200:
            if len(response.content) > 0:
                print(response.content)
                return Image(response.content)
            else:
                print("No content found")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None

   @classmethod
   def find_book_cover(cls, query: str) -> Image | None:
        """Find book cover image: fetches books via cls.get_books, then tries cover by ISBN."""
        books = cls.get_books(query)
        for book in books:
            if book.isbns:
                isbns = [s.strip() for s in book.isbns.split(",")] if "," in book.isbns else [book.isbns]
                for isbn in isbns:
                    image = cls.get_book_cover_image(isbn)
                    if image:
                        return image
        return None









    
