"""Experiments in permuting and matching dense vectors.

There are some overlaps and some differences with sparse_permutations.py, we haven't attempted to unify these.
"""
import numpy as np
import permutations.constants as c


def get_random_vector(dimension):
    """
    Generate a dense random normal vector of a given dimension.
    Returns a 32bit float vector as a numpy array of shape (100,).
    """
    return np.random.randn(dimension).astype(np.float32)


def normalize(vector):
    """
    Compute the L2 norm (||v||2) for a vector, v.
    Returns the normalized vector (same dtype). 
    Note that spares permutations modifies the vector in place in contrast.
    See test_dense_permutations.py test case difference.
    """   
    return vector / np.sqrt(np.dot(vector, vector))


def get_sort_permutation(vector):
    """
    Returns the permutation that sorts the input array in descending order.
    Permutation vectors are index vectors, being a permutation of the 
    integers between 0 and the dimension of a vector minus one. 
    """
    return np.argsort(vector)[::-1] #[::-1] to get descending order


def get_random_permutation(dimension):
    """
    Returns a random permutation vector for a given dimension.
    Permutation vectors are index vectors, being a permutation of the 
    integers between 0 and the dimension of a vector minus one 
    (equivalent to np.arange(dimension)).
    """
    return np.random.permutation(np.arange(dimension))


def permute_vector(permutation, vector):
    """
    Returns the result of applying the given permutation to the given vector.
    Input permutation and vector should be of the same length.
    Input permutation should be an index vector (e.g. a permutation of
    the integers from 0 to dimension-1 of the vector)
    """
    return vector[permutation]


def inverse_permutation(permutation):
    """
    Returns the inverse of a given permutation.
    Input permutation should be an index vector (e.g. a permutation of
    the integers from 0 to dimension-1 of the vector). Note that for this
    inverse to work, each number in the range should occur exactly once
    (i.e. is a true index vector).
    """
    return np.argsort(permutation)


def permutation_to_matrix(permutation):
    """
    Returns a matrix version of a permutation, as a linear transformation.
    Permutation should be a 1 dimensional index vector.
    """
    perm_matrix = np.zeros((permutation.shape[0], permutation.shape[0]), dtype=np.float32)
    perm_matrix[permutation, np.arange(permutation.shape[0])] = 1
    return perm_matrix


def cosine_similarity(vector1, vector2):
    vector1 = vector1.astype(np.float64)
    vector2 = vector2.astype(np.float64)
    norm1 = np.sqrt(np.dot(vector1,vector1))
    norm2 = np.sqrt(np.dot(vector2, vector2))
    _cosine_similarity = np.dot(vector1, vector2) / (norm1*norm2) # value between -1 and 1
    return ((_cosine_similarity + 1)/2).astype(np.float32) # scale to 0 to 1


def main():
    vector1 = get_random_vector(c.DIMENSION)
    normalized_vector1 = normalize(vector1)
    vector2 = get_random_vector(c.DIMENSION)
    normalized_vector2 = normalize(vector2)
    print('')
    print('Normalized or not, values should be the same (give or take a rounding error).')
    print('For dense vectors, they should generally be around 0.5 similarity. Higher dimensions',
          'will be more consistent.')
    print(f"Similarity before sorting, no normalization: {cosine_similarity(vector1, vector2):.4f}")
    print(f"Similarity before sorting, normalized: {cosine_similarity(normalized_vector1, normalized_vector2):.4f}")
    print('\n') #prints two newlines

    perm_vector1 = permute_vector(get_sort_permutation(vector1), vector1)
    perm_vector2 = permute_vector(get_sort_permutation(vector2), vector2)
    norm_perm_vector1 = permute_vector(get_sort_permutation(normalized_vector1), normalized_vector1)
    norm_perm_vector2 = permute_vector(get_sort_permutation(normalized_vector2), normalized_vector2)
    print('For dense vectors with a sort permutation, they are likely to be more similar after permuting.')
    print(f"Similarity after sorting, no normalization: {cosine_similarity(perm_vector1, perm_vector2):.4f}")
    print(f"Similarity after sorting, normalized: {cosine_similarity(norm_perm_vector1, norm_perm_vector2):.4f}")
    print('\n')

    randompermvec = get_random_permutation(c.DIMENSION)
    randompermvec2 = get_random_permutation(c.DIMENSION)
    rperm_vector1 = permute_vector(randompermvec, vector1)
    rperm_vector2 = permute_vector(randompermvec, vector2)
    rnorm_perm_vector1 = permute_vector(randompermvec, normalized_vector1)
    rnorm_perm_vector2 = permute_vector(randompermvec, normalized_vector2)
    rperm2_vector2 = permute_vector(randompermvec2, vector2)
    rnorm_perm2_vector2 = permute_vector(randompermvec2, normalized_vector2)
    print('For dense vectors with random permutations, they should still be around 0.5 similarity.')
    print('With identical permutation, they should have the same similarity as before permutation:')
    print(f"Similarity after sorting, no normalization: {cosine_similarity(rperm_vector1, rperm_vector2):.4f}")
    print(f"Similarity after sorting, normalized: {cosine_similarity(rnorm_perm_vector1, rnorm_perm_vector2):.4f}")
    print('')
    print('And with two different permutations, we should get differing values still trending to 0.5 similarity:')
    print(f"Similarity after sorting, no normalization: {cosine_similarity(rperm_vector1, rperm2_vector2):.4f}")
    print(f"Similarity after sorting, normalized: {cosine_similarity(rnorm_perm_vector1, rnorm_perm2_vector2):.4f}")
    print('')


if __name__ == '__main__':
    main()

