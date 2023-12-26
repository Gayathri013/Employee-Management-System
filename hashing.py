from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"] , deprecated = ["auto"])

class Hasher:

    @staticmethod
    def get_hash(plain_password):
        return pwd_context.hash(plain_password)
    
    @staticmethod
    def verify_pass(plain_password , hash_password):
        return pwd_context.verify(plain_password , hash_password)

