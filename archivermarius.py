import os
import argparse
import errno
from stat import *

description = """This is an archiver program. It takes files as input 
    and creates a .mk archive or it unpacks .mk archives"""

parser = argparse.ArgumentParser(description=description)

parser.add_argument('-u', '--unpack', metavar='archive file', type=str, help="unpacks a .mk archive file")
parser.add_argument('-o', '--output', metavar='output file', type=str, help="output archive file", default='packed.mk')
parser.add_argument('-p', '--pack', metavar='files', type=str, nargs="+", help="packs files to a .mk archive file")
parser.add_argument('-r', '--recursive', metavar='directory', type=str, help="packs a directory recursively")
parser.add_argument('-l', '--list', metavar='archive file', type=str, help="lists all the files in an archive file")


class File:

    def __init__(self, name, location, file_permissions, uid, gid, text):
        self.name = name
        self.__name_size = len(self.name)
        self.__location = location
        self.__location_size = len(self.__location)
        self.text = text
        self.__text_size = len(self.text)
        self.__file_permissions = file_permissions
        self.__uid = str(uid)
        self.__uid_size = len(self.__uid)
        self.__gid = str(gid)
        self.__gid_size = len(self.__gid)

    def get_name(self):
        return self.name

    def get_location(self):
        return self.__location

    def get_text(self):
        return self.text

    def get_attributes(self):
        return self.name, self.__location, self.text

    def get_name_size(self):
        return self.__name_size

    def get_text_size(self):
        return self.__text_size

    def get_location_size(self):
        return self.__location_size

    def get_permissions(self):
        return self.__file_permissions

    def get_uid(self):
        return self.__uid

    def get_uid_size(self):
        return self.__uid_size

    def get_gid(self):
        return self.__gid

    def get_gid_size(self):
        return self.__gid_size

    def set_name(self, name):
        self.name = name
        self.__name_size = len(self.name)

    def set_location(self, location):
        self.__location = location
        self.__location_size = len(self.__location)

    def set_text(self, text):
        self.text = text


class Archive:

    def __init__(self, files=None):
        if files == None:
            self.files = []
        else:
            self.files = files

    def add_file(self, name, flag=True):
        location = os.path.dirname(os.path.abspath(__file__))
        with open(name, 'r') as f:
            permissions = oct(os.stat(name)[ST_MODE])[-3:]
            suid = os.stat(file).st_uid
            gid = os.stat(file).st_gid
            if flag:
                name = os.path.basename(name)
            self.files.append(File(name, location, permissions, suid, gid, f.read()))

    def get_files(self):
        return self.files

    def get_biggest_name(self):
        highest = float('-inf')
        for i in self.files:
            if i.get_name_size() > highest:
                highest = i.get_name_size()
        return str(len(str(highest)))

    def get_biggest_location(self):
        highest = float('-inf')
        for i in self.files:
            if i.get_location_size() > highest:
                highest = i.get_location_size()
        return str(len(str(highest)))

    def get_biggest_text(self):
        highest = float('-inf')
        for i in self.files:
            if i.get_text_size() > highest:
                highest = i.get_text_size()
        return str(len(str(highest)))

    def get_biggest_uid(self):
        highest = float('-inf')
        for i in self.files:
            if i.get_uid_size() > highest:
                highest = i.get_uid_size()
        return str(len(str(highest)))

    def get_biggest_gid(self):
        highest = float('-inf')
        for i in self.files:
            if i.get_gid_size() > highest:
                highest = i.get_gid_size()
        return str(len(str(highest)))

    def write_archive(self, name):
        if name.split(".")[-1] != "mk":
            f_name = str(name) + ".mk"
        else:
            f_name = name
        with open(f_name, 'w') as f:
            f.write(self.get_biggest_name() + ",")
            f.write(self.get_biggest_location() + ",")
            f.write(self.get_biggest_uid() + ",")
            f.write(self.get_biggest_gid() + ",")
            f.write(self.get_biggest_text() + ",")
            for file in self.files:
                f.write(str(file.get_name_size()).rjust(int(self.get_biggest_name()), '0') +
                        file.get_name() +
                        str(file.get_location_size()).rjust(int(self.get_biggest_location()), '0') +
                        file.get_location() +
                        str(file.get_permissions()) +
                        str(file.get_uid_size()).rjust(int(self.get_biggest_uid()), '0') +
                        str(file.get_uid()) +
                        str(file.get_gid_size()).rjust(int(self.get_biggest_gid()), '0') +
                        str(file.get_gid()) +
                        str(file.get_text_size()).rjust(int(self.get_biggest_text()), '0') +
                        file.get_text())

    def unpack_archive(self, archive):
        with open(archive, 'r') as a:
            data = a.read()
        d = ","
        data = data.split(d)
        biggest_name = int(data[0])
        biggest_location = int(data[1])
        biggest_uid = int(data[2])
        biggest_gid = int(data[3])
        biggest_text = int(data[4])
        split_data = []
        for i in data[5:-1]:
            split_data.append((i + ","))
        split_data.append(data[-1])
        data = ''.join(split_data)
        while len(data) > 0:
            min_size = 0
            max_size = biggest_name
            name_size = int(data[min_size:max_size])
            min_size = max_size
            max_size = min_size + name_size
            name = data[min_size:max_size]
            min_size = max_size
            max_size = min_size + biggest_location
            location_size = int(data[min_size:max_size])
            min_size = max_size
            max_size = max_size + location_size
            location = data[min_size:max_size]
            min_size = max_size
            max_size = min_size + 3
            permissions = data[min_size:max_size]
            min_size = max_size
            max_size = min_size + biggest_uid
            uid_size = int(data[min_size:max_size])
            min_size = max_size
            max_size = min_size + uid_size
            uid = data[min_size:max_size]
            min_size = max_size
            max_size = min_size + biggest_gid
            gid_size = int(data[min_size:max_size])
            min_size = max_size
            max_size = min_size + gid_size
            gid = data[min_size:max_size]
            min_size = max_size
            max_size = min_size + biggest_text
            text_size = int(data[min_size:max_size])
            min_size = max_size
            max_size = min_size + text_size
            text = data[min_size:max_size]
            data = data[max_size:]
            self.files.append(File(name, location, permissions, uid, gid, text))

    def write_files(self):
        for file in self.files:
            exists = os.path.exists(os.path.dirname(file.get_name()))
            if not exists and os.path.dirname(file.get_name()) != '':
                try:
                    os.makedirs(os.path.dirname(file.get_name()))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            with open(file.name, 'w') as f:
                f.writelines(file.get_text())
            os.chmod(file.name, int(file.get_permissions(), 8))


if __name__ == "__main__":
    args = parser.parse_args()
    if args.unpack != None:
        if args.unpack.split('.')[-1] == 'mk':
            ar2 = Archive()
            ar2.unpack_archive(args.unpack)
            ar2.write_files()
        else:
            parser.error("The file to unpack should end with .mk")
    elif args.pack != None:
        ar = Archive()
        for file in args.pack:
            ar.add_file(file)
            ar.write_archive(args.output)
    elif args.list != None:
        ar = Archive()
        if args.list.split('.')[-1] != 'mk':
            parser.error("The file to unpack should end with .mk")
        ar.unpack_archive(args.list)
        for file in ar.get_files():
            print(f"name: {file.get_name()}, "
                  f"content size: {file.get_text_size()}, "
                  f"file permissions: {file.get_permissions()}, "
                  f"uid: {file.get_suid()}, "
                  f"gid: {file.get_gid()}")
    else:
        if len(args.recursive.split('/')) > 1:
            file = args.recursive.split('/')[-1]
            os.chdir('/'.join(args.recursive.split('/')[:-1]))
        else:
            file = args.recursive
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
        ar = Archive()
        for root, dirs, files in os.walk(file, topdown=True):
            for name in files:
                file = os.path.join(root, name)
                ar.add_file(file, flag=False)
                ar.write_archive(args.output)
