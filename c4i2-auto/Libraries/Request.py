import json
import requests
import Libraries.Config as Config
from datetime import datetime


def SendRequest(txtUrl, txtMethod, payload=None, strToken=None, txtCookies=None):
    headers = {
        "Content-Type": "application/json",
        "authorization": f"bearer {strToken}" if strToken else "Basic dmJkOnZiZA=="
    }

    if txtCookies:
        headers["Cookie"] = txtCookies

    try:
        res = requests.request(txtMethod.upper(), txtUrl, json=payload, headers=headers)
        res.raise_for_status()
        return res
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")
        return None


def modifyPayload(txtDatetime, strCarnumber, routing_key):
    payload = {
        "vhost": "/",
        "name": "amq.default",
        "properties": {
            "delivery_mode": 2,
            "headers": {}
        },
        "routing_key": routing_key,
        "delivery_mode": "2",
        "payload": "\r\n[\r\n  { \"uuid\": { \"value\": \"89b26df1-1377-49f7-a1ef-ef445baf4724\", \"type\": \"uuid\" } },\r\n  { \"mime_type\": { \"value\": \"image/jpg\", \"type\": \"string\" } },\r\n  {\r\n    \"lpr_meta\": [\r\n      { \"datetime\": { \"value\": \"2023-08-09 15:29:08.000\", \"type\": \"string\" } },\r\n      { \"gmtdatetime\": { \"value\": \"2023-08-09 08:29:08.000\", \"type\": \"string\" } },\r\n      { \"carnumber\": { \"value\": \"65A22626\", \"type\": \"string\" } },\r\n      { \"carnumber_2\": { \"value\": \"65A22626\", \"type\": \"string\" } },\r\n      { \"timezone\": { \"value\": \"SE AST\", \"type\": \"string\" } },\r\n      { \"version\": { \"value\": \"6.3.171.5.202006221655\", \"type\": \"string\" } },\r\n      { \"latitude\": { \"value\": 10.8083834, \"type\": \"double\" } },\r\n      { \"longitude\": { \"value\": 106.664789, \"type\": \"double\" } },\r\n      { \"learn_username\": { \"value\": \"un02\", \"type\": \"string\" } },\r\n      { \"learn_agency\": { \"value\": \"2\", \"type\": \"string\" } },\r\n      { \"learn_systemname\": { \"value\": \"TruongSon\", \"type\": \"string\" } },\r\n      { \"cameraname\": { \"value\": \"TruongSon_PTZ\", \"type\": \"string\" } },\r\n      { \"accuracy\": { \"value\": 94, \"type\": \"int32\" } }\r\n    ]\r\n  }\r\n]",
        "payload_encoding": "string",
        "headers": {},
        "props": {}
    }

    # Convert the payload string to a dictionary
    payload_dict = json.loads(payload['payload'].strip())

    # Modify the datetime and carnumber values
    payload_dict[2]['lpr_meta'][0]['datetime']['value'] = txtDatetime
    payload_dict[2]['lpr_meta'][2]['carnumber']['value'] = strCarnumber
    payload_dict[2]['lpr_meta'][3]['carnumber_2']['value'] = strCarnumber

    # Convert the modified dictionary back to a string
    payload['payload'] = json.dumps(payload_dict, indent=2)

    return payload


def get_current_timestamp():
    """Get the current timestamp in the format YYYY-MM-DD HH:MM:SS.sss."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def EventSimulator(strCarnumber, txtDatetime=None, routing_key=None, rabbit_url=None, cookies=None):
    """
        Simulates an event by sending a POST request.

        Args:
            strCarnumber (str): The car number to notify.
            txtDatetime (str, optional): Datetime in "YYYY-MM-DD HH:MM:SS.sss". Defaults to current timestamp.
            routing_key (str, optional): Routing key. Defaults to Config.Default.routing_key.
            rabbit_url (str, optional): RabbitMQ URL. Defaults to Config.Default.rabbit_url.
            cookies (dict, optional): Request cookies. Defaults to Config.Default.cookies.

        Returns:
            bool: True if notification succeeds, else False.
        """
    # Sử dụng giá trị mặc định nếu không có giá trị được truyền vào
    txtDatetime = txtDatetime or get_current_timestamp()
    routing_key = routing_key or Config.Default.routing_key
    rabbit_url = rabbit_url or Config.Default.rabbit_url
    cookies = cookies or Config.Default.cookies

    # Tạo payload và gửi yêu cầu
    payload = modifyPayload(txtDatetime, strCarnumber, routing_key)
    print(payload)
    res = SendRequest(rabbit_url, "POST", payload, None, cookies)

    # Kiểm tra kết quả phản hồi
    if res.status_code == 200:
        print(f"Notify carnumber: {strCarnumber} is success")
        return True
    else:
        print(f"Notify carnumber: {strCarnumber} is not success")
        return False


# # Exampt
# 50F01053
routing_key = "vdfs_vig_lpr_staging_v6"
res = EventSimulator("50F02054")
if res:
    print("okie")
