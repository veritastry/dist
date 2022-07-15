import logging
import os
import csv
import pandas as pd
import json

data_dir = 'D:\\study\\asr\\perf\\results'
compare_dir = 'D:\\study\\asr\\perf\\results.test'
output_file = 'D:\\study\\asr\\perf\\compare.xlsx'


def asr_result_process(data_dir):
    dp = ASR_Result_Processor(data_dir)
    dp.process()
    pass


class ASR_Result_Processor():
    def __init__(self, *args):
        self.data_dir = args[0]
        self.output_file = output_file
        self.compare_dir = compare_dir
        pass

    def process(self):
        writer = pd.ExcelWriter(self.output_file, engine="xlsxwriter")
        listds = []
        for parent, dirs, filenames in os.walk(self.data_dir):
            for dir in dirs:
                # logging.debug("dir:" + os.path.join(parent, dir, "RESULTS.TXT"))
                # logging.debug(dir.split('__', )[2])
                f1 = open(os.path.join(parent, dir, "RESULTS.TXT"))
                data = f1.readline()
                logging.debug(data)
                if not data or data == '':
                    continue
                logging.debug('dataset:' + dir.split('__', )[2])
                jdata = json.loads(data)
                oldcer = str(round(jdata['token_error_rate'], 2)) + '%'
                oldser = str(round(jdata['sentence_error_rate'], 2)) + '%'
                f1.close()
                for parent2, dirs2, filenames in os.walk(self.compare_dir):
                    for dir2 in dirs2:
                        if dir2.split('__', )[2] == dir.split('__', )[2]:
                            f1 = open(os.path.join(parent2, dir2, "RESULTS.TXT"))
                            data = f1.readline()
                            jdata = json.loads(data)
                            newcer = str(round(jdata['token_error_rate'], 2)) + '%'
                            newser = str(round(jdata['sentence_error_rate'], 2)) + '%'
                            f1.close()
                            recd = {"数据集": dir2.split('__', )[2], '老版字错率': oldcer, '老版句错率': oldser,
                                    "新版字错率": newcer, '新版句错率': newser}
                            listds.append(recd)
        ds = pd.DataFrame(listds, columns=['数据集', '老版字错率', '老版句错率', '新版字错率', '新版句错率'])
        ds.to_excel(writer, index=True, index_label='序号',
                    header=['数据集', '老版字错率', '老版句错率', '新版字错率', '新版句错率'], encoding='utf-8')
        writer.save()
        pass


def main():
    asr_result_process(data_dir)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    main()
