# Problem Set 4B
# Name: Shuang Wu
# Collaborators: Deepseek and buil-in AI in Trae IDE
# Time Spent: 4:00

import string

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
        wordlist.extend([word.lower() for word in line.split()])#remove ' ' from the argument of split()
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

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        try:
            if not isinstance(text, str):
                raise ValueError("text must be a string")
            else:
                self.message_text = text
                self.valid_words = load_words(WORDLIST_FILENAME)
        except ValueError as e:
            print('ValueError: ' + str(e))
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

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        try:
            if shift < 0 or shift >= 26:
                raise ValueError("shift must be between 0 and 25")
            else:
                ans = {}
                alphabet = string.ascii_lowercase
                for i in alphabet:
                    ans[i] = alphabet[(alphabet.index(i) + shift) % 26]
                    ans[i.upper()] = ans[i].upper()
                return ans
        except ValueError as e:
            print('ValueError: ' + str(e))
            return None

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        ans = ''
        alphabet = string.ascii_letters
        shift_dict = self.build_shift_dict(shift)
        for i in self.message_text:
            if i in alphabet:
                ans += shift_dict[i]
            else:
                ans += i
        return ans

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, shift)
        self.message_text_encrypted = Message.apply_shift(self, shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        try:
            if not isinstance(shift, int):
                raise TypeError('shift must be an integer')
            elif shift < 0 or shift >= 26:
                raise ValueError('shift must be bigger than 0 and smaller than 26')
            else:
                self.shift = shift
                self.encryption_dict = Message.build_shift_dict(self, shift)
                self.message_text_encrypted = Message.apply_shift(self, shift)
        except TypeError as t:
            print('TypeError: ' + str(t))
        except ValueError as e:
            print('ValueError: ' + str(e))
        return None



class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        shift = 0
        max_valid_words = 0
        for i in range(26):
            num_valid_words = 0
            list_words = Message.apply_shift(self, i).split()
            for word in list_words:
                if is_word(self.valid_words, word):
                    num_valid_words += 1
            if num_valid_words > max_valid_words:
                shift = i
                max_valid_words = num_valid_words
        return (shift, Message.apply_shift(self, shift))

if __name__ == '__main__':
    #TODO: WRITE YOUR TEST CASES HERE
#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    plaintext = PlaintextMessage('AA, FILA', 6)
#    print('Expected Output: GG, LORG')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    plaintext = PlaintextMessage('mommy Lee^_^', 25)
#    print('Expected Output: lnllx Kdd^_^')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('GG, LORG')
#    print('Expected Output:', (20, 'AA, FILA'))
#    print('Actual Output:', ciphertext.decrypt_message())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('lnllx Kdd^_^')
#    print('Expected Output:', (1, 'mommy Lee^_^'))
#    print('Actual Output:', ciphertext.decrypt_message())
    #Debugging
#    wordlist = load_words(WORDLIST_FILENAME)
#    print(wordlist[33300])
    #TODO: best shift value and unencrypted story 
    STORY = get_story_string()
    ciphertext = CiphertextMessage(STORY)
    print(ciphertext.decrypt_message())
