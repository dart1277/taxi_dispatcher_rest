from pydantic import BaseModel, ConfigDict


class DtoBaseModel(BaseModel):
    model_config = ConfigDict(extra='forbid',
                              validate_assignment=True,
                              strict=True,
                              validate_default=True,
                              validate_return=True,
                              use_enum_values=True
                              )
