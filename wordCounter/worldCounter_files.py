from collections import Counter

import pandas as pd
import os


def main():

    PATH = "../data_text/"
    wordPATH = "../data_file/SearchWords.xlsx"

    list_file = dict((key, dict()) for key in os.listdir(PATH))
    searchWord = load_searchWord(wordPATH)

    print(list_file)

    for file_path in list_file.keys():
        text = open(PATH+file_path, 'rt', encoding='utf8').read()

        for word in searchWord:
            cntNum = text.count(word)

            if cntNum > 0:
                if list_file[file_path].get(word):
                    list_file[file_path][word] += cntNum
                    print(" Add countNum :", word, " : ", cntNum)
                else:
                    list_file[file_path][word] = cntNum
                    print(" New word in department : ", word, " : ", cntNum)

    print(list_file)
    sort_length(list_file)
    deduplicate_word(list_file)
    view_count_department(list_file)
    totalCount = count_total(list_file)
    print(totalCount)

    # Excel 저장 부분 임시 (수정 중 210430)
    departmentData = pd.DataFrame.from_dict(list_file, orient="index")
    print(departmentData)
    departmentData = departmentData.T

    totalData = pd.DataFrame(data=[totalCount], index=["빈도수"])
    totalData = totalData.T

    with pd.ExcelWriter('result.xlsx') as writer:
        departmentData.to_excel(writer, sheet_name="파일별")
        totalData.to_excel(writer, sheet_name="총 합")
    # Excel 저장 부분


def sort_length(dictList):
    for i in list(dictList):
        dictList[i] = dict(sorted(dictList[i].items(), key=lambda x: len(x[0]), reverse=True))


def view_count_department(dictList):
    for listUnique in list(dictList):
        res = sorted(dictList[listUnique].items(), key=(lambda x:x[1]), reverse=True)
        print(listUnique, " : ", res)


def count_total(dictList : dict):
    totalCount = Counter()

    for listDict in dictList.values():
        totalCount = totalCount + Counter(listDict)

    return totalCount


# str.count() 중복 제거
def deduplicate_word(dictList : dict):

    for file in dictList:
        for i in dictList[file]:
            for j in dictList[file]:
                if i != j:
                    if i in j:
                        dictList[file][i] = dictList[file][i] - dictList[file][j]


def load_searchWord(file_path):
    df = pd.read_excel(file_path, sheet_name=0)  # can also name of sheet
    my_list = df['대상어'].tolist()

    return my_list


def remove_whitespaces(text):
    lines = text.split('\n')
    lines = (l.strip() for l in lines)
    lines = (l for l in lines if len(l) > 0)

    return '\n'.join(lines)



if __name__ == '__main__':
    main()