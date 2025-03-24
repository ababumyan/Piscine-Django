def my_var():
    tmp = 42
    print(tmp," has type %s" % type(tmp))
    tmp = "42"
    print(tmp," has type %s" % type(tmp))
    tmp = "quarante-deux"
    print(tmp," has type %s" % type(tmp))
    tmp = 42.0
    print(tmp," has type %s" % type(tmp))
    tmp = True
    print(tmp," has type %s" % type(tmp))
    tmp = [42]
    print(tmp," has type %s" % type(tmp))
    tmp = {42: 42}
    print(tmp," has type %s" % type(tmp))
    tmp = (42,)
    print(tmp," has type %s" % type(tmp))
    tmp = set([42])
    print(tmp," has type %s" % type(tmp))
    tmp = None
    return
    
if __name__ == '__main__':
    my_var()