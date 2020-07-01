#Andrew Nguyen
#ID:1467896


import csv
import math
from datetime import datetime


def isExpired(dateString):
  itemExpire = datetime.strptime(dateString, "%m/%d/%Y")
  today = datetime.today()
  #print(itemExpire, "<", today, itemExpire < today)
  return itemExpire < today

def sortArrays(inputArr = [], indexToSort = 0, reverse = False):
  def sortingFunc(e):
    return e[indexToSort]
  inputArr.sort(reverse = reverse, key=sortingFunc)
  return inputArr

def sortArrayUsingDates(inputArr = [], indexToSort = 0, reverse = False):
  def sortingFunc(e):
    return datetime.strptime(e[indexToSort], "%m/%d/%Y")
  inputArr.sort(reverse = reverse, key=sortingFunc)
  return inputArr

def sortArrayUsingInts(inputArr = [], indexToSort = 0, reverse = False):
  def sortingFunc(e):
    return int(e[indexToSort])
  inputArr.sort(reverse = reverse, key=sortingFunc)
  return inputArr


#read values from ManufacturerList PriceList ServiceDatesList
inventoryConstruction = {};

with open('ManufacturerList.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',')
  for row in spamreader:
    inventoryConstruction[row[0]] = {"manufacturer": row[1], "type": row[2], "condition":row[3]}

with open('PriceList.csv', newline='') as csvfile2:
  spamreader = csv.reader(csvfile2, delimiter=',')
  for row in spamreader:
    if(len(row) > 0 and row[0] in inventoryConstruction):
      inventoryConstruction[row[0]]["price"] =  str(row[1])
    elif(not row[0] in inventoryConstruction):
      inventoryConstruction[row[0]]= {"price": str(row[1])}

with open('ServiceDatesList.csv', newline='') as csvfile3:
  spamreader = csv.reader(csvfile3, delimiter=',')
  for row in spamreader:
    if(len(row) > 0 and row[0] in inventoryConstruction):
      inventoryConstruction[row[0]]["date"] =  row[1]
    elif(not row[0] in inventoryConstruction):
      inventoryConstruction[row[0]] = {"date": row[1]}


#create files
with open('DamagedInventory.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  rowHolder = []
  for idNumber in inventoryConstruction:
    if(inventoryConstruction[idNumber]["condition"] == "damaged"):
      row = [idNumber]
      fields =["manufacturer", "type", "price", "date"]
      for field in fields:
        row.append(inventoryConstruction[idNumber][field])
      rowHolder.append(row)
  final = sortArrays(rowHolder, 3, True)
  for row in final:
    spamwriter.writerow(row)


def getTypes():
  difTypes = []
  for idNumber in inventoryConstruction:
    if(inventoryConstruction[idNumber]["type"] not in difTypes):
      difTypes.append(inventoryConstruction[idNumber]["type"])
  return difTypes

types = getTypes()
for iType in types:
  with open(iType.capitalize() +'Inventory.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    rowHolder = []
    for idNumber in inventoryConstruction:
      if(inventoryConstruction[idNumber]["type"] == iType):
        row = [idNumber]
        fields =["manufacturer", "type", "price", "date", "condition"]
        for field in fields:
          row.append(inventoryConstruction[idNumber][field])
        rowHolder.append(row)
    final = sortArrays(rowHolder, 1)
    for row in final:
      spamwriter.writerow(row)
      
with open('PastServiceDateInventory.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  rowHolder = []
  for idNumber in inventoryConstruction:
    if(isExpired(inventoryConstruction[idNumber]["date"])):
      row = [idNumber]
      fields =["manufacturer", "type", "price", "date", "condition"]
      for field in fields:
        row.append(inventoryConstruction[idNumber][field])
      rowHolder.append(row)

  final = sortArrayUsingDates(rowHolder, 4)
  for row in final:
      spamwriter.writerow(row)

with open('FullInventory.csv', 'w', newline='') as csvfile:
  spamwriter = csv.writer(csvfile, delimiter=',')
  rowHolder = []
  for idNumber in inventoryConstruction:
    row = [idNumber]
    fields =["manufacturer", "type", "price", "date", "condition"]
    for field in fields:
      row.append(inventoryConstruction[idNumber][field])
    rowHolder.append(row)

  final = sortArrays(rowHolder, 1)
  for row in final:
      spamwriter.writerow(row)

#############################################################

inventoryList = []

#read FullInventory csv into array of arrays
with open('FullInventory.csv', newline='') as csvfile:
  spamreader = csv.reader(csvfile, delimiter=',')
  for row in spamreader:
    for x in range(len(row)):
       row[x] = row[x].strip()
    if(row[5] == ""):
      row[5] = "undamaged"
    inventoryList.append(row)

FIDataOrder = ["id", "manufacturer", "type", "price", "date", "condition"]

#query using name in FIDataOrder and value
def queryBy(catagory, query, queryarray = inventoryList):
  lookUpIndex = FIDataOrder.index(catagory.lower())
  if(lookUpIndex < 0):
    return False
  results = []
  for row in queryarray:
    if(row[lookUpIndex].lower() == query.lower() and row[FIDataOrder.index("condition")] != 'damaged' and not isExpired(row[FIDataOrder.index("date")])):
      results.append(row)
  #print("q Results for ", catagory, "and", query, ":", results)
  return results

def andQuery(catagory1, value1, catagory2, value2, queryarray = inventoryList):
  result = queryBy(catagory1, value1)
  result = queryBy(catagory2, value2, result)
  return result

def getClosest(dataInput = []):
  #query type that is not same brand
  qtype = dataInput[FIDataOrder.index("type")]
  brand = dataInput[FIDataOrder.index("manufacturer")]
  price = dataInput[FIDataOrder.index("price")]
  query = queryBy("type", qtype);
  #get closest price to OG
  closest = []
  closestDiference = math.inf
  for row in query:
    if(row[FIDataOrder.index("manufacturer")] != brand and abs(int(price) - int(row[FIDataOrder.index("price")])) < closestDiference):
      closestDiference = abs(int(price) - int(row[FIDataOrder.index("price")]))
      closest = row

  if len(closest) > 0:
    return closest
  return False
  
def formatOutput(inputArr = []):
  if(len(inputArr) != len(FIDataOrder)):
    return False
  
  final = ""
  for i in range(len(FIDataOrder) - 2):
    final += FIDataOrder[i].upper() + ":" + inputArr[i] + " "
  return final + "\n"

def dataHasInput(iString = "", catagory = "manufacturer"):
  i = FIDataOrder.index(catagory.lower())
  for row in inventoryList:
    if row[i].lower() in iString.lower():
      return row[i]

  return False

def finalMessage(inputArr = []):
  if(len(inputArr) == 0):
    return "No such item in inventory"
  else:
    #get undamaged and non expired items
    # passed = []
    # for row in inputArr:
    #   print(row[0],"not Passed because:", row[FIDataOrder.index("condition")] != 'damaged', not isExpired(row[FIDataOrder.index("date")]))
    #   if(row[FIDataOrder.index("condition")] != 'damaged' and isExpired(row[FIDataOrder.index("date")]) == False):
    #     passed.append(row)
    # get most expensive
    highprice = -1
    result = []
    for row in inputArr: 
      if( int(row[FIDataOrder.index("price")]) > highprice):
        highprice = int(row[FIDataOrder.index("price")])
        result = row
    if(len(result) == 0):
      return "No such item in inventory"

    #output closest price but different brand “You may, also, consider:”
    closest = getClosest(result)
    if(closest):
      final = formatOutput(result) + "\nYou may, also, consider: \n" +formatOutput(closest)
      return final
    else:
      return formatOutput(result)
    

# print(dataHasInput("something phone", "type"))

# print("items matching:")
# print(finalMessage(andQuery("manufacturer", "apple", "type","phone")))


running = True
while(running):
  #get inputs
  qBrand = ""
  while(qBrand == ""):
    qBrand = input("What manufacturer are you looking for? (q to quit):");
    if(qBrand == "q"):
      running = False
      break
    qBrand = dataHasInput(qBrand)
    if(qBrand == False):
      print("\nUnknown manufacturer!\n")
      qBrand = ""
  if(running == False):
    break

  qType = ""
  while(qType == ""):
    qType = input("What type of devices are you looking for? (q to quit):");
    if(qType == "q"):
      running = False
      break
    qType = dataHasInput(qType, "type")
    if(qType == False):
      print("\nUnknown Type!\n")
      qType = ""
  if(running == False):
    break

  #query data
  print(finalMessage(andQuery("manufacturer", qBrand, "type", qType)))
