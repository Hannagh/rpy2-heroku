import falcon
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import sys
from datetime import datetime

# import R's utility package
utils = rpackages.importr('utils')

# select a mirror for R packages
utils.chooseCRANmirror(ind=1) # select the first mirror in the list

# Finally, import BlockTools
bt = rpackages.importr('blockTools')


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class DiagResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        
        # capture each of the blocking vars
        cap_race = req.params["race"]
        cap_gender = req.params["gender"]
        cap_age = req.params["age"]
        
        day, month, year= int(cap_age[0:2]), int(cap_age[3:5]), int(cap_age[6:10])
        today= datetime.today().strftime('%Y,%m,%d')
        birthdate= datetime.date(year, month, day)
        diff= today - birthdate
        age= diff.years
        age_dic= {24: 0, 34: 1, 44: 2, 54: 3, 64: 4, 74: 5, 150: 6}
        for key in age_dic.keys():
            if age<= key:
                age_block= age_dic[key]
                break
        
        cap_id = req.params["id"]
        py_session = req.params["session"] + ".RData"
        
        py_exact_var = ["race", "gender", "age"]
        py_exact_val = [cap_race, cap_gender, cap_age]
        
        robjects.r('''
                       f <- function(id, exact_var, exact_val, session) {

                        # the session has not been seen before, then the corresponding file doesn't exist
                        # and this must be the first assignment
                        if(!file.exists(session)) {
                            seqout <- seqblock(query = FALSE
                                            , id.vars = "ID"
                                            , id.vals = id
                                            , n.tr = 2
                                            , tr.names = c("treatment1", "treatment2") 
                                            , assg.prob = c(1/2, 1/2)
                                            , exact.vars = exact_var
                                            , exact.vals = exact_val
                                            , file.name = session)
                        }
                        else {
                            seqout <- seqblock(query = FALSE
                                            , object = session
                                            , id.vals = id
                                            , n.tr = 2
                                            , tr.names = c("treatment1", "treatment2") 
                                            , assg.prob = c(1/2, 1/2)
                                            , exact.vals = exact_val
                                            , file.name = session)
                        }
                        seqout$x[seqout$x['ID'] == id , "Tr"]
                        }
                       ''')

        r_f = robjects.r['f']
        out = r_f(cap_id, py_exact_var, py_exact_val, py_session)
        resp.body = 'Treatment=' + str(out[0])
        
# falcon.API instances are callable WSGI apps
app = falcon.API()

app.add_route('/test', DiagResource())
