import logging
import os
import csv
from shutil import copyfile

data_dir = 'F:\\RemoteTest\\Remote_PCM'
output_dir = 'F:\\RemoteTest\\ASRTest2'


def asr_data_process(data_dir):
    dp = ASR_test_Data_Processor(data_dir)
    dp.process()
    pass


class ASR_test_Data_Processor():
    def __init__(self, *args):
        self.data_dir = args[0]
        self.output_dir = output_dir
        pass

    def process(self):
        with open(os.path.join(self.output_dir, "dataset.txt"), 'w')as ds:
            for parent, test, filenames in os.walk(self.data_dir):
                # logging.debug('dir:' + os.path.basename(parent))
                if os.path.basename(parent) == 'Remote_PCM':
                    continue
                logging.debug('parent: ' + os.path.basename(parent))
                ds.write('test_sets="$test_sets ' + os.path.basename(parent) + '"\n')
                logging.debug('dir:' + (parent))
                if not os.path.exists(os.path.join(self.output_dir, os.path.basename(parent))):
                    os.makedirs(os.path.join(self.output_dir, os.path.basename(parent)))
                with open(os.path.join(self.output_dir, os.path.basename(parent), "metadata.tsv"), 'w',encoding='utf-8') as of:
                    cw = csv.writer(of, delimiter='\t')
                    cw.writerow(["ID", "AUDIO", "DURATION", "TEXT"])
                    id = 1
                    for file in filenames:
                        if file.endswith('pcm'):
                            # logging.debug('parent:' + os.path.basename(''.join(parent)) + ' filename:' + file)
                            if not os.path.exists(os.path.join(self.output_dir, os.path.basename(parent), "audio")):
                                os.makedirs(os.path.join(self.output_dir, os.path.basename(parent), "audio"))
                            copyfile(os.path.join(parent, file),
                                     os.path.join(self.output_dir, os.path.basename(parent), "audio", file))
                            cw.writerow(
                                [id, os.path.join("audio", file), 0, file.split('.')[0]])
                            id += 1
        pass


def main():
    asr_data_process(data_dir)


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    main()
