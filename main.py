import tkinter as tk
from controlador.gerente_fluxo import GerenteFluxo
from visao.painel_usuario import PainelUsuario

def principal():
    janela = tk.Tk()
    janela.state("zoomed")  
    
    modulo_controle = GerenteFluxo()
    modulo_visao = PainelUsuario(janela, modulo_controle)
    
    modulo_controle.vincular_view(modulo_visao)
    
    janela.mainloop()

if __name__ == "__main__":
    principal()