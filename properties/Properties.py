# -*- coding: UTF-8 -*-

import re
import os
import tempfile


class Properties:
    file_name= 'config.properties'
    def __init__(self):

        self.properties = {}
        try:
            fopen = open(self.file_name, 'r', encoding='utf-8', errors='ignore')
            for line in fopen:
                line = line.strip()
                if line.find('=') > 0 and not line.startswith('#'):
                    strs = line.split('=')
                    self.properties[strs[0].strip()] = strs[1].strip()
        except Exception as e:
            raise e
        finally:
            fopen.close()

    def has_key(self, key):
        return key in self.properties

    def get(self, key, default_value=''):
        if key in self.properties:
            return self.properties[key]
        return default_value

    def put(self, key, value):
        self.properties[key] = value
        replace_property(self.file_name, key + '=.*', key + '=' + value, True)

def replace_property(file_name, from_regex, to_str, append_on_not_exists=True):
    tmpfile = tempfile.TemporaryFile()

    if os.path.exists(file_name):
        r_open = open(file_name, 'r', encoding='utf-8', errors='ignore')
        pattern = re.compile(r'' + from_regex)
        found = None
        for line in r_open:
            if pattern.search(line) and not line.strip().startswith('#'):
                found = True
                line = re.sub(from_regex, to_str, line)
            tmpfile.write(line.encode())
        if not found and append_on_not_exists:
            tmpfile.write((to_str+'\n').encode())
        r_open.close()
        tmpfile.seek(0)

        content = tmpfile.read()

        if os.path.exists(file_name):
            os.remove(file_name)

        w_open = open(file_name, 'wb', encoding='utf-8', errors='ignore')
        w_open.write(content)
        w_open.close()

        tmpfile.close()
    else:
        print ("file %s not found" % file_name)


# if __name__ == "__main__":
#     props = Properties('c.properties')  # 读取文件
#     props.put('copyright', 'True')  # 修改/添加key=value
#     print (props.get('MdFileName_type'))  # 根据key读取value
#     print ("props.has_key('MdFileName_type')=" + str(props.has_key('MdFileName_type'))) # 判断是否包含该key