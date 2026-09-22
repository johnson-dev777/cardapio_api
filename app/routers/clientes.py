from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import obter_sessao
from app.models import Cliente, ClienteCreate, ClienteUpdate


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.post(
    "/",
    response_model=Cliente,
    status_code=status.HTTP_201_CREATED
)
def criar_cliente(
    cliente: ClienteCreate,
    session: Session = Depends(obter_sessao)
):
    novo_cliente = Cliente.model_validate(cliente)

    session.add(novo_cliente)
    session.commit()
    session.refresh(novo_cliente)

    return novo_cliente


@router.get(
    "/",
    response_model=List[Cliente]
)
def listar_clientes(
    session: Session = Depends(obter_sessao)
):
    clientes = session.exec(
        select(Cliente)
    ).all()

    return clientes


@router.get(
    "/{cliente_id}",
    response_model=Cliente
)
def buscar_cliente(
    cliente_id: int,
    session: Session = Depends(obter_sessao)
):
    cliente = session.get(Cliente, cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    return cliente


@router.put(
    "/{cliente_id}",
    response_model=Cliente
)
def atualizar_cliente(
    cliente_id: int,
    dados: ClienteUpdate,
    session: Session = Depends(obter_sessao)
):
    cliente = session.get(Cliente, cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    dados_atualizados = dados.model_dump(exclude_unset=True)

    for campo, valor in dados_atualizados.items():
        setattr(cliente, campo, valor)

    session.add(cliente)
    session.commit()
    session.refresh(cliente)

    return cliente


@router.delete(
    "/{cliente_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def excluir_cliente(
    cliente_id: int,
    session: Session = Depends(obter_sessao)
):
    cliente = session.get(Cliente, cliente_id)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente não encontrado"
        )

    session.delete(cliente)
    session.commit()

    return None
