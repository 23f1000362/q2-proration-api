from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

app = FastAPI()


class Request(BaseModel):
    model_config = ConfigDict(extra="ignore")

    old_price: float
    new_price: float
    days_remaining: float
    days_in_actual_month: float
    spec: str


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/charge")
def charge(req: Request):
    spec = req.spec.strip().lower()

    diff = float(req.new_price) - float(req.old_price)

    if spec == "v1":
        charge = diff * (float(req.days_remaining) / 30.0)

    elif spec == "v2":
        if req.days_in_actual_month == 0:
            return JSONResponse(
                status_code=400,
                content={"error": "days_in_actual_month cannot be zero"},
            )
        charge = diff * (
            float(req.days_remaining)
            / float(req.days_in_actual_month)
        )

    else:
        return JSONResponse(
            status_code=400,
            content={"error": "invalid spec"},
        )

    return {"charge": float(charge)}
