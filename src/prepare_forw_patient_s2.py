# Prepare date from raw data.
# prepare_forw_patient.py: separate the train, test dataset, and produce graph
# in a patient-wise manner.
from collections import defaultdict as dd
import io
import os
import random

# prepare the data for our experiments.

def extract_sga2deg(path_sga2deg_all,path_sga2deg_train,thresh):
    print 'reading from: {}...'.format(path_sga2deg_all)
    sga2deg = []
    sga2deg_str = []
    sga2deg_all_list = []
    sga_corpus = set()
    deg_corpus = set()
    for line in open(path_sga2deg_all, 'r'):
        values = line.strip().split('\t')
        sga,deg,prob = values[1],values[2],float(values[3])
        sga2deg_all_list.append((sga,deg))
        if prob > thresh:
            sga2deg.append((sga,deg,prob))
            sga_corpus.add(sga)
            deg_corpus.add(deg)
            sga2deg_str.append('\t'.join(values))

    print 'saving to {}...'.format(path_sga2deg_train)
    f = open(path_sga2deg_train,'w')
    for row in sga2deg_str:
        print >> f, row
    f.close
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

    print 'preparing training set'

    root = '/usr1/public/yifeng/GenePathway'
    dest = root+'/pathway_forw_patient'


    # get the training(?) edges.

    path_sga2deg_all = dest+'/pathway_processed/pathway_prob.graph'
    path_sga2deg_train = dest+'/pathway_origin/pathway.graph'
    thresh = 3
    sga2deg,sga_corpus,deg_corpus,sga2deg_all_list = extract_sga2deg(path_sga2deg_all,path_sga2deg_train,thresh)
    print 'sga2deg,sga,deg'
    print len(sga2deg),len(sga_corpus),len(deg_corpus)
    print 1.0*len(sga2deg)/1496128,1.0*len(sga_corpus)/9829,1.0*len(deg_corpus)/5776


    # get the labels.cfacts
    path_label = dest+'/pathway_origin/labels.cfacts'
    print 'saving to {}...'.format(path_label)
    f = open(path_label,'w')
    for deg in deg_corpus:
        print >> f, 'isDEG\t'+deg
    f.close

    # generate the testing set.


    sga2deg_all = dd(list)
    print 'len(sga2deg_all)={}'.format(len(sga2deg_all_list))

    for line in sga2deg_all_list:
        sga = line[0]
        deg = line[1]
        sga2deg_all[sga].append(deg)

    writeSample(dest+'/pathway_origin', 'test.examples', sga2deg_all, deg_corpus)



    print 'Done!'
    # Q.E.D.