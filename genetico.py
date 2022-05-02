# INDIVÍDUO, TERMO, DIA, MATÉRIA...

import pandas as pd
import json
import random
import os


class SmartTime:
    def __init__(self):
        self.tamanho_populacao, self.numero_termos, self.numero_aulas, self.numero_dias, self.numero_professores, self.disponibilidade_professores, self.informacoes_excel = self.coletar_informacoes()
        self.verificar_erros_importacao()
        self.populacao_inicial = self.gerar_populacao()
        self.avaliar_populacao(self.populacao_inicial)

    @staticmethod
    def coletar_informacoes():
        tamanho_populacao = None
        numero_termos = None
        numero_aulas = None
        numero_dias = None
        numero_professores = None
        informacoes_completas = []

        df = pd.read_excel(f"{os.path.dirname(os.path.realpath(__file__))}/planilha.xlsx")
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/disponibilidade.json") as f:
            disponibilidade_professores = json.load(f)

        for configuracao in df['Configurações']:
            if pd.isnull(configuracao) is False:
                if "população" in str(configuracao):
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

        return tamanho_populacao, numero_termos, numero_aulas, numero_dias, numero_professores, disponibilidade_professores, informacoes_completas

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

    def gerar_populacao(self):
        populacao = []

        for individuo in range(self.tamanho_populacao):
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

                    while matriz_grade[termo][dia].count(None) != 0:

                        disciplina_sorteada = random.randint(0, len(disciplinas_termo)-1)

                        if matriz_grade[termo][dia].count(None) >= int(disciplinas_termo[disciplina_sorteada][2]):
                            contador = 0
                            for aula in range(len(matriz_grade[termo][dia])):
                                if matriz_grade[termo][dia][aula] is None:
                                    contador += 1
                                    if int(disciplinas_termo[disciplina_sorteada][2]) >= contador:
                                        matriz_grade[termo][dia][aula] = (f'{disciplinas_termo[disciplina_sorteada][0]}', f'{disciplinas_termo[disciplina_sorteada][1]}')
                            disciplinas_termo.remove(disciplinas_termo[disciplina_sorteada])

                        elif matriz_grade[termo][dia].count(None) < int(disciplinas_termo[disciplina_sorteada][2]):
                            contador = 0
                            for aula in range(len(matriz_grade[termo][dia])):
                                if matriz_grade[termo][dia][aula] is None:
                                    contador += 1
                                    matriz_grade[termo][dia][aula] = (f'{disciplinas_termo[disciplina_sorteada][0]}', f'{disciplinas_termo[disciplina_sorteada][1]}')
                            copia_disciplina = (f'{disciplinas_termo[disciplina_sorteada][0]}', f'{disciplinas_termo[disciplina_sorteada][1]}', f'{int(disciplinas_termo[disciplina_sorteada][2])-contador}')
                            disciplinas_termo.remove(disciplinas_termo[disciplina_sorteada])
                            disciplinas_termo.append(copia_disciplina)

            populacao.append(matriz_grade)
        """
        for pop in populacao:
            print(pop, end="\n\n\n")
        """
        return populacao

    def avaliar_populacao(self, pop):
        fitness_populacao = []

        for individuo in pop:
            valor_fitness = int(self.funcao_fitness(individuo))
            fitness_populacao.append(valor_fitness)
            print(f"O valor fitness do indivíduo é: {valor_fitness}")

    def funcao_fitness(self, individuo):
        valor_fitness = 0

        """indi = [
            [[('Logica de programação', 'Hilário'), ('Logica de programação', 'Hilário'), ('Logica de programação', 'Hilário'), ('Logica de programação', 'Hilário')], [('Fundamentos de leitura e produção de textos', 'Eloiza'), ('Fundamentos de leitura e produção de textos', 'Eloiza'), ('Sociedade, tecnologia e inovação', 'Cézar'), ('Sociedade, tecnologia e inovação', 'Cézar')], [('Matemática Discreta', 'Marçal'), ('Matemática Discreta', 'Marçal'), ('Matemática Discreta', 'Marçal'), ('Matemática Discreta', 'Marçal')], [('Produção vegetal de culturas anuais', 'Élvio'), ('Produção vegetal de culturas anuais', 'Élvio'), ('Inglês I', 'Eloiza'), ('Inglês I', 'Eloiza')], [('Ética e valores', 'Cézar'), ('Ética e valores', 'Cézar'), ('Introdução a big data', 'Allan'), ('Introdução a big data', 'Allan')]],
            [[('Java I orientação a objetos', 'Isaque'),('Java I orientação a objetos', 'Isaque'),('Java I orientação a objetos', 'Isaque'),('Java I orientação a objetos', 'Isaque')], [('Produção vegetal de culturas perenes e green houses', 'Élvio'),('Produção vegetal de culturas perenes e green houses', 'Élvio'),('', 'Eloiza'),('', 'Eloiza')], [('','Favan'),('','Favan'),('','Favan'),('','Favan')], [('', 'Cézar'),('', 'Cézar'),('', 'Dario'),('', 'Dario')], [('','Marçal'),('','Marçal'),('','Marçal'),('','Marçal')]],
            [[('','Favan'),('','Favan'),('','Marisa'),('','Marisa')], [('', 'Isaque'),('', 'Isaque'),('', 'Isaque'),('', 'Isaque')], [('', 'Deise'),('', 'Deise'),('', 'Deise'),('', 'Deise')], [('', 'Eloiza'),('', 'Eloiza'),('','Marçal'),('','Marçal')], [('','Querino'),('','Querino'),('','Querino'),('','Querino')]],
            [[('', 'Eloiza'),('', 'Eloiza'),('', 'Faulin'),('', 'Faulin')], [('', 'Marcel'),('', 'Marcel'),('', 'Marcel'),('', 'Marcel')], [('', 'Adriano'),('', 'Adriano'),('', 'Adriano'),('', 'Adriano')], [('', 'Adriano'),('', 'Adriano'),('','Cézar'),('','Cézar')], [('', 'Adriano'),('', 'Adriano'),('', 'Adriano'),('', 'Adriano')]],
            [[('','Marisa'), ('','Marisa'), ('','Favan'), ('','Favan')], [('','Favan'),('','Favan'),('','Favan'),('','Favan')], [('','Querino'),('','Querino'),('','Querino'),('','Querino')], [('','Querino'),('','Querino'),('','Querino'),('','Querino')], [('', 'Marcel'),('', 'Marcel'),('', 'Eloiza'),('', 'Eloiza')]],
            [[('','Querino'), ('','Querino'), ('', 'Eloiza'), ('', 'Eloiza')], [('','Querino'), ('','Querino'), ('','Querino'), ('','Querino')], [('', 'Mauricio'), ('', 'Mauricio'), ('', 'Mauricio'), ('', 'Mauricio')], [('','Favan'), ('','Favan'), ('','Favan'), ('','Favan')], [('','Favan'), ('','Favan'), ('','Favan'), ('','Favan')]],
        ]"""

        """
        for termo_fixo in range(self.numero_termos):

            for aula in range(self.numero_aulas):

                for dia in range(self.numero_dias):

                    for termo in range(termo_fixo+1, self.numero_termos):

                        if individuo[termo_fixo][dia][aula][1] == individuo[termo][dia][aula][1]:
                            valor_fitness = 0
                            return valor_fitness
        """

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
        """
        picote = False
        for termo in range(self.numero_termos):
            disciplinas_termo = []
            for disciplina in self.informacoes_excel[termo]:
                disciplinas_termo.append(disciplina)

            for dia in range(self.numero_dias):
                aula = 0
                primeira_execucao = True

                while aula < self.numero_aulas:
                    for x in disciplinas_termo:
                        if x[0] == individuo[termo][dia][aula][0]:
                            disciplina = x
                            break

                    #print(individuo[termo][dia][aula])
                    #print(x)
                    #print(disciplinas_termo, end="\n\n")

                    if int(disciplina[2]) <= self.numero_aulas:
                        if aula+int(disciplina[2]) <= self.numero_aulas:
                            for verificacao in range(1, int(disciplina[2])):
                                if individuo[termo][dia][aula-1][0] != individuo[termo][dia][aula+verificacao-1][0]:
                                    picote = True
                                    print("Picotou")
                                    break
                        else:
                            picote = True
                            print("Picotou")
                            break
                        disciplinas_termo.remove(disciplina)

                    elif int(disciplina[2]) > self.numero_aulas:
                        for verificacao in range(1, self.numero_aulas):
                            if individuo[termo][dia][aula-1][0] != individuo[termo][dia][aula+verificacao-1][0]:
                                picote = True
                                print("Picotou")
                                break

                        copia_disciplina = (f'{disciplina[0]}', f'{disciplina[1]}', f'{int(disciplina[2])-self.numero_aulas}')
                        disciplinas_termo.remove(disciplina)
                        disciplinas_termo.append(copia_disciplina)

                    aula += int(disciplina[2])
                    print(aula)

                if picote is True:
                    break

            if picote is True:
                break

        if picote is False:
            for termo in range(self.numero_termos):
                print(individuo[termo], end="\n\n")
        """
        return valor_fitness


SmartTime()
