from machine import Pin, I2C
import time

# =========================
# LCD 16x2 I2C
# =========================

class LCD1602:
    def __init__(self, i2c, addr=0x27):
        self.i2c = i2c
        self.addr = addr

    def write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data | 0x08]))

    def pulse_enable(self, data):
        self.write_byte(data | 0x04)
        time.sleep_us(1)
        self.write_byte(data & ~0x04)
        time.sleep_us(50)

    def send(self, data, mode):
        high = data & 0xF0
        low = (data << 4) & 0xF0

        self.write_byte(high | mode)
        self.pulse_enable(high | mode)

        self.write_byte(low | mode)
        self.pulse_enable(low | mode)

    def command(self, cmd):
        self.send(cmd, 0)

    def write(self, char):
        self.send(char, 1)

    def clear(self):
        self.command(0x01)
        time.sleep_ms(2)

    def set_cursor(self, row, col):
        self.command(0x80 + (0x40 * row) + col)

    def print_text(self, text):
        for char in text:
            self.write(ord(char))

    def init(self):
        time.sleep_ms(50)
        self.command(0x33)
        self.command(0x32)
        self.command(0x28)
        self.command(0x0C)
        self.command(0x06)
        self.clear()


# =========================
# LCD
# =========================

i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)
lcd = LCD1602(i2c)


# =========================
# BOTÕES
# =========================

botao_1 = Pin(14, Pin.IN, Pin.PULL_UP)
botao_2 = Pin(15, Pin.IN, Pin.PULL_UP)
botao_3 = Pin(16, Pin.IN, Pin.PULL_UP)


# =========================
# LEDS
# =========================

leds = {
    "EV1": {
        "verde": Pin(6, Pin.OUT),
        "amarelo": Pin(7, Pin.OUT),
        "vermelho": Pin(8, Pin.OUT)
    },
    "EV2": {
        "verde": Pin(9, Pin.OUT),
        "amarelo": Pin(10, Pin.OUT),
        "vermelho": Pin(11, Pin.OUT)
    },
    "EV3": {
        "verde": Pin(12, Pin.OUT),
        "amarelo": Pin(13, Pin.OUT),
        "vermelho": Pin(18, Pin.OUT)
    }
}


# =========================
# DADOS DOS VEÍCULOS
# =========================

veiculos = [
    {"id": "EV1", "bateria": 40, "solicitada": 2000},
    {"id": "EV2", "bateria": 70, "solicitada": 2500},
    {"id": "EV3", "bateria": 25, "solicitada": 3000}
]


def desligar_leds():
    for carro in leds.values():
        for led in carro.values():
            led.value(0)


def definir_led(veiculo, potencia):
    carro = leds[veiculo["id"]]

    for led in carro.values():
        led.value(0)

    if potencia >= veiculo["solicitada"]:
        carro["verde"].value(1)
    elif potencia > 0:
        carro["amarelo"].value(1)
    else:
        carro["vermelho"].value(1)


def gerenciar(energia):
    demanda = sum(v["solicitada"] for v in veiculos)
    resultados = {}

    # Energia suficiente: todos recebem o solicitado.
    if energia >= demanda:
        for veiculo in veiculos:
            resultados[veiculo["id"]] = veiculo["solicitada"]

    # Energia limitada: distribuição proporcional.
    elif energia >= 4000:
        for veiculo in veiculos:
            potencia = veiculo["solicitada"] * energia // demanda
            resultados[veiculo["id"]] = potencia

    # Energia muito baixa: prioriza a menor bateria.
    else:
        prioritario = min(veiculos, key=lambda v: v["bateria"])

        for veiculo in veiculos:
            if veiculo["id"] == prioritario["id"]:
                resultados[veiculo["id"]] = energia
            else:
                resultados[veiculo["id"]] = 0

    return resultados


def mostrar_serial(energia, resultados):
    demanda = sum(v["solicitada"] for v in veiculos)

    print()
    print("==============================")
    print("GOODWE SMART CHARGING STATION")
    print("==============================")
    print("Energia disponivel:", energia, "W")
    print("Demanda total:", demanda, "W")
    print()

    for veiculo in veiculos:
        potencia = resultados[veiculo["id"]]

        if potencia >= veiculo["solicitada"]:
            estado = "RECARGA ATIVA"
        elif potencia > 0:
            estado = "RECARGA REDUZIDA"
        else:
            estado = "AGUARDANDO"

        print(
            veiculo["id"],
            "| Bateria:", str(veiculo["bateria"]) + "%",
            "| Solicitada:", str(veiculo["solicitada"]) + "W",
            "| Recebida:", str(potencia) + "W",
            "|", estado
        )

    print()
    print("REPRESENTACAO DE DADOS")
    print("-----------------------")
    print("Decimal:", energia)
    print("Hexadecimal:", hex(energia))
    print("Binario:", bin(energia))
    print()


def mostrar_lcd(energia, resultados):
    # Tela geral
    lcd.clear()
    lcd.set_cursor(0, 0)
    lcd.print_text("ENERGIA:" + str(energia) + "W")
    lcd.set_cursor(1, 0)
    demanda = sum(v["solicitada"] for v in veiculos)
    lcd.print_text("DEMANDA:" + str(demanda) + "W")
    time.sleep(2)

    # Uma tela para cada veículo
    for veiculo in veiculos:
        lcd.clear()
        lcd.set_cursor(0, 0)
        lcd.print_text(veiculo["id"] + " " + str(veiculo["bateria"]) + "%")
        lcd.set_cursor(1, 0)
        lcd.print_text(
            str(resultados[veiculo["id"]]) +
            "W/" +
            str(veiculo["solicitada"]) +
            "W"
        )
        time.sleep(2)


def executar_cenario(numero):
    if numero == 1:
        energia = 8000
        nome = "ALTA DISPONIBILIDADE"
    elif numero == 2:
        energia = 5000
        nome = "ENERGIA LIMITADA"
    else:
        energia = 2000
        nome = "BAIXA DISPONIBILIDADE"

    print()
    print("CENARIO", numero, "-", nome)

    resultados = gerenciar(energia)

    desligar_leds()

    for veiculo in veiculos:
        definir_led(veiculo, resultados[veiculo["id"]])

    mostrar_serial(energia, resultados)
    mostrar_lcd(energia, resultados)


# =========================
# INICIALIZAÇÃO
# =========================

lcd.init()
desligar_leds()

lcd.clear()
lcd.set_cursor(0, 0)
lcd.print_text("SMART CHARGING")
lcd.set_cursor(1, 0)
lcd.print_text("1 2 3 = CENARIO")

print("Sistema iniciado.")
print("Botao 1 = 8000 W")
print("Botao 2 = 5000 W")
print("Botao 3 = 2000 W")

cenario_anterior = 0

while True:
    if botao_1.value() == 0:
        if cenario_anterior != 1:
            executar_cenario(1)
            cenario_anterior = 1
        time.sleep_ms(300)

    elif botao_2.value() == 0:
        if cenario_anterior != 2:
            executar_cenario(2)
            cenario_anterior = 2
        time.sleep_ms(300)

    elif botao_3.value() == 0:
        if cenario_anterior != 3:
            executar_cenario(3)
            cenario_anterior = 3
        time.sleep_ms(300)

    time.sleep_ms(50)
