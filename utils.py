from cryptography.fernet import Fernet


def generate_key(filename="keys/key.key"):

    key = Fernet.generate_key()
    with open(filename, 'wb') as key_file:
        key_file.write(key)
    return key


def get_key(filename="keys/key.key"):
    with open(filename, 'rb') as key_file:
        key = key_file.read()
    
    return key

def columns_apply(df, columns, func):
    for c in columns:
            df[c] = df[c].apply(func)
    return df

def text_to_int(text):
    return int(text.encode('utf-8').hex(), 16)
    

def int_to_text(number):

    return bytes\
        .fromhex(hex(number)[2:])\
        .decode(encoding="utf-8")


if __name__ == "__main__":
    a = text_to_int("hello")
    print(a)
    b = int_to_text(a)
    print(b)