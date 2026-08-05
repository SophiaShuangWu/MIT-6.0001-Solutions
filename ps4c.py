# Problem Set 4C
# Name: Shuang Wu
# Collaborators: Deepseek and built-in AI in Trae IDE
# Time Spent: 3:00

import string
from ps4a import get_permutations

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split()])#remove argument ' ' from the line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
                
        text (string): the message's text

        A SubMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        try:
            if not isinstance(text, str):
                raise TypeError('The type of input to SubMessage function should be string, but it is ' + type(text).__name__)
            elif text == '':
                raise ValueError('The input to SubMessage function is an empty string')
            else:            
                self.message_text = text
                self.valid_words = load_words(WORDLIST_FILENAME)
        except TypeError as t:
            print('TypeError: ' + t.__str__())
        except ValueError as v:
            print('ValueError: ' + v.__str__())
        return None

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled 
        according to vowels_permutation. The first letter in vowels_permutation 
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52 
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        
        try:
            if not isinstance(vowels_permutation, str):
                raise TypeError('The type of input to build_transpose_dict function should be string, but it is ' + type(vowels_permutation).__name__)
            elif vowels_permutation not in get_permutations(VOWELS_LOWER):
                raise ValueError('The input to build_transpose_dict function is not a permutation of vowels')
            else:
                ans = {}
                for i in VOWELS_LOWER:
                    ans[i] = vowels_permutation[VOWELS_LOWER.index(i)]
                    ans[i.upper()] = ans[i].upper()
                for i in CONSONANTS_LOWER + CONSONANTS_UPPER:
                    ans[i] = i
            return ans                    
        except TypeError as t:
            print('TypeError: ' + t.__str__())
        except ValueError as v:
            print('ValueError: ' + v.__str__())
        return None
        
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        try:
            if not isinstance(transpose_dict, dict):
                raise TypeError('The type of input to apply_transpose function should be dict, but it is ' + type(transpose_dict).__name__)
            ans = ''
            for i in self.message_text:
                if i in VOWELS_LOWER or i in VOWELS_UPPER:
                    ans += transpose_dict[i]
                else:
                    ans += i
            return ans            
        except TypeError as t:
            print('TypeError: ' + t.__str__())
        return None
            
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message 
        
        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.
        
        If no good permutations are found (i.e. no permutations result in 
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message    
        
        Hint: use your function from Part 4A
        '''
        ans = ''
        possible_permutations = get_permutations(VOWELS_LOWER)
        max_valid_words = 0
        for perm in possible_permutations:
            message = SubMessage.apply_transpose(self, SubMessage.build_transpose_dict(self, perm))
            message_words =  message.split()
            num_valid_words = 0
            for i in message_words:
                if is_word(self.valid_words, i):
                    num_valid_words += 1
            if num_valid_words > max_valid_words:
                ans = message
                max_valid_words = num_valid_words
        if max_valid_words == 0:
            return self.message_text
        else:
            return ans
    

if __name__ == '__main__':

    # Example test case
#    message = SubMessage("Hello World!")
#    permutation = "eaiuo"
#    enc_dict = message.build_transpose_dict(permutation)
#    print("Original message:", message.get_message_text(), "Permutation:", permutation)
#    print("Expected encryption:", "Hallu Wurld!")
#    print("Actual encryption:", message.apply_transpose(enc_dict))
#    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
#    print("Decrypted message:", enc_message.decrypt_message())

    #Debugging
#    em = EncryptedSubMessage('Hallu Wurld!')
#    print(SubMessage.apply_transpose(em, SubMessage.build_transpose_dict(em, 'eaiuo')))
#    enc_message = EncryptedSubMessage('Hallu Wurld!')
#    print(enc_message.decrypt_message())
    #TODO: WRITE YOUR TEST CASES HERE
    # Test case 1 for SubMessage class
#    message = SubMessage("HALLAHS ^_^ PERIGYNY")
#    permutation = "iuoea"
#    enc_dict = message.build_transpose_dict(permutation)
#    print("Original message:", message.get_message_text(), "Permutation:", permutation)
#    print("Expected encryption:", "HILLIHS ^_^ PUROGYNY")
#    print("Actual encryption:", message.apply_transpose(enc_dict))
    # Test case 2 for SubMessage class
#    message = SubMessage("periodic ^_^ SCRAPIES ~~ UREaSES")
#    permutation = "oaeui"
#    enc_dict = message.build_transpose_dict(permutation)
#    print("Original message:", message.get_message_text(), "Permutation:", permutation)
#    print("Expected encryption:", "pareudec ^_^ SCROPEAS ~~ IRAoSAS")
#    print("Actual encryption:", message.apply_transpose(enc_dict))
    # Test case 1 for EncryptedSubMessage class
#    enc_message = EncryptedSubMessage('HILLIHS ^_^ PUROGYNY')
#    print("Expected decrypted message:", "HALLAHS ^_^ PERIGYNY")
#    print("Actual decrypted message:", enc_message.decrypt_message())
    # Test case 2 for EncryptedSubMessage class
    enc_message = EncryptedSubMessage('pareudec ^_^ SCROPEAS ~~ IRAoSAS')
    print("Expected decrypted message:", "periodic ^_^ SCRAPIES ~~ UREaSES")
    print("Actual decrypted message:", enc_message.decrypt_message())