# RESTful API for OTI Backend Oprec

## API Endpoints
1. **GET /**
   - Deskripsi  : Tes Run API.
   - Response   :
   ```json
    {
    "message": "Selamat! Anda berhasil masuk API, semangat debug"
    } 
   
2. **POST /register**
    - Deskripsi : Registrasi user baru dan mendapat ID.
    - Body (raw):
    ```
    {
    "username": "Geralt Rivia", 
    "password": "YennGang123" 
    }
    ```
    - Response  :
    ```json
    {
    "id": <id>,
    "message": "User berhasil dibuat"
    }
    ```
3. **POST /login**
    - Deskripsi : User login dengan username dan password yang telah dibuat kemudian mendapatkan token untuk akses database.
    - Body (raw):
    ```
    {
    "username": "Geralt Rivia", 
    "password": "YennGang123" 
    }
    ```
    - Response  :
    ```json
    {
        "token": "<token>" 
    }
    ```
4. **GET /users**
    - Deskripsi : Akses database seluruh user (id(otomatis) dan username).
    - Authorization Bearer Token : <token>
    - Response :
    ```json
    {
    "users": [
        {
            "id": 1,
            "username": "user"
        },
        {
            "id": 2,
            "username": "user1"
        }
      ]
    }
    ```
5. **DEL /delete/<int:id>**
    - Deskripsi : Hapus user dengan ID user.
    - Authorization Bearer Token: <token>
    - Response :
    ```json
    {
    "message": "User dengan ID 1, dengan nama Geralt Rivia berhasil dihapus"
    }
    ```
## Testing
- Semua endpoint diuji menggunakan Postman.
https://documenter.getpostman.com/view/39785938/2sAYBPmEoy
