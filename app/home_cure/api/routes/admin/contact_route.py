from fastapi import APIRouter, Depends, HTTPException, status, Request


contact_router = APIRouter(prefix="/contact", tags=["Contact"])