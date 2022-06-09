# from datetime import time



# lo = []
# eth = []
# wlan = []
# i = 0
# for inoctet, outoctet , speed in zip(inoctets, outoctets, speeds):
#     if i == 0 :
#         lo.append(inoctet)
#         lo.append(outoctet)
#         lo.append(speed)
#     elif i == 1 :
#         eth.append(inoctet)
#         eth.append(outoctet)
#         eth.append(speed)
#     elif i == 2 :
#         wlan.append(inoctet)
#         wlan.append(outoctet)
#         wlan.append(speed)
#     i = i + 1 
        
# print(lo)
# print(eth)
# print(wlan)

from time import time, sleep

counter = 0


while True:
    print("hello") 
    counter += 1
    if counter == 2 : 
        break
    sleep(5 - time() % 5)
	# thing to run
    
    

