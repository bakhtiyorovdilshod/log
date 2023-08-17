from src.database import mongo_manager
from src.oauth_log.utils import log_helper


class OauthLogService:

    async def logs(self):
        db = mongo_manager.db
        logs = []
        for student in db.oauth_logs.find():
            logs.append(log_helper(student))
        return logs


oauth_log_service = OauthLogService()

