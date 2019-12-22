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

| Number | API Link | Params                            | Method | Examples                                                     |
| ------ | -------- | --------------------------------- | ------ | ------------------------------------------------------------ |
| 1      | /        | id, name, birthday, school, phone | POST   | /?id=1&name="Hoàng Sơn Tùng"&birthday="08/08/1999"&school=ABCD&phone=0967134899 |
| 2      | /        | id                                | DELETE | /?id=1                                                       |

Remember to send DELETE request after get the id card.

## **Running This Service**

`chmod +x id_card_service_run.sh`

`./id_card_service_run.sh`

