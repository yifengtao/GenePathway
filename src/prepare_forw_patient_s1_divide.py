# Prepare date from raw data.
# prepare_forw_patient.py: separate the train, test dataset, and produce graph
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

# devide the data in the form of test, train and network.

# 2016/08/28
# especially for the patient-wised division of data.
# prepare the data for our experiments.

def get_sga2deg(path_sga2deg_all, path_sga2deg_train, patid_train):
    print 'reading from: {}...'.format(path_sga2deg_all)
    sga2deg = dd(float)
    sga2deg_str = []
    sga2deg_all_list = set()
    sga_corpus = set()
    deg_corpus = set()
    for line in open(path_sga2deg_all, 'r'):
        values = line.strip().split('\t')
        patid,sga,deg,prob = int(values[0]),values[1],values[2],float(values[3])
        sga2deg_all_list.add((sga,deg))
        if patid not in patid_train: continue
        sga2deg[(sga,deg)]+= prob
        sga_corpus.add(sga)
        deg_corpus.add(deg)
        #sga2deg_str.append('\t'.join(values))

    for row in sga2deg.keys():
        sga2deg_str.append('leadTo'+'\t'+row[0]+'\t'+row[1]+'\t'+str(sga2deg[row]))

    print 'saving to {}...'.format(path_sga2deg_train)
    f = open(path_sga2deg_train,'w')
    for row in sga2deg_str:
        print >> f, row
    f.close

    sga2deg = sga2deg.keys()
    return sga2deg,sga_corpus,deg_corpus,sga2deg_all_list

def save2txt_list(path, table):
    '''
    path: the filename to be saved.
    table: list/set of string, data to be saved.
    '''
    print 'saving to {}...'.format(path)
    f = open(path, 'w')
    for row in table:
        print >> f, row
    f.close()
    
def writeSample(path, filename, sga2deglist, deg_corpus):
    # print 'saving to {}...'.format(path+'/'+filename)
    #i,j = 0,0
    with io.open(path+'/tmp','w') as file:
        for itr, sga in enumerate(sga2deglist):
            if itr%1000 == 0:
                print itr
            deg = sga2deglist[sga]
            file.write(u'pathTo(%s,Y)'%sga)
            # TODO:
            for gene in deg_corpus:
                # TODO:
                if gene in deg:
                    file.write(u'\t+')
                    #i += 1
                else:
                    file.write(u'\t-')
                    #j += 1
                file.write(u'pathTo(%s,%s)'%(sga,gene))
            file.write(u'\n')

    #print 'len(pos) = {}, len(neg) = {}'.format(i,j)

    examples = []
    for line in open(path+'/tmp', 'r'):
        line = line.strip()
        examples.append(line)

    print 'len(samples) = {}'.format(len(examples))

    SEED = 666
    random.seed(SEED)
    random.shuffle(examples)
    os.remove(path+'/tmp');
    path_out = path+'/'+filename
    save2txt_list(path_out,examples)


if __name__ == '__main__':

    print 'preparing training and test set...'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'


    # get the training(?) edgesself.

    NUM_PAT = 4468
    patid_list = range(1,NUM_PAT+1)
    SEED = 888
    random.seed(SEED)
    random.shuffle(patid_list)

    thresh1 = 0.1
    thresh2 = 0.2
    cut1 = int(thresh1*NUM_PAT)
    cut2 = int(thresh2*NUM_PAT)
    patid_train = patid_list[0:cut1]
    patid_test = patid_list[cut1:cut2]
    patid_remain = patid_list[cut2:]

    # check
    print len(patid_train),len(patid_test),len(patid_remain),len(patid_train)+len(patid_test)+len(patid_remain)

    path_sga2deg_all = dest+'/pathway_processed/pathway_pat_all.graph'
    path_sga2deg_train = dest+'/pathway_origin/train'
    path_sga2deg_test = dest+'/pathway_origin/test'
    path_sga2deg_remain = dest+'/pathway_origin/remain'


    print 'reading from: {}...'.format(path_sga2deg_all)

    sga2deg_train = dd(float)
    sga2deg_test = dd(float)
    sga2deg_remain = dd(float)

    sga_train_corpus = set()
    deg_train_corpus = set()
    sga_test_corpus = set()
    deg_test_corpus = set()
    sga_remain_corpus = set()
    deg_remain_corpus = set()

    count = 0

    for line in open(path_sga2deg_all, 'r'):
        count += 1
        if count%100000 == 0:
            print count
        values = line.strip().split('\t')
        patid,sga,deg,prob = int(values[0]),values[1],values[2],float(values[3])
        if patid in patid_train:
            sga_train_corpus.add(sga)
            deg_train_corpus.add(deg)
            sga2deg_train[(sga,deg)] += prob
        elif patid in patid_test:
            sga_test_corpus.add(sga)
            deg_test_corpus.add(deg)
            sga2deg_test[(sga,deg)] += prob
        elif patid in patid_remain:
            sga_remain_corpus.add(sga)
            deg_remain_corpus.add(deg)
            sga2deg_remain[(sga,deg)] += prob
        else:
            print 'error!!!'

    print 'saving to {}...'.format(path_sga2deg_train)
    f = open(path_sga2deg_train, 'w')
    for row in sga2deg_train.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(sga2deg_train[row])
    f.close()

    print 'saving to {}...'.format(path_sga2deg_test)
    f = open(path_sga2deg_test, 'w')
    for row in sga2deg_test.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(sga2deg_test[row])
    f.close()

    print 'saving to {}...'.format(path_sga2deg_remain)
    f = open(path_sga2deg_remain, 'w')
    for row in sga2deg_remain.keys():
        print >> f, row[0]+'\t'+row[1]+'\t'+str(sga2deg_remain[row])
    f.close()
    # sga2deg,sga_corpus,deg_corpus,sga2deg_all_list = extract_sga2deg(path_sga2deg_all, path_sga2deg_train, patid_train)


    print 'sga2deg_train\tsga2deg_test\tsga2deg_remain'
    print '{}\t{}\t{}'.format(len(sga2deg_train.keys()),len(sga2deg_test.keys()),len(sga2deg_remain.keys()))
    print '\t\t{}\t{}'.format(len(set(sga2deg_train.keys()).intersection(set(sga2deg_test.keys()))), \
        len(set(sga2deg_train.keys()).intersection(set(sga2deg_remain.keys()))))

    print 'sga_train\tsga_test\tsga_remain'
    print '{}\t{}\t{}'.format(len(sga_train_corpus),len(sga_test_corpus),len(sga_remain_corpus))
    print '\t\t{}\t{}'.format(len(sga_train_corpus.intersection(sga_test_corpus)), \
        len(sga_train_corpus.intersection(sga_remain_corpus)))

    print 'deg_train\tdeg_test\tdeg_remain'
    print '{}\t{}\t{}'.format(len(deg_train_corpus),len(deg_test_corpus),len(deg_remain_corpus))
    print '\t\t{}\t{}'.format(len(deg_train_corpus.intersection(deg_test_corpus)), \
        len(deg_train_corpus.intersection(deg_remain_corpus)))



    #print 1.0*len(sga2deg)/1496128,1.0*len(sga_corpus)/9829,1.0*len(deg_corpus)/5776


    path_graph = dest+'/pathway_origin/pathway.graph'
    print 'saving to {}...'.format(path_graph)
    f = open(path_graph,'w')
    for row in sga2deg_remain.keys():
        sga,deg,prob = row[0],row[1],str(sga2deg_remain[row])
        print >> f, 'leadTo\t'+sga+'\t'+deg+'\t'+prob

    f.close






    # get the labels.cfacts
    path_label = dest+'/pathway_origin/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for deg in deg_train_corpus:
        print >> f, 'isDEG\t'+deg
    f.close

    # generate the testing set.


    # sga2deg_all = dd(list)
    # print 'len(sga2deg_all)={}'.format(len(sga2deg_all_list))

    # for line in sga2deg_all_list:
    #     sga = line[0]
    #     deg = line[1]
    #     sga2deg_all[sga].append(deg)

    # writeSample(dest+'/pathway_origin', 'test.examples', sga2deg_all, deg_corpus)



    print 'Done!'
# Q.E.D.
