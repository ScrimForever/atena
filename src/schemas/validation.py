from pydantic import BaseModel, Field
from decimal import Decimal

class ValidationSchemaClientes(BaseModel):

    id: int
    name: str
    country: str


class ValidationSchemaPedidos(BaseModel):

    id: int
    client_id: int
    product: str
    price: Decimal = Field(decimal_places=2)
