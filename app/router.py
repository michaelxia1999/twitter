from app.auth.router import router as auth_rouer
from app.comment.router import router as comment_router
from app.follow.router import router as follow_router
from app.message.router import router as message_router
from app.notification.router import router as notification_router
from app.reaction.router import router as reaction_router
from app.tweet.router import router as tweet_rouer
from app.user.router import router as user_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(router=auth_rouer)
router.include_router(router=user_router)
router.include_router(router=tweet_rouer)
router.include_router(router=follow_router)
router.include_router(router=reaction_router)
router.include_router(router=comment_router)
router.include_router(router=message_router)
router.include_router(router=notification_router)
