from fastapi import APIRouter
from app.model.name_schema import NameRequest, NameResponse
from app.services.parser_service import ParserService
from app.model.contants import Country, NameSchema
from app.core.logging_config import logger_manager

router = APIRouter()
parser = ParserService()
log = logger_manager.get_logger(__name__)

@router.post("/parse-name", response_model=NameResponse)
async def parse_name(request: NameRequest):
    log.info(f"Request received: full_name={request.full_name}, country={request.country}")

    result = parser.search(request.full_name, request.country)

    response = NameResponse(
        first_name=str(result.get(NameSchema.first_name) or ""),
        last_name=str(result.get(NameSchema.last_name) or ""),
        chance=int(result.get(NameSchema.chance) or 0)
    )

    log.info(f"Result: {response}")
    return response


@router.get("/get-countries")
def get_countries():
    return {"countries": [c.value for c in Country]}

