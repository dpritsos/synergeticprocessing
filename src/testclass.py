



# Simple task for testing
class sor(object):
    def sorting(self, data):
        print("SortTask starting for: %s" % data)
        data.sort()
        print("SortTask done for: %s" % data)
        return "Data Sorted: ", data