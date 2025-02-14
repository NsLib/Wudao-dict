# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import subprocess

PADDING = '        '
QUIZLET_PADDING = ''
QUIZLET_DELIMITER = '<<<>>>'


class TableItem(object):
    def __init__(self):
        self.word = ''
        self.soundmark = []
        self.paraphrase = []
        self.other = []


class CommandDraw:
    RED_PATTERN = '\033[31m%s\033[0m'
    GREEN_PATTERN = '\033[32m%s\033[0m'
    BLUE_PATTERN = '\033[34m%s\033[0m'
    PEP_PATTERN = '\033[36m%s\033[0m'
    BROWN_PATTERN = '\033[33m%s\033[0m'
    
    @staticmethod
    def beautiy_print(text):
        try:
            wigth = int(os.popen('stty size', 'r').read().split()[1])
            if len(text) >= wigth and text[wigth - 1].isalpha() and text[wigth].isalpha():
                spaces = 0
                i = wigth - 1
                while i > wigth/2:
                    if not text[i].isalpha():
                        spaces = wigth - 1 - i
                        break
                    i -= 1
                print(text, text[wigth - 1:wigth+5])
                text = text[:i] + ' '*spaces + text[i:]
                print(text, spaces)
            else:
                print(text)
        except BaseException as e:
            print(text)
    
    def draw_text(self, word, conf):
        clipbard_text = ''
        # Word
        print(self.RED_PATTERN % word['word'])
        clipbard_text += word['word']
        if conf['quizlet']:
            clipbard_text += QUIZLET_DELIMITER
        clipbard_text += '\n'
        table = conf['table']
        table_item = TableItem()
        table_item.word = word['word']
        padding = QUIZLET_PADDING if conf['quizlet'] else PADDING
        # pronunciation
        if word['pronunciation']:
            uncommit = padding 
            clipbard_text += padding
            if '英' in word['pronunciation']:
                uncommit += u'英 ' + self.PEP_PATTERN % word['pronunciation']['英'] + '  '
                clipbard_text += u'英 ' +  word['pronunciation']['英'] + '  '
                table_item.soundmark.append(
                    u'英 ' +  word['pronunciation']['英'])
            if '美' in word['pronunciation']:
                uncommit += u'美 ' + self.PEP_PATTERN % word['pronunciation']['美']
                clipbard_text += u'美 ' + word['pronunciation']['美']
                table_item.soundmark.append(
                    u'美 ' + word['pronunciation']['美'])
            if '' in word['pronunciation']:
                uncommit = u'英/美 ' + self.PEP_PATTERN % word['pronunciation']['']
                clipbard_text += u'英/美 ' + word['pronunciation']['']
                table_item.soundmark.append(
                    u'英/美 ' + word['pronunciation'][''])
            print(uncommit)
            clipbard_text += '\n'
        # paraphrase
        for v in word['paraphrase']:
            print(padding + self.BLUE_PATTERN % v)
            clipbard_text += padding + v + '\n'
            table_item.paraphrase.append(v)
        if word['pattern']:
            print(padding + self.RED_PATTERN % word['pattern'].strip())
            clipbard_text += padding + word['pattern'] + '\n'
            table_item.other.append(word['pattern'])
        print('')
        clipbard_text += '\n'
        if table:
            text = (
                '| {word} | {soundmark} | <TODO> | {paraphrase} | {other} |'
            ).format(
                word=table_item.word,
                soundmark=' '.join(table_item.soundmark),
                paraphrase=' '.join(table_item.paraphrase),
                other=' '.join(table_item.other)
            )
            self.copy_to_clipboard(text)
        else:
            self.copy_to_clipboard(clipbard_text)

        # short desc
        if word['rank']:
            print(self.RED_PATTERN % word['rank'], end='  ')
        if word['pattern']:
            print(self.RED_PATTERN % word['pattern'].strip())
        # sentence
        if conf['short']:
            print('')
        else:
            count = 1
            if word['sentence']:
                print('')
                if len(word['sentence'][0]) == 2:
                    collins_flag = False
                else:
                    collins_flag = True
            else:
                return
            for v in word['sentence']:
                if collins_flag:
                    # collins dict
                    if len(v) != 3:
                        continue
                    if v[1] == '' or len(v[2]) == 0:
                        continue
                    sentence_t = ''
                    if v[1].startswith('['):
                        sentence_t += str(count) + '. ' + self.GREEN_PATTERN % (v[1])
                    else:
                        sentence_t += str(count) + '. ' + self.GREEN_PATTERN % ('[' + v[1] + ']')
                    sentence_t += v[0] + '\n'
                    for sv in v[2]:
                        sentence_t += self.GREEN_PATTERN % u'  例: ' + self.BROWN_PATTERN % (sv[0] + sv[1]) + '\n'
                    count += 1
                    print(sentence_t)
                else:
                    # 21 new year dict
                    if len(v) != 2:
                        continue
                    print(str(count) + '. ' + self.GREEN_PATTERN % '[例]', end=' ')
                    print(v[0], end='  ')
                    print(self.BROWN_PATTERN % v[1])
                    count += 1

    def draw_zh_text(self, word, conf):
        # Word
        print(self.RED_PATTERN % word['word'])
        # pronunciation
        if word['pronunciation']:
            print(self.PEP_PATTERN % word['pronunciation'])
        # paraphrase
        if word['paraphrase']:
            for v in word['paraphrase']:
                v = v.replace('  ;  ', ', ')
                print(self.BLUE_PATTERN % v)
        # complex
        if not conf['short']:
            # description
            count = 1
            if word["desc"]:
                print('')
                for v in word['desc']:
                    if not v:
                        continue
                    # sub title
                    print(str(count) + '. ', end='')
                    v[0] = v[0].replace(';', ',')
                    print(self.GREEN_PATTERN % v[0])
                    # sub example
                    sub_count = 0
                    if len(v) == 2:
                        for e in v[1]:
                            if sub_count % 2 == 0:
                                e = e.strip().replace(';', '')
                                print(self.BROWN_PATTERN % ('    ' + e + '    '), end='')
                            else:
                                print(e)
                            sub_count += 1
                    count += 1
            # example
            if word['sentence']:
                count = 1
                print(self.RED_PATTERN % '\n例句:')
                for v in word['sentence']:
                    if len(v) == 2:
                        print('')
                        print(str(count) + '. ' + self.BROWN_PATTERN % v[0] + '    '+ v[1])
                    count += 1

    def copy_to_clipboard(self, text):
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(text.encode('utf-8'))
        p.stdin.close()
