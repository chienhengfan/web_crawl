from multiprocessing import Pool
import crowler104



def main():
    arealist = [str(i) for i in range(6001011001, 6001011013)]  #
    for i in range(0,1):  #
        arealist.append(str(i))
    paramlist = []
    print("paramslist making ")
    for area in arealist:
        paramlist += crowler104.make_params(sceng=0, area=area, min=0, max=37999) # params(salary0~37999,所有地區)
        paramlist += crowler104.make_params(sceng=1, area=area, min=38000, max=40000)
        paramlist += crowler104.make_params(sceng=0, area=area, min=40001, max='')
    print("paramslist done",paramlist)
    print("paramslist length:",len(paramlist))
    print("getting index.....")

    index = []

    for i in paramlist:
        try:
            index += crowler104.index(i)
        except :
            print(i)

    indexjson = {'index': index} if index != [] or len(index)<10 else False
    print('all done,total index amount:{}'.format(len(indexjson['index'])))
    crowler104.dump_json_file(indexjson)


if __name__ == '__main__':

    main()