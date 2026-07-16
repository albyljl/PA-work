# PA-work — Editor Gráfico

Projeto da disciplina Programação A. O programa é um editor gráfico feito com Tkinter e organizado com MVC.

## Recursos

- desenho livre, retângulo, oval, polígono e borracha;
- seleção simples e múltipla com `Shift`;
- mover, apagar, copiar/colar e alterar a ordem das figuras;
- alteração de contorno, preenchimento e espessura;
- salvar e abrir em JSON;
- agrupar e desagrupar figuras usando o padrão **Composite**;
- ferramentas de desenho organizadas com o padrão **State**.

## Executar

É necessário Python 3.10 ou superior.

```bash
python main.py
```

## Testes

```bash
python -m unittest discover -s tests -v
```

## Agrupar e desagrupar

1. Escolha **Selecionar**.
2. Selecione mais de uma figura mantendo `Shift` pressionado.
3. Clique em **Agrupar** ou use `Ctrl+G`.
4. Para desfazer o grupo, selecione-o e clique em **Desagrupar** ou use `Ctrl+Shift+G`.

A figura composta pode ser selecionada, movida, copiada, apagada, recolorida, reordenada e salva como qualquer figura simples.
