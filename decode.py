# encoding: utf8

def simple_str_handler(s):
    return s[1:].rstrip()

def error_handler(s):
    return  s[1:].rstrip()

def int_handler(s):
    return int(s[1:].rstrip())

def bulk_str_handler(s):
    parts = s.split("\r\n")
    length = int(parts[0][1:])
    if length == -1:
        return None
    if length == 0:
        return ""
    return parts[1]

def array_handler(s):
    if s == "*-1\r\n":
        return None
    parts = s.split("\r\n")
    array = []
    index = 1
    while index < len(parts):
        if parts[index] == "":
            break
        resp_type = parts[index][0]
        if resp_type == "$":
            str_length = int(parts[index][1:])
            if str_length >= 1:
                data = bulk_str_handler("\r\n".join([parts[index], parts[index+1]]))
                index += 2
            else:
                data = bulk_str_handler(parts[index])
                index += 1
        elif resp_type == "*":
            count = int(parts[index][1:])
            if count == -1:
                data = None
                index += 1
            else:
                data = array_handler("\r\n".join(parts[index: index+count+1]))
                index += count + 1
        else:
            data = handler_map[resp_type](parts[index])
            index += 1
        array.append(data)
    return array


handler_map = {"+": simple_str_handler, "-": error_handler, ":": int_handler,
               "$": bulk_str_handler, "*": array_handler}

def decode_resp(string):
    try:
        resp_type = string[0]
        if not resp_type in handler_map:
            raise Exception("invalid response")
        handler = handler_map[resp_type]
        result = handler(string)
        return result
    except Exception as e:
        print(e.message)

if __name__ == "__main__":
    assert decode_resp("""*3\r\n$3\r\nfoo\r\n$0\r\n$3\r\nbar\r\n""") == ['foo', '', 'bar']
    assert decode_resp("*-1\r\n") == None
    assert decode_resp("*3\r\n$3\r\nfoo\r\n*-1\r\n$3\r\nbar\r\n") == ['foo', None, 'bar']
