from fastapi import APIRouter, Request, Response
from repository import MailRepository
from dtypes import APIResponse, HttpStatus
from util import Mailer, CustomLogger


router = APIRouter(prefix="/api/v1/mail", tags=["Mail"])
mail_service = MailRepository(
    mailer=Mailer(),
    logger=CustomLogger("MailService")
)


@router.post("/send")
async def send_mail(request: Request, response: Response):
    body = await request.json()
    mail_type = body.get("type", None)
    data = body.get("data", None)
    if mail_type is None or data is None:
        response.status_code = 400
        return APIResponse(
            status=HttpStatus.BAD_REQUEST, 
            data=None, 
            message="Mail type and data are required"
        )
    success, data = mail_service.send_mail(mail_type, data)
    if not success:
        response.status_code = 500
        return APIResponse(
            status=HttpStatus.INTERNAL_SERVER_ERROR, 
            data=None, 
            message="Failed to send mail"
        )
    response.status_code = 201
    return APIResponse(
        status=HttpStatus.CREATED, 
        data=data, 
        message="Mail sent successfully"
    )