import kw

KEYWORD, IDENTIFIER, OPERATOR, SPECIAL_CHARACTER, CONSTANT, UNKNOWN, EOF = 'KEYWORD', 'IDENTIFIER', 'OPERATOR', 'SPECIAL_CHARACTER', 'CONSTANT', 'UNKNOWN', 'EOF'

#special characters found in sql include: 
spec_char = {'$', '[', ']', '(', ')', ',', ':', ';', '*', '.'}

#operators in sql include:
oper = {'+', '-', '*', '/', '<', '>', '=', '~', '!', '@', '%', '^', '&', '|', '`', '?'}

keyword_reserved = set()
keyword_non_reserved = set()

with open('keyword.txt', 'r') as keyword_lists:
    fil_line = keyword_lists.readline().strip()

    while(fil_line):
        typ = fil_line.split(',')
        if typ[1] == 'reserved':
            keyword_reserved.add(typ[0])
        else:
            keyword_non_reserved.add(typ[0])
        
        fil_line = keyword_lists.readline().strip()

class Token:
    def __init__(self,type, value):
        self.value = value
        self.type = type
    
    def __str__(self):
        ret = 'Token({type}, {value}'.format(type = self.type, value = repr(self.value))
        return ret
    
    def __repr__(self):
        return self.__str__()

class Tokenize:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.current_token = None
        self.token_list = []

    def error(self):
        raise Exception('Invalid Syntax')

    def get_next_char(self):    
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def get_next_non_whitespace(self):
        while self.current_char.isspace() and self.current_char is not None:
            self.get_next_char()
    
    def get_number(self):
        num = ''
        while self.current_char.isdigit() and self.current_char is not None:
            num += self.current_char
            self.current_char = self.get_next_char()
        return num
    
    def get_word(self):
        word = ''
        while self.current_char.isalpha() and self.current_char is not None:
            word += self.current_char
            self.get_next_char()
        return word
    
    def get_token_list(self):
        self.current_token = self.get_next_token()

        while self.current_token is not EOF:
            self.token_list.append(self.current_token)
            self.current_token = self.get_next_token()
        
        return self.token_list
    
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.get_next_char()
            
            if self.current_char in oper:
                return Token(OPERATOR,self.current_char)
            
            if self.current_char in spec_char:
                return Token(SPECIAL_CHARACTER, self.current_char)
            
            if self.current_char.isdigit():
                num = self.get_number()
                return Token(CONSTANT, num)
            
            if self.current_char.isalpha():
                word = self.get_word()
                if word in keyword_reserved:
                    return Token(KEYWORD, word)
                elif word in keyword_non_reserved:
                    return Token(KEYWORD, word)
                else:
                    return Token(IDENTIFIER, word)
            
            if self.current_char == None:
                return Token(EOF, None)
                
            self.error()

def Main():
    while True:
        try:
            text = input('SQL> ')
        
        except EOFError:
            break
        
        if not text:
            continue
        
        tokenize = Tokenize(text)
        lst = tokenize.get_token_list()
        for t in lst:
            print(t)
            

if __name__ == '__main__':
    Main()






    # stream = []
    # tokens = []
    # name = ''

    # #read through stream and create tokens

    # def run(strm):
    #     global tokens, stream
    #     stream = strm
    #     eval_stream()
    #     return tokens

    # def clear_name():
    #     global name
    #     name = ''

    # def eval_name():    
    #     global name
    #     name = str.lower(name)
    #     if len(name) > 0:
    #         if kw.is_keyword_identifier(name):
    #             if name in kw.keyword_reserved:
    #                 tokens.append(tkn.keyword(name,True))
    #             elif name in kw.keyword_non_reserved:
    #                 tokens.append(tkn.keyword(name,False))
    #             elif name[0] == '\"':
    #                 tokens.append(tkn.identifier(name,True))
    #             else:
    #                 tokens.append(tkn.identifier(name,False))
    #         elif kw.is_operator(name):
    #             tokens.append(tkn.operator(name))
    #         elif kw.is_special_character(name):
    #             tokens.append(tkn.special_character(name))
    #         elif kw.is_constant(name):
    #             tokens.append(tkn.constant(name,kw.constant_type(name)))
    #         else:
    #             tokens.append(tkn.token('Unknown', name))
    #         #should signify token identity      
    #     clear_name()

    # def skip_wht_space(cur_char, lin, pointer, len_max):
    #     new_pointer = pointer
    #     while new_pointer < len_max:
    #         if lin[new_pointer] in kw.wht and new_pointer+1 < len_max:
    #             new_pointer += 1  
    #         else:
    #             break
    #     return new_pointer  

    # def GetConstant(current_pointer, lin):
    #     global name
    #     name += "'"
    #     this_pointer = current_pointer + 1
    #     #find next '
    #     next_const = current_pointer
    #     while this_pointer < len(lin):
    #         if lin[this_pointer] == "'":
    #             next_const = this_pointer
    #             next_const += 1
    #             name += "'"
    #             break
    #         else:
    #             name += lin[this_pointer]
    #             this_pointer += 1  
    #     eval_name() 
    #     return next_const

    # def eval_stream():                
    #     global name
    #     counter = 0 
    #     for lin in stream:
                
    #         eos = False
    #         prev_char = ''
    #         cur_char = ''
    #         next_char = ''
    #         pointer = 0  
        
    #         while pointer < len(lin):            
    #             cur_char = lin[pointer]            
    #             if cur_char in kw.wht:
    #                 #find next non whitespace char
    #                 pointer = skip_wht_space(cur_char, lin, pointer, len(lin))
    #                 if pointer + 1 == len(lin):
    #                     pointer += 1
    #                     continue
    #                 else:            
    #                     cur_char =  lin[pointer]
                
    #             if cur_char == "'":
    #                 eval_name()
    #                 pointer = GetConstant(pointer, lin)
    #                 continue

    #             name += cur_char

    #             if pointer != 0:
    #                 prev_char = lin[pointer-1]
    #             if pointer + 1 == len(lin):
    #                 #at end set end of lin = true
    #                 eos = True
    #                 next_char = ''
    #             else:
    #                 eos = False
    #                 next_char = lin[pointer+1]

    #             if next_char in kw.wht or eos:
    #                 eval_name()               
                
    #             elif next_char in kw.oper:
    #                 #comment
    #                 if cur_char == '-'  and next_char == '-':
    #                     clear_name()
    #                     break                
    #                 if cur_char not in kw.oper:
    #                     eval_name()
                
                            
    #             elif next_char not in kw.oper and cur_char in kw.oper:
    #                 eval_name()

    #             elif next_char in kw.spec_char:
    #                 eval_name()                 
                
    #             elif cur_char in kw.spec_char:
    #                 eval_name()
                
    #             pointer += 1
    #     counter += 1