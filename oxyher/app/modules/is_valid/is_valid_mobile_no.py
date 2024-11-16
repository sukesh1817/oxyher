import re                                                             

def check_mobile_no(num):
    try:
        is_valid = re.fullmatch('[6-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]',num)   
        if is_valid!=None:           
            return True
        else:  
            return False
    except Exception as e:
        print(e)