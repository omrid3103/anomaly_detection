# importing pandas as pd
import pandas as pd

# list of name, degree, score
dprtmnt = ["Engineering", "Tool Design", "Sales", "Marketing", "Purchasing", "Research", "Production", "Production Control", "Human Resources", "Finance", "Information Services", "Document Control", "Quality Assurance", "Facilities and Maintenance", "Shipping and Receiving", "Executive"]
nme = ["engnrng", "tldsgn", "sales", "mrktng", "prchsng", "rsrch", "prdctn", "prdctncntrl", "hr", "fnnce", "infosrvcs", "dcmntcntrl", "qa", "fcltsmntnc", "shpngrcvng", "exec"]
grpnme = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]

# dictionary of lists
dict = {'DepartmentID': grpnme, 'Name': dprtmnt, 'GroupName': nme}

df = pd.DataFrame(dict)

#print(df)

# DepartmentID,Name,GroupName,
# 1,Engineering,Research and Development,
# 2,Tool Design,Research and Development,
# 3,Sales,Sales and Marketing,
# 4,Marketing,Sales and Marketing,
# 5,Purchasing,Inventory Management,
# 6,Research and Development,Research and Development,
# 7,Production,Manufacturing,
# 8,Production Control,Manufacturing,
# 9,Human Resources,Executive General and Administration,
# 10,Finance,Executive General and Administration,
# 11,Information Services,Executive General and Administration,
# 12,Document Control,Quality Assurance,
# 13,Quality Assurance,Quality Assurance,
# 14,Facilities and Maintenance,Executive General and Administration,
# 15,Shipping and Receiving,Inventory Management,
# 16,Executive,Executive General and Administration