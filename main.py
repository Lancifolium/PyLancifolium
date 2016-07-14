from SgfLancifolium import SgfStruct
from SgfLancifolium import GnNode
from GnCalculate import GnCalculate


if __name__ == '__main__':
    manual = SgfStruct()
    bord = GnCalculate()
    filename = input("File name of Manual: ")
    manual.configManual(filename)

