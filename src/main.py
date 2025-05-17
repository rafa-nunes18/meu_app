import flet as ft

carga_por_bitola = {
    2.5: 24,
    4: 32,
    6: 41,
    10: 57,
    16: 76,
    25: 101,
    35: 125
}

agrupamento_de_circuitos = {
    1: 1, 
    2: 0.80,
    3: 0.70,
    4: 0.65,
    5: 0.60,
    6: 0.57,
    7: 0.54,
    8: 0.52
}

lista_disjuntores = [6,10,16,20,25,32,40,50,63]


def main(page: ft.Page):
    page.title= 'Dimencionador de cabo e disjuntor'
    page.window_height= 700   
    page.window_width = 400   
    page.theme_mode= ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.TRANSPARENT
    page.padding = 0
    page.margin = ft.Margin(0, 0, 0, 0)
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.update() 

    def fator_potencia():
        if fator_poten.visible == True:

            fator_p = fator_poten.value

            try:
                if fator_p == "":
                    return ""
                fator_p = str(fator_p)
                if "," in (fator_p):
                    fator_poten.value = fator_poten.value.replace(",",".")
                fator_p = float(fator_poten.value)
                if fator_p > 1:
                    aviso_dialog.content = ft.Text("Digite apenas de 0,00 á 1,00\npara fator potência.")
                    aviso_dialog.open = True
                    page.dialog = aviso_dialog
                    fator_poten.border_color = "red"
                    page.update()
                    return "erro"      
                pass            
            except ValueError:
                aviso_dialog.content = ft.Text("Digite apenas números\npara fator potência.")
                aviso_dialog.open = True
                page.dialog = aviso_dialog
                fator_poten.border_color = "red"
                page.update()
                return "erro"
            
        else:
            fator_poten.value = 0.92
            return "1"            

    def fator_agrupamento():
        agru = circuito.value
        
        if agru == "":
            return ""       
        elif agru.isdigit() and 1 <= int(agru) <= 8:
            for circuitos, fator in agrupamento_de_circuitos.items():
                if circuitos == int(agru):
                    agrupamento = fator 
                    return agrupamento           
        else:
            aviso_dialog.content = ft.Text("Digite apenas de 1 a 8 para circuitos.")
            aviso_dialog.open = True
            page.dialog = aviso_dialog
            circuito.border_color = "red"
            page.update()
            return "erro"
    
    def corrente_equipamento():

        watts = potencia.value

        if watts == "":
            return ""
        
        try:
            if "," in watts:
                watts = watts.replace(",",".") 
            potenc =float(watts)
            pass
        except ValueError:
            aviso_dialog.content = ft.Text("Digite apenas números para potência.")
            aviso_dialog.open = True
            page.dialog = aviso_dialog
            potencia.border_color = "red"
            page.update()
            return "erro"
        
        if dropdown.value is not None:
            try:
                float(circuito.value)
                float(temperatura.value)
                float(fator_poten.value)
                tensao = int(dropdown.value)
                if fator_poten.visible == False:  
                   carga_necessaria = (potenc / tensao)
                else:
                    fp = float(fator_poten.value)
                    carga_necessaria = (potenc / fp) /tensao

                carga_maxima_bitola_tabela = max(carga_por_bitola.values())*1.22

                if carga_necessaria > carga_maxima_bitola_tabela:
                    aviso_dialog.content = ft.Text(f"Apotência {carga_necessaria:.0f} excede a capacidade máxima do programa.")
                    aviso_dialog.open = True
                    page.dialog = aviso_dialog
                    potencia.border_color = "red"
                    page.update()
                    return "erro"
                else:                
                    return carga_necessaria
            except:
                return "erro"    
                    
    def fator_temperatura():
        
        tempe=(temperatura.value)        
            
        if tempe == "":
            return ""
        
        try:
            if "," in tempe:
                tempe = tempe.replace(",",".") 
            temp=float(tempe)
            pass
        except ValueError:
            aviso_dialog.content = ft.Text("Digite apenas números para temperatura.")
            aviso_dialog.open = True
            page.dialog = aviso_dialog
            temperatura.border_color = "red"
            page.update()
            return "erro"

        if temp < 10 or temp > 60:
            aviso_dialog.content = ft.Text(f" A temperatura {temp}°C esta fora do intervalo permitido.\n Coloque de 10 a 60 °C.")
            aviso_dialog.open = True
            page.dialog = aviso_dialog
            temperatura.border_color = "red"
            page.update()
            return "erro"
   
        elif 10 <= temp < 15:  
            return 1.22  
        elif 15 <= temp < 20:  
            return 1.17  
        elif 20 <= temp < 25:  
            return 1.12  
        elif 25 <= temp < 30:  
            return 1.06  
        elif 30 <= temp < 35:  
            return 1  
        elif 35 <= temp < 40:  
            return 0.94  
        elif 40 <= temp < 45:  
            return 0.87  
        elif 45 <= temp < 50:  
            return 0.79  
        elif 50 <= temp < 55:  
            return 0.71  
        elif 55 <= temp < 60:  
            return 0.61  
        elif temp == 60:  
            return 0.50
        
    def limpar_resultados():
        resultado_cabo.value = ""
        resultado_disjuntor.value = ""
        carga_nece.value = ""
        carga_disj.value = ""
        corrente_corrig.value = ""
        

    def verificar_campos(e):       
        
        limpar_resultados()
        fator_potc = fator_potencia()
        fator_temp = fator_temperatura()
        fator_agrup = fator_agrupamento()
        corrente_necessaria = corrente_equipamento()

        if "erro" in (corrente_necessaria, fator_temp, fator_agrup, fator_potc):
            return
        
        campos = {
            "Potência": potencia.value.strip(),
            "Temperatura": temperatura.value.strip(),
            "Voltagem": dropdown.value,
            "Circuitos": circuito.value.strip(),
            "Fator potência": fator_poten.value
        }
        
       
        campos_invalidos = []

        for nome, valor in campos.items():
            if valor == "" or valor == None:
                campos_invalidos.append(nome)
            else:
                try:
                    float(valor)
                except ValueError:
                    campos_invalidos.append(nome)       

        if campos_invalidos:
            aviso_dialog.content = ft.Text(f"Corrija o(s) campo(s): {', '.join(campos_invalidos)}")
            aviso_dialog.open = True
            page.dialog = aviso_dialog

            potencia.border_color = "red" if "Potência" in campos_invalidos else None
            temperatura.border_color = "red" if "Temperatura" in campos_invalidos else None
            dropdown.border_color = "red" if "Voltagem" in campos_invalidos else None
            circuito.border_color = "red" if "Circuitos" in campos_invalidos else None
            fator_poten.border_color = "red" if "Fator potência" in campos_invalidos else None

            page.update()      

        else:
            potencia.border_color = None
            temperatura.border_color = None
            dropdown.border_color = None
            circuito.border_color = None
            fator_poten.border_color = None     
            
            i = 0
            dimensionado = False

            bitolas_correntes = list(carga_por_bitola.items())
            bitolas_correntes.sort()            

            while not dimensionado and i < len(bitolas_correntes):
                cabo, carga = bitolas_correntes[i]
                carga_corrigida = carga * fator_temp * fator_agrup

                if corrente_necessaria <= carga_corrigida:

                    disjuntor_encontrado = False
                    folga = 1.15

                    while folga >= 1.00:

                        carga_disjuntor = corrente_necessaria * folga
                        
                        for disj in lista_disjuntores:
                            if carga_disjuntor <= disj <= carga_corrigida:
                                disjuntor = disj
                                bitola = cabo
                                resultado_disjuntor.value = f"{disjuntor} A"
                                resultado_cabo.value = f"{bitola} mm²"
                                carga_disj.value = f"{carga_disjuntor:.2f} A"
                                corrente_corrig.value = f"{carga_corrigida:.2f} A"
                                carga_nece.value = f"{corrente_necessaria:.2f} A"
                                dimensionado = True
                                disjuntor_encontrado = True
                                page.update()
                                break

                        if disjuntor_encontrado:
                            aviso_dialog.title = ft.Text("Folga da corrente")
                            aviso_dialog.content = ft.Text(f"Foi adicionado {((folga - 1) * 100):.0f}% na carga necessária\npara dimensionar o disjuntor.")
                            aviso_dialog.open = True
                            page.dialog = aviso_dialog
                            page.update()
                            break

                        folga -= 0.01

                    if not disjuntor_encontrado:
                        i += 1  
                else:
                    i += 1  

            if not dimensionado:
                aviso_dialog.content = ft.Text(f"Nenhuma combinação de cabo e disjuntor\natende à carga de {corrente_necessaria:.2f} A.")
                aviso_dialog.open = True
                
                potencia.border_color = None
                temperatura.border_color = None
                dropdown.border_color = None
                circuito.border_color = None

                page.dialog = aviso_dialog
                page.update()               
           

    def focus_textfield(textfield: ft.TextField):
        textfield.focus()  
        page.update()

    def fechar_dialogo():
        aviso_dialog.open = False
        page.update()
    
    def change_button(e):
        if e.state == ft.AudioState.PAUSED:
            botao.text = "Play Music"
            botao.on_click = lambda e: audio.resume()
        elif e.state == ft.AudioState.PLAYING:
            botao.text = "Pause Music"
            botao.on_click = lambda e: audio.pause()

        botao.update()

    def switch_changed(e):
        fator_poten.visible = not e.control.value  
        page.update() 

    audio = ft.Audio(
        src="alarm.mp3",
        autoplay=True,
        on_state_changed=change_button
    )

    aviso_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Erro de preenchimento"),
        content=ft.Text(""),
        actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialogo())]
    )

    botao= ft.ElevatedButton(
        "Pause playing",
        style=ft.ButtonStyle(text_style=ft.TextStyle(
            size=12
            )
        ),
        width=50,
        height=50,
         on_click=lambda _: audio.pause()
    )

    texto = ft.Text(
        value="Dimensionar",
        size= 35,
        weight=ft.FontWeight.BOLD
    )

    resistivo = ft.Text(
        value="Resistivo?",
        size= 25,
        weight=ft.FontWeight.BOLD
    )
    
    resistivo_switch = ft.Switch(
        value=False,
        on_change=switch_changed
    )

    fator_poten = ft.TextField(
        label="FATOR POTÊNCIA",
        hint_text="0,92",
        value= .92,
        label_style=ft.TextStyle(
            size=20,
            weight=ft.FontWeight.BOLD
        ),
        width=170,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD            
        ),
        text_align=ft.TextAlign.CENTER
    )

    potencia = ft.TextField(
        label="Potência",
        hint_text="Digite a potência (W)",
        label_style=ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        ),
        width=350,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        )
    )

    temperatura  = ft.TextField(
        label="Temperatura",
        hint_text="Digite a temperatura",
        label_style=ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        ),
        width=350,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        )
    )

    circuito  = ft.TextField(
        label="Circuitos",
        hint_text="Digite os circuitos",
        label_style=ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        ),
        width=350,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        )
    )

    resultado_cabo = ft.TextField(
        label="Cabo recomendado",
        label_style=ft.TextStyle(
            size=16,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
            ),
        bgcolor=ft.Colors.WHITE54 ,
        read_only=True,
        filled=True,
        width=150,
        text_align=ft.TextAlign.CENTER
    )

    resultado_disjuntor = ft.TextField(
        label="Disjuntor recomendado",
        label_style=ft.TextStyle(
            size=16,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
            ),
        bgcolor= ft.Colors.WHITE54,
        read_only=True,
        filled=True,
        width=150,
        text_align=ft.TextAlign.CENTER
    )

    carga_nece = ft.TextField(
        label="Carga necessária",
        label_style=ft.TextStyle(
            size=16,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=20,
            weight=ft.FontWeight.BOLD
            ),
        bgcolor=ft.Colors.WHITE12,
        read_only=True,
        filled=True,
        width=110,
        text_align=ft.TextAlign.CENTER
    )
    
    carga_disj = ft.TextField(
        label="Carga p/ Disjuntor",
        label_style=ft.TextStyle(
            size=16,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=20,
            weight=ft.FontWeight.BOLD
            ),
        bgcolor=ft.Colors.WHITE12,
        read_only=True,
        filled=True,
        width=105,
        text_align=ft.TextAlign.CENTER
    )

    corrente_corrig = ft.TextField(
        label="Max cabo(A) corrigida",
        label_style=ft.TextStyle(
            size=16,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=20,
            weight=ft.FontWeight.BOLD
            ),
        bgcolor= ft.Colors.WHITE12,
        read_only=True,
        filled=True,
        width=105,
        text_align=ft.TextAlign.CENTER
    )         

    potencia.on_click = lambda e: focus_textfield(potencia)
    temperatura.on_click = lambda e: focus_textfield(temperatura)
    circuito.on_click = lambda e: focus_textfield(circuito)

    dropdown = ft.Dropdown(
        label="Volts",
        hint_text="Escolha a tensão", 
        label_style=ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
            ),
        width=160,
        focused_border_color='transparent',
        options=
        [
            ft.DropdownOption("127"),
            ft.DropdownOption("220")
        ]        
    )    

    botao_iniciar = ft.ElevatedButton(
        text="I N I C I A R",
        width=100,
        height=50,        
        on_click=verificar_campos,
        bgcolor= ft.Colors.WHITE70,
    )

    minha_assinatura = ft.Text(
        value="Craker - 2025",
        size= 15 ,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE
    )

    versao = ft.Text(
        value="versão (beta-0.2)",
        size= 15 ,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE
    )         

    fundo = ft.Stack(
        controls= 
        [
            ft.Image(
                src= "bg2.gif",
                expand=True,
                fit= ft.ImageFit.COVER
            ),
            ft.Container(                    
                width=380,
                height=670,
                border_radius=15,
                bgcolor= ft.Colors.WHITE30,
                blur = 1.5,
                padding= 10,
                margin=ft.Margin(10, 5, 5, 5),                    
                content= ft.Column(
                    controls=
                    [      
                        ft.Row(
                            [
                             texto,
                             botao],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                             ft.Container(
                                content=botao_iniciar,
                                margin=ft.Margin(top=-10, right= 0, bottom=0, left=0)  
                             ),
                             resistivo,
                             resistivo_switch
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        potencia,
                        temperatura,
                        circuito,
                        ft.Row(
                            [
                             dropdown,
                             fator_poten
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                             carga_nece,
                             carga_disj,
                             corrente_corrig
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                             resultado_cabo,
                             resultado_disjuntor
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                             minha_assinatura,
                             ft.Container(
                                    content=versao,
                                    margin=ft.Margin(top=0, right= 0, bottom=0, left=110)  
                             )
                            ],
                            alignment=ft.MainAxisAlignment.START
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.MainAxisAlignment.CENTER
                    
                )                
            )
        ]                     
    )

    page.overlay.append(aviso_dialog)
    page.add(        
        audio,
        fundo
    )
       
    page.update()

ft.app(target=main,  assets_dir="assets")