# Karbit

by Dimas Maulana

---

## Flag

```
gemastik{S3l4m4t_anda_t3lah_m3nj4d1_r4j4_karbit}
```

## Description
Setelah bertahun tahun menjadi orang normal, akhirnya kamu berkesempatan untuk menjadi raja Karbit. Tapi, untuk menjadi raja Karbit, kamu harus menyelesaikan tantangan yang diberikan oleh raja Karbit sebelumnya. Kamu harus bisa membuktikan bahwa kamu bisa mencuri data rahasia dari raja Karbit sebelumnya. Curi data tersebut dan buktikan bahwa kamu layak menjadi raja Karbit.

## Difficultys
medium

## Hints
* it's seems you need something to bypass the alert, try to learn how sanboxing works. Note, this may require us to deploy our own http server, i suggest you to use `ngrok tcp <port>` command to expose your local server to the internet.
* the cookie is set to SameSite=Strict, the browser will block the cookie from being sent in a cross-site request, try to learn how origin works and what you can do to access "non-restricted" context from "restricted" context.
## Tags
XSS, XSS Sanitizer Bypass, SameSite Strict Bypass, Alert and Location Redirect Bypass

## Deployment
Penjelasan cara menjalankan service yang dibutuhkan serta requirementsnya.
- Install docker engine>=19.03.12 and docker-compose>=1.26.2.
- Run the container using:
    ```
    docker-compose up --build --detach
    ```

## Attachment
- ./dist.zip
