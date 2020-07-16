import os
import sys

os.system('antlr4 ./Decaf.g4')
os.system('javac -cp ./antlr-4.8-complete.jar -g *.java')
os.system('grun Decaf program -gui')

