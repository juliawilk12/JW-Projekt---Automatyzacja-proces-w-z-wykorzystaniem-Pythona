import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, filedialog
from fpdf import FPDF
import PyPDF2
import pickle


def differential_equation(y, x, param):
    # Definiowanie równania różniczkowego
    dydx = param * y * x  # Przykładowe równanie: y' = param * y * x
    return dydx


def solve_differential_equations(param_values):
    # Ustawienie wartości początkowej
    x0 = 0
    y0 = 1

    # Zakres x
    x_range = np.linspace(0, 10, 100) 

    for param in param_values:
        # Rozwiązanie równania różniczkowego metodą Eulera dla każdego parametru
        y = np.zeros_like(x_range)
        y[0] = y0
        for i in range(1, len(x_range)):
            h = x_range[i] - x_range[i-1]
            y[i] = y[i-1] + h * differential_equation(y[i-1], x_range[i-1], param)

        # Generowanie raportu PDF
        generate_report(param, x_range, y)


def generate_report(param, x_range, y):
    # Tworzenie nowego obiektu PDF
    pdf = FPDF()

    # Dodawanie strony 1
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Raport dla parametru: {param}", ln=True, align="C")

    # Dodawanie opisu równań różniczkowych
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Tutaj mozna dodac nieco teorii do RR i wzorki ogolne", ln=True)

    # Dodawanie strony 2 z wykresem
    pdf.add_page()
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Rozwiazanie rownania rozniczkowego typu y' = param * x * y:", ln=True)
    chart_file = generate_chart(x_range, y)
    pdf.image(chart_file, x=10, y=20, w=pdf.w - 20)

    # Dodawanie stron z tabelą
    page_num = 3
    rows_per_page = 40
    total_rows = len(x_range)
    num_pages = total_rows // rows_per_page + 1

    for page in range(num_pages):
        pdf.add_page()
        pdf.set_font("Arial", "", 10)
        pdf.cell(0, 10, "Tabela z danymi punktow tworzacych wykres:", ln=True)
        cell_width = pdf.w / 2
        cell_height = 10
        pdf.cell(cell_width, cell_height, "x", 1, 0, "C")
        pdf.cell(cell_width, cell_height, "y", 1, 1, "C")

        start_row = page * rows_per_page
        end_row = min(start_row + rows_per_page, total_rows)

        for i in range(start_row, end_row):
            pdf.cell(cell_width, cell_height, str(x_range[i]), 1, 0, "C")
            pdf.cell(cell_width, cell_height, str(y[i]), 1, 1, "C")

        page_num += 1

    # Zapisanie raportu do pliku
    report_filename = f"report_param_{param}.pdf"
    pdf.output(report_filename)

    # Serializacja danych do pliku
    data = {
        'param': param,
        'x_data': x_range,
        'y_data': y
    }
    data_filename = f"data_param_{param}.pkl"
    with open(data_filename, 'wb') as file:
        pickle.dump(data, file)

def generate_chart(x, y):
    fig, ax = plt.subplots(figsize=(6, 4), dpi=300)
    ax.plot(x, y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Wykres rozwiazania rownania rozniczkowego')
    chart_file = "chart.png"
    plt.savefig(chart_file, bbox_inches='tight', dpi=300)
    plt.close(fig)
    return chart_file


def read_table_from_pdf(filename):
    # Odczyt tabeli z pliku PDF

    # Otwieranie pliku PDF w trybie do odczytu binarnego
    with open(filename, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        # Inicjalizacja zmiennych przechowujących dane tabeli
        x_data = []
        y_data = []

        # Odczytywanie stron z tabelą
        for page_num in range(3, len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]

            # Wyszukiwanie wierszy tabeli
            lines = page.extract_text().split('\n')
            table_lines = [line.split() for line in lines if len(line.split()) == 2]

            # Wyciąganie danych z kolumn x i y
            x_column = []
            y_column = []

            for row in table_lines:
                try:
                    x = float(row[0])
                    y = float(row[1])
                    x_column.append(x)
                    y_column.append(y)
                except ValueError:
                    continue

            # Dodawanie danych do listy
            x_data.extend(x_column)
            y_data.extend(y_column)

    return x_data, y_data

def select_pkl_file():
    # Wybór pliku PKL
    filename = filedialog.askopenfilename(filetypes=[("PKL Files", "*.pkl")])
    if filename:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        print("Dane z pliku PKL:")
        print(data)

def run_solver():
    # Pobranie wartości parametrów z pól tekstowych
    param1 = float(entry_param1.get())
    param2 = float(entry_param2.get())
    param3 = float(entry_param3.get())
    param4 = float(entry_param4.get())
    param5 = float(entry_param5.get())

    # Tworzenie listy parametrów
    param_values = [param1, param2, param3, param4, param5]

    # Rozwiązanie równań różniczkowych 
    solve_differential_equations(param_values)


def select_pdf_file():
    # Wybór pliku PDF
    filename = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if filename:
        x_data, y_data = read_table_from_pdf(filename)
        print("Dane z pliku PDF:")
        print("Kolumna 'x':", x_data)
        print("Kolumna 'y':", y_data)

        # Rysowanie wykresu
        plt.plot(x_data, y_data)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Wykres rozwiazania rownania rozniczkowego')
        plt.show()



# Tworzenie GUI
root = Tk()
root.title("Solwer rownan rozniczkowych typu y' = param * x * y")
root.geometry("300x280")

# Etykiety
label_param1 = Label(root, text="Param 1:")
label_param1.pack()

# Pola tekstowe
entry_param1 = Entry(root)
entry_param1.insert(0, "0")
entry_param1.pack()

label_param2 = Label(root, text="Param 2:")
label_param2.pack()

entry_param2 = Entry(root)
entry_param2.insert(0, "0")
entry_param2.pack()

label_param3 = Label(root, text="Param 3:")
label_param3.pack()

entry_param3 = Entry(root)
entry_param3.insert(0, "0")
entry_param3.pack()

label_param4 = Label(root, text="Param 4:")
label_param4.pack()

entry_param4 = Entry(root)
entry_param4.insert(0, "0")
entry_param4.pack()

label_param5 = Label(root, text="Param 5:")
label_param5.pack()

entry_param5 = Entry(root)
entry_param5.insert(0, "0")
entry_param5.pack()

# Przycisk uruchamiający solver
button_solve = Button(root, text="Rozwiaz rownania", command=run_solver)
button_solve.pack()

# Przycisk wyboru pliku PDF
button_select_pdf = Button(root, text="Wybierz PDF", command=select_pdf_file)
button_select_pdf.pack()

# Przycisk wyboru pliku PKL
button_select_pkl = Button(root, text="Wybierz PKL", command=select_pkl_file)
button_select_pkl.pack()

# Uruchomienie głównej pętli programu
root.mainloop()
