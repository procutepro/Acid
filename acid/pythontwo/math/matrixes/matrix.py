import acid.pythontwo.math.Vectors.Vec3D as v

class matrix:
    def __init__(self, martix):
        self.matrix = martix

    def returnmatrix(self):
        return self.matrix
    
    def tranfoation(self, vector):
        vectors = vector.returnvec()
        result = [0] * len(self.matrix)

        for i in range(len(self.matrix)):

            for j in range(len(vectors)):

                result[i] += self.matrix[i][j] * vectors[j]

        return v.Vect3D(result[0], result[1], result[2])

    def matrixmul(self, other):
        matrix_a = self.returnmatrix()
        matrix_b = other.returnmatrix()
        rows_a = len(matrix_a)
        cols_a = len(matrix_a[0]) if rows_a > 0 else 0
        rows_b = len(matrix_b)
        cols_b = len(matrix_b[0]) if rows_b > 0 else 0

        if cols_a != rows_b:
            print("Matrices cannot be multiplied due to incompatible dimensions.")
            return None

        # Initialize the result matrix with zeros
        result_matrix = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

        # Perform matrix multiplication
        for i in range(rows_a):
            for j in range(cols_b):
                for k in range(cols_a):
                    result_matrix[i][j] += matrix_a[i][k] * matrix_b[k][j]

        return result_matrix
    
    
