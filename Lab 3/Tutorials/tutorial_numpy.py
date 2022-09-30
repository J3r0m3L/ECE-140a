import numpy as np

# Question 1
def first_question():
    array1 = np.array([0, 10, 4, 12])
    print(array1) # [0, 10, 4, 12]

    array1 = array1 - 20
    print(array1) # [-20, -10, -16, -8]

    print(array1.shape) # (4,)

# Question 2
def second_question():
    array2 = np.array([[0, 10, 4, 12],[1, 20, 3, 41]])
    print(array2) # [[ 0 10 4 12]] \n [1 20 3 41]]

    array2 = array2.flatten()
    new_array2 = np.resize(array2[2:6], (2, 2))
    print(new_array2) # [[ 4 12], [1 20]]

# Question 3
def third_question():
    array3 = np.array([0, 10, 4, 12])
    array3 = np.hstack((array3, array3))
    array3 = np.vstack((array3, array3, array3))
    print(array3)
    # [[ 0 10 4 12 0 10 4 12]
    #  [ 0 10 4 12 0 10 4 12]
    #  [ 0 10 4 12 0 10 4 12]]

# Question 4
def fourth_question():
    array4a = np.arange(-3, 16, 6)
    print(array4a) # [-3 3 9 15]

    array4b = np.arange(-7, -20, -2)
    print(array4b) # [-7 -9 -11 -13 -15 -17 -19]

# Question 5
def fifth_question():
    array5 = np.linspace(0, 100, 49, True)
    print(array5) # Outputs 0 to 100 with 49 steps

    # This differs from arrange, because arrange uses stepsize vs linspace which uses number of steps. You would
    # use linspace when only number of steps is known and arrange when only stepsize is known.

# Question 6
def sixth_question():
    array6 = np.zeros((3, 4))
    array6[0] = [12, 3, 1, 3]
    array6[1] = [0, 0, 1, 2]
    array6[2] = [4, 2, 3, 1]
    print(array6) # output is as expected

def main():
    #first_question()
    #second_question()
    #third_question()
    #fourth_question()
    #fifth_question()
    sixth_question()

if __name__ == "__main__":
    main()