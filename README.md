AIM : Masking/ Shuffling/ Encoding/ Decoding 
        PII columnar data 
        from different sources
        for HIPAA compliance
implemented: 
    1. SHA256 hash masking - to_hash()
    2. Fake masking - to_mask()
    3. Fernet Encoding/ Decoding - to_encrypt()/ to_decrypt()
    4. Simple RSA encryption/ decryption - rsa_encrypt()/ rsa_decrypt()
        -At this moment, using a very small n value and hence only 1 characted input like gender can be used

Note:   Column names, algorithms are all hardcoded. 
        Consider using decorators/ separate parent class for different functions
        import libraries dynamically
        encrypt each file storing the keys


Testing functionality:

> python securePII.py

Setting up MySQL database (for hardcoded config)
- download and install MySQL workbench (or compatible)
- add a connection inside MySQL
    - connection method: TCP/IP
    - hostname: localhost
    - port: 3500
    - username:python_client
    - password:1_am_python)
- open connection
- run script mysql/employees_employees.sql to populate tables



