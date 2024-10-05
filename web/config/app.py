from fastapi import FastAPI, HTTPException, Request
from sqlalchemy import text, CursorResult
from starlette.responses import JSONResponse

from web.config.database import database, async_session

# Create Web APP FastAPI
app: FastAPI = FastAPI(
    title="Flower AI Bot"
)


class AppDefaultHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        SingleTone Pattern
        """
        if not cls._instance:
            return super(AppDefaultHandler, cls).__new__(cls)
        if cls._instance:
            raise Exception("Only one instance of AppHandler can be created.")

    @staticmethod
    async def custom_http_exception_handler(
            request: Request,
            exc: HTTPException
    ) -> JSONResponse:
        """
        Custom HTTPException Response
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail
            }
        )

    @staticmethod
    async def startup():
        """
        Connect To DataBase
        """
        await database.connect()

    @staticmethod
    async def shutdown():
        """
        Disconnect To DataBase
        """
        await database.disconnect()

    @staticmethod
    async def app_status():
        """
        Just APP Status
        """
        return {
            "status": "success"
        }

    @staticmethod
    async def db_status():
        """
        Just for DB Status of Checking Successful Working with DB
        """
        async with async_session() as session:
            # Perform a Simple Query to Check Database Connection
            result: CursorResult = await session.execute(text("SELECT 1"))
            return JSONResponse(
                {
                    "result": result.scalar()
                },
                status_code=200
            )


app_default_handler: AppDefaultHandler = AppDefaultHandler()

app.add_exception_handler(HTTPException, app_default_handler.custom_http_exception_handler)

app.add_event_handler("startup", app_default_handler.startup)
app.add_event_handler("shutdown", app_default_handler.shutdown)

app.get("/app-status")(app_default_handler.app_status)
app.get("/db-status")(app_default_handler.db_status)
