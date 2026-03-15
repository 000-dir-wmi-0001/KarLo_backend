from pydantic import BaseModel, Field


class GeocodeSearchResult(BaseModel):
    display_name: str | None = None
    lat: float
    lon: float


class GeocodeSearchResponse(BaseModel):
    results: list[GeocodeSearchResult]
    total: int


class ReverseGeocodeRequest(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)


class ReverseGeocodeResponse(BaseModel):
    result: GeocodeSearchResult