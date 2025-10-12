from fastapi import APIRouter, Depends, HTTPException, status, Request

user_router = APIRouter(prefix="/user", tags=["User"])