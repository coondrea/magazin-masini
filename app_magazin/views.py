from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
from urllib.parse import urlsplit


class Accesare:
    contor = 0

    def __init__(self, ip_client, url, parametri=None):
        Accesare.contor += 1

        self.id = Accesare.contor
        self.ip_client = ip_client
        self.url = url
        self.parametri = {} if parametri is None else parametri.copy()
        self.data = datetime.now()

    def lista_parametri(self):
        rezultat = []

        for nume, valoare in self.parametri.items():
            if valoare == "":
                valoare = None

            rezultat.append((nume, valoare))

        return rezultat
    
    def string_url(self):
        return self.url

    def pagina(self):
        cale = urlsplit(self.url).path
        cale_aplicatie = cale.removeprefix("/app_magazin")

        return cale_aplicatie or "/"
    
    def formateaza_data(self, format="%A, {zi} %B %Y"):
        zile_saptamana = [
            "Luni", "Marți", "Miercuri", "Joi",
            "Vineri", "Sâmbătă", "Duminică"
        ]

        luni = [
            "Ianuarie", "Februarie", "Martie", "Aprilie",
            "Mai", "Iunie", "Iulie", "August",
            "Septembrie", "Octombrie", "Noiembrie", "Decembrie"
        ]

        zi_saptamana = zile_saptamana[self.data.weekday()]
        luna = luni[self.data.month - 1]

        format_romanesc = format.replace("%A", zi_saptamana)
        format_romanesc = format_romanesc.replace("%B", luna)
        format_romanesc = format_romanesc.replace(
            "{zi}", str(self.data.day)
        )

        return self.data.strftime(format_romanesc)
    
    def __str__(self):
        return (
            f"id: {self.id}\n"
            f"ip_client: {self.ip_client}\n"
            f"string_url: {self.string_url()}\n"
            f"pagina: {self.pagina()}\n"
            f"calculeaza_data: {self.calculeaza_data()}\n"
            f"lista_parametri: {self.lista_parametri()}"
        )
        
    def calculeaza_data(
        self, format="%A, {zi} %B %Y", optiune=""
    ):
        if optiune == "zi":
            continut = self.formateaza_data("{zi} %B %Y")

        elif optiune == "timp":
            continut = self.formateaza_data("%H:%M:%S")

        else:
            data_formatata = self.formateaza_data(format)
            ora_formatata = self.formateaza_data("%H:%M:%S")
            continut = f"{data_formatata}, ora {ora_formatata}"

        return (
            "<section>"
            "<h2>Data și ora</h2>"
            f"<p>{continut}</p>"
            "</section>"
        )










def index(request):
    accesare = Accesare(
        ip_client=request.ip_client,
        url=request.build_absolute_uri(),
        parametri=request.GET.dict()
    )
    print(accesare)
    print(accesare.id, accesare.ip_client, accesare.url,
    accesare.parametri, accesare.data)
    
    descriere = (
        "Magazinul nostru oferă spre vânzare autoturisme noi și "
        "second-hand. Clienții vor putea consulta ofertele disponibile "
        "și detaliile fiecărei mașini, precum marca, modelul, "
        "anul fabricației, kilometrajul și prețul."
    )

    return HttpResponse(descriere)


def info(request):
    accesare = Accesare(
        ip_client=request.ip_client,
        url=request.build_absolute_uri(),
        parametri=request.GET.dict()
    )

    print(accesare)

    optiune_data = request.GET.get("data", "")

    sectiune_data = accesare.calculeaza_data(
        optiune=optiune_data
    )

    html = """
    <!DOCTYPE html>
    <html lang="ro">
        <head>
            <meta charset="UTF-8">
            <title>Informații despre server</title>
        </head>
        <body>
            <h1>Informații despre server</h1>
    """

    html += sectiune_data
    html += """
        </body>
    </html>
    """

    return HttpResponse(html)

