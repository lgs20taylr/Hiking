import time
import os.path

def main():
   if not os.path.exists("logs"):
      os.mkdir("logs")
   new = input("Create new file? (y/n)").lower() == "y"
   fileChoice = getFileChoice(new)
   while not validateFile(fileChoice) and not new:
      print("That file does not exist.")
      new = input("Create new file instead? (y/n)").lower() == "y"
      fileChoice = getFileChoice(new)
   writeLog(fileChoice, new)

def getFileChoice(new):
   if new:
      fileChoice = input("Enter the name of the log to create it.\n")+".txt"
      fileChoice = ".\logs"+"\\"+fileChoice
   else:
      fileChoice = input("Enter the name of the log to open it.\n")+".txt"
      fileChoice = ".\logs"+"\\"+fileChoice
   return fileChoice

def validateFile(file):
    return os.path.isfile(file)

def validateEntry(entry, new, prevEntry=(0,0), finished=False):
   if not finished:
      if entry[0] != "(":
         print("Opening bracket missing or incorrectly placed.")
         return False
      if entry[-1] != ")":
         print("Closing bracket missing or incorrectly placed.")
         return False
      if "," not in entry:
         print("Comma missing.")
         return False
      tupEntry = entryToTuple(entry)
      lat, long = tupEntry
      pLat, pLong = prevEntry
      latdiff = abs(lat - pLat)
      longdiff = abs(long - pLong)
      if lat < -90.0 or lat > 90.0:
         print("Invalid latitude coordinate.")
         return False
      if long < -180.0 or long > 180.0:
         print("Invalid longitude coordinate.")
         return False
      sure = False
      if latdiff < 0.25 and not sure and not new:
         sure = input(f"The entered latitude or longitude coordinate is less than 0.25\N{DEGREE SIGN} different to the previous entry. Are you sure this entry is correct? (y/n)").lower() == "y"
         if not sure:
            return False
      if longdiff < 0.25 and not sure and not new:
         sure = input(f"The entered latitude or longitude coordinate is less than 0.25\N{DEGREE SIGN} different to the previous entry. Are you sure this entry is correct? (y/n)").lower() == "y"
         if not sure:
            return False
      return True
   else:
      return False

def entryToTuple(entry):
   tupEntry = entry.rstrip(")").lstrip("(").split(",")
   tupEntry[0], tupEntry[1] = (round(float(tupEntry[0]),6),round(float(tupEntry[1]),6))
   tupEntry = tuple(tupEntry)
   return tupEntry

def readLog(log,format):
   match format:
       case "list":
        with open(log, "r") as f:
           logaslist = f.readlines()
        return logaslist
       case "string":
        with open(log, "r") as f:
           logasstring = f.read()
        return logasstring
       case _:
           print("Invalid log variable type requested.")
           return False

def writeLog(log,new):
    addition = []
    if not new:
      contents = readLog(log, "list")
      for e in contents:
         print(e.rstrip("\n"))
    entry = input("Enter your first entry in the format (lat,long).\n")
    while not validateEntry(entry, new):
      entry = input("Enter your first entry in the format (lat,long).\n")
    addition.append(entryToTuple(entry))
    new = False
    while entry.lower() != "fin":
        entry = input("Enter your next entry in the format (lat,long), or 'fin' if finished.\n")
        if validateEntry(entry, new, addition[-1], entry.lower() == "fin"):
           addition.append(entryToTuple(entry))
    for e in range(len(addition)):
       addition[e] = str(addition[e])+"\n"
    with open(log, "a") as f:
       f.writelines(addition)
        
    
    
if __name__ == "__main__":
    main()
