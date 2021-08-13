import os,re, glob

import pandas as pd

if __name__ == "__main__":
    
    """Script to scrape UK Land Registry Filings
        
        Requirements:
        
        -> qpdf
        -> pdftk
        -> pdftotext
        -> GNU Parallel
    
    """
    
    files = glob.glob("pages/*.txt")    
    
    rows = {}

    rows["entry"] = []
    rows["registration_date"] = []
    rows["property_description"] = []
    rows["lease_term_date"] = []
    rows["title"] = []
    rows["notes"] = []
    
    for fn in files:
        
        with open(fn,"r") as f:
            lines = f.read()
        
        print(f"...currently doing {os.path.basename(fn)}")   
        lines = lines.strip().split("\n")[:-2]
        
        index = []

        for row,line in enumerate(lines):
            
            span = line[0:6]
            
            if re.search("^[0-9]",str(span)):
            
                index.append(row)
                
        index.append(len(lines))
        
        char_range = zip(index,index[1:len(index)])

        cell_1 = []
        cell_3 = []

        for _,line in enumerate(lines[7:index[0]]):
                
            cell_1.append(line[6:22].strip())    
            
            cell_3.append(line[51:70].strip())
                
        rows["entry"].append("-1")
        rows["registration_date"].append(" ".join(cell_1))
        rows["property_description"].append("")
        rows["lease_term_date"].append(" ".join(cell_3))
        rows["title"].append("")
        rows["notes"].append("")

        for a,b in char_range:
            
            cell_0 = []
            cell_1 = []
            cell_2 = []
            cell_3 = []
            cell_4 = []
            cell_5 = []
            
            for i,line in enumerate(lines):
                            
                if i >= a and i < b:
                    
                    cell_0.append(line[0:5].strip())
                    
                    reg_date_cell = line[6:22].strip()
                    
                    cell_1.append(reg_date_cell)
                    
                    if re.search("NOTE\:",reg_date_cell):
                        note = "".join(lines[i:b])

                    else:
                        note = ""
                        
                    cell_2.append(line[22:50].strip())
                    cell_3.append(line[50:69].strip())
                    cell_4.append(line[68:].strip())
                    cell_5.append(note)
            
            notes = " ".join(cell_5).strip()
            rows["entry"].append(" ".join(cell_0).strip())
            
            reg_cell_data = " ".join(cell_1)
            reg_cell_data = re.sub("NOTE\:.*$","",reg_cell_data)
            rows["registration_date"].append(reg_cell_data)
            
            if not(notes == ""):
                rows["property_description"].append(" ".join(cell_2[:4]).strip())
                rows["lease_term_date"].append(" ".join(cell_3[:4]))
                rows["title"].append(" ".join(cell_4[:4]).strip())
            else:
                rows["property_description"].append(" ".join(cell_2).strip())
                rows["lease_term_date"].append(" ".join(cell_3))
                rows["title"].append(" ".join(cell_4).strip())
            
            rows["notes"].append(notes)
            
    df = pd.DataFrame(rows)
    
    for i,row in enumerate(df["entry"]):
        try:
            if row == "-1":
                df.loc[i-1,"registration_date"] = f"{df['registration_date'][i-1]}  {df['registration_date'][i]}"
                df.loc[i-1,"lease_term_date"] = f"{df['lease_term_date'][i-1]} {df['lease_term_date'][i]}"
        except Exception as e:
            print(e)
    
    df = df[df.entry != "-1"]
    
    df.to_csv("land-registry.csv",index=True,header=["Entry","Registration date","Property description","Date of lease and term","Lessee's title","Notes"])
            
    