from IPython.display import display, Math
import numpy as np
import math
from fractions import Fraction

"""
The functions num_to_latex and vector_to_latex are modified versions of functions that are part of IBM's Qiskit textbook tools:
https://github.com/qiskit-community/qiskit-textbook
That code is under an Apache 2.0 license, and I have received direct authorization from Frank Harkins     
(who wrote the original code) to reuse the functions in here.
https://github.com/frankharkins
"""

def num_to_latex(num, precision=5):
    """Takes a complex number as input and returns a latex representation
    
        Args:
            num (numerical): The number to be converted to latex.
            precision (int): If the real or imaginary parts of num are not close
                             to an integer, the number of decimal places to round to
        
        Returns:
            str: Latex representation of num
    """
    r = np.real(num)
    i = np.imag(num)
    common_factor = None
    
    # try to factor out common terms in imaginary numbers
    if np.isclose(abs(r), abs(i)) and not np.isclose(r, 0):
        common_factor = abs(r)
        r = r/common_factor
        i = i/common_factor
    
    common_terms = {
        1/math.sqrt(2): '\\tfrac{1}{\\sqrt{2}}',
        1/math.sqrt(3): '\\tfrac{1}{\\sqrt{3}}',
        math.sqrt(2/3): '\\sqrt{\\tfrac{2}{3}}',
        math.sqrt(3/4): '\\sqrt{\\tfrac{3}{4}}',
        1/math.sqrt(8): '\\tfrac{1}{\\sqrt{8}}'
    }
    def proc_value(val):
        # See if val is close to an integer
        val_mod = np.mod(val, 1)
        if (np.isclose(val_mod, 0) or np.isclose(val_mod, 1)):
            # If so, return that integer
            return str(int(np.round(val)))
        # Otherwise, see if it matches one of the common terms
        for term, latex_str in common_terms.items():
             if np.isclose(abs(val), term):
                    if val > 0:
                        return latex_str
                    else:
                        return "-" + latex_str
        # try to factorise val nicely
        frac = Fraction(val).limit_denominator()
        num, denom = frac.numerator, frac.denominator
        if num + denom < 20:
            if val > 0:
                return ("\\tfrac{%i}{%i}" % (abs(num), abs(denom)))
            else:
                return ("-\\tfrac{%i}{%i}" % (abs(num), abs(denom)))
        else:
            # Failing everything else, return val as a decimal
            return "{:.{}f}".format(val, precision).rstrip("0")
    
    if common_factor != None:
        common_facstring = proc_value(common_factor)
    else:
        common_facstring = None
    realstring = proc_value(r)
    if i > 0:
        operation = "+"
        imagstring = proc_value(i)
    else:
        operation = "-"
        imagstring = proc_value(-i)
    if imagstring == "1":
        imagstring = ""
    if imagstring == "0":
        return realstring
    if realstring == "0":
        if operation == "-":
            return "-{}i".format(imagstring)
        else:
            return "{}i".format(imagstring)
    if common_facstring != None:
        return "{} \\left( {} {} {}i \\right)".format(common_facstring, realstring, operation, imagstring)
    else:
        return "\\left( {} {} {}i \\right)".format(realstring, operation, imagstring)

def vector_to_latex(vector, display_all=False, precision=5, pretext=""):
    """Latex representation of a complex numpy array (with dimension 1)

        Args:
            vector (ndarray): The vector to be converted to latex, must have dimension 1.
            precision: (int) For numbers not close to integers, the number of decimal places to round to.
            pretext: (str) Latex string to be prepended to the latex, intended for labels.
        
        Returns:
            str: ket representation of the vector in Latex, wrapped in $$
    """
    l = np.log2(len(vector))
    
    if (l).is_integer() == False:
        raise ValueError("array is not a valid statevector (length is not a power of 2)")
    else:
        l = int(l)
    out_string = "\n$$\n{}\n".format(pretext)

    for i, amplitude in enumerate(vector):
        num_string = num_to_latex(amplitude, precision=precision)
        
        if display_all or (num_string != '0'): # only add ket term if prob amplitude is non-zero
            if (out_string[-2] == '+') and (num_string[0] == '-'): # remove + sign from summation if next prob amplitude is neg
                out_string = out_string[:-2]
            if num_string != '1': # don't include prob amplitude next to ket if equal to 1
                out_string += num_string
            out_string += "|" +  "{num:0{width}b}".format(num=i, width=l) + "\\rangle + "
    if len(vector) != 0:
        out_string = out_string[:-3] + "\n" # remove trailing characters
    out_string += "$$"
    return out_string


def print_statevector(array, precision=5, pretext="", display_all=False, display_output=True):
    """Converts a numpy array with the probability amplitudes of a statevector into its ket representation in Latex

        Args:
            array (ndarray or Statevector): The array to be converted to latex, must have dimension 1.
            precision: (int) For numbers not close to integers, the number of decimal places to round to.
            pretext: (str) Latex string to be prepended to the latex, intended for labels.
        
        Returns:
            str: Latex representation of the array, wrapped in $$
        
        Raises:
            ValueError: If array can not be interpreted as a numerical array
            ValueError: If the dimension of array is not 1
    """

    if type(array).__name__ == 'Statevector':
        array = array.data

    try:
        array = np.asarray(array)
        array+1 # Test array contains numerical data
    except:
        raise ValueError("print_statevector can only convert arrays containing numerical data, or types that can be converted to such arrays")

    if array.ndim == 1:
        output = vector_to_latex(array, display_all=display_all, precision=precision, pretext=pretext)
    else:
        raise ValueError("print_statevector can only convert numpy ndarrays of dimension 1")
    
    if display_output:
        display(Math(output))
    else:
        return(output)        
