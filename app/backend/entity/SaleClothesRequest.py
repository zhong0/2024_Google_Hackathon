from pydantic import BaseModel, field_validator, confloat, constr

class SaleClothesRequest(BaseModel):
    username: str
    filename: str
    size: str
    brand: str
    owner_description: constr(max_length=100)
    price: confloat(gt=0)

    @field_validator('price')
    def check_price(cls, value):
        if value < 0:
            raise ValueError("Price must be greater than 0")
        return value
    
    @field_validator('owner_description')
    def check_description_length(cls, value):
        if len(value) > 100:
            raise ValueError("Owner description must not exceed 100 characters")
        return value