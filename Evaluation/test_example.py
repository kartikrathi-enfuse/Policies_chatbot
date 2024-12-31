from rag_evaluator import RAGEvaluator

evaluator = RAGEvaluator()

question = "Under what conditions can an employee apply for Compensatory Off?"
response = '''The Employees can only apply for Compensatory Off if they fulfill the following two criteria:  
▪ The Employee should have worked for One Full Day - On account of a project 
requirement pre -approved by the respective Manager  
▪ The Employee should be a Full -time resource
approved  Holiday / Week off working would be marked as a compensatory off in the system. 
It can be availed during the eligibility period (provided all the eligibility / validity criteria are 
qualifying).  
1.3.  Eligibility for Applying for Compensatory Off"
'''
reference = ''' "1. The employee should have worked for one full day due to a project requirement, pre-approved by the respective manager.
    2. The employee should be a full-time resource.
    3. The compensatory off can be applied during the eligibility period, provided all the eligibility/validity criteria are qualifying."
'''

metrics = evaluator.evaluate_all(question, response, reference)