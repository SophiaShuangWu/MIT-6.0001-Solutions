# Problem Set 4A
# Name: Shuang Wu
# Collaborators: Deepseek and built-in AI in Trae IDE 
# Time Spent: 1:30

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    try:
        if not isinstance(sequence, str):
            raise TypeError('The type of input to get_permutations function should be string, but it is ' + type(sequence).__name__)
        elif sequence == '':
            raise ValueError('The input to get_permutations function is an empty string')
        ans = []
        # special case
        if len(sequence) == 1:
            return [sequence]
        else:
            list_of_permutations = get_permutations(sequence[1:])
            dict_of_permutations = {}
            for perm in list_of_permutations:
                for i in range(len(perm) + 1):
                    dict_of_permutations.setdefault(perm[:i] + sequence[0] + perm[i:], None)
            return list(dict_of_permutations.keys())
    except TypeError as t:
        print('TypeError: ' + t.__str__())
    except ValueError as v:
        print('ValueError: ' + v.__str__())
    return None
    
if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    #example 1
#    example_input = 'a  '
#    print('Input:', example_input)
#    print('Expected Output:', ['a  ', ' a ', '  a'])
#    print('Actual Output:', get_permutations(example_input))
    #example 2
#    example_input = 'a a'
#    print('Input:', example_input)
#    print('Expected Output:', ['a a', 'a a', 'aa'])
#    print('Actual Output:', get_permutations(example_input))
    #example 3
#    example_input = 'aabb'
#    print('Input:', example_input)
#    print('Expected Output:', ['aabb', 'abba', 'abab', 'baab', 'baba', 'bbaa'])
#    print('Actual Output:', get_permutations(example_input))
    #example 4
#    print(get_permutations(1))
    #example 5
#    print(get_permutations(''))
#    #too long to get result
#    VOWELS_LOWER = 'aeiou'
#    VOWELS_UPPER = 'AEIOU'
#    CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
#    CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'
#    letters = VOWELS_LOWER + VOWELS_UPPER + CONSONANTS_LOWER + CONSONANTS_UPPER
#    print(letters)
#    print(get_permutations(letters))
   