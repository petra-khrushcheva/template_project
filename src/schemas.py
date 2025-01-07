from pydantic import BaseModel, ConfigDict


class UserCountStatistics(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_count: int
