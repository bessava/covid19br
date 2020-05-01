''' CovidBr - Vagner Bessa 2020

This module needs file from:
 https://covid.saude.gov.br/
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class CovidBr:
    def __init__(self, nome_arquivo, local='CE'):
        nome_arquivo.split('.') != '.csv'
        nome_arquivo += '.csv'

        self.dados = None
        self.local_atual = local

        try:
            self.dados = pd.read_csv(nome_arquivo, sep=';')
        except ValueError:
            print(f'O arquivo \'{nome_arquivo}\' não está correto.')
        except FileNotFoundError:
            print(f'Arquivo \'{nome_arquivo}\' não encontrado.')

        if self.dados is not None:
            self.colunas = list(self.dados.keys())
            self.siglas = self.dados[self.colunas[1]].unique()
            self.regioes = self.dados[self.colunas[0]].unique()

    def __iter__(self):
        self.estado = 0
        return self

    def __next__(self):
        if self.estado < len(self.siglas):
            tabela = self.tabela_estado(self.siglas[self.estado])
            self.estado += 1
            return tabela
        else:
            raise StopIteration

    def __str__(self):
        if self.dados is not None:
            return str(self.dados)
        else:
            return 'Sem dados'

    def tabela_estado(self, estado=None):
        if estado is None:
            estado = self.local_atual
        return self.dados[self.dados[self.colunas[1]] == estado].reset_index()

    def tabela_regiao(self, regiao):
        return self.dados[self.dados[self.colunas[0]] == regiao].reset_index()

    def selecao_zero(self, info='casosNovos', local=None, marco=0):
        tabela = None
        init = 0
        try:
            if local is None:
                local = self.local_atual
            if local in self.siglas:
                tabela = self.tabela_estado(local)
                init = tabela[info].ne(marco).idxmax()
            elif local in self.regioes:
                tabela = self.tabela_regiao(local)
                init = tabela[info].ne(marco).idxmax()
            else:
                raise ValueError
            if (marco > max(tabela[info])):
                raise Exception('Marco invalido')
        except ValueError:
            print('Local inválido!')
            print('Escolha uma sigla:\n', *self.siglas)
            print('Ou escolha uma região:\n', *self.regioes)
        except KeyError:
            print('Chave inválida!')
            print('Escolha dentre as seguintes:\n', *self.colunas[3:])
        except Exception as err:
            print(err)

        return tabela.iloc[init:]

    def grafico(self, info, **kwargs):
        pass


def main():
    estudo = CovidBr('dados20200501')

    estudo.selecao_zero(marco=4000000)


if __name__ == '__main__':
    main()
