from codecs import ascii_encode
import pandas as pd
from utils import *

filename = "data/Employees.csv"

class SecurePII:
    def __init__(self, filename=filename, mysql=False):
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
        

    
    def to_hash(self, columns=['PhoneNumber']):

        from hashlib import sha256 

        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: lambda x: sha256(x.encode()).hexdigest())
        return self
        # for c in columns:
        #     self.df[c] = self.df[c].apply(lambda x: sha256(x.encode()).hexdigest())
        # return self

    def to_mask(self, columns=['EmailAddress']):
        from faker import Faker
        fake = Faker()
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: fake.email())
        return self

    def to_encrypt(self, columns=['NationalIDNumber']):
        key = generate_key("keys/columns.key")
        f = Fernet(key)
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: f.encrypt(bytes(str(x),'utf-8')))
        return self

    def rsa_encrypt(self, columns=['Gender']):
        n = 143
        d_key = int(get_key("keys/rsa_d.key"))
        # print(d_key)
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: pow(text_to_int(x), d_key, n))
        return self


    def rsa_decrypt(self, columns=['Gender']):
        n = 143
        e_key = int(get_key("keys/rsa_e.key"))
        # print(e_key)
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: int_to_text(pow(x, e_key, n)))
        return self
        


    def to_decrypt(self, columns=['NationalIDNumber']):
        key = get_key("keys/columns.key")
        f = Fernet(key)
        self.df = columns_apply(\
            df = self.df, 
            columns = columns, 
            func = lambda x: int(f.decrypt(x).decode()))
        return self

        
        

    def __repr__(self) -> str:
        print(self.df)
        return ""
        

if __name__ == "__main__":
    
    from pandas import testing as tm

    """ Test csv column implementation """

    secure = SecurePII('data/Employees.csv')
    before = secure.df['NationalIDNumber']
    encrypt = secure.to_hash().to_mask().to_encrypt().df['NationalIDNumber']
    after = secure.to_decrypt().df['NationalIDNumber']
    tm.assert_series_equal(before, after)
    
    """ Test MySQL Database implementation """

    secure = SecurePII(mysql=True)
    before = secure.df['NationalIDNumber']
    encrypt = secure.to_hash().to_mask().to_encrypt().df['NationalIDNumber']
    after = secure.to_decrypt().df['NationalIDNumber']
    tm.assert_series_equal(before, after)

    """ Test Simple RSA implementation """

    secure = SecurePII('data/Employees.csv')
    before = secure.df['Gender']
    enc =  secure.rsa_encrypt()
    after = secure.rsa_decrypt().df['Gender']
    tm.assert_series_equal(before, after)
   