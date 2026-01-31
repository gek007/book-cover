import requests
from IPython.display import Image
import os
from dotenv import load_dotenv
from typing import Optional
from PIL import Image as PILImage


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

    @staticmethod
    def _in_jupyter() -> bool:
        try:
            return get_ipython() is not None  # type: ignore
        except NameError:
            return False

    @staticmethod
    def show_image(data: bytes) -> None:
        if Book._in_jupyter():
            from IPython.display import display, Image

            display(Image(data))
        else:
            from PIL import Image as PILImage
            import io

            PILImage.open(io.BytesIO(data)).show()

    @classmethod
    def get_books(cls, my_query: str, limit: int = 3) -> list["Book"]:
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
                isbns = [
                    s[5:]
                    for s in doc["ia"]
                    if isinstance(s, str) and s.startswith("isbn_")
                ]
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
    def get_book_cover_image(isbn: str) -> Optional[bytes]:
        """Get book cover image from Open Library. No class/instance needed."""

        url = f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"

        response = requests.get(url)

        # this function return image .
        # display this image if status ok
        if response.status_code == 200 and len(response.content) > 0:
            content_type = response.headers.get("Content-Type", "")
            if content_type.startswith("image/"):
                print("Image found. Content-Type:", content_type)
                return response.content
            else:
                print("Content is not an image. Content-Type:", content_type)
                return None
        else:
            print("No content found or bad response")
            return None

    @classmethod
    def get_book_isbn(cls, books: Optional[list["Book"]]) -> Optional[str]:
        """get ISBN from books."""

        if not books:
            return None

        for book in books:
            if (
                book.isbns
                and book.isbns != "—"
                and book.isbns != ""
                and len(book.isbns) > 5
            ):
                isbns = (
                    [s.strip() for s in book.isbns.split(",")]
                    if "," in book.isbns
                    else [book.isbns]
                )
                for isbn in isbns:
                    if isbn:
                        return isbn
        return None


if __name__ == "__main__":
    query = "books written by James Patterson"
    books = Book.get_books(query)

    print("\n\nfound", len(books), f" books for query: {query}")
    if books:
        for book in books:
            print(book)

        isbn = Book.get_book_isbn(books)
        if isbn:
            print(f"retrieved ISBN: {isbn}")

            data = Book.get_book_cover_image(isbn)
            if data:
                print("retrieved image:")

                # To display an image in a Jupyter notebook, use:
                # from IPython.display import display
                # display(image)

                # If you are running a standard Python script, you can use PIL's show() method:
                Book.show_image(data)
            else:
                print("No image found")

        else:
            print("No ISBN found")
