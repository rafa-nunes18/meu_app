import flet as ft

carga_por_bitola = {
    2.5: 24,
    4: 32,
    6: 41,
    10: 57,
    16: 76,
    25: 101,
    35: 125,
    50: 151,
    70: 192,
    95: 232,
    120: 269
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

lista_disjuntores = [6,10,16,20,25,32,40,50,63,70,80,100,125]


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

    def aviso(caixa_red,texto):
        aviso_dialog.content = ft.Text(texto)
        aviso_dialog.open = True        
        caixa_red.border_color = "red"
        page.update()

    def focus_textfield(textfield: ft.TextField):
        textfield.focus()  
        page.update()

    def fechar_dialogo():
        aviso_dialog.open = False
        page.update()
    
    def change_button(e):
        if e.state == ft.AudioState.PAUSED:
            botao_audio.text = "Play Music"
            botao_audio.on_click = lambda e: audio.resume()
        elif e.state == ft.AudioState.PLAYING:
            botao_audio.text = "Pause Music"
            botao_audio.on_click = lambda e: audio.pause()

        botao_audio.update()

    def switch_changed(e):
        fator_poten.visible = not e.control.value  
        page.update() 

    def mostrar_info(e):
        aviso_dialog.title=ft.Text(
            value="Resultado Completo",
            size= 25,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER
        )
        aviso_dialog.content = ft.Text(
            value=resultado_completo.value,
            size= 20,
            weight=ft.FontWeight.BOLD
        )
        aviso_dialog.actions=[ft.TextButton("Fechar", on_click= esconder_info)]
        aviso_dialog.open = True        
        page.update()

    def esconder_info(e):
        aviso_dialog.title=ft.Text("Erro de preenchimento"),
        aviso_dialog.content=ft.Text("")        
        aviso_dialog.actions=[ft.TextButton("Fechar", on_click=lambda e: fechar_dialogo())]
        aviso_dialog.open = False        
        page.update()

    def mostrar_help(e):
        info_box.visible = True
        page.update()

    def esconder_help(e=None):
        info_box.visible = False
        page.update()     

    def fator_potencia():
        if fator_poten.visible == True:

            try:
                fator_p = str(fator_poten.value).strip()
                if fator_p == "":
                    return ""                
                if "," in (fator_p):
                    fator_poten.value = fator_poten.value.replace(",",".")
                fator_p = float(fator_poten.value)                    
                if fator_p > 1 or fator_p < 0:
                    aviso(fator_poten,"Digite apenas de 0,00 á 1,00\npara Fator Potência.")
                    return "erro"
                else:
                    return fator_p                           
            except ValueError:
                aviso(fator_poten,"Digite apenas números\npara Fator Potência.")
                return "erro"
            
        else:
            fator_poten.value = 0.92
            return "1"            

    def fator_agrupamento():   
        try:
            agru= str(circuito.value).strip() 

            if agru == "":
                return "" 
            elif "," in agru:
                aviso(circuito,"Não digite virgulas em Circuitos.")
                return "erro"
            
            agru = int(agru) 

            if agru <= 0:
                aviso(circuito,"Digite 1 ou mais circuitos.")
                return "erro"     
            elif  1 <= agru <= 8:
                for circuitos, fator in agrupamento_de_circuitos.items():
                    if circuitos == agru:
                        agrupamento = fator 
                        return agrupamento
            elif 9 <= agru <= 11:
                return 0.50
            elif 12 <= agru <= 15:
                return 0.45   
            elif 16 <= agru <= 19:
                return 0.41
            elif agru >= 20:
                return 0.38           
            
        except ValueError:
            aviso(circuito,"Digite apenas números\npara Circuitos.")
            return "erro"
    
    def corrente_equipamento():     
        
        try:
            watts = str(potencia.value).strip()
            if watts == "":
                return ""
            if "," in watts:
                potencia.value = potencia.value.replace(",","")
            watts =float(potencia.value)
            return watts
        except ValueError:
            aviso(potencia,"Digite apenas números para Potência.")
            return "erro"           
                    
    def fator_temperatura():      
        
        try:
            temp = str(temperatura.value).strip()
            if temp == "":            
                return ""
            if "," in temp:
                temperatura.value = temperatura.value.replace(",",".") 
            temp=float(temperatura.value)
            if temp < 10 or temp > 60:
                aviso(temperatura,f" A temperatura {temp}°C esta fora do intervalo permitido.\n Coloque de 10 a 60 °C.")
                return "erro"
        except ValueError:
            aviso(temperatura,"Digite apenas números para temperatura.")
            return "erro"        
   
        if 10 <= temp < 15:  
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
        resultado_fa.value =  "" 
        resultado_ft.value = ""     

    def verificar_campos(e):       
        
        limpar_resultados()
        potencia_watts = corrente_equipamento()
        fator_temp = fator_temperatura()
        fator_agrup = fator_agrupamento()
        fator_potc = fator_potencia()       
        volts = dropdown.value
       
        campos = {
            "Potência": potencia_watts, 
            "Temperatura": fator_temp,
            "Tensão": volts,
            "Circuitos": fator_agrup,
            "Fator potência": fator_potc
        }      
       
        campos_invalidos = []

        for nome, valor in campos.items():
            if "erro" == valor:
                botao_info.visible=False
                return
            elif valor == "" or valor == None:
                campos_invalidos.append(nome)
            else:
                pass      

        if campos_invalidos:
            aviso_dialog.content = ft.Text(f"Corrija o(s) campo(s): {', '.join(campos_invalidos)}")
            aviso_dialog.title= ft.Text("Erro de preenchimento")
            aviso_dialog.open = True
            botao_info.visible= False

            potencia.border_color = "red" if "Potência" in campos_invalidos else None
            temperatura.border_color = "red" if "Temperatura" in campos_invalidos else None
            dropdown.border_color = "red" if "Tensão" in campos_invalidos else None
            circuito.border_color = "red" if "Circuitos" in campos_invalidos else None
            fator_poten.border_color = "red" if "Fator potência" in campos_invalidos else None

            page.update()      

        else:
            potencia.border_color = None
            temperatura.border_color = None
            dropdown.border_color = None
            circuito.border_color = None
            fator_poten.border_color = None     
            
            tensao = int(volts)
            carga_maxima_bitola_tabela = max(carga_por_bitola.values())*1.22
            bitolas_correntes = list(carga_por_bitola.items())
            bitolas_correntes.sort()

            if fator_poten.visible == False:  
                carga_necessaria = (potencia_watts / tensao)
            else:
                carga_necessaria = (potencia_watts / fator_potc) / tensao                          

            if carga_necessaria > carga_maxima_bitola_tabela:
                aviso(potencia,f"Apotência {carga_necessaria:.0f} excede a capacidade máxima do programa.")
                return          
            
            i = 0
            dimensionado = False 

            while not dimensionado and i < len(bitolas_correntes):
                cabo, carga = bitolas_correntes[i]
                carga_corrigida = carga * fator_temp * fator_agrup

                if carga_necessaria <= carga_corrigida:

                    disjuntor_encontrado = False
                    folga = 1.15

                    while folga >= 1.10:

                        carga_disjuntor = carga_necessaria * folga
                        
                        for disj in lista_disjuntores:
                            if carga_disjuntor <= disj <= carga_corrigida:
                                disjuntor = disj
                                bitola = cabo
                                resultado_ft.value = f"{fator_temp}"
                                resultado_fa.value = f"{fator_agrup}"
                                resultado_disjuntor.value = f"{disjuntor} A"
                                resultado_cabo.value = f"{bitola} mm²"
                                carga_disj.value = f"{carga_disjuntor:.2f} A"
                                corrente_corrig.value = f"{carga_corrigida:.2f} A"
                                carga_nece.value = f"{carga_necessaria:.2f} A"
                                botao_info.visible=True
                                dimensionado = True
                                disjuntor_encontrado = True                                
                                resultado_completo.value = (
                                    f"⚡ Potência fornecida: {potencia_watts:.0f} (W)\n"
                                    f"🔌 Tensão escolhida: {tensao} (V)\n"
                                    f"➡️ Corrente calculada: {carga_necessaria:.2f} (A)\n"
                                    f"🌡️ Temperatura fornecida: {temperatura.value} (C°)\n"
                                    f"🔀 Circuitos fornecido: {circuito.value}\n"
                                    f"📉 Fator de temperatura: {fator_temp}\n"                                    
                                    f"📦 Fator de agrupamento: {fator_agrup}\n"                                    
                                    f"🔁 Fator de potência: {fator_potc}\n"
                                    f"📈 Folga da corrente: +{((folga - 1) * 100):.0f} % \n"                 
                                    f"⚙️ Corrente corrigida: {carga_disjuntor:.2f} (A)\n"
                                    f"🧮 Max(A) cabo corrigida: {carga_corrigida:.2f} (A)\n"
                                    f"🌀 Cabo recomendado: {bitola} mm²\n"
                                    f"🛡️ Disjuntor recomendado: {disjuntor} (A)"
                                )                                
                                page.update()
                                break

                        if disjuntor_encontrado:
                            aviso_dialog.title = ft.Text("Folga da corrente")
                            aviso_dialog.content = ft.Text(
                                f"Por segurança foi adicionado {((folga - 1) * 100):.0f}% na carga necessária para dimensionar o disjuntor.\n"
                                "Clique em INFO para mais informaçoes."
                            )
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
                aviso(potencia,f"Nenhuma combinação de cabo e disjuntor\natende à Potencia de {carga_necessaria:.2f} A.")
                return   

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

    botao_iniciar = ft.ElevatedButton(
        text="I N I C I A R",
        width=100,
        height=50,        
        on_click=verificar_campos,
        bgcolor= ft.Colors.WHITE70,
    )

    resultado_completo = ft.Text(
        value="casa",
        size=16,
        weight=ft.FontWeight.BOLD
    )    

    conteudo_com_rolagem = ft.Column(
        scroll="auto",
        controls=[
            ft.TextButton("Fechar", on_click=esconder_help),
            ft.Text(
                value="---------------- ATENÇÃO ----------------",
                size= 16,
                weight=ft.FontWeight.BOLD
            ),
            ft.Text(
                "Todos os calculos foram baseados na NBR-5410.\n"
                "O programa está definido para utilizar apenas:\n"
                "• Tipo de isolador do cabo - PVC.\n"
                "• Método de instalação - B1.\n"
                "• Número de condutores carregados - 2.\n"
                "• Tensão - 127v ou 220v.\n"
                "• Cabos de cobre - de 2,5 até 120 mm².\n"
                "• Capacidade dos disjuntores - de 6 a 125 Amperes.\n"
                "• Número de circuitos agrupados - 1 ou mais.\n"
                "• Temperatura ambiente - de 10 a 60 graus Celsius.\n"
                "• Fator de potência - de 0.00 até 1.00.\n"
                "O programa automaticamente inicia com FP de 0.92 mas pode ser alterado.\n" 
                "Quando o botão equipamento resistivo for ativado o FP será 1.00,\n"
                "basta desligalo para voltar a opção de alterar o FP.\n"
                "O programa vai automaticamente acrescentar de 15 a 10 porcento na corrente necessária do equipamento, após ela já ter sido corrigida pelos fatores acima descritos."
            ),

            ft.Text(
                value= "----------- TABELAS NBR 5410 -----------",
                size= 16,
                weight=ft.FontWeight.BOLD        
            ),
            ft.Text(
                "• Método de instalaçao B1 - tabela 33 págiga 90.\n",
                spans=[
                    ft.TextSpan(
                        "TABELA 33 - Tipos de linhas elétricas",
                        url="https://static.wixstatic.com/media/cb85c2_95059abcb3e341b98e880478155c9262~mv2.png/v1/fill/w_350,h_716,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/cb85c2_95059abcb3e341b98e880478155c9262~mv2.png",
                        style=ft.TextStyle(
                            color=ft.Colors.BLUE,
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    )
                ]
            ),           
            ft.Text(
                "• Máxima condução do cabo 30° - tabela 36 págiga 101.\n",
                spans=[
                    ft.TextSpan(
                        "TABELA 36 - Capacidades de condução de corrente",
                        url="https://blog.rhmateriaiseletricos.com.br/wp-content/uploads/2019/06/Tabela-de-Dimensionamento-de-Cabos-El%C3%A9tricos.png",
                        style=ft.TextStyle(
                            color=ft.Colors.BLUE,
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    )
                ]
            ),
            ft.Text(
                "• Fator temperatura diferente de 30° - tabela 40 págiga 106.\n",
                spans=[
                    ft.TextSpan(
                        "TABELA 40 - Fatores de correção para temperaturas ambientes",
                        url="https://viverdeeletrica.com/wp-content/uploads/2022/04/tabela-de-cabos-com-fator-de-correcao-ambiente-NBR-5410-tabela-40-1024x651.jpg.webp",
                        style=ft.TextStyle(
                            color=ft.Colors.BLUE,
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    )
                ]
            ),
            ft.Text(
                "• Fator de agrupamento - tabela 42 págiga 108.\n",
                spans=[
                    ft.TextSpan(
                        "TABELA 42 - Fatores de correção para condutores agrupados",
                        url="https://blog.rhmateriaiseletricos.com.br/wp-content/uploads/2019/06/Tabela-42-da-NBR5410.png",
                        style=ft.TextStyle(
                            color=ft.Colors.BLUE,
                            decoration=ft.TextDecoration.UNDERLINE
                        )
                    )
                ]
            ),
            ft.Text(
                value= "------------- SOBRE O APK --------------",
                size= 16,
                weight=ft.FontWeight.BOLD        
            ),
            ft.Text(
                "Nome: Dimensionar\n"
                "versão: Beta-0.2\n"
                "Criador: Rafael Alves(Craker)2025\n",
                spans=[
                    ft.TextSpan(
                        "Outros projetos no GITHUB",
                        url="https://github.com/rafa-nunes18",
                        style=ft.TextStyle(
                            color=ft.Colors.BLUE,
                            decoration=ft.TextDecoration.UNDERLINE
                        )    
                    )
                ],
            ),
            ft.Text(    
                "Criado com:\n"
                "• Windows 11\n"
                "• VsCode\n"
                "• Phyton\n"
                "• Flet"
            ),
            ft.TextButton("Fechar", on_click=esconder_help)
        ],
        expand=True
    )

    info_box = ft.Container(
        content=conteudo_com_rolagem,
        bgcolor=ft.Colors.WHITE54,
        padding=20,
        border_radius=10,
        width=400,
        height=650, 
        visible=False
    )

    botao_info = ft.ElevatedButton(
        text="INFO",
        width=80,
        height=50,        
        on_click=mostrar_info,
        bgcolor= ft.Colors.WHITE70,
        visible= False        
    )
    botao_help = ft.ElevatedButton(
        text="HELP",
        width=50,
        height=50,        
        on_click=mostrar_help,
        bgcolor= ft.Colors.WHITE70,       
    )

    botao_audio= ft.ElevatedButton(
        "Pause playing",
        style=ft.ButtonStyle(text_style=ft.TextStyle(
            size=12
            )
        ),
        width=50,
        height=50,
         on_click=lambda _: audio.pause()
    )

    titulo = ft.Text(
        value="Dimensionar",
        size= 35,
        weight=ft.FontWeight.BOLD
    )

    resultado_completo = ft.Text(
        value="casa",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    resultado = ft.Text(
        value="Resultados",
        size= 25,
        weight=ft.FontWeight.BOLD
    )

    resistivo = ft.Text(
        value="Equipamento Resistivo",
        size= 25,
        weight=ft.FontWeight.BOLD
    )
    
    resistivo_switch = ft.Switch(
        value=False,
        on_change=switch_changed
    )

    fator_poten = ft.TextField(
        label="FATOR POTÊNCIA",
        hint_text="FP",
        value= .92,
        label_style=ft.TextStyle(
            size=22,
            weight=ft.FontWeight.BOLD
        ),
        width=170,
        height=60,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD            
        ),
        text_align=ft.TextAlign.CENTER
    )

    potencia = ft.TextField(
        label="Potência(W)",
        hint_text="WATTS",
        label_style=ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
        ),
        width=180,
        height=60,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        ),
        text_align=ft.TextAlign.CENTER
    )

    temperatura  = ft.TextField(
        label="Temperatura",
        hint_text="Graus(°C)",
        label_style=ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
        ),
        width=180,
        height=60,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD  
        ),
        text_align=ft.TextAlign.CENTER
    )

    circuito  = ft.TextField(
        label="Circuitos",
        hint_text="FA",
        label_style=ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
        ),
        width=170,
        height=60,
        text_style= ft.TextStyle(
            size=30,
            weight=ft.FontWeight.BOLD
        ),
        text_align=ft.TextAlign.CENTER
    )

    resultado_ft = ft.TextField(
        label="Fator Temperatura",
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
        width=130,
        text_align=ft.TextAlign.CENTER
    )

    resultado_fa = ft.TextField(
        label="Fator Agrupamento",
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
        width=135,
        text_align=ft.TextAlign.CENTER
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
        bgcolor=ft.Colors.WHITE54,
        read_only=True,
        filled=True,
        width=140,
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
        width=140,
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
        label="Tensão",
        hint_text="VOLTS", 
        label_style=ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
            ),
        text_style= ft.TextStyle(
            size=25,
            weight=ft.FontWeight.BOLD
            ),
        width=175,
      
        focused_border_color='transparent',
        options=
        [
            ft.DropdownOption("127"),
            ft.DropdownOption("220")
        ]        
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
                        ft.Container(content=info_box),  
                        ft.Row(
                            [
                             titulo,
                             botao_audio],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [                            
                             resistivo,
                             resistivo_switch
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [potencia,
                             fator_poten
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                             temperatura,
                             circuito,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row(
                            [
                             dropdown,
                              ft.Container(
                                content=botao_iniciar,
                                margin=ft.Margin(top=0, right= 35, bottom=0, left=0)  
                             )                           
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        ft.Row([
                            resultado 
                            ],
                            alignment=ft.MainAxisAlignment.CENTER                        
                        ),
                        ft.Row([
                            resultado_ft,
                            botao_info,
                            resultado_fa
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
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
                             botao_help,
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
    page.dialog = aviso_dialog       
    page.update()

ft.app(target=main,  assets_dir="assets")