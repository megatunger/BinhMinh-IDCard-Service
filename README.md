# **Binh Minh Student ID Card (API Service)**

**Written in**: Python

## How it works?

Use plain.png for template and draw text via draw library

## Execute Using Terminal

```
main.py [student_id, name, birthday, school, phone]
```

**Example**

```
main.py 2 "Hoàng Sơn Tùng" 08/08/1999 "THPT Chuyên Hà Nội Amsterdam" 0967134899
```

**Output**

Filepath to image

## **API Examples**

| Number | API Link | Params                            | Method | Examples                                                     | Responses                                                    |
| ------ | -------- | --------------------------------- | ------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 1      | /        | id, name, birthday, school, phone | POST   | /?id=1&name="Hoàng Sơn Tùng"&birthday="08/08/1999"&school=ABCD&phone=0967134899 | {"card_image":"output/png/2.png","pdf":"output/pdf/2.pdf","qr_image":"output/qr/2.png"}. Use this to combine with server path to download it like "http://binhminh-idcard-service.megatunger.codes/ouput/png/2.png" |
| 2      | /        | id                                | DELETE | /?id=1                                                       | Success                                                      |

Remember to send DELETE request after get the id card.
