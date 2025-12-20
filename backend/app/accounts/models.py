from beanie import Document, Indexed
from pydantic import EmailStr
from typing import Optional, Annotated
 

# object of class of Document subclass will be saved in the db 
# the Document class was inherited from pydantic BaseModel package

class User(Document):
    name: str
    email: Annotated[EmailStr, Indexed(unique=True)]

    hashed_password: Optional[str] = None

    # Annotated is used to add metadata to the type hint --> here Indexed is metaData and None is the default value
    # indexing makes sure there is fast lookup on these fields --> since we query according to email and google_id mostly
    google_id: Optional[Annotated[str | None, Indexed(unique=True, sparse=True)]] = None
    is_active: bool = True
    is_verified: bool = False

    class Settings:
        name = "users"
        indexes = [
            "email",
            "google_id",
        ]

