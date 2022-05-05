# ------------------------------------------------- IMPORT TKINTER -------------------------------------------------- #
from tkinter import *
# ------------------------------------------------- IMPORT DATETIME -------------------------------------------------- #
import datetime as dt
# ------------------------------------------------- IMPORTS SELENIUM ------------------------------------------------- #
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --------------------------------------------- CONFIGURAÇÕES DO SELENIUM -------------------------------------------- #
options = Options()
options.add_argument("--headless")
caminho_chrome_web_driver = Service("C:\chromeWebDriver\chromedriver.exe")
driver = webdriver.Chrome(service=caminho_chrome_web_driver, options=options)
# ------------------------------------------------ CONSTANTES DE ESTILO ---------------------------------------------- #
BLACK = "#292929"
VERDE = "green"
VERMELHO = "red"
AMARELO = "yellow"
FONTE_SIZE = 15
# --------------------------------------- CRIANDO A JANELA DE INTERFACE GRÁFICA -------------------------------------- #
tela = Tk()
tela.title("Placar Jogos")
tela.configure(bg=BLACK)
tela.state("zoomed")
largura_maxima = tela.winfo_screenwidth()
altura_maxima = tela.winfo_screenheight()
tela.maxsize(largura_maxima, altura_maxima)
tela.minsize(largura_maxima, altura_maxima)
# ---------------------------------- FUNÇÃO PARA CRIAR OS COMPONENTES DA TELA ---------------------------------------- #
global list_box01
global list_box02


def criar_componentes():
	global list_box01
	global list_box02

	data = dt.date.today()
	data_formatada = data.strftime("%d-%m-%Y")

	jogos_hoje_label = Label(
		width=100,
		text=f"Jogos de Hoje - Data: {data_formatada} Acompanhe em tempo real",
		background=BLACK,
		fg="white",
		font=("Courier", FONTE_SIZE, "bold"),
		pady=10,
	)
	jogos_hoje_label.grid(row=0, column=0, columnspan=4)
	list_box01 = Listbox(
		width=55,
		height=int(altura_maxima / 20),
		borderwidth=0,
		highlightthickness=0,
		background=BLACK,
		fg="white",
		activestyle="none",
		selectbackground=BLACK,
		highlightcolor="blue",
		font=("Courier", FONTE_SIZE, "bold")
	)
	list_box01.grid(row=1, column=0, columnspan=2, padx=20)
	list_box02 = Listbox(
		width=55,
		height=int(altura_maxima / 20),
		borderwidth=0,
		highlightthickness=0,
		bg=BLACK,
		fg="white",
		activestyle="none",
		selectbackground=BLACK,
		font=("Courier", FONTE_SIZE, "bold")
	)
	list_box02.grid(row=1, column=2, columnspan=2, padx=20)
	obter_dados()


# ----------------------------------- FUNÇÕES QUE VÃO DESTRUIR O LISTBOX --------------------------------------------- #
def destruir_listbox02():
	list_box02.destroy()
	criar_componentes()


def destruir_listbox01():
	list_box01.destroy()
	criar_componentes()


# ------------------------ CONTADOR QUE VAI AUXILIAR NA DIVISÃO DA LISTA EM DUAS PARTES ------------------------------ #
contador = 0


# ----------------------------- FUNÇÃO QUE OBTÉM OS DADOS E INSERE OS JOGOS NA LISTBOX ------------------------------- #
def obter_dados():
	global contador
	driver.get(url="https://superplacar.com.br/")
	jogos_divs = driver.find_elements(by=By.CLASS_NAME, value="linhaPartida")
	lista_de_jogos01 = []
	lista_de_jogos02 = []
	for jogo in jogos_divs:
		if contador < 13:
			lista_de_jogos01.append(jogo.text.strip().replace("\n", " "))
		else:
			lista_de_jogos02.append(jogo.text.strip().replace("\n", " "))
		contador += 1
	contador = 0
	for jogo in lista_de_jogos01:
		print(jogo)
		list_box01.insert(0, jogo)
		list_box01.insert(0, "")
		if "Em andamento" in jogo:
			list_box01.itemconfigure(1, fg=VERDE)
		if "Em breve" in jogo:
			list_box01.itemconfigure(1, fg=AMARELO)
		if "Encerrado" in jogo:
			list_box01.itemconfigure(1, fg=VERMELHO)
	list_box01.after(ms=60000, func=destruir_listbox01)
	for jogo in lista_de_jogos02:
		print(jogo)
		list_box02.insert(0, jogo)
		list_box02.insert(0, "")
		if "Em andamento" in jogo:
			list_box02.itemconfigure(1, fg=VERDE)
		if "Em breve" in jogo:
			list_box02.itemconfigure(1, fg=AMARELO)
		if "Encerrado" in jogo:
			list_box02.itemconfigure(1, fg=VERMELHO)
	list_box02.after(ms=60000, func=destruir_listbox02)
	tela.mainloop()

	driver.quit()


# ----------------------------------- CHAMADA DA FUNÇÃO PARA INICIAR O PROGRAMA -------------------------------------- #
criar_componentes()
