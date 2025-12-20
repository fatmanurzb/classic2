from abc import ABC, abstractmethod

class BaseCipher(ABC):

    @abstractmethod
    def encrypt(self, text, key=None):
        pass

    @abstractmethod
    def decrypt(self, text, key=None):
        pass
