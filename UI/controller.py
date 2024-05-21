import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []


    def fillDD(self):
        colori = self._model.get_colori()
        for c in colori:
            self._view._ddcolor.options.append(ft.dropdown.Option(c["Product_color"]))


    def handle_graph(self, e):
        self._view.txtOut.controls.append(ft.Text("Iniziato creazione grafo"))
        self._view.update_page()
        anno = int(self._view._ddyear.value)
        colore = self._view._ddcolor.value
        self._model.crea_grafo(colore, anno)
        num_nodi = self._model.get_num_nodi()
        num_archi = self._model.get_num_archi()
        self._view.txtOut.controls.append(ft.Text(f"Numero nodi: {num_nodi}"))
        self._view.txtOut.controls.append(ft.Text(f"Numero archi: {num_archi}"))
        archi, common_products = self._model.get_nodi_da_stampare()
        for a in archi:
            self._view.txtOut.controls.append(ft.Text(f"Arco da {a[0]} a {a[1]} di peso {a[2]}"))
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono:"))
        for c in common_products:
            self._view.txtOut.controls.append(ft.Text(f"- {c}"))
        self._view._ddnode.disabled = False
        self._view.btn_search.disabled = False
        self.fillDDProduct()
        self._view.update_page()

    def fillDDProduct(self):
        prodotti = self._model.get_prodotti()
        for c in prodotti:
            self._view._ddnode.options.append(ft.dropdown.Option(c))


    def handle_search(self, e):
        nodo = int(self._view._ddnode.value)
        longest_path = self._model.find_longest_increasing_path(nodo)
        print(longest_path)