from fastapi import APIRouter, HTTPException, Query, Request, status

from app.karlo_c.schemas import geocode_schema
from app.karlo_c.services.geocoding import geocoding_service


geocode_router = APIRouter(prefix="/geocode", tags=["Geocode"])


def _client_key(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else "unknown"


@geocode_router.get("/search", response_model=geocode_schema.GeocodeSearchResponse)
def search_places(request: Request, q: str = Query(min_length=2, max_length=200)):
    try:
        results = geocoding_service.search_places(q, _client_key(request))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Geocoding service unavailable") from exc

    return {"results": results, "total": len(results)}


@geocode_router.post("/reverse", response_model=geocode_schema.ReverseGeocodeResponse)
def reverse_geocode(payload: geocode_schema.ReverseGeocodeRequest, request: Request):
    try:
        result = geocoding_service.reverse_geocode(payload.lat, payload.lon, _client_key(request))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Geocoding service unavailable") from exc

    return {"result": result}