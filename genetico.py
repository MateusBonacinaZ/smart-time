# INDIVÍDUO, TERMO, DIA, MATÉRIA...

import pandas as pd
import random
import os


class SmartTime:
    def __init__(self):
        self.tamanho_populacao, self.numero_termos, self.numero_aulas, self.numero_dias, self.informacoes_excel\
            = self.coletar_informacoes()
        self.populacao_inicial = self.gerar_populacao()

    @staticmethod
    def coletar_informacoes():
        df = pd.read_excel(f"{os.path.dirname(os.path.realpath(__file__))}/planilha.xlsx")

        tamanho_populacao = None
        numero_termos = None
        numero_aulas = None
        numero_dias = None

        primeiro_termo = []
        segundo_termo = []
        terceiro_termo = []
        quarto_termo = []
        quinto_termo = []
        sexto_termo = []
        informacoes_completas = []

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

        for termo in range(1, numero_termos+1):
            for aula in df[f'{termo}° Termo']:
                if pd.isnull(aula) is False:
                    infos = str(aula).split("/")
                    if termo == 1:
                        primeiro_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))
                    elif termo == 2:
                        segundo_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))
                    elif termo == 3:
                        terceiro_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))
                    elif termo == 4:
                        quarto_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))
                    elif termo == 5:
                        quinto_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))
                    elif termo == 6:
                        sexto_termo.append((f'{infos[0].strip()}', f'{infos[1].strip()}', f'{int(str(infos[2]).strip())}'))

        primeiro_termo.sort(key=lambda x: x[2], reverse=True)
        segundo_termo.sort(key=lambda x: x[2], reverse=True)
        terceiro_termo.sort(key=lambda x: x[2], reverse=True)
        quarto_termo.sort(key=lambda x: x[2], reverse=True)
        quinto_termo.sort(key=lambda x: x[2], reverse=True)
        sexto_termo.sort(key=lambda x: x[2], reverse=True)

        informacoes_completas.append(primeiro_termo)
        informacoes_completas.append(segundo_termo)
        informacoes_completas.append(terceiro_termo)
        informacoes_completas.append(quarto_termo)
        informacoes_completas.append(quinto_termo)
        informacoes_completas.append(sexto_termo)

        return tamanho_populacao, numero_termos, numero_aulas, numero_dias, informacoes_completas

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
        for pop in populacao:
            print(pop, end="\n\n\n")
        return populacao


SmartTime()

"""
for aula in df["1° Termo"]:
    if pd.isnull(aula) is False:
        infos = str(aula).split("-")
        primeiro_termo.append((f'{infos[0]}', f'{infos[1]}', f'{infos[2]}'))

for aula in df["2° Termo"]:
    if pd.isnull(aula) is False:
        infos = str(aula).split("-")
        segundo_termo.append((f'{infos[0]}', f'{infos[1]}', f'{infos[2]}'))

for aula in df["3° Termo"]:
    if pd.isnull(aula) is False:
        infos = str(aula).split("-")
        terceiro_termo.append((f'{infos[0]}', f'{infos[1]}', f'{infos[2]}'))

for aula in df["4° Termo"]:
    if pd.isnull(aula) is False:
        infos = str(aula).split("-")
        quarto_termo.append((f'{infos[0]}', f'{infos[1]}', f'{infos[2]}'))

for aula in df["5° Termo"]:
    if pd.isnull(aula) is False:
        infos = str(aula).split("-")
        quinto_termo.append((f'{infos[0]}', f'{infos[1]}', f'{infos[2]}'))

for aula in df["6° Termo"]:
    if pd.isnull(aula) is False:
        infos = str(aula).split("-")
        sexto_termo.append((f'{infos[0]}', f'{infos[1]}', f'{infos[2]}'))


        for individuo in range(TAM_POPULACAO):
            grade_list = []

            for termo in range(NUM_TERMOS):

                copia_termo = []
                for disciplina in self.informacoes_excel[termo]:
                    for aula in range(int(disciplina[2])):
                        copia_termo.append((f'{disciplina[0]}', f'{disciplina[1]}'))

                termo_list = []
                for quantidade_aulas in range(len(copia_termo)):
                    aleatorio = random.choice(copia_termo)
                    copia_termo.remove(aleatorio)
                    termo_list.append(aleatorio)

                grade_list.append(termo_list)

            populacao.append(grade_list)



                    
                    if int(disciplinas_termo[disciplina][2]) >= 4:
                        if matriz_grade[termo][dia] == [None, None, None, None]:
                            if int(disciplinas_termo[disciplina][2]) == 4:
                                for x in range(self.numero_aulas):
                                    matriz_grade[termo][dia][x] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                                disciplinas_termo.remove(disciplinas_termo[disciplina])
                            elif int(disciplinas_termo[disciplina][2]) > 4:
                                for x in range(self.numero_aulas):
                                    matriz_grade[termo][dia][x] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                                disciplinas_termo[disciplina][2] = disciplinas_termo[disciplina][2] - 4
                    




                disciplinas_termo = []
                for disciplina in self.informacoes_excel[termo]:
                    for numero in range(int(disciplina[2])):
                        disciplinas_termo.append((f'{disciplina[0]}', f'{disciplina[1]}'))

                for dia in range(self.numero_dias):
                    for aula in range(self.numero_aulas):
                        if matriz_grade[termo][dia][aula] is None:
                            contador = 0
                            materia = random.choice(disciplinas_termo)
                            while materia in disciplinas_termo:
                                try:
                                    if contador != 0:
                                        matriz_grade[termo][dia][aula+contador] = materia
                                    else:
                                        matriz_grade[termo][dia][aula] = materia
                                    disciplinas_termo.remove(materia)
                                    contador += 1
                                except IndexError:
                                    break

"""


"""
                    disciplina = random.randint(0, len(disciplinas_termo)-1)
                    dia = random.randint(0, self.numero_dias - 1)

                    print(len(disciplinas_termo))

                    if int(disciplinas_termo[disciplina][2]) > 4:
                        if matriz_grade[termo][dia].count(None) >= 4:
                            for campo in range(self.numero_aulas):
                                if matriz_grade[termo][dia][campo] is None:
                                    matriz_grade[termo][dia][campo] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                            disciplinas_termo[disciplina][2] = disciplinas_termo[disciplina][2] - self.numero_aulas

                    elif int(disciplinas_termo[disciplina][2]) == 4:
                        if matriz_grade[termo][dia].count(None) >= 4:
                            for campo in range(self.numero_aulas):
                                if matriz_grade[termo][dia][campo] is None:
                                    matriz_grade[termo][dia][campo] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                            disciplinas_termo.remove(disciplinas_termo[disciplina])

                    elif int(disciplinas_termo[disciplina][2]) == 3:
                        if matriz_grade[termo][dia].count(None) >= 3:
                            for campo in range(self.numero_aulas):
                                if matriz_grade[termo][dia][campo] is None:
                                    matriz_grade[termo][dia][campo] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                            disciplinas_termo.remove(disciplinas_termo[disciplina])

                    elif int(disciplinas_termo[disciplina][2]) == 2:
                        if matriz_grade[termo][dia].count(None) >= 2:
                            for campo in range(self.numero_aulas):
                                if matriz_grade[termo][dia][campo] is None:
                                    matriz_grade[termo][dia][campo] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                            disciplinas_termo.remove(disciplinas_termo[disciplina])

                    elif int(disciplinas_termo[disciplina][2]) == 1:
                        if matriz_grade[termo][dia].count(None) >= 1:
                            for campo in range(self.numero_aulas):
                                if matriz_grade[termo][dia][campo] is None:
                                    matriz_grade[termo][dia][campo] = (f'{disciplinas_termo[disciplina][0]}', f'{disciplinas_termo[disciplina][1]}')
                            disciplinas_termo.remove(disciplinas_termo[disciplina])
"""