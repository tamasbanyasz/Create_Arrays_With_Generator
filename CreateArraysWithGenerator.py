import numpy as np
import time
import types
from itertools import chain

'''

In this code an object function gets parameters (start, end, dytype, *arg) from outside. This object function 
return as an generator object. Inside this function using np.fromiter() function with np.arange().  

This created generator object can add to an another object function to append to a list inside the class. 
Than an another object method which is run over this list mentioned above to check the elemets are generator type 
or not. 

If element is generator type, the elemets add to a list which is return the return value of the function.
Than put this function to an np.array to create numpy array and add it to an another object function to a lst.
Than call the "one_dimension_array" which is return back as an np.array which contains the elements from the mentioned 
list above without duplicated items.

This class has two "get" function and they return back as an np.array with only integer numbers or float numbers what 
added to parameters at first time. 

The code doesnt handle what happen if the object functions gets another values/parameters

'''


class MergeGeneratorObjects:
    def __init__(self):
        self.list_of_generators = []
        self.lists_to_merge_process = []

    @staticmethod
    def create_arrays_by_itering(start, end, dtype, *arg):  # create generator object
        yield np.fromiter((i for i in np.arange(start, end, *arg)), dtype=dtype)

    def append_iterated_array_to_list_of_generators(self, func):  # add generator object to list
        self.list_of_generators.append(func)

    def get_elements_from_generator_object(self):  # get itmes from the generator objects
        items_from_generators = []
        for i, _ in enumerate(self.list_of_generators):
            if isinstance(self.list_of_generators[i], types.GeneratorType):
                for generators in iter(self.list_of_generators[i]):
                    items = (item for item in generators)
                    items_from_generators.append(items)

            else:
                print("Not a generator type value")

        self.list_of_generators.clear()
        return items_from_generators

    def append_array_to_merge(self, array):  # add the arrays to ready merge the items into one array

        for i in array:
            self.lists_to_merge_process.append(i)

    def one_dimension_array(self):  # create the merged array without duplicated items

        result = np.array(list(set(chain.from_iterable(self.lists_to_merge_process))))
        self.lists_to_merge_process.clear()
        return result

    @staticmethod
    def get_int_array(array):
        return np.array([int(i) for i in array if i.is_integer()])

    @staticmethod
    def get_float_array(array):
        return np.array(sorted([i for i in array if not i.is_integer()]))


start_time = time.time()

obj = MergeGeneratorObjects()

# append two created generator objects at the same time
obj.append_iterated_array_to_list_of_generators(obj.create_arrays_by_itering(1, 100000, "int", 1))
obj.append_iterated_array_to_list_of_generators(obj.create_arrays_by_itering(1, 100000, "float", 1.25))

first_array = np.array(obj.get_elements_from_generator_object(), dtype=object)
print("\nFirst generator object: \n", first_array)

# append an another generator object
obj.append_iterated_array_to_list_of_generators(obj.create_arrays_by_itering(1, 101000, "int", 1))
second_array = np.array(obj.get_elements_from_generator_object(), dtype=object)
print("\nSecond generator object: \n", second_array)

obj.append_array_to_merge(first_array)
obj.append_array_to_merge(second_array)

one_dimension_array = obj.one_dimension_array()
print("\nMerged array: ", one_dimension_array)
print("Lenght of the merged array: ", len(one_dimension_array))

int_array = obj.get_int_array(one_dimension_array)

float_array = obj.get_float_array(one_dimension_array)

print("\nInteger array: ", int_array)
print("\nFloat array: ", float_array)

end_time = time.time()
print(end_time-start_time)
