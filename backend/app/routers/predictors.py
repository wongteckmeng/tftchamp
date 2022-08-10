from fastapi import APIRouter, Depends

from models.predictor import Predictor, PredictionInput, PredictionOutput, MDIOutput, get_model
from models.match import Match

model_router = APIRouter()


@ model_router.get("/prediction", response_model=MDIOutput)
async def models(
        model: Predictor = Depends(get_model)) -> MDIOutput:
    output: MDIOutput = model.get_mdi()
    return output


@ model_router.post("/prediction", response_model=PredictionOutput)
async def prediction(
        request: Match,
        model: Predictor = Depends(get_model)) -> PredictionOutput:
    output: PredictionOutput = model.predict(request)
    return output


@ model_router.on_event("startup")
async def startup():
    """Initialize the tftchamp pipeline"""
    get_model().load_model()
