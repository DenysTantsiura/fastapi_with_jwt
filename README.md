# fastapi_with_jwt

hometask. jwt authorization

poetry add python-jose["cryptography"]
poetry add passlib["bcrypt"]
poetry add python-multipart

python-jose["cryptography"] - це пакет, який надає функціональність для роботи з JSON Web Tokens (JWT) та допомагає створювати безпечні токени аутентифікації та авторизації для REST API
passlib["bcrypt"] пакет необхідний для хешування паролів користувачів. Хешування паролів необхідно, щоб їх не можна було відновити у вихідний вигляд, навіть, якщо дані витечуть з бази даних.
python-multipart - цей пакет для роботи з файлами у форматі multipart/form-data, який є основним форматом для завантаження файлів по HTTP, необхідний у цьому випадку для правильної роботи FastAPI.
