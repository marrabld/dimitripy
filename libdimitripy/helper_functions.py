__author__ = 'marrabld'

import scipy


class Index():
    def __init__(self):
        pass

    @staticmethod
    def where_in(a, b):
        """
        return logical index of where a is in b.  Size of b
        WARNING this will be slow!

        @param a:
        @param b:
        @return:
        """

        idx = scipy.zeros(b.shape)  # assume they are all false

        if a.ndim == 2:
            for i_int in range(0, a.shape[0]):
                for j_int in range(0, a.shape[1]):
                    sub_idx = scipy.where(b == a[i_int, j_int])
                    idx[sub_idx] = True

        if a.ndim == 1:
            count = 0
            for i_int in a:
                for j_int in b:

                    #sub_idx = scipy.where(b == i_int)
                    #idx[sub_idx] = True
                    if i_int == j_int:
                        idx[count] = 1
                        #print('True')
                    else:
                        idx[count] = 0
                        #print('False')

                count += 1

        for i in idx:
            print i

        return idx


