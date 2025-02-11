# =============================================================================
# Authors: Wang Jun Xian (2309011) & Phylicia Ng (2308908)
# Date: 12/2/2025
# Description: App info and option selection menu
# =============================================================================

from EvaluateExpression import EvaluateExpression
from SortExpressions import SortExpressions
from GenerateSolutions import GenerateSolutions
from TrigoExpressions import TrigoExpressions
from RearrangeNumbers import RearrangeExpression
from GradientDescent import GradientDescent

class App():
    def __init__(self, menu_options = [EvaluateExpression(), SortExpressions(), GenerateSolutions(), GradientDescent(), TrigoExpressions(), RearrangeExpression()]):
        self.__menu_options = menu_options

    def __info(self):
        input('''
*****************************************************************
* ST1507 DSAA: Expression Evaluator and Sorter                  *
*-----------------------------------------------------------    *
*                                                               *
*  - Done by: Wang Jun Xian (2309011) & Phylicia Ng (2308908)   *
*  - Class DAAA/2A/22                                           *
*                                                               *
*****************************************************************
              
Press Enter, to continue....''')

    def start(self, info='yes'):
        if info == 'yes': 
            self.__info()
        choice_array = [str(i) for i in range(1, len(self.__menu_options) + 1)]
        choice_array.append(str(len(self.__menu_options) + 1))
        loop = True
        while loop:
            menu_input = input(
                f'\nPlease select your choice ({", ".join([f"{choice}" for choice in choice_array])}):\n' +
                '\n'.join(f'\t{choice}. {self.__menu_options[int(choice) - 1]}' for choice in choice_array[:-1]) +
                f'\n\t{int(choice_array[-1])}. Exit\nEnter Choice: '
            )
            if menu_input in choice_array:
                loop = False
            else:
                print('Please enter a valid choice!')
        if menu_input == choice_array[-1]:
            print('\nBye, thanks for using ST1507 DSAA: Expression Evaluator and Sorter')
        else:
            self.__menu_options[int(menu_input) - 1].run()
            input("Press any key to continue...")
            self.start(info='no')