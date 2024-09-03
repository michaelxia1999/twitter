from pydantic import BaseModel, ConfigDict


# Base class for all data models entering and leaving routes, ensures all data models are in the correct format
class Model(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, from_attributes=True)
