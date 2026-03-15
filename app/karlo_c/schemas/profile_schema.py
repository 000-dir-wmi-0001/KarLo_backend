from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    full_name: str | None = None
    phone_number: str | None = None
    profile_picture: str | None = None
    bio: str | None = None
    country: str | None = None
    state: str | None = None
    city: str | None = None
    zip_code: str | None = None
    address: str | None = None
