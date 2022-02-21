import ast
tt = "{'start_row': 0, 'end_row': 0, 'env': 0, 'now': 0}"
tt = ast.literal_eval(tt)
print(tt, type(tt))
