import re
import os


class Parser:
    def __init__(self):
        self.document = None

    def read_pdf(self):
        """
        Lists all .txt documents within current working directory, opens it and
        initializes Parser class
        """

        list_of_files = [i for i in os.listdir() if i.endswith('.txt')]
        dict_of_files = dict(enumerate(list_of_files, 1))
        print('Available text documents:\n')
        for num, title in dict_of_files.items():
            print(f'{num} - {title}')
        selection = int(input('\nPlease select one by typing its number: '))
        doc_selected = dict_of_files[selection]
        print(f'\nDocument named {doc_selected} has been selected')
        self.document = doc_selected

    def extract_from_document(self):
        """
        Captures first 1-200 characters before keyword starting after a stop
        and 100 and gets rid of the initial characters of each paragraph if they
        are not the beginning of a sentence.
        """

        with open(self.document) as f:
            self.content = f.read()

        while True:
            self.keyword = input('\nWhich keyword would you like to search?: ')
            if self.keyword not in self.content:
                print(f'\n{self.keyword} not found')
            else:
                break
        pattern = '[^\.].{1,200}' + self.keyword + '.{100}.*[^\.]'
        self.paragraphs = re.findall(pattern, self.content)

        try:
            temp_para = []
            for para in self.paragraphs:
                para = para.strip()
                if para[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    temp_para.append(para)
                else:
                    pattern = '[^\.]*\.\s(.*)'
                    w = re.findall(pattern, para)
                    temp_para.append(w[0])
            self.paragraphs = temp_para
        except IndexError:
            pass

        print(f'\n{len(self.paragraphs)} instances of {self.keyword} were found')

    def export_to_text_file(self):
        """
        Exports to .txt file adding 'extracted_' + 'keyword' preffix to filename
        """
        content = ''
        for i in self.paragraphs:
            content += i + '\n'
        filename = 'extracted_' + self.keyword + '_' + self.document
        with open(filename, 'w') as f:
            f.write(content)
