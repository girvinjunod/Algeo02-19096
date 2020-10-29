import glob
import errno
path = 'D:/git/Algeo02-19096/test/*.txt' #note C:
files = glob.glob(path)
for name in files:
    try:
        with open(name) as f:
            for line in f:
                print(line)
    except IOError as exc: #Not sure what error this is
        if exc.errno != errno.EISDIR:
            raise