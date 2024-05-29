from pydantic import BaseModel, EmailStr, validator, conint
from typing import Optional
from datetime import datetime

class DoacaoModel(BaseModel):
    nome: str
    cpf: Optional[str] = None
    cnpj: Optional[str] = None
    email: EmailStr
    telefone: str
    endereco: str
    horario: str
    alimento_id: str
    categoria: str
    alimento: str
    quantidade: conint(gt=0)
    validade: Optional[datetime] = None

    @validator('cpf')
    def cpf_must_be_valid(cls, v):
        if v is not None and len(v) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        return v

    @validator('cnpj')
    def cnpj_must_be_valid(cls, v):
        if v is not None and len(v) != 14:
            raise ValueError('CNPJ deve conter 14 dígitos')
        return v

class RecebimentoModel(BaseModel):
    alimento_id: str
    nome_recebedor: str
    quantidade_retirou: conint(gt=0)
    cnpj_recebedor: str
    email_recebedor: EmailStr

    @validator('cnpj_recebedor')
    def cnpj_must_be_valid(cls, v):
        if len(v) != 14:
            raise ValueError('CNPJ deve conter 14 dígitos')
        return v
