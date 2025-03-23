from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import select
from core.db.models.user import User
from core.db.models.result import Result, ResultEnum
from sqlalchemy.exc import SQLAlchemyError
from core.db.engine import async_session_factory
from logger import logger
from schemas.detector import UserResultResponse



async def get_user_results(user_id: int) -> List[Result]:
    """
    Retrieve all results for a given user by user_id.
    """
    try:
        async with async_session_factory() as session:
            query = select(Result.classified_at, Result.result).filter(Result.user_id == user_id)
            result = await session.execute(query)
            user_results = result.all()
            return [UserResultResponse(classified_at=r.classified_at, result=r.result) for r in user_results]
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database exception"
        else:
            msg = "Unknown exception"
        msg += ": can't get user results"
        extra = {
            "user_id": user_id
        }
        logger.error(msg, extra=extra, exc_info=True)


async def add_user_result(user_id: int, result_value: ResultEnum) -> Result:
    """
    Add a new result for the given user.

    Parameters:
        user_id (int): The ID of the user.
        result_value (ResultEnum): The result value (e.g., ResultEnum.healthy, ResultEnum.unhealthy, or ResultEnum.artifact).

    Returns:
        The newly created Result instance.
    """
    try:
        async with async_session_factory() as session:
            new_result = Result(result=result_value, user_id=user_id)
            session.add(new_result)
            await session.commit()
            await session.refresh(new_result)
            return new_result
    except (SQLAlchemyError, Exception) as e:
        if isinstance(e, SQLAlchemyError):
            msg = "Database exception"
        else:
            msg = "Unknown exception"
        msg += ": can't add user result"
        extra = {"user_id": user_id}
        logger.error(msg, extra=extra, exc_info=True)
        raise
