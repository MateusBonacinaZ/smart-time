# INDIVÍDUO, TERMO, DIA, MATÉRIA...

from datetime import datetime
import pandas as pd
import json
import random
import os


class SmartTime:
    def __init__(self):
        self.numero_geracoes, self.tamanho_populacao, self.numero_termos, self.numero_aulas, self.numero_dias, self.numero_professores, self.disponibilidade_professores, self.informacoes_excel = self.coletar_informacoes()
        self.verificar_erros_importacao()
        self.populacao = self.gerar_populacao_inicial()

        lista_media = []
        self.melhor_individuo = {
            "Pontuação": 0,
            "Index": None,
            "Grade": None
        }

        for geracao in range(1, self.numero_geracoes+1):
            print(f"Geração: {geracao}")
            self.fitness_populacao = self.avaliar_populacao()

            lista_media.append(sum(self.fitness_populacao)/len(self.fitness_populacao))


            if max(self.fitness_populacao) > self.melhor_individuo["Pontuação"]:
                self.melhor_individuo = {
                    "Pontuação": max(self.fitness_populacao),
                    "Grade": self.populacao[self.fitness_populacao.index(max(self.fitness_populacao))]
                }

            if geracao == 1:
                self.valor_inicial = self.melhor_individuo

            self.vetor_roleta = self.gerar_roleta()
            self.populacao = self.gerar_nova_populacao()

        self.salvar_excel()
        print("Estatísticas: ")
        print(f"Foram avaliadas {self.tamanho_populacao*self.numero_geracoes}.")
        print(f"A média das grades foram {round(sum(lista_media)/len(lista_media), 2)}.")
        print(f"A grade evoluiu de {self.valor_inicial['Pontuação']} -> {self.melhor_individuo['Pontuação']}.")
        print(f"Você pode encontrar o melhor indivíduo na pasta de resultados!")


    @staticmethod
    def coletar_informacoes():
        tamanho_populacao = None
        numero_termos = None
        numero_aulas = None
        numero_dias = None
        numero_professores = None
        numero_geracoes = None
        informacoes_completas = []

        df = pd.read_excel(f"{os.path.dirname(os.path.realpath(__file__))}/planilha.xlsx")
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/disponibilidade.json", encoding="utf-8") as f:
            disponibilidade_professores = json.load(f)

        for configuracao in df['Configurações']:
            if pd.isnull(configuracao) is False:
                if "gerações" in str(configuracao):
                    numero_geracoes = int(str(configuracao).split(':')[1].strip())
                elif "população" in str(configuracao):
                    tamanho_populacao = int(str(configuracao).split(':')[1].strip())
                elif "termos" in str(configuracao):
                    numero_termos = int(str(configuracao).split(':')[1].strip())
                elif "aulas" in str(configuracao):
                    numero_aulas = int(str(configuracao).split(':')[1].strip())
                elif "dias" in str(configuracao):
                    numero_dias = int(str(configuracao).split(':')[1].strip())
                elif "professores" in str(configuracao):
                    numero_professores = int(str(configuracao).split(':')[1].strip())

        for termo in range(1, numero_termos+1):

            informacoes_termo = []
            for aula in df[f'{termo}° Termo']:

                if pd.isnull(aula) is False:
                    infos = str(aula).split("/")
                    informacoes_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))

            informacoes_termo.sort(key=lambda x: x[2], reverse=True)
            informacoes_completas.append(informacoes_termo)

        return numero_geracoes, tamanho_populacao, numero_termos, numero_aulas, numero_dias, numero_professores, disponibilidade_professores, informacoes_completas

    def verificar_erros_importacao(self):

        if len(self.disponibilidade_professores) != self.numero_professores:
            print("Número de professores incorreto!")
            quit()

        if len(self.informacoes_excel) != self.numero_termos:
            print("Número de termos incorreto!")
            quit()

        for professor_disponivel in self.disponibilidade_professores:
            if len(self.disponibilidade_professores[professor_disponivel]) != self.numero_dias:
                print("ERRO: Quantidade de dias discrepante!")
                quit()

            for dia_disponivel in self.disponibilidade_professores[professor_disponivel]:
                if len(self.disponibilidade_professores[professor_disponivel][dia_disponivel]) != 0:
                    if max(self.disponibilidade_professores[professor_disponivel][dia_disponivel]) > self.numero_aulas-1:
                        print("ERRO: Quantidade de aulas discrepante!")
                        quit()

        for termo in range(self.numero_termos):
            for disciplina in range(len(self.informacoes_excel[termo])):
                if self.informacoes_excel[termo][disciplina][1] not in self.disponibilidade_professores:
                    print("ERRO: Professores discrepantes!")
                    quit()

    def gerar_populacao_inicial(self):
        populacao = []

        tamanho = len(populacao)
        while tamanho != self.tamanho_populacao:
            individuo = self.gerar_cromossomo()

            if individuo is not False:
                populacao.append(individuo)
                tamanho = len(populacao)

        return populacao

    def gerar_cromossomo(self):
        matriz_grade = []

        for matriz_termos in range(self.numero_termos):
            matriz_grade.append([])

            for matriz_dias in range(self.numero_dias):
                matriz_grade[matriz_termos].append([])

                for matriz_aulas in range(self.numero_aulas):
                    matriz_grade[matriz_termos][matriz_dias].append(None)

        for termo in range(self.numero_termos):

            disciplinas_termo = []
            for disciplina in self.informacoes_excel[termo]:
                disciplinas_termo.append(disciplina)

            for dia in range(self.numero_dias):

                erro = 0
                while matriz_grade[termo][dia].count(None) != 0:
                    contador = 0

                    disciplina_sorteada = random.randint(0, len(disciplinas_termo)-1)

                    if matriz_grade[termo][dia].count(None) >= int(disciplinas_termo[disciplina_sorteada][2]):
                        for aula in range(int(disciplinas_termo[disciplina_sorteada][2])):
                            posicao = matriz_grade[termo][dia].index(None)
                            if self.verificar_choques(matriz_grade, termo, dia, posicao, disciplinas_termo[disciplina_sorteada][1]) is False:
                                matriz_grade[termo][dia][posicao] = (f'{disciplinas_termo[disciplina_sorteada][0]}', f'{disciplinas_termo[disciplina_sorteada][1]}')
                                contador += 1
                            else:
                                erro += 1
                                if erro == 50:
                                    return False

                    elif matriz_grade[termo][dia].count(None) < int(disciplinas_termo[disciplina_sorteada][2]):
                        for aula in range(matriz_grade[termo][dia].count(None)):
                            posicao = matriz_grade[termo][dia].index(None)
                            if self.verificar_choques(matriz_grade, termo, dia, posicao, disciplinas_termo[disciplina_sorteada][1]) is False:
                                matriz_grade[termo][dia][posicao] = (f'{disciplinas_termo[disciplina_sorteada][0]}', f'{disciplinas_termo[disciplina_sorteada][1]}')
                                contador += 1
                            else:
                                erro += 1
                                if erro == 50:
                                    return False

                    if int(disciplinas_termo[disciplina_sorteada][2]) == contador:
                        disciplinas_termo.remove(disciplinas_termo[disciplina_sorteada])
                    else:
                        copia_disciplina = (f'{disciplinas_termo[disciplina_sorteada][0]}', f'{disciplinas_termo[disciplina_sorteada][1]}', f'{int(disciplinas_termo[disciplina_sorteada][2]) - contador}')
                        disciplinas_termo.remove(disciplinas_termo[disciplina_sorteada])
                        disciplinas_termo.append(copia_disciplina)

        return matriz_grade

    @staticmethod
    def verificar_choques(individuo, termo_individuo, dia_individuo, aula_individuo, professor_sorteado):
        if termo_individuo != 0:
            for termo_comparacao in range(0, termo_individuo):
                if individuo[termo_comparacao][dia_individuo][aula_individuo][1] == professor_sorteado:
                    return True
        return False

    def verificar_choques_crossover(self, individuo):
        for termo_fixo in range(self.numero_termos):

            for aula in range(self.numero_aulas):

                for dia in range(self.numero_dias):

                    for termo in range(termo_fixo+1, self.numero_termos):

                        if individuo[termo_fixo][dia][aula][1] == individuo[termo][dia][aula][1]:
                            return True

        return False

    def avaliar_populacao(self):
        fitness_populacao = []

        for individuo in self.populacao:
            valor_fitness = int(self.funcao_fitness(individuo))
            fitness_populacao.append(valor_fitness)
            # print(f"O valor fitness do indivíduo é: {valor_fitness}")

        return fitness_populacao

    def funcao_fitness(self, individuo):
        valor_fitness = 0

        for termo_fixo in range(self.numero_termos):

            for aula in range(self.numero_aulas):

                for dia in range(self.numero_dias):

                    for termo in range(termo_fixo+1, self.numero_termos):

                        if individuo[termo_fixo][dia][aula][1] == individuo[termo][dia][aula][1]:
                            valor_fitness = 0
                            return valor_fitness

        for termo in range(self.numero_termos):

            for dia in range(self.numero_dias):

                for aula in range(self.numero_aulas):
                    informacao_disponibilidade = self.disponibilidade_professores[individuo[termo][dia][aula][1]]

                    if dia == 0:
                        informacao_disponibilidade = informacao_disponibilidade["Segunda"]
                    elif dia == 1:
                        informacao_disponibilidade = informacao_disponibilidade["Terça"]
                    elif dia == 2:
                        informacao_disponibilidade = informacao_disponibilidade["Quarta"]
                    elif dia == 3:
                        informacao_disponibilidade = informacao_disponibilidade["Quinta"]
                    elif dia == 4:
                        informacao_disponibilidade = informacao_disponibilidade["Sexta"]
                    elif dia == 5:
                        informacao_disponibilidade = informacao_disponibilidade["Sábado"]
                    elif dia == 6:
                        informacao_disponibilidade = informacao_disponibilidade["Domingo"]

                    if aula in informacao_disponibilidade:
                        valor_fitness += 1

        for termo in range(self.numero_termos):

            disciplinas_termo = []
            for disciplina in self.informacoes_excel[termo]:
                if int(disciplina[2]) >= self.numero_aulas:
                    disciplinas_termo.append(disciplina)

            for dia in range(self.numero_dias):

                disciplinas_dia = []
                for aula in range(self.numero_aulas):
                    disciplinas_dia.append(individuo[termo][dia][aula][0])

                for disciplina_comparacao in disciplinas_termo:
                    if disciplinas_dia.count(disciplina_comparacao[0]) == self.numero_aulas:
                        valor_fitness += 1

        return valor_fitness

    def gerar_roleta(self):
        vetor_roleta = []
        soma_fitness = sum(self.fitness_populacao)

        melhor_individuo = {
            "Individuo": 0,
            "Valor": 0
        }

        for individuo in range(self.tamanho_populacao):

            valor = (self.fitness_populacao[individuo]/soma_fitness)*100
            peso_roleta = int(round(valor))

            if valor > melhor_individuo["Valor"]:
                melhor_individuo["Individuo"] = individuo
                melhor_individuo["Valor"] = valor

            for posicao in range(peso_roleta):
                if len(vetor_roleta) > 99:
                    break
                else:
                    vetor_roleta.append(individuo)

        if len(vetor_roleta) < 100:
            for individuo in range(len(vetor_roleta), 100):
                vetor_roleta.append(melhor_individuo["Individuo"])
            vetor_roleta = sorted(vetor_roleta)

        return vetor_roleta

    def gerar_nova_populacao(self):
        trava = True
        while trava is not False:
            nova_populacao = []

            roleta = []
            for ponto in self.vetor_roleta:
                roleta.append(ponto)

            tamanho_nova_populacao = len(nova_populacao)
            tamanho_atual_populacao = len(self.populacao)
            erros = 0
            while tamanho_nova_populacao != tamanho_atual_populacao:
                index_individuo_1 = random.choice(roleta)
                index_individuo_2 = random.choice(roleta)

                if index_individuo_1 != index_individuo_2:
                    termo_corte = random.randint(1, self.numero_termos)

                    individuo_1 = self.populacao[index_individuo_1]
                    individuo_2 = self.populacao[index_individuo_2]

                    individuo_1_modificado = individuo_1[:termo_corte]+individuo_2[termo_corte:]
                    individuo_2_modificado = individuo_2[:termo_corte] + individuo_1[termo_corte:]

                    individuos_modificados = []
                    for individuo in range(1,3):
                        if individuo == 1:
                            individuos_modificados.append(individuo_1_modificado)
                        elif individuo == 2:
                            individuos_modificados.append(individuo_2_modificado)

                    choque = False
                    for individuo in individuos_modificados:
                        if self.verificar_choques_crossover(individuo):
                            choque = True
                            erros += 1
                            break

                    if erros > 1000:
                        break

                    if choque is False:

                        index_remover = []
                        for posicao in range(len(roleta)):
                            if roleta[posicao] == index_individuo_1 or roleta[posicao] == index_individuo_2:
                                index_remover.append(posicao)

                        index_remover = sorted(index_remover, reverse = True)

                        for posicao in index_remover:
                            del roleta[posicao]

                        for individuo in individuos_modificados:
                            nova_populacao.append(individuo)

                        tamanho_nova_populacao = len(nova_populacao)

            if tamanho_nova_populacao == tamanho_atual_populacao:
                trava = False

        # nova_populacao.remove(random.choice(nova_populacao))
        # nova_populacao.append(self.melhor_individuo["Grade"])

        return nova_populacao

    def salvar_excel(self):

        dados = {}
        dict_termo_horario = {"Aula e termo": []}
        for termo in range(1, self.numero_termos+1):
            for aula in range(1, self.numero_aulas+1):
                dict_termo_horario["Aula e termo"].append(f"{aula}° aula - {termo}° termo")
            dict_termo_horario["Aula e termo"].append("")
        dados.update(dict_termo_horario)

        for dia in range(self.numero_dias):

            dict_dia = {}
            if dia == 0:
                dict_dia = {"Segunda-feira": []}
                index_dia = dict_dia["Segunda-feira"]
            elif dia == 1:
                dict_dia = {"Terça-feira": []}
                index_dia = dict_dia["Terça-feira"]
            elif dia == 2:
                dict_dia = {"Quarta-feira": []}
                index_dia = dict_dia["Quarta-feira"]
            elif dia == 3:
                dict_dia = {"Quinta-feira": []}
                index_dia = dict_dia["Quinta-feira"]
            elif dia == 4:
                dict_dia = {"Sexta-feira": []}
                index_dia = dict_dia["Sexta-feira"]
            elif dia == 5:
                dict_dia = {"Sábado": []}
                index_dia = dict_dia["Sábado"]
            elif dia == 6:
                dict_dia = {"Domingo": []}
                index_dia = dict_dia["Domingo"]

            for termo in range(self.numero_termos):

                for aula in range(self.numero_aulas):
                    disciplina = self.melhor_individuo["Grade"][termo][dia][aula][0]
                    professor = self.melhor_individuo["Grade"][termo][dia][aula][1]
                    index_dia.append(f"{disciplina}, {professor}")

                index_dia.append("")

            dados.update(dict_dia)

        data_frame = pd.DataFrame(dados)
        data_frame.to_excel(f"{os.path.dirname(os.path.realpath(__file__))}/Resultados/{datetime.now().strftime('%d-%m-%Y %Hh %Mm')} ({self.melhor_individuo['Pontuação']}).xlsx")

SmartTime()
