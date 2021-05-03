#!/usr/bin/env python
from pandocfilters import toJSONFilter, RawBlock, RawInline, Para

def caption(source):
  return Para([RawInline('latex', r'\caption{')] + source + [RawInline('latex', r'}')])

def align(columns):
  aligns = {
    "AlignDefault": 'r',
    "AlignLeft": 'l',
    "AlignCenter": 'c',
    "AlignRight": 'r',
  }
  return "".join([aligns[column[0]['t']] for column in columns])

def header(source):
  value = source[0][4][0]['c']
  for column in source[1:]:
    value.append(RawInline('latex', r' & '))
    value.extend(column[4][0]['c'])
  value.append(RawInline('latex', r' \\\hline'))
  return Para(value)

def data(source):
  value = []
  for row in source[1:]:
    tmp = []
    for column in row:
      if column != []:
	      tmp.extend(column[4][0]['c'])
      tmp.append(RawInline('latex', r' & '))
    value.extend(tmp)
    value[-1] = RawInline('latex', r' \\' '\n')
  return Para(value)

def replaceLongtable_table(key, value, format, meta):
  if key == "Table":
    return [RawBlock('latex', r'\begin{table}[tbp]' '\n' r'\centering' '\n'), caption(value[1][1][0]['c']), RawBlock('latex', r'\begin{tabular}{@{}%s@{}}' % align(value[2]) + ('\n' r'\hline')), header(value[3][1][0][1]), data(value[4][0][3][0]), RawBlock('latex', r'\hline' '\n' r'\end{tabular}' '\n' r'\end{table}')]

if __name__=="__main__":
  toJSONFilter(replaceLongtable_table)