import pandas as pd
from utils import *

from hashlib import sha256

filename = "data/Employees.csv"


class SecurePII:
    def __init__(self, filename=filename, algorithm='hash1', mysql=False):
        if mysql:
            # consider using SQLAlchemy for wider support of databases
            import MySQLdb
            cnx = MySQLdb.connect(
                user= 'python_client',
                password= '1_am_python',
                host= '127.0.0.1', 
                port=3500,
                db='employees')

            self.df = pd.read_sql("select * from employees;", con=cnx)
            cnx.close()
        else:
            self.df = pd.read_csv(filename)
        
        if algorithm == 'mask':
            hash_columns = ['EmailAddress']
            self.df[hash_columns] = self.to_mask(self.df[hash_columns])

        if algorithm == 'hash':
            hash_columns = ['PhoneNumber']
            self.df[hash_columns] = self.to_hash(hash_columns)
            # print(self.df)

    """decorator to perform encryption and masking
       Parameters: 
        1. Encryption function "operation" to apply to specified columns
        2. calls the encryption algorithm 
    """
    def encrypt(operation, columns):
        def algo(func):
            func(self, columns, *args, **kwargs)
            for c in columns:
                self.df[c] = self.df[c].apply(operation)
            return self
        return algo
    
    @encrypt(operation = lambda x: sha256(x.encode()).hexdigest(), columns=['PhoneNumber'])
    def hash1(self,hash_type = "sha256"):
        return
        

    def to_hash(self, columns=['PhoneNumber'],hash_type = "sha256"):

        from hashlib import sha256 

        for c in columns:
            self.df[c] = self.df[c].apply(lambda x: sha256(x.encode()).hexdigest())
        return self

    def to_mask(self, columns=['EmailAddress'], fakes=['email']):
        from faker import Faker
        fake = Faker()
        # for c in columns:
        #     self.df[c] = self.df[c].apply(lambda x: fake.email())
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: fake.email())
        return self

    def to_encrypt(self, columns=['NationalIDNumber']):
        key = generate_key("keys/columns.key")
        f = Fernet(key)
        # for c in columns:
        #     self.df[c] = self.df[c].apply(lambda x: f.encrypt(bytes(str(x),'utf-8')))
        # return self
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: f.encrypt(bytes(str(x),'utf-8')))
        return self
        

    def to_decrypt(self, columns=['NationalIDNumber']):
        key = get_key("keys/columns.key")
        f = Fernet(key)
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: int(f.decrypt(x).decode()))
        return self

        # for c in columns:
        #     self.df[c] = self.df[c].apply(lambda x: int(f.decrypt(x).decode()))
        # return self
        

    def __repr__(self) -> str:
        print(self.df)
        return ""
        

if __name__ == "__main__":

    from pandas import testing as tm


    # secure = SecurePII('data/Employees.csv')
    # before = secure.df['NationalIDNumber']
    # encrypt = secure.to_hash().to_mask().to_encrypt().df['NationalIDNumber']
    # after = secure.to_decrypt().df['NationalIDNumber']
    # tm.assert_series_equal(before, after)
    

    # secure = SecurePII(mysql=True)
    # before = secure.df['NationalIDNumber']
    # encrypt = secure.to_hash().to_mask().to_encrypt().df['NationalIDNumber']
    # after = secure.to_decrypt().df['NationalIDNumber']
    # tm.assert_series_equal(before, after)

    secure = SecurePII('data/Employees.csv')
    print(secure.hash1().df['PhoneNumber'])