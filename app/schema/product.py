from pydantic import (
    BaseModel,
    Field,
    AnyUrl,
    field_validator,
    model_validator,
    computed_field,
    EmailStr
)
from typing import Annotated, Literal, Optional, List
from uuid import UUID,uuid4
from datetime import datetime

#CREATE PYDANTIC
class Dimension(BaseModel):
    length:Annotated[float,Field(ge=0,strict=True,title="length of the product",description="product length",examples=[56.99,])]
    width:Annotated[float,Field(ge=0,strict=True,title="width of the product",description="product's width",examples=[67.87])]
    height:Annotated[float,Field(ge=0,strict=True,title="height of the product",
    description="product's height",examples=[90.67],),]
class Seller(BaseModel):
    seller_id: UUID

    name: Annotated[
        str,
        Field(
            min_length=5,
            
            title="seller's name",
            description="seller's name",
            examples=["apple store"],
        ),
    ]

    email:EmailStr
    website:AnyUrl
    @field_validator("email",mode="after")
    @classmethod
    def validate_seller_email_domain(cls,value:EmailStr):
        allowed_domains = [
        "mistore.in", "hpworld.in", "applestore.in", "oneplusshop.in",
        "techzone.in", "gadgethub.in", "mobileshop.in", "electronicsworld.in",
        "smartbuy.in", "techmart.in", "digishop.in", "techbazaar.in",
        "gizmo.in", "gadgetstore.in", "computercorner.in", "techplanet.in",
        "smarttech.in", "deviceshop.in", "electronicsplus.in", "techworld.in","example.com"]

        domain=str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"seller email domain not allowed:{domain}")

        return value




class Product(BaseModel):
    id: UUID=uuid4()

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=80,
            title="product name",
            description="readable product name (3-80 chars)",
            examples=["Xiaomi Model PRO", "Apple model x"],
        ),
    ]

    sku: Annotated[
        str,
        Field(
            min_length=6,
            max_length=30,
            title="SKU",
            description="stock keeping unit",
            examples=["xiao-7346-001"],
        ),
    ]

    description: Annotated[
        str,
        Field(max_length=200, description="short product description"),
    ]

    category: Annotated[
        str,
        Field(
            min_length=3,
            max_length=30,
            description="category like mobiles/laptops/electronics",
        ),
    ]

    brand: Annotated[
        str,
        Field(min_length=3, max_length=20, examples=["apple", "one plus"]),
    ]

    price: Annotated[
        float,
        Field(gt=0, strict=True, description="Base Price (INR)"),
    ]

    currency: Literal["INR"] = "INR"

    discount_percent: Annotated[
        float,
        Field(ge=0, le=90, description="discount in percent (0-90)"),
    ]

    stock: Annotated[
        int,
        Field(ge=0, description="available stock (>=0)"),
    ]

    is_active: Annotated[
        bool,
        Field(description="is product active?"),
    ]

    rating: Annotated[
        float,
        Field(ge=0, le=5, strict=True, description="Rating out of 5"),
    ]

    tags: Annotated[
        Optional[List[str]],
        Field(default=None, max_items=10, description="up to 10 tags"),
    ]

    image_urls: Annotated[
        List[AnyUrl],
        Field(min_items=1, description="at least one image url"),
    ]
    seller:Seller
    dimensions_cm:Dimension
    

    created_at: datetime
    
    

    @field_validator("sku", mode="after")
    @classmethod
    def validate_sku_format(cls, value: str):
        if "-" not in value:
            raise ValueError("SKU must contain '-'")

        last = value.split("-")[-1]
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with a 3-digit sequence like -234")

        return value

    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, then is_active must be false")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have a rating")

        return model
    @computed_field
    @property
    def final_price(self)->float:
        return  round(self.price*(1-self.discount_percent/100),2)

    @computed_field
    @property
    def  volume_of_product(self)->float:
        d=self.dimensions_cm
        return round(d.length*d.height*d.width,2)   
    








#UPDATE PYDANTIC

class DimensionUpdate(BaseModel):
    length:Optional[float]=Field(gt=0)
    width:Optional[float]=Field(gt=0)
    height:Optional[float]=Field(gt=0)
    
class SellerUpdate(BaseModel):
    

    name:Optional[str]=Field(min_length=2,max_length=60)

    email:Optional[EmailStr]
    website:Optional[AnyUrl]
    @field_validator("email",mode="after")
    @classmethod
    def validate_seller_email_domain(cls,value:EmailStr):
        allowed_domains = [
        "mistore.in", "hpworld.in", "applestore.in", "oneplusshop.in",
        "techzone.in", "gadgethub.in", "mobileshop.in", "electronicsworld.in",
        "smartbuy.in", "techmart.in", "digishop.in", "techbazaar.in",
        "gizmo.in", "gadgetstore.in", "computercorner.in", "techplanet.in",
        "smarttech.in", "deviceshop.in", "electronicsplus.in", "techworld.in","example.com"]

        domain=str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"seller email domain not allowed:{domain}")

        return value




class ProductUpdate(BaseModel):
    

    name: Optional[str]=Field(min_length=3,max_length=80)
    
    description:Optional[str]=Field(max_length=200)

    category:Optional[str]

    brand:Optional[str]

    price:Optional[float]=Field(gt=0)

    currency: Optional[Literal["INR"]]

    discount_percent:Optional[int]=Field(ge=0,le=90)

    stock:Optional[int]=Field(ge=0)


    is_active:Optional[bool]

    rating:Optional[float]=Field(ge=0,le=5)

    tags:Optional[List[str]]=Field(max_length=10)

    image_urls:Optional[
        List[AnyUrl]]
    seller:Optional[SellerUpdate]
    dimensions_cm:Optional[DimensionUpdate]
    

    created_at: datetime
    
    @model_validator(mode="after")
    @classmethod
    def validate_business_rules(cls, model: "Product"):
        if model.stock == 0 and model.is_active is True:
            raise ValueError("If stock is 0, then is_active must be false")

        if model.discount_percent > 0 and model.rating == 0:
            raise ValueError("Discounted product must have a rating")

        return model
    @computed_field
    @property
    def final_price(self)->float:
        return  round(self.price*(1-self.discount_percent/100),2)

    @computed_field
    @property
    def  volume_of_product(self)->float:
        d=self.dimensions_cm
        return round(d.length*d.height*d.width,2)   
    





        
