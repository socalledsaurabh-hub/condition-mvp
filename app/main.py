from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
import logging
from fastapi.templating import Jinja2Templates
from app.models import CaseRequest, AnalyzeResponse
from app.services.ai_service import analyze_case

app = FastAPI(title="Condition MVP API")
templates = Jinja2Templates(directory="app/templates")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


    

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc)
        }
    )

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_case_endpoint(request: Request, body: CaseRequest):

    logger.info(
        f"Analyze request | age={body.age} | "
        f"gender={body.gender} | "
        f"symptom_count={len(body.symptoms)}"
    )

    
    raw_result = analyze_case(
        age=body.age,
        gender=body.gender,
        symptoms=body.symptoms,
        duration=body.duration
    )

    
    predictions = sorted(
        raw_result,
        key=lambda x: x["probability"],
        reverse=True
    )

    
    for item in predictions:
        item["probability"] = round(item["probability"], 2)

    
    prediction_confidence = predictions[0]["probability"]

    
    if prediction_confidence > 0.75:
        certainty_level = "High"
    elif prediction_confidence > 0.4:
        certainty_level = "Moderate"
    else:
        certainty_level = "Low"

    logger.info("Analyze completed successfully")

    
    return {
        "success": True,
        "predictions": predictions,
        "prediction_confidence": prediction_confidence,
        "certainty_level": certainty_level,
        "disclaimer": (
            "This AI system is for informational purposes only and does not "
            "constitute medical advice. Please consult a licensed healthcare professional."
        )
    }


