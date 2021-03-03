Talana
==============================

__Version:__ 0.0.0

Pequeño sorteo de prueba
------------------------------------------

# Endpoints

## Register

```
POST /api/auth/register
```

__Parameters__

| Name       | Description                                                |
| ---------- | ------------------------------------------------------------------------ |
| email      | email of the user. Errors out if email already registered.               |
| first_name | first name of the user.                                                  |
| last_name  | last name of the user.                                                   |

**Request**

```json
{
    "username": "test",
    "email": "hello@example.com",
    "first_name": "S",
    "last_name": "K"
}
```

__Response__

```json

Status: 201 Created
{
    "auth_token": "eyJ0eXAiOiJKV1QiLCJh",
    "email": "test@test.com",
    "id": "f9dceed1-0f19-49f4-a874-0c2e131abf79",
    "first_name": "S",
    "last_name": "K"
}
```

## Confirm password reset

Confirm password reset for the user using the token sent in email.

```
POST /api/auth/password_reset_confirm
```

__Parameters__

Name          | Description
--------------|-------------------------------------
new_password  | New password of the user
token         | Token decoded from the url (verification link)


__Request__
```json
{
    "new_password": "new_pass",
    "token" : "IgotTHISfromTHEverificationLINKinEmail"
}
```

__Response__
```
Status: 204 No-Content
```

!!!Note
    The verification link uses the format of key `password-confirm` in `FRONTEND_URLS` dict in settings/common.


## Get the winner

```
GET /api/get_winner  (requires authentication)
```


__Request__
```json
{
    "id": "1519641b-c18c-4ecd-ad5b-d72383436aef",
    "first_name": "",
    "last_name": "",
    "email": "adawdawd@adfawd.co"
}
```

__Response__
```
Status: 200 Ok
```
