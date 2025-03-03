def pm25_color(value: float) -> str:
    if value <= 10:
        return "green"
    elif value <= 25:
        return "yellowgreen"
    elif value <= 50:
        return "orange"
    elif value <= 75:
        return "orangered"
    else:
        return "red"


def pm10_color(value: float) -> str:
    if value <= 20:
        return "green"
    elif value <= 50:
        return "yellowgreen"
    elif value <= 100:
        return "orange"
    elif value <= 150:
        return "orangered"
    else:
        return "red"


def no2_color(value: float) -> str:
    if value <= 40:
        return "green"
    elif value <= 100:
        return "yellowgreen"
    elif value <= 200:
        return "orange"
    elif value <= 400:
        return "orangered"
    else:
        return "red"


def o3_color(value: float) -> str:
    if value <= 60:
        return "green"
    elif value <= 120:
        return "yellowgreen"
    elif value <= 180:
        return "orange"
    elif value <= 240:
        return "orangered"
    else:
        return "red"


def co_color(value: float) -> str:
    if value <= 4:
        return "green"
    elif value <= 10:
        return "yellowgreen"
    elif value <= 20:
        return "orange"
    elif value <= 30:
        return "orangered"
    else:
        return "red"


def so2_color(value: float) -> str:
    if value <= 20:
        return "green"
    elif value <= 50:
        return "yellowgreen"
    elif value <= 100:
        return "orange"
    elif value <= 200:
        return "orangered"
    else:
        return "red"


def voc_color(value: float) -> str:
    if value <= 100:
        return "green"
    elif value <= 300:
        return "yellowgreen"
    elif value <= 500:
        return "orange"
    elif value <= 700:
        return "orangered"
    else:
        return "red"


def color_by_sensor(sensor: str, value: float)-> str:
    sensor = sensor.upper()
    if sensor == "PM2.5":
        return pm25_color(value)
    elif sensor == "PM10":
        return pm10_color(value)
    elif sensor == "NO2":
        return no2_color(value)
    elif sensor == "O3":
        return o3_color(value)
    elif sensor == "CO":
        return co_color(value)
    elif sensor == "SO2":
        return so2_color(value)
    elif sensor == "VOC":
        return voc_color(value)
    else:
        return "red"
