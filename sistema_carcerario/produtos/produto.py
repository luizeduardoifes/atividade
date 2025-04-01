from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class Presidiario(BaseModel):
    id: Optional[int] = None
    nome: str
    data_nascimento: date
    crime: str
    cela: int

    @field_validator('id')
    def validar_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('O id do presidiário não pode ser negativo ou zero.')
        return v

    @field_validator('nome')
    def validar_nome(cls, v):
        nome_limpo = v.strip()
        if not nome_limpo:
            raise ValueError('O nome do presidiário não pode ser vazio.')
        if len(nome_limpo) > 100:
            raise ValueError('O nome do presidiário não pode exceder 100 caracteres.')
        return nome_limpo

    @field_validator('crime')
    def validar_crime(cls, v):
        crime_limpo = v.strip()
        if not crime_limpo:
            raise ValueError('O crime não pode ser vazio.')
        if len(crime_limpo) > 200:
            raise ValueError('A descrição do crime não pode exceder 200 caracteres.')
        return crime_limpo

    @field_validator('cela')
    def validar_cela(cls, v):
        if v <= 0:
            raise ValueError('O número da cela deve ser maior que zero.')
        return v
