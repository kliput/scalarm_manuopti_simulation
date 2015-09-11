#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scalarm_manuopti
from subprocess import Popen
from subprocess import PIPE

# scalarm_manuopti.copy_binaries()

CONFIG = scalarm_manuopti.InputReader()

## w zaleznosci co jest w procesie na wejściu

def _execute_element(trans_name, input_dir, output_dir, param_names, bin_cmd):
    transformer_parameters = []
    # dla każdego parametru u Was
    # wiemy, że tutaj brane jest t1_a i t1_b
    for p_name in param_names:
        transformer_parameters.append(CONFIG[p_name])

    t_output = Popen(["bash", "-c", "./%s %s %s %s" % (trans_name, input_dir, output_dir, ' '.join(transformer_parameters))], stdout=PIPE).communicate()[0]

    print "transformet output:"
    print t_output

    ## data.txt wygenerowawanuy

    bin_dir = output_dir
    #bin_name = "rectangle.sh data.txt"

    output = Popen(["bash", "-c", bin_cmd], cwd=bin_dir, stdout=PIPE).communicate()[0]

    print "exec output:"
    print output

from collections import namedtuple
ProcessElement = namedtuple("ProcessElement", "trans_name input_dir output_dir param_names bin_cmd")

def execute_element(process_element):
    pe = process_element
    _execute_element(trans_name=pe.trans_name, input_dir=pe.input_dir, output_dir=pe.output_dir, param_names=pe.param_names, bin_cmd=pe.bin_cmd)

# użytkownik pisze final transformera, który tworzy plik final_results.txt zawierający wartości wynikowe MOE w formacie:
## nazwa_param wartosc
## nazwa_param2 wartosc2
def final_transformer(trans_name, input_dir):
    output = Popen(["bash", "-c", "./%s %s" % (trans_name, input_dir)], stdout=PIPE).communicate()[0]
    print output
    # TODO: sprawdzić, czy plik istnieje
    # TODO: non-floats
    results = {}
    with open("final_results.txt", 'r') as final_results:
        with scalarm_manuopti.OutputWriter() as output:
            for line in final_results.readlines():
                # TODO: check if results is valid
                # TODO: check if line is not empty
                name, value = line.split(' ')
                output[name] = float(value)


# Manuopti ---> [Scalarm --> executor ---> ]  ---> transformer ... ---> Manuopti

# - stdin
# >>- param wywoł
# - plik

# ./transformer.exe <input_dir> <output_dir> 3 5

# execute_element(trans_name="trans1.sh", input_dir=".", output_dir="bin1", param_names=['t1_a', 't1_b'], bin_cmd="./rectangle.sh data.txt")
# execute_element(trans_name="trans2.sh", input_dir="bin1", output_dir="bin2", param_names=['t2_c'], bin_cmd="./add.sh data2.txt")

## TODO: GENERATE
elements = [
    ProcessElement(
            trans_name="trans1.sh",
            input_dir=".",
            output_dir="bin1",
            param_names=['t1_a', 't1_b'],
            bin_cmd="./rectangle.sh data.txt"
    ),
    ProcessElement(
            trans_name="trans2.sh",
            input_dir="bin1",
            output_dir="bin2",
            param_names=['t2_c'],
            bin_cmd="./add.sh data2.txt"
    )
]

for elem in elements:
    execute_element(elem)

final_transformer("trans_final.sh", "bin2")

# with scalarm_manuopti.OutputWriter() as output:
