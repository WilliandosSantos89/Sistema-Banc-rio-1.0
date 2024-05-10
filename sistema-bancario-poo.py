from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []

    def realizar tra