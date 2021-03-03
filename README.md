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
| password   | password (optional)                                                      |

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



__Response__
```
Status: 200 Ok

{
    "id": "1519641b-c18c-4ecd-ad5b-d72383436aef",
    "first_name": "",
    "last_name": "",
    "email": "adawdawd@adfawd.co"
}
```


This an example of the email was sent
```
[2021-03-03 05:21:53,814: WARNING/ForkPoolWorker-2] Content-Type: multipart/alternative;
 boundary="===============2022195741176726036=="
MIME-Version: 1.0
Subject: Reset your Password!
From: panttojo@yandex.com
To: user@random.com
Date: Wed, 03 Mar 2021 05:21:53 -0000
Message-ID: <161474891381.165984.1170073708844176654@panttojo>

--===============2022195741176726036==
Content-Type: text/plain; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

You're receiving this email because you requested a password reset
for your user account.

Please go to the following page and choose a new password:

http://localhost:8000/reset-password/OGNmMGVlN2MtYWJkMi00NDJmLWEzOTUtMjE5NTU2YmIzMjk1::aix5kh-06a8a4435d1d7343177806a46a142da5/

Thanks for using our site!
--===============2022195741176726036==
Content-Type: text/html; charset="utf-8"
MIME-Version: 1.0
Content-Transfer-Encoding: 7bit

<p>You're receiving this email because you requested a password reset
for your user account.</p>

<p>Please go to the following page and choose a new password:
<a href="http://localhost:8000/reset-password/OGNmMGVlN2MtYWJkMi00NDJmLWEzOTUtMjE5NTU2YmIzMjk1::aix5kh-06a8a4435d1d7343177806a46a142da5/">Reset Password</a>
</p>

<p>Thanks for using our site!</p>
--===============2022195741176726036==--
[2021-03-03 05:21:53,818: WARNING/ForkPoolWorker-2] -------------------------------------------------------------------------------
```
