# version 19-03-04


import os.path
import json

TRASH_DIR = 'trash'


def mk_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def sep_dir_file(filepath):
    s = filepath.split('/')
    filename = ''.join(s[-1])
    dirname = '/'.join(s[:-1]) + '/'
    if dirname == '/':
        dirname = './'
    return dirname, filename


def remove_dir(dirname):
    if os.path.isdir(dirname) == False:
        return
    new_name = TRASH_DIR + '/' + dirname
    while os.path.isdir(new_name) == True:
        new_name += '-'
    os.rename(dirname, new_name)


def remove_old_file(path, filename):
    if os.path.isfile(path + '/' + filename) == False:
        return
    new_path = TRASH_DIR + '/' + path
    mk_dir(new_path)
    new_name = filename
    while os.path.isfile(new_path + '/' + new_name) == True:
        new_name += '-'
    # print('Will rename %s to %s' % (path+'/'+filename, new_path+'/'+new_name))
    # input()
    os.rename(path + '/' + filename, new_path + '/' + new_name)


def load_file(path):
    if os.path.isfile(path) == False:
        return False
    r = open(path, 'r')
    return r


def save_to_file(filepath, data, mode='pretty'):
    dirname, filename = sep_dir_file(filepath)
    mk_dir(dirname)
    remove_old_file(dirname, filename)
    underwrite_file(filepath, data, mode)


def underwrite_file(filepath, data, mode='pretty'):
    dirname, filename = sep_dir_file(filepath)
    mk_dir(dirname)
    f = open(dirname + filename, 'w')
    if mode == 'pretty':
        f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))
    else:
        f.write(str(data).replace('\'', '\"'))
    f.close()


def get_variable_from_file(filepath):
    g = load_file(filepath)
    if g == False:
        return False
    try:
        return json.load(g)
    except:
        return False


mk_dir(TRASH_DIR)
