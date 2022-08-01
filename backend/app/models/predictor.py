from pydantic import BaseModel, Field

import uuid

class MongoBaseModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id", examples=[
                    'NA1_4387530978-wgvrKfcuCGDmgyrUmiXknS41acg6Y26hfQwsXNj_eJ86Tv8_Bb7SBOUVSQqI1JdyBSmq92XGDrGYHA'])

class Predictor(BaseModel):
    pass
