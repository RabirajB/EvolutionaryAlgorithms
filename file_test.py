fp = open('test_result.txt', 'w')
#print(fp)
for i in range(20):
    fp.writelines(str(i))
#print(fp)
fp.close()